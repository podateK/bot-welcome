import discord
from discord.ext import commands
import data


class LevelCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="level")
    async def level_cmd(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        entry = data.get_xp(ctx.guild.id, member.id)

        embed = discord.Embed(
            title=f"Poziom - {member.display_name}",
            color=discord.Color.blurple(),
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Poziom", value=str(entry["level"]), inline=True)
        embed.add_field(name="XP", value=str(entry["xp"]), inline=True)
        embed.add_field(
            name="Nastepny poziom",
            value=f"{entry['xp'] - (entry['level'] * 100)}/100 XP",
            inline=True,
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(LevelCommand(bot))
