#Import discord.py
from datetime import datetime
import discord
import os
import importlib
from discord import channel
from discord.flags import Intents
import pymongo
import asyncio
from threading import Timer
from dotenv import load_dotenv
load_dotenv()

#initialize connection to database
dbclient = pymongo.MongoClient(os.environ.get("DATABASE_ADDRESS"))
db = dbclient.test







#create client class which will hold what to do on certain events
class MyClient(discord.Client):
    spamobj = {}
    #when the bot is initialized...
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        while True:
            for server in db.ServerInfo.find():
                for n,listofannouncements in server["announcements"].items():
                    if listofannouncements != []:
                        for announcement in listofannouncements:
                            if announcement["freq"] == "daily" and announcement["time"].minute == datetime.now().minute:
                                guild = self.get_guild(announcement["guild"])
                                channel = guild.get_channel(announcement["channel"])
                                await channel.send(announcement["message"])
                            elif announcement["freq"] == "weekly" and announcement["day"] == datetime.now().weekday() and announcement["time"].minute == datetime.now().minute:
                                guild = self.get_guild(announcement["guild"])
                                channel = guild.get_channel(announcement["channel"])
                                await channel.send(announcement["message"])
            await asyncio.sleep(60)

                            

    #when the bot detects a message...
    def deletespamuser(self,userid):
        self.spamobj.pop(userid)


    async def update_spam(self,userid):
        if userid in self.spamobj:
            print(str(self.spamobj[userid][1].is_alive()))
            self.spamobj[userid][1].cancel()
            self.spamobj[userid][1].join()
            self.spamobj[userid][1] = Timer(10.0, self.deletespamuser, [userid])
            self.spamobj[userid][1].start()
            self.spamobj[userid][0] += 1
        else:
            t = Timer(10.0, self.deletespamuser, [userid])
            self.spamobj[userid] = [1, t]
            self.spamobj[userid][1].start()


    async def on_message(self, message):

        #if no database entry exists for the server, make one.
        if not db.ServerInfo.find_one({"_id":message.guild.id}):
            dictofusers = {}
            for member in message.guild.members:
                dictofusers[str(member.id)] = {"xp":0,"level":1}
                
            post = {
                "_id":message.guild.id,
                "prefix":"!",
                "users":dictofusers,
                "announcements":{"recurring":[],"standalone":[]}
            }
            db.ServerInfo.insert_one(post)
        #grab the sever settings from the database
        settings = db.ServerInfo.find_one({"_id":message.guild.id})
        
        await self.update_spam(message.author.id)
        print(str(self.spamobj))

        #add xp
        #max_xp = db.ServerInfo.find_one()







        #if the message starts with the prefix and the message wasn't sent by the bot...
        if not self.user == message.author and message.content.startswith(settings["prefix"]):
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
                await file.main(self,message,args,db)

            else:
                await message.reply("Command not found :(")



    async def on_member_join(self, member):
        if member.guild.system_channel:
            await member.guild.system_channel.send("Hello, {0.name}. Welcome to {0.guild.name}".format(member))

#create an instance of the client class we made
client = MyClient(intents=discord.Intents.all())
#run the bot with the token you provide
client.run(os.environ.get("DISCORD_TOKEN"))