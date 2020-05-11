import asyncio
import commands
import importlib
import json
import os
import random
import time
import warnings
from shutil import copy

import discord
import pymysql
import youtube_dl
from discord import FFmpegPCMAudio
from discord.utils import get

import globals
from globals import get_setting, music, tickets
from statics import config as conf
from statics import init

warnings.simplefilter("ignore")

print("starting...")

# test part 3

class client_class(discord.Client):
    async def on_message(self, message):
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


    async def on_guild_join(self, guild):
        print("joined the Server: %s" % guild.name)
        print("creating configs...")
        init.init_db(client)


    async def on_ready(self):
        print("Bot started succesfully...\n")
        # await client.change_presence(activity=discord.Game(name='nothing...'))

        init.init_db(client)

        print("trying to register commands...")
        global list_commands
        list_commands = []
        for file in os.listdir("commands/"):
            # print(file)
            if file.endswith(".py"):
                if file.startswith("command_"):
                    module = file[:-3]
                    print("adding module/command to register: " + module)
                    list_commands.append(module)
        print("found %s commands" % len(list_commands))
        print(list_commands)


    async def on_voice_state_update(self, member, before, after):
        supportchannel = get_setting(str(member.guild.id), "supportchannel")
        supportrole = get_setting(str(member.guild.id), "supportrole")
        voice = get(client.voice_clients, guild=member.guild)
        channel = member.guild.get_channel(int(supportchannel))

        if member.id == client.user.id:
            return

        if after.channel is not None and str(after.channel.id) == supportchannel:
            print(member.name, "joined support channel.")

            id = 0
            while id == 0:
                id = random.getrandbits(64)
                for item in tickets.keys():
                    if tickets[item]["id"] == id:
                        id == 0

            tickets[member.id] = {
                "id": id,
                "guild": member.guild.id
            }

            await member.send("Your Support Ticket has been created and the support team has been notified.\n"
                              "You will be automatically moved as soon as a supporter accepts your ticket.\n"
                              "You can enjoy some music while you are waiting.")
            
            for user in member.guild.members:
                user = member.guild.get_member_named(str(user))
                if get(user.roles, id=int(supportrole)):
                    await user.send("A new Support Ticket has been created.\n"
                                    "User: %s\n"
                                    "Server: %s\n"
                                    "You can use the accept command in the support channel to claim the ticket.\n"
                                    "The ID is: **%s**"
                                    % (str(member.name), str(member.guild), str(id)))


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
                        voice.play(discord.FFmpegPCMAudio(url, before_options=" -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", options="-bufsize 640k -b:a 192k"))
                    except:
                        pass

                    while voice.is_playing():
                        await asyncio.sleep(1)
                    voice.stop()
                    asyncio.sleep(1)


        elif after.channel is None:
            if str(before.channel.id) == str(supportchannel):
                try:
                    del tickets[member.id]
                except KeyError:
                    pass
                print(member.name, "left support channel.")
                if voice is not None:
                    for key in tickets.keys():
                        if tickets[key]["guild"] == member.guild.id:
                            return
                    await voice.disconnect()
                return

        elif before.channel is not None:
            if before.channel.id == after.channel.id:
                return
            if str(before.channel.id) == str(supportchannel) and str(supportchannel) != str(after.channel.id):
                try:
                    del tickets[member.id]
                except KeyError:
                    pass
                print(member.name, "left support channel.")
                if voice is not None:
                    for key in tickets.keys():
                        if tickets[key]["guild"] == member.id:
                            return
                    await voice.disconnect()
                return         
        
        
globals.init()


client = client_class()

client.run(conf.bot.get("token"))
