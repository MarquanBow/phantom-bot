import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Ghost on!")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Whats good, {ctx.author.mention}!")

with open("token.txt") as file:
    token = file.read()


bot.run(token)
