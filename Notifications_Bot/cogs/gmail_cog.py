import discord

from discord.ext import commands
from discord.ext import tasks

from gmail import setup_gmail_service
from gmail import delete_gmail_message
from gmail import gmail_email_threads
from gmail import mark_email_as_read

"""
All Gmail related commands and events to interact with Gmail API

"""

class Gmail(commands.Cog):

    # Initialize Bot 
    def __init__(self, bot):
        self.bot = bot
        self.send_message.start()
        
    # Make sure Gmail cog is activated 
    @commands.Cog.listener()
    async def on_ready(self):
        print("Gmail cog loaded")

    
    #If trash reaction is selected and the bot didn't add it, delete the gmail message and it's embed version
    #If checkmark reaction is selected and the bot didn't add it, mark the gmail message as read

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        if user != self.bot.user and reaction.emoji == "🗑":
            
            # Extract list of gmail threadIds by calling the following function
            # Use reaction.message to fetch Id and extract embed's title information
            threadId_list = gmail_email_threads()
            reaction_message = reaction.message 
        
            try:
                
                # Fetch the message
                message = await reaction_message.channel.fetch_message(reaction_message.id)
                # Extract the threadId from the embed
                threadId = message.embeds[0].title
                print(threadId)

                # Check if threadId is in msgId and delete the Gmail message
                if threadId in threadId_list:
                    delete_gmail_message(threadId) #Call delete_gmail_function method that will communicate with the Gmail API
                    await reaction_message.delete()
        
            except discord.errors.NotFound:
                print("Message not found...")
            except Exception as e:
                print(f"An error occurred: {e}")
        

        if user != self.bot.user and reaction.emoji == "✅":
            threadId_list = gmail_email_threads()
            reaction_message = reaction.message

            try:
                
                # Fetch the message
                message = await reaction_message.channel.fetch_message(reaction_message.id)
                # Extract the threadId from the embed
                threadId = message.embeds[0].title
                print(threadId)

                # Check if threadId is in msgId and delete the Gmail message
                if threadId in threadId_list:
                    mark_email_as_read(threadId) #Call delete_gmail_function method that will communicate with the Gmail API
                    await message.channel.send("Message marked as read! ✅")
        
            except discord.errors.NotFound:
                print("Message not found..")
            except Exception as e:
                print(f"An error occurred: {e}")


    # Communicate with Gmail API every 60 minutes to check for new emails 

    @tasks.loop(minutes=30)
    async def send_message(self):

        # Make sure bot posts embeds only in specified channel
        channel = self.bot.get_channel("insert_channel_id")
        print(f"Channel: {channel}")
        if channel:
        
            emailing_list,_ = setup_gmail_service() # Call Gmail API and retrieve list of emails


            for email in emailing_list: # Traverse list of emails and extract information to set as discord embed information
                
                #Some email lengths may exceed 6000 characters
                if len(email[3]) > 4000:
                    gmail_embed = discord.Embed(colour=discord.Colour.dark_green(),
                                                description=email[3][:4000] + '...',
                                                title=email[0])
                else:
                    gmail_embed = discord.Embed(colour=discord.Colour.dark_green(),
                                                description=email[3],
                                                title=email[0])
        
                gmail_embed.set_author(name= email[1])
                gmail_embed.set_footer(text=f'Date:{email[2]}')
                gmail_embed.set_thumbnail(url="https://w7.pngwing.com/pngs/799/918/png-transparent-mail-google-gmail-google-s-logo-icon.png")
        
                myid = '<@insert_id_here>'
            
                final_embed_message = await channel.send(f'{myid} you got mail!', embed=gmail_embed)
                await final_embed_message.add_reaction("✅")
                await final_embed_message.add_reaction("🗑")
                
 
    @send_message.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()


async def setup_gmail(bot):
    await bot.add_cog(Gmail(bot))
    print("Setup and adding gmail cog completed.")





