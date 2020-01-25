import asyncio
import commands
import importlib
import json
import os
import time
import warnings
from shutil import copy

import discord
import pymysql

from globals import get_setting
from statics import config as conf
from statics import init

warnings.simplefilter("ignore")

print("starting...")


class client_class(discord.Client):
    async def on_message(self, message):
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

client = client_class()

client.run(conf.bot.get("token"))
