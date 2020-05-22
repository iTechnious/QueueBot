import discord
import asyncio


async def execute(client, message, args):
    await message.add_reaction("✅")
    await message.channel.send(embed=discord.Embed(color=discord.Color.green(), description="Hello there 🙃"))
    return