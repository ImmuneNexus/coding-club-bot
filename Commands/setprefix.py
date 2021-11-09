async def main(message,args,db):
    if len(args)>0:
        db.ServerInfo.update_one({"_id":message.guild.id},{"$set":{"prefix":args[0]}})
        await message.reply("Server prefix was set to "+"\""+args[0]+"\"")
    else:
        await message.reply("No arguments were provided!")

info = {
    "usage":"`!setprefix ?`",
    "description":"A command to change the prefix of the server",
    "args":["new prefix"]
}

