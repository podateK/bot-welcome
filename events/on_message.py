import discord
from discord.ext import commands
import time
import data


class OnMessageEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.guild:
            return

        guild_id = message.guild.id
        user_id = message.author.id
        now = time.time()

        last_time = self.cooldowns.get(f"{guild_id}:{user_id}", 0)
        if now - last_time < 60:
            return

        self.cooldowns[f"{guild_id}:{user_id}"] = now

        entry, leveled_up = data.add_xp(guild_id, user_id, 10)

        if leveled_up:
            level = entry["level"]
            embed = discord.Embed(
                title="Level Up!",
                description=f"{message.author.mention} awansowal(a) na **poziom {level}**!",
                color=discord.Color.gold(),
            )
            embed.set_thumbnail(url=message.author.display_avatar.url)
            try:
                await message.channel.send(embed=embed)
            except discord.Forbidden:
                pass

        await self.bot.process_commands(message)


async def setup(bot):
    await bot.add_cog(OnMessageEvent(bot))
