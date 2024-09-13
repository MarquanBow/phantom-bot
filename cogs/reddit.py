import discord
from discord.ext import commands
from random import choice
import asyncpraw as praw

class Reddit(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot
        self.reddit = praw.Reddit(client_id="rkguW1ygrHSwsTkWQdbHKQ", client_secret="fUEPjtZ2138TI0pYTTJnHNesa21H6Q", user_agent="script:randommeme:v1.0 (by u/RugduQuan)")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready!")

    @commands.command()
    async def meme(self, ctx: commands.Context):

        subreddit = await self.reddit.subreddit("Animemes")
        posts_list = []

        async for post in subreddit.hot(limit=30):
            if not post.over_18 and post.author is not None and any(post.url.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif"]):
                author_name = post.author.name
                posts_list.append((post.url, author_name))
            if post.author is None:
                posts_list.append((post.url, "N/A"))

        if posts_list:

            random_post = choice(posts_list)

            meme_embed = discord.Embed(title="Random Meme", description="Fetches random memes from r/Animemes", color=discord.Color.random())
            meme_embed.set_author(name=f"Meme requested by {ctx.author.name}", icon_url=ctx.author.avatar)
            meme_embed.set_image(url=random_post[0])
            meme_embed.set_footer(text=f"Post created by {random_post[1]}.", icon_url=None)
            await ctx.send(embed=meme_embed)

        else:
            await ctx.send("Unable to fetch post, try again later")

    def cog_unload(self):
        self.bot.loop.create_task(self.reddit.close())    

async def setup(bot):
     await bot.add_cog(Reddit(bot))