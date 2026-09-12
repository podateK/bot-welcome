import discord
from discord.ext import commands
import data


class OnMemberUpdateEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles == after.roles:
            return

        log_channel_id = data.get_guild_setting(before.guild.id, "log_channel")
        if not log_channel_id:
            return
        log_channel = before.guild.get_channel(log_channel_id)
        if not log_channel:
            return

        added = set(after.roles) - set(before.roles)
        removed = set(before.roles) - set(after.roles)

        if added:
            for role in added:
                embed = discord.Embed(
                    title="Rola nadana",
                    description=f"{after.mention} otrzymal role {role.mention}",
                    color=discord.Color.blue(),
                )
                await log_channel.send(embed=embed)

        if removed:
            for role in removed:
                embed = discord.Embed(
                    title="Rola zabrana",
                    description=f"{after.mention} stracil role {role.mention}",
                    color=discord.Color.orange(),
                )
                await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(OnMemberUpdateEvent(bot))
