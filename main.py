import discord
from discord.ext import commands, tasks
import os
import asyncio
from itertools import cycle
import logging
from dotenv import load_dotenv

load_dotenv()
TOKEN: str = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

bot_statuses = cycle(["Welcome to Q-T Blerd House", "Hello from ThatBlerdQuan", "Hello from MMToby", "Subscribe to ThatBlerdQuan", "Subscribe to MMToby"])

@tasks.loop(seconds=5)
async def change_bot_status():
    await bot.change_presence(activity=discord.Game(next(bot_statuses)))

@bot.event
async def on_ready():
    print("Bot ready!")
    change_bot_status.start()

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello there, {ctx.author.mention}!")

@bot.command(aliases=["gm", "morning"])
async def goodmorning(ctx):
    await ctx.send(f"Good morning, {ctx.author.mention}!")

@bot.command()
async def sendembed(ctx):
    embedded_msg = discord.Embed(title="Title of embed", description="Description of embed", color=discord.Color.random())
    embedded_msg.set_thumbnail(url=ctx.author.avatar)
    embedded_msg.add_field(name="Name of field", value="Value of field", inline=False)
    embedded_msg.set_image(url=ctx.guild.icon)
    embedded_msg.set_footer(text="Footer text", icon_url=ctx.author.avatar)
    await ctx.send(embed=embedded_msg)

async def load():
    for filename in os.listdir("phantom/cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)

bot.run(main())
