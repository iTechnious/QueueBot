import discord
from discord.utils import get

from globals import tickets

async def execute(client, message, args):
    try:
        args[0] = int(args[0])
    except ValueError:
        await message.channel.send("Please Provide a ticket ID. You can find the ticket ID by looking in the chat with me or by listing them with the tickets command.\n")
        return

    for key in tickets.keys():
        if tickets[key]["id"] == args[0]:
            if message.author.voice is not None:
                member = message.guild.get_member(key)
                await member.move_to(message.guild.get_channel(message.author.voice.channel.id))
                return
            else:
                await message.channel.send("Please join a voice channel you wish to support in so I can move the user.")
                return
        
    await message.channel.send("This ticket id is not valid.")