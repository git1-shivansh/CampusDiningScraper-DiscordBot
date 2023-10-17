from discord.ext import commands
from scraper import scrape_menu


class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello!')

    @commands.command()
    async def menu(self, ctx, meal, *, date):
        scraped_data = scrape_menu(meal, date)
        message = "\n".join([f"{key}: {' '.join(value)}" for key, value in scraped_data.items()])
        await ctx.send(f"Menu for {meal} on {date}\n{message}")

