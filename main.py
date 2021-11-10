#Import discord.py
import discord
import os
import importlib
from discord import channel
from discord.flags import Intents
import pymongo
from dotenv import load_dotenv
load_dotenv()

#initialize connection to database
dbclient = pymongo.MongoClient(os.environ.get("DATABASE_ADDRESS"))
db = dbclient.test

#create client class which will hold what to do on certain events
class MyClient(discord.Client):
    #when the bot is initialized...
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    #when the bot detects a message...





    async def on_message(self, message):

        #if no database entry exists for the server, make one.
        if not db.ServerInfo.find_one({"_id":message.guild.id}):
            dictofusers = {}
            print(str(message.guild.members))
            for member in message.guild.members:
                # !!ADD LEVELS!!!
                dictofusers[str(member.id)] = {"xp":0}
                
            post = {
                "_id":message.guild.id,
                "prefix":"!",
                "users":dictofusers
            }
            db.ServerInfo.insert_one(post)
        #grab the sever settings from the database
        settings = db.ServerInfo.find_one({"_id":message.guild.id})
        #if the message starts with the prefix and the message wasn't sent by the bot...
        if not self.user == message.author and message.content[:len(settings["prefix"])] == settings["prefix"]:
            #extract the arguments
            args = message.content.split(" ")
            #remove whitespace arguments
            args = list(filter(None, args))

            #extract the command (first word minus the prefix)
            command = args[0][len(settings["prefix"]):]
            args = args[1:]
            #try to find the command in the commands folder
            if command.lower()+".py" in os.listdir("./Commands") and command.lower()+".py" != "__init__.py":
                #import the file containing the command dynamically
                file = importlib.import_module("Commands."+command.lower(),"Commands")
                #execute the command
                await file.main(message,args,db)

            else:
                await message.reply("Command not found :(")



    async def on_member_join(self, member):
        if member.guild.system_channel:
            await member.guild.system_channel.send("Hello, {0.name}. Welcome to {0.guild.name}".format(member))

#create an instance of the client class we made
client = MyClient(intents=discord.Intents.all())
#run the bot with the token you provide
client.run(os.environ.get("DISCORD_TOKEN"))
