import discord
from funcs import change_prefix, change_queue, change_role, change_text, change_video

async def execute(client, message, args):
    if args[0] == "prefix":
        await change_prefix.execute(client, message, args)
    elif args[0] == "queue":
        await change_queue.execute(client, message, args)
    elif args[0] == "role":
        await change_role.execute(client, message, args)
    elif args[0] == "video":
        await change_video.execute(client, message, args)
    elif args[0] == "text":
        await change_text.execute(client, message, args)