import discord
import asyncio
import os
from shutil import copy
import importlib
import json
import time
import pymysql
import warnings

from statics import config as conf
import commands

from globals import get_setting

warnings.simplefilter("ignore")

print("starting...")

client = discord.Client()

def init_db():
    connection = pymysql.connect(
        host=conf.mysql["host"],
        port=conf.mysql["port"],
        user=conf.mysql["user"],
        password=conf.mysql["pass"]
    )

    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS %s" % conf.mysql["db"])
        connection.commit()
        connection.close()

    connection = pymysql.connect(
        host=conf.mysql["host"],
        port=conf.mysql["port"],
        user=conf.mysql["user"],
        password=conf.mysql["pass"],
        db=conf.mysql["db"]
    )
    with connection.cursor() as cursor:
        for guild in client.guilds:
            name = int(guild.id)
            name = "_%s" % str(name)
            print("checking config for server '%s' (%s)" %(str(guild.name), int(guild.id)))
            
            cursor.execute('CREATE TABLE IF NOT EXISTS %s ('
                           "id INT(20) AUTO_INCREMENT PRIMARY KEY,"
                           "setting VARCHAR(100),"
                           "value VARCHAR(100)"
                           ")" % str(name))
            if cursor.execute("SELECT * FROM %s" % name) == 0:
                cursor.execute("INSERT INTO %s (setting, value) VALUES ('prefix', '!')" % name)

            print()
    connection.commit()
    connection.close()

    return True


@client.event
async def on_message(message):
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


@client.event
async def on_guild_join(guild):
    print("joined the Server: %s" % guild.name)
    print("creating configs...")
    init_db()


@client.event
async def on_ready():
    print("Bot started succesfully...\n")
    await client.change_presence(activity=discord.Game(name='nothing...'))

    init_db()

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
