import os
import discord
import importlib

from discord.embeds import Embed
async def main(client,message,args,db):
    commands = os.listdir("./Commands")
    commands = list(filter(lambda a: os.path.isfile("./Commands/"+a),commands))
    commands.remove("__init__.py")
    prefix = db.ServerInfo.find_one({"_id":message.guild.id})["prefix"]
    if len(args) >= 1:
        command = args[0]+".py"
        print(command[len(prefix):])
        if command in commands or (command.startswith(prefix) and command[len(prefix):] in commands):
            alias = command if not command.startswith(prefix) else command[len(prefix):]
            file = importlib.import_module("."+alias[:-3],"Commands") 
            emb = discord.Embed(title=alias[:-3])
            text = file.info["usage"].replace("!pr",prefix)+"\n"+file.info["description"]
            emb.add_field(name=prefix+alias[:-3],value=text,inline=False)
            await message.reply(embed=emb) 
    else:
        emb = discord.Embed(title="List of Commands")
        for i in commands:
            file = importlib.import_module("."+i[:-3],"Commands")
            emb.add_field(name=prefix+i[:-3],value=file.info["description"],inline=False)
        await message.reply(embed=emb)
    
        
info = {
    "usage":"`!prhelp` or `!prhelp` `cmdname`",
    "description":"A command to get information on the different commands",
}