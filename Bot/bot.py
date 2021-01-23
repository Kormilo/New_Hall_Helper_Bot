# Bot.py

import discord
import random
from discord.ext import commands, tasks
import os
from itertools import cycle

client = commands.Bot(command_prefix="$")


@client.event
async def on_ready():
    #await client.change_presence(status=discord.Status.idle, activity=discord.Game("Just living"))
    change_status.start()
    print("Bot is ready")


@client.event
async def on_member_join(member):
    '''This function tells the console when a user has joined the server for the first time'''
    print(f"{member} has joined the server!")


@client.event
async def on_member_remove(member):
    '''This function tells the console when a user has been kicked'''
    print(f"{member} has been removed from the server.")


# Commands

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong {round(client.latency * 1000)}ms")


@client.command(aliases=["8ball", "eightball", "Eightball"])
async def _8ball(ctx, *, question):
    responses = ["As I see it, yes",
                 "Ask again later.",
                 "Better not tell now",
                 "Cannot predict now",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "It is certain",
                 "It is decidedly so",
                 "Most likely",
                 "My reply is no",
                 "My sources say no",
                 "Outlook not so good",
                 "Outlook good.",
                 "Reply hazy, try again.",
                 "Signs point to yes.",
                 "Very doubtful.",
                 "Without a doubt.",
                 "yes.",
                 "yes - definitely.",
                 "You may rely on it"
                 ]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")


@client.command()
async def clear(ctx, amount=3):
    await ctx.channel.purge(limit=amount)


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention}")


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")


@client.command()
# We dont have the member in the server so we cant use the 'discord.Member'
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return


# Cogs

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

# Tasks
status = cycle(["Welcome to the server!", "Hope you are feeling great!", "You're awesome!", "If you need help message Lucas",
          "Help command is $help"])


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


client.run("ODAwNzc2NDI4ODA3MjU4MTEy.YAXDKg.vuv4LcJSZ3zL61oHx5ZFW2MV4Aw")
