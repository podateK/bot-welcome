import discord
from discord.ext import commands
import data


class OnGuildRoleCreateEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        log_channel_id = data.get_guild_setting(role.guild.id, "log_channel")
        if not log_channel_id:
            return
        log_channel = role.guild.get_channel(log_channel_id)
        if not log_channel:
            return

        embed = discord.Embed(
            title="Nowa rola utworzona",
            color=discord.Color.green(),
        )
        embed.add_field(name="Nazwa", value=role.mention, inline=True)
        embed.add_field(name="ID", value=role.id, inline=True)
        embed.add_field(name="Kolor", value=str(role.color), inline=True)
        embed.add_field(name="Oddzielna", value="Tak" if role.hoist else "Nie", inline=True)
        embed.add_field(name="Mentionowalna", value="Tak" if role.mentionable else "Nie", inline=True)
        embed.set_footer(text=f"Pozycja: {role.position}")
        await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(OnGuildRoleCreateEvent(bot))
