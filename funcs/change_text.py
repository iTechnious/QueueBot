import discord
from globals import change_setting, get_setting

async def execute(client, message, args):
    try:
        args[1] = int(args[1])
    except ValueError:
        await message.channel.send("Please Provide a channel ID. You can get the role ID by right clicking on the channel.\n"
        "Please make sure to enable developer mode first.")
        return
    
    if discord.utils.get(message.guild.text_channels, id=args[1]):
        if change_setting(message.guild.id, "supporttext", str(args[1])):
            await message.channel.send("Text Channel changed.")
        else:
            await message.channel.send("There was an error changing the Support Channel. It's probably not your fault. Please consult the bot hoster!")

    else:
        await message.channel.send("This channel doesn't exist on this server or is not a text channel.")
        return
    return
