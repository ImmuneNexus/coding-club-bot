import datetime

async def main(client,message, args, db):
    await message.reply("What do you want your announcement to be?")
    gettext = await client.wait_for("message", check=lambda a : a.author == message.author and a.channel == message.channel)
    announcementtext = gettext.content
    
    while True:
        await gettext.reply("How often do you want the announcment to be sent? (Daily, Weekly, Monthly)")
        getfreq = await client.wait_for("message", check=lambda a : a.author == message.author and a.channel == message.channel)
        freq = getfreq.content.strip()

        if not freq in ["daily", "weekly", "monthly"]:
            await getfreq.reply("Invalid input, buddy. Try again.")
            continue
        else:
            break
    
    while True:
        await getfreq.reply("What date do you want the announcment? (Day, HH:MM AM/PM) eg.(Friday, 05:00 PM) ")
        getdate = await client.wait_for("message", check=lambda a : a.author == message.author and a.channel == message.channel)
        date = getdate.content.strip().lower()
        try:    
            dateobj = datetime.datetime.strptime(" ".join(date.split()[1:]), "%I:%M %p")
            print(str(dateobj))
            break
        
        except ValueError:
            await getdate.reply("Invalid input, check your formatting, buddy.")
            continue

#STORE DAY AND RESOLVE TO NEAREST DAY AND STUFF

info = {
    "usage":"`Message content` `How often` `Day` `Time`",
    "description":"A command to set recurring announcements.",
}