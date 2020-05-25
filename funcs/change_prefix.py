import discord
import time
import json
from globals import change_setting, get_setting

async def execute(client, message, args):
    success = False
    if len(args) <= 0:
        res = await message.channel.send(embed=discord.Embed(color=discord.Color.red(), title="**Error**", description="**Please enter the new prefix**"))
    else:
        success = change_setting(message.guild.id, "prefix", args[1])

    if success:
        res = await message.channel.send(embed=discord.Embed(color=discord.Color.green(), title="**Success**", description="Prefix changed successfully to **%s**!" % get_setting(message.guild.id, "prefix")))

    try:
        await message.delete()
    except discord.errors.Forbidden:
        pass # contact admins (comming soon)

    time.sleep(2)
    await res.delete()
