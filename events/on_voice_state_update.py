import discord
from discord.ext import commands
import time
import data


class OnVoiceStateUpdateEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vc_xp_cooldowns = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        guild_id = member.guild.id
        user_id = member.id
        now = time.time()

        in_vc = after.channel is not None and before.channel is None
        moved = after.channel is not None and before.channel is not None and after.channel != before.channel

        if in_vc or moved:
            key = f"{guild_id}:{user_id}"
            last_time = self.vc_xp_cooldowns.get(key, 0)
            if now - last_time < 120:
                return

            self.vc_xp_cooldowns[key] = now
            entry, leveled_up = data.add_xp(guild_id, user_id, 15)

            if leveled_up:
                log_channel_id = data.get_guild_setting(guild_id, "log_channel")
                log_channel = member.guild.get_channel(log_channel_id) if log_channel_id else None
                channel = log_channel or member.guild.system_channel
                if channel:
                    embed = discord.Embed(
                        title="Level Up!",
                        description=f"{member.mention} awansowal(a) na **poziom {entry['level']}** (za aktywnosc na VC)!",
                        color=discord.Color.gold(),
                    )
                    embed.set_thumbnail(url=member.display_avatar.url)
                    try:
                        await channel.send(embed=embed)
                    except discord.Forbidden:
                        pass


async def setup(bot):
    await bot.add_cog(OnVoiceStateUpdateEvent(bot))
