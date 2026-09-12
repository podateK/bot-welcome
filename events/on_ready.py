import discord
from discord.ext import commands


class OnReadyEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"-----------------------------")
        print(f"Zalogowano jako: {self.bot.user}")
        print(f"ID Bota: {self.bot.user.id}")
        print(f"Liczba serwerow: {len(self.bot.guilds)}")
        print(f"discord.py wersja: {discord.__version__}")
        print(f"-----------------------------")
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(self.bot.guilds)} serwerow | !pomoc"
            )
        )


async def setup(bot):
    await bot.add_cog(OnReadyEvent(bot))
