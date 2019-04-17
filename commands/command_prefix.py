import discord
import time
import json


async def execute(client, message, args):
    success = False
    if len(args) <= 0:
        res = await message.channel.send(embed=discord.Embed(color=discord.Color.red(), title="**Fehler**", description="**Bitte gebe den neunen Prefix an!**"))
    else:
        name = ""
        for letter in message.guild.name:
            if letter.isalpha():
                name += letter

        config = json.load(open("configs/%s.json" % name))
        config["config"]["prefix"] = args[0]
        success = True

    if success:
        res = await message.channel.send(embed=discord.Embed(color=discord.Color.green(), title="**Erfolg**", description="Prefix erfolgreich zu **%s** geändert!" % config["config"]["prefix"]))

    await message.delete()
    time.sleep(2)
    await res.delete()
