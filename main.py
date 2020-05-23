import asyncio
import datetime
import importlib
import os
import random
import time
import warnings

import discord
import youtube_dl
from discord.utils import get

from globals import get_setting, tickets
from helpers.create_ticket import run as create_ticket
from statics import config as conf
from statics import init

warnings.simplefilter("ignore")

print("starting...")


class ClientClass(discord.Client):
    @staticmethod
    async def on_message(message):
        if message.author.id == client.user.id:
            return
        prefix = get_setting(message.guild.id, "prefix")

        if str(message.content).startswith(prefix):
            invoke = str(message.content).split(" ")[0][len(prefix):]
            if list_commands.__contains__("command_" + invoke):
                args = str(message.content).split(" ")
                del args[0]
                print("------- new command handle -------")
                print(invoke)
                print(args)
                module = importlib.import_module("commands.command_" + invoke)
                await getattr(module, "execute")(client, message, args)

    @staticmethod
    async def on_guild_join(guild):
        print("joined the Server: %s" % guild.name)
        print("creating configs...")
        init.init_db(client)

    @staticmethod
    async def on_ready():
        print("Bot started succesfully...\n")
        
        init.init_db(client)

        print("trying to register commands...")
        global list_commands
        list_commands = []
        for file in os.listdir("commands/"):
            if file.endswith(".py"):
                if file.startswith("command_"):
                    module = file[:-3]
                    print("adding module/command to register: " + module)
                    list_commands.append(module)
        print("found %s commands" % len(list_commands))
        print(list_commands)

    @staticmethod
    async def on_voice_state_update(member, before, after):
        supportchannel = get_setting(str(member.guild.id), "supportchannel")
        voice = get(client.voice_clients, guild=member.guild)
        channel = member.guild.get_channel(int(supportchannel))

        join = False
        leave = False

        if after.channel is None:
            if before.channel is not None:
                if str(before.channel.id) == supportchannel:
                    leave = True
        elif str(after.channel.id) != supportchannel:
            if before.channel is None:
                pass
            elif str(before.channel.id) == supportchannel:
                leave = True
        elif str(after.channel.id) == supportchannel:
            join = True
        if member.id == client.user.id:
            return

        if join:
            print(member.name, "joined support channel.")
            create_ticket(member)

            await member.send("", embed=discord.Embed(title="Your ticket has been created!", description="You will be automatically moved as soon as a supporter accepts your ticket.\nYou can enjoy some music while you are waiting.", color=discord.Color.purple()))

            supporter_chat = await client.fetch_channel(get_setting(member.guild.id, "supporttext"))
            emb = discord.Embed(title=member.name+" opened ticket #"+str(tickets[member.id]["id"])+".", description="<@"+str(member.id)+"> is waiting in the queue.\nClaim the ticket and move him to your voice channel by reacting to this message.", color=discord.Color.green())
            ticket_message = await supporter_chat.send("", embed=emb)
            await ticket_message.add_reaction("✅")
            
            tickets[member.id]["message"] = ticket_message

            if voice is None:
                voice = await channel.connect()

            elif not voice.is_connected():
                voice = await channel.connect()
            else:
                await voice.move_to(channel)

            with youtube_dl.YoutubeDL({}) as ydl:
                song_info = ydl.extract_info(get_setting(member.guild.id, "supportvideo"), download=False)
                url = song_info["formats"][1]["url"]

                while voice.is_connected():
                    try:
                        voice.play(discord.FFmpegPCMAudio(url, before_options=" -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))
                    except discord.errors.ClientException:
                        pass

                    while voice.is_playing():
                        await asyncio.sleep(1)
                    voice.stop()
                    await asyncio.sleep(1)

        if leave:            
            try:
                supporttext = await client.fetch_channel(get_setting(member.guild.id, "supporttext"))
                ticket_msg = await supporttext.fetch_message(tickets[member.id]["message"].id)
                await ticket_msg.delete()
                del tickets[member.id]
            except KeyError:
                pass
            print(member.name, "left support channel.")
            if voice is not None:
                for key in tickets.keys():
                    if tickets[key]["guild"] == channel.guild.id:
                        return
                await voice.disconnect()
            return
                
    @staticmethod
    async def on_reaction_add(reaction, user):
        if user.id == client.user.id:
            return
        
        if reaction.emoji == "✅" and str(reaction.message.channel.id) == get_setting(reaction.message.guild.id, "supporttext") and reaction.message.author.name == "Queue":
            role_names = [role.name for role in user.roles]
            if "Support" in role_names:
                if user.voice is not None:
                    for key in tickets.keys():
                        if tickets[key]["message"].id == reaction.message.id:
                            ticket = tickets[key]
                            break

                    await reaction.message.delete()
                    await reaction.message.channel.send("", embed=discord.Embed(title="Ticket #"+str(ticket["id"])+" closed.", description="Author: <@"+str(key)+">\nOpened: " + ticket["time"] + "\nClosed: " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + "\nClaimed by: <@"+str(user.id)+">\n", color=discord.Color.gold()))
                    await reaction.message.channel.guild.get_member(key).move_to(user.voice.channel)
                else:
                    error_message = await reaction.message.channel.send("", embed=discord.Embed(title="", description="🚫 You must be in a voice channel to claim a ticket.", color=discord.Color.red()))
                    await reaction.remove(user)
                    time.sleep(2)
                    await error_message.delete()
                    
            else:
                await reaction.remove(user)
                return
        else:
            return
        return

client = ClientClass()

client.run(conf.bot.get("token"))
