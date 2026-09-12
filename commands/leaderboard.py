import discord
from discord.ext import commands
import data


class LeaderboardCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="leaderboard", aliases=["lb", "top"])
    async def leaderboard_cmd(self, ctx):
        leaderboard = data.get_leaderboard(ctx.guild.id, limit=10)
        if not leaderboard:
            embed = discord.Embed(
                description="Brak danych w rankingu.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        medals = ["", "", ""]
        description = ""
        for i, (user_id, xp, level) in enumerate(leaderboard):
            member = ctx.guild.get_member(user_id)
            name = member.display_name if member else f"Uzytkownik ({user_id})"
            medal = medals[i] if i < 3 else f"**#{i+1}**"
            description += f"{medal} {name} - **{xp} XP** (poziom {level})\n"

        embed = discord.Embed(
            title="Ranking TOP 10",
            description=description,
            color=discord.Color.gold(),
        )
        embed.set_footer(text=f"Serwer: {ctx.guild.name}")
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else "")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(LeaderboardCommand(bot))
