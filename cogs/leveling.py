import discord
from discord.ext import commands
from pymongo import MongoClient
import math
import random
import os

class LevelSys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Connect to MongoDB using the connection string
        mongo_uri: str = os.getenv("mongo_uri")  # Store this securely in environment variables
        self.client = MongoClient(mongo_uri)
        self.db = self.client['Users']  # Use your database name
        self.collection = self.db['levels']   # Use your collection name
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Leveling system is online!")
        
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return 

        guild_id = message.guild.id
        user_id = message.author.id
        
        user_data = self.collection.find_one({"guild_id": guild_id, "user_id": user_id})

        if user_data is None:
            cur_level = 0
            xp = 0
            level_up_xp = 100
            self.collection.insert_one({
                "guild_id": guild_id,
                "user_id": user_id,
                "level": cur_level,
                "xp": xp,
                "level_up_xp": level_up_xp
            })
        else:
            cur_level = user_data["level"]
            xp = user_data["xp"]
            level_up_xp = user_data["level_up_xp"]
            
            xp += random.randint(1, 25)
            
            if xp >= level_up_xp:
                cur_level += 1            
                new_level_up_xp = math.ceil(50 * cur_level ** 2 + 100 * cur_level + 50)
                xp = 0  # Reset XP after leveling up
                
                await message.channel.send(f"{message.author.mention} has leveled up to level {cur_level}!")
                
                self.collection.update_one(
                    {"guild_id": guild_id, "user_id": user_id},
                    {"$set": {"level": cur_level, "xp": xp, "level_up_xp": new_level_up_xp}}
                )
            else:
                self.collection.update_one(
                    {"guild_id": guild_id, "user_id": user_id},
                    {"$set": {"xp": xp}}
                )

    @commands.command()
    async def level(self, ctx: commands.Context, member: discord.Member=None):
        if member is None:
            member = ctx.author
        
        member_id = member.id
        guild_id = ctx.guild.id
        
        user_data = self.collection.find_one({"guild_id": guild_id, "user_id": member_id})
        
        if user_data is None:
            await ctx.send(f"{member.name} currently does not have a level.")
        else:
            level = user_data["level"]
            xp = user_data["xp"]
            level_up_xp = user_data["level_up_xp"]
            
            await ctx.send(f"Level Statistics for {member.name}: \nLevel: {level} \nXP: {xp} \nXP To Level Up: {level_up_xp}")
    
    def cog_unload(self):
        self.client.close()

async def setup(bot):
    await bot.add_cog(LevelSys(bot))