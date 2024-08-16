# Notifications Discord Bot

### Description / Summary:
Notifications is a Discord bot that alerts you when a new email arrives in your Gmail inbox within a set timeframe. It shows you when the email was sent, who it’s from, and the recipient’s email address in a Discord embed message. The bot can also mark emails as read and delete them by communicating with the Gmail API and Discord API. I created this bot to help me manage my emails more efficiently using Discord, a platform I use daily, while learning about API communication.

### Language Used:
Python (3.8)

### Libraries Used: 
BeautifulSoup, base64, discord.py, google.api, re

### Features (as of 8/15/2024):
- Delete messages
- Mark messages as read

### Usage demonstration:

[TO BE ADDED SOON]

### Development Process
1.) Create the Bot: Use the Discord Developer portal to create a bot and set the necessary permissions.

2.) Connect to Discord API: Use discord.py to authenticate and connect the bot to the Discord API.

3.) Set Up Google API: Authenticate with Google and enable the Gmail API. Set up the necessary scopes and permissions.

4.) Fetch Emails: Use the Gmail API to get the most recent unread emails from your inbox.

5.) Process Emails: Use BeautifulSoup and base64 to extract and decode the email details (thread_id, message_content, date/time). Store this information in a list.

6.) Create Discord Embeds: Set up a task loop that runs every few minutes to check the list of emails and create a new Discord embed for each email. The bot will post these embeds in a specified channel with options to mark the email as read or delete it.

7.) Host the Bot: Upload the bot code to a hosting service.

### Future developments:
I plan to add more commands to help control and organize my inbox more efficiently. Additionally, I aim to expand this bot to detect and notify me of data breaches.
