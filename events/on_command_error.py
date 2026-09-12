import discord
from discord.ext import commands


class OnCommandErrorEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                description=f"Nie znaleziono komendy `{ctx.invoked_with}`. Uzyj `!help` aby zobaczyc dostepne komendy.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed, delete_after=10)

        elif isinstance(error, commands.MissingPermissions):
            perms = ", ".join(error.missing_permissions)
            embed = discord.Embed(
                description=f"Brak uprawnien. Wymagane: `{perms}`",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed, delete_after=10)

        elif isinstance(error, commands.BotMissingPermissions):
            perms = ", ".join(error.missing_permissions)
            embed = discord.Embed(
                description=f"Bot nie posiada wymaganych uprawnien: `{perms}`",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed, delete_after=10)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed =discord.Embed(
                description=f"Brakujacy argument: `{error.param.name}`. Uzyj `!help {ctx.command}` po wiecej informacji.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed, delete_after=10)

        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                description=f"Nieprawidlowy argument. Uzyj `!help {ctx.command}` po wiecej informacji.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed, delete_after=10)

        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                description=f"Komenda na cooldownie. Sprobuj za {error.retry_after:.1f}s.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed, delete_after=10)

        else:
            embed = discord.Embed(
                description=f"Wystapil blad: `{type(error).__name__}: {error}`",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed, delete_after=15)
            raise error


async def setup(bot):
    await bot.add_cog(OnCommandErrorEvent(bot))
