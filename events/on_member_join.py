import discord
from discord.ext import commands
import data


class OnMemberJoinEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        log_channel_id = data.get_guild_setting(guild.id, "log_channel")
        log_channel = guild.get_channel(log_channel_id) if log_channel_id else None

        welcome_msg = data.get_guild_setting(
            guild.id, "welcome_msg", "Witamy na serwerze {user}!"
        )
        welcome_channel_id = data.get_guild_setting(guild.id, "welcome_channel")
        welcome_channel = guild.get_channel(welcome_channel_id) if welcome_channel_id else guild.system_channel

        if welcome_channel:
            embed = discord.Embed(
                title="Witamy na serwerze!",
                description=welcome_msg.format(user=member.mention, server=guild.name),
                color=discord.Color.green(),
                timestamp=member.joined_at,
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"ID: {member.id}")
            embed.add_field(
                name="Konto utworzone",
                value=f"<t:{int(member.created_at.timestamp())}:R>",
                inline=True,
            )
            embed.add_field(
                name="Numer membera",
                value=f"#{guild.member_count}",
                inline=True,
            )
            try:
                await welcome_channel.send(embed=embed)
            except discord.Forbidden:
                pass

        autorole_id = data.get_guild_setting(guild.id, "autorole")
        if autorole_id:
            role = guild.get_role(autorole_id)
            if role:
                try:
                    await member.add_roles(role, reason="Auto-role dla nowych memberow")
                except discord.Forbidden:
                    if log_channel:
                        await log_channel.send(
                            embed=discord.Embed(
                                description=f"Brak uprawnien do nadania roli {role.mention} memberowi {member.mention}.",
                                color=discord.Color.red(),
                            )
                        )

        if log_channel:
            embed = discord.Embed(
                title="Nowy member",
                description=f"{member.mention} dolaczyl do serwera.",
                color=discord.Color.green(),
                timestamp=member.joined_at,
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.add_field(name="Konto utworzone", value=f"<t:{int(member.created_at.timestamp())}:R>")
            embed.add_field(name="Numer membera", value=f"#{guild.member_count}")
            await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(OnMemberJoinEvent(bot))
