import asyncio
import commands
import importlib
import json
import os
import time
import random
import warnings
from shutil import copy

import discord
from discord.utils import get
import pymysql

import globals

from globals import get_setting
from statics import config as conf
from statics import init

warnings.simplefilter("ignore")

print("starting...")


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

        if after.channel is None:
            if str(before.channel.id) == str(supportchannel):
                del tickets[member.id]
                print(member.name, "left support channel.")

        elif before.channel is not None:
            if before.channel.id == after.channel.id:
                return
            if str(before.channel.id) == str(supportchannel) and str(supportchannel) != str(after.channel.id):
                del tickets[member.id]
                print(member.name, "left support channel.")
                

        elif str(after.channel.id) == supportchannel:
            print(member.name, "joined support channel.")

            id = 0
            while id == 0:
                id = random.getrandbits(64)
                for item in tickets.keys():
                    if item["id"] == id:
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
        
        print(tickets)
        

globals.init()

from globals import tickets, music

client = client_class()

client.run(conf.bot.get("token"))
