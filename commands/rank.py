import discord
from discord.ext import commands
import data


class RankCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rank")
    async def rank_cmd(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        guild_id = ctx.guild.id
        user_id = member.id
        entry = data.get_xp(guild_id, user_id)

        xp = entry["xp"]
        level = entry["level"]
        next_level = (level + 1) * 100
        xp_in_level = xp - (level * 100)
        xp_needed = 100

        all_data = data.get_all_xp()
        prefix = f"{guild_id}:"
        sorted_users = sorted(
            [(k, v) for k, v in all_data.items() if k.startswith(prefix)],
            key=lambda x: x[1]["xp"],
            reverse=True,
        )
        rank_pos = None
        for i, (k, v) in enumerate(sorted_users, 1):
            if k == f"{guild_id}:{user_id}":
                rank_pos = i
                break

        bar_length = 20
        filled = int(bar_length * xp_in_level / xp_needed)
        bar = "█" * filled + "░" * (bar_length - filled)

        embed = discord.Embed(
            title=f"Rank - {member.display_name}",
            color=discord.Color.blurple(),
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Poziom", value=str(level), inline=True)
        embed.add_field(name="XP", value=f"{xp}", inline=True)
        embed.add_field(name="Nastepny poziom", value=f"{xp_in_level}/{xp_needed} XP", inline=True)
        embed.add_field(name="Pasek postepu", value=f"`{bar}`", inline=False)
        if rank_pos:
            embed.add_field(name="Miejsce w rankingu", value=f"#{rank_pos}", inline=True)
        embed.set_footer(text=f"ID: {user_id}")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(RankCommand(bot))
