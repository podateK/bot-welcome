import discord
from discord.ext import commands


class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping_cmd(self, ctx):
        latency_ms = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="Pong!",
            color=discord.Color.green() if latency_ms < 200 else discord.Color.orange() if latency_ms < 500 else discord.Color.red(),
        )
        embed.add_field(name="Opoznienie bota", value=f"{latency_ms}ms", inline=True)
        embed.add_field(name="Websocket", value=f"{latency_ms}ms", inline=True)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(PingCommand(bot))
