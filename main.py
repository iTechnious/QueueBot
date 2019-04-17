import discord
import asyncio
import os
from shutil import copy
import importlib
import json
import time

from statics import config as conf
import commands

client = discord.Client()


def parse_server_name(guild_name):
    name = ""
    for letter in guild_name:
        if letter.isalpha():
            name += letter
    return str(name)


def create_confs():
    for guild in client.guilds:
        print(guild.name)

        name = parse_server_name(guild.name)

        print("creating config if not extits")

        if not os.path.isfile("configs/%s.json" % name):
            copy("standartconf.json", "configs/%s.json" % name)
        else:
            print("config exits...")
        print()


@client.event
async def on_message(message):
    print()
    server_name = parse_server_name(message.guild.name)

    config = json.load(open("configs/%s.json" % server_name))
    prefix = config["config"]["prefix"]

    if str(message.content).startswith(prefix):
        invoke = str(message.content).split(" ")[0][1:]
        print(invoke)
        if list_commands.__contains__("command_" + invoke):
            args = str(message.content).split(" ")
            del args[0]
            print(args)
            module = importlib.import_module("commands.command_" + invoke)
            await getattr(module, "execute")(client, message, args)


@client.event
async def on_guild_join(guild):
    print("joined the Server: %s" % guild.name)
    create_confs()


@client.event
async def on_ready():
    print("Bot started succesfully...")
    await client.change_presence(activity=discord.Game(name='Sösels Bot'))

    create_confs()

    print("trying to register commands...")
    global list_commands
    list_commands = []
    for file in os.listdir("commands/"):
        await asyncio.sleep(0.1)
        # print(file)
        if file.endswith(".py"):
            if file.startswith("command_"):
                module = file[:-3]
                print("adding module/command to register: " + module)
                list_commands.append(module)
    print("found %s commands" % len(list_commands))
    print(list_commands)


client.run(conf.bot.get("token"))
