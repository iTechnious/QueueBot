import discord
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
            await message.channel.send("", embed=discord.Embed(title="Insufficient permissions!", description="You need the 'Queue Admin' role to be able to perform this action.", color=discord.Color.red()))
            return

    if change_setting(message.guild.id, "supportchannel", args[0]) == True:
        message.add_reaction("✅")
        await message.channel.send("", embed=discord.Embed(title="Support channel changed!", description="✅ The support channel has been changed successfully!", color=discord.Color.green()))
    else:
        await message.channel.send("There was an error changing the Support Channel. It's probably not your fault. Please consult the bot hoster!")

    return