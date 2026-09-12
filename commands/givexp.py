import discord
from discord.ext import commands
import data


class GivexpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="givexp")
    @commands.has_permissions(administrator=True)
    async def givexp_cmd(self, ctx, member: discord.Member = None, amount: int = None):
        if member is None or amount is None:
            embed = discord.Embed(
                description="Uzycie: `!givexp @uzytkownik <ilosc>`",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        if amount <= 0:
            embed = discord.Embed(
                description="Ilosc XP musi byc wieksza od 0.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        entry, leveled_up = data.add_xp(ctx.guild.id, member.id, amount)

        embed = discord.Embed(
            title="XP nadane",
            description=f"+{amount} XP dla {member.mention}",
            color=discord.Color.green(),
        )
        embed.add_field(name="Aktualne XP", value=str(entry["xp"]), inline=True)
        embed.add_field(name="Poziom", value=str(entry["level"]), inline=True)

        if leveled_up:
            embed.add_field(
                name="Awans!",
                value=f"{member.mention} awansowal(a) na **poziom {entry['level']}**!",
                inline=False,
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(GivexpCommand(bot))
