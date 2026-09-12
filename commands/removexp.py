import discord
from discord.ext import commands
import data


class RemovexpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="removexp")
    @commands.has_permissions(administrator=True)
    async def removexp_cmd(self, ctx, member: discord.Member = None, amount: int = None):
        if member is None or amount is None:
            embed = discord.Embed(
                description="Uzycie: `!removexp @uzytkownik <ilosc>`",
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

        entry = data.remove_xp(ctx.guild.id, member.id, amount)

        embed = discord.Embed(
            title="XP usuniete",
            description=f"-{amount} XP od {member.mention}",
            color=discord.Color.red(),
        )
        embed.add_field(name="Aktualne XP", value=str(entry["xp"]), inline=True)
        embed.add_field(name="Poziom", value=str(entry["level"]), inline=True)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(RemovexpCommand(bot))
