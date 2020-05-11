import discord
import youtube_dl

from globals import change_setting, get_setting


async def execute(client, message, args):
    # check permission of user
    roles = []
    for role in message.author.roles:
        roles.append(role.name)
    if not "Queue Admin" in roles:
        if message.author.id == message.guild.owner_id:
            await message.channel.send("Notice: You are allowed to use this command, because you are the owner of this server. Would you mind giving yourself the **Queue Admin** role for redundance? You can also give it to other people for administrating QueueBot.")
        else:
            await message.channel.send("You don't have permission to do that.\nAsk for the **Queue Admin** role.")
            return

    test = await message.channel.send("Testing link...")
    with youtube_dl.YoutubeDL({}) as ydl:
        try:
            ydl.extract_info(args[0], download=False)
            change_setting(message.guild.id, "supportvideo", args[0])
            await client.delete_message(test)
            await message.channel.send("Video changed.")
        except:
            await message.channel.send("This link is not valid.")
