import discord
from discord.ext import commands
import data


class OnMemberRemoveEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        log_channel_id = data.get_guild_setting(guild.id, "log_channel")
        log_channel = guild.get_channel(log_channel_id) if log_channel_id else None

        goodbye_msg = data.get_guild_setting(
            guild.id, "goodbye_msg", "{user} opuscil(a) nasz serwer."
        )
        goodbye_channel_id = data.get_guild_setting(guild.id, "goodbye_channel")
        goodbye_channel = guild.get_channel(goodbye_channel_id) if goodbye_channel_id else guild.system_channel

        if goodbye_channel:
            roles = [r.mention for r in member.roles[1:]]
            embed = discord.Embed(
                title="Do widzenia!",
                description=goodbye_msg.format(user=member.display_name, server=guild.name),
                color=discord.Color.red(),
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"ID: {member.id}")
            if roles:
                embed.add_field(name="Role", value=", ".join(roles), inline=False)
            embed.add_field(name="Pozostali", value=f"{guild.member_count} memberow")
            try:
                await goodbye_channel.send(embed=embed)
            except discord.Forbidden:
                pass

        if log_channel:
            embed = discord.Embed(
                title="Member opuscil serwer",
                description=f"{member.display_name}#{member.discriminator} opuscil serwer.",
                color=discord.Color.red(),
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.add_field(name="Pozostali", value=f"{guild.member_count} memberow")
            await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(OnMemberRemoveEvent(bot))
