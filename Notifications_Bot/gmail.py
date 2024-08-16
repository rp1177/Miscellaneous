import os.path
import re
import base64

from bs4 import BeautifulSoup

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


"""
Setup Gmail API connection, extract
crucial email information and decode 
using base64 and BeautifulSoup python library

"""

SCOPES = ['https://mail.google.com/'] 


def setup_gmail_service():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  email_list = []
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)

    #get 10 emails max out of the results dictionary
    results = service.users().messages().list(userId='me', labelIds=["UNREAD"], maxResults=10, q="newer_than:1d").execute()

    #traverse each message dictionary in dictionary messages
    messages = results.get('messages', [])
    print(f'Received {len(messages)} new messages')

    if not messages:
        print('No messages found...')
    else:
        print('Messages:')
        #traverse each email and extract the payload: header, body, and attachments and decode them from html form
        for message in messages:

          msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()

          # If email type is basic and easy to access content:
          if msg.get('payload').get('body').get('data'):
              msg_str = base64.urlsafe_b64decode(msg.get('payload').get('body').get('data')).decode("utf-8")

          # Else, if the data is 'None', the email type is text/plain or text/html with inline images/content then we need to directly traverse msg, find the payload and convert data to base64 decode
          else:
             for message_info in msg['payload']['parts']:
              if message_info["mimeType"] in ["text/plain", "text/html"]:
                 msg_str = base64.urlsafe_b64decode(message_info["body"]["data"]).decode("utf-8")

          soup = BeautifulSoup(msg_str, 'html.parser')

          # Access payload key dictionary from inner msg dictionary, then access the header list of dictionaries and access the value keys
          sent_to = msg['payload']['headers'][0]['value']
          date = msg['payload']['headers'][1]['value']

              #if 'header.from' in sender:
                 #sender = re.sub('.+ header.from=', '', sender).strip()

          if 'by' in date:
              date = re.sub('.+;\s+', '', date).strip()
    
          message_content = soup.get_text() 
          email_list.append([message['id'], sent_to, date, message_content])


        return email_list, service
            

  except HttpError as error:
    print(f"An error occurred: {error}")


# Dedicate a function for list of threadIds that easily helps cross reference discord version of embed emails
def gmail_email_threads():

  threadId_list = []
  emails,_ = setup_gmail_service()
  print(emails)

  for email in emails:
    threadId_list.append(email[0])

  return threadId_list


# Function with the purpose to delete email by threadId -> Prevent repeat emails from showing up
def delete_gmail_message(target_email_id):
  
  # Initialize the Gmail service again to delete target email
  emails, service = setup_gmail_service()
 
    
  # Get the list of emails (threads)
  # Iterate through the emails to find the target email ID
  for email_info in emails:

    # Delete the thread if it matches the target email ID
    if email_info[0] == target_email_id:
        
        print(f"Deleted thread with ID: {target_email_id}")
        return service.users().threads().delete(userId='me', id=target_email_id).execute()
        

# Function to mark emails as read by threadId -> Prevent repeat emails from showing up
def mark_email_as_read(target_email_id):
   
   # Initialize the Gmail service 
   emails, service = setup_gmail_service()

  # Iterate through the emails to find the target email ID
   for email_info in emails:
      
      # Mark email message as read if it matches the target email ID
      if email_info[0] == target_email_id:
         
         print(f"Marked as read for thread with ID: {target_email_id}")
         return service.users().messages().modify(userId='me', id=target_email_id, body={'removeLabelIds': ['UNREAD']}).execute()
