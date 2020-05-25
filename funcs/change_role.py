import discord
from discord.utils import get
from globals import get_setting, change_setting


async def execute(client, message, args):
    # check permission of user
    roles = []
    for role in message.author.roles:
        roles.append(role.name)
    if not "Queue Admin" in roles:
        if message.author.id == message.guild.owner_id:
            await message.channel.send("Notice: You are allowed to use this command, because you are the owner of this server. Would you mind giving yourself the **Queue Admin** role for redundance? You can also give it to other people for administrating QueueBot.")
        else:
            await message.channel.send("", embed=discord.Embed(title="Insufficient permissions!", description="You need the 'Queue Admin' role to be able to perform this action.", color=discord.Color.red()))
            return

    # check if correct option was provided
    if args == []:
        await message.channel.send("Please provide the role id of the support team.")
        return
    
    else:
        try:
            args[1] = int(args[1])
        except ValueError:
            await message.channel.send("", embed=discord.Embed(title="🚫 Please provide a role ID.", description="You need to provide the role id of the support role.", color=discord.Color.red())
                                                .add_field(
                                                    name="Step 1 (Enable developer mode)",
                                                    value="Go to User settings -> Appearance, scroll down and check 'developer mode'.",
                                                    inline=False
                                                )
                                                .add_field(
                                                    name="Step 2 (Copy the role ID of the support role)",
                                                    value="Go to you server's settings -> Roles, right click the support role and click 'Copy ID'.",
                                                    inline=False
                                                ))
            return

        if not get(message.guild.roles, id=args[1]):
            await message.channel.send("", embed=discord.Embed(title="", description="🚫 This role does not exist.", color=discord.Color.red()))
            return

        # change and check change; notify on discord
        if change_setting(message.guild.id, "supportrole", str(args[1])):
            await message.channel.send("", embed=discord.Embed(title="Support role changed!", description="✅ The support role has been changed successfully!", color=discord.Color.green()))
        else:
            await message.channel.send("There was an error changing the Support role. It's probably not your fault. Please consult the bot hoster!")        

        return
