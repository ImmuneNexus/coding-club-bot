import os
import discord
import importlib
async def main(message,args,db):
    commands = os.listdir("./Commands")
    commands = list(filter(lambda a: os.path.isfile("./Commands/"+a),commands))
    commands.remove("__init__.py")

    emb = discord.Embed(title="List of Commands")
    for i in commands:
        file = importlib.import_module("."+i[:-3],"Commands")
        emb.add_field(name=db.ServerInfo.find_one({"_id":message.guild.id})["prefix"]+i[:-3],value=file.info["description"],inline=False)
    await message.reply(embed=emb)
    
        
info = {
    "usage":"`!help` or `!help cmdname`",
    "description":"A command to get information on the different commands",
    "args":["optional name of specific command"]
}