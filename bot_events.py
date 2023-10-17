from discord.ext import commands

class BotEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name} ({self.bot.user.id})')
        print('Bot is ready')
        channel = self.bot.get_channel(1124371481825136683)
        await channel.send("Hello! I'm online now 🚀")

    @commands.Cog.listener()
    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(f"Command error: {error}")
