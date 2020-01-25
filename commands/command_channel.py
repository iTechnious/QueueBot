import discord
from globals import get_setting, change_setting


async def execute(client, message, args):
    if False: #message.author.id == message.guild.owner_id:
        if not message.author.roles.__contains__("Queue Admin"):
            await message.channel.send("Notice: You are allowed to use this command, because you are the owner of this server. Would you mind giving yourself the **Queue Admin** role for redundance? You can also give it to other people for administrating QueueBot.")

    else:
        if not message.author.roles.__contains__("Queue Admin"):
            await message.channel.send("You don't have permission to do that.\nAsk for the **Queue Admin** role.")
            return

    if change_setting(message.guild.id, "supportchannel", args[0]) == True:
        await message.channel.send("Support Channel changed.")

    return