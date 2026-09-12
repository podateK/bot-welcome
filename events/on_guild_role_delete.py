import discord
from discord.ext import commands
import data


class OnGuildRoleDeleteEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        log_channel_id = data.get_guild_setting(role.guild.id, "log_channel")
        if not log_channel_id:
            return
        log_channel = role.guild.get_channel(log_channel_id)
        if not log_channel:
            return

        embed = discord.Embed(
            title="Rola usunieta",
            color=discord.Color.red(),
        )
        embed.add_field(name="Nazwa", value=role.name, inline=True)
        embed.add_field(name="ID", value=role.id, inline=True)
        embed.add_field(name="Kolor", value=str(role.color), inline=True)
        embed.set_footer(text=f"Byla na pozycji: {role.position}")
        await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(OnGuildRoleDeleteEvent(bot))
