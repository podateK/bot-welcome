import discord
from discord.ext import commands
import data


class ResetstatsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="resetstats")
    @commands.has_permissions(administrator=True)
    async def resetstats_cmd(self, ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed(
                description="Uzycie: `!resetstats @uzytkownik`",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        data.reset_xp(ctx.guild.id, member.id)

        embed = discord.Embed(
            title="Statystyki zresetowane",
            description=f"XP i poziom {member.mention} zostaly zresetowane.",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ResetstatsCommand(bot))
