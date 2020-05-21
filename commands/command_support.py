import discord
from discord.utils import get
from globals import get_setting, change_setting


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

    # check if correct option was provided
    if args == []:
        await message.channel.send("Please provide the role id of the support team.\n"
                                   "You can also set the support text channel by typing 'text' before the channel id.")
        return
    
    if args[0] == "text":
        try:
            args[1] = int(args[1])
        except ValueError:
            await message.channel.send("Please Provide a channel ID. You can get the role ID by right clicking on the channel.\n"
            "Please make sure to enable developer mode first.")
            return
        if get(message.guild.text_channels, id=args[1]):
            if change_setting(message.guild.id, "supporttext", str(args[1])):
                await message.channel.send("Text Channel changed.")
            else:
                await message.channel.send("There was an error changing the Support Channel. It's probably not your fault. Please consult the bot hoster!")

        else:
            await message.channel.send("This channel doesn't exist on this server or is not a text channel.")
            return
        return

    else:
        try:
            args[0] = int(args[0])
        except ValueError:
            await message.channel.send("Please Provide a role ID. You can get the role ID by right clicking on the role in your server settings.\n"
            "Please make sure to enable developer mode first.")
            return

        if not get(message.guild.roles, id=args[0]):
            await message.channel.send("The role provided doesn't exist on this server.")
            return

        # change and check change; notify on discord
        if change_setting(message.guild.id, "supportrole", str(args[0])):
            await message.channel.send("Support Role changed.")
        else:
            await message.channel.send("There was an error changing the Support role. It's probably not your fault. Please consult the bot hoster!")        

        return
