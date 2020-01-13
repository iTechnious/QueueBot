import discord
import asyncio


async def execute(client, message, args):
    await message.channel.send(embed=discord.Embed(color=discord.Color.green(), description="**IT WORKS!**"))
    return