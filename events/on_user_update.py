import discord
from discord.ext import commands
import data


class OnUserUpdateEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if not before.guilds:
            return

        for guild in before.mutual_guilds:
            log_channel_id = data.get_guild_setting(guild.id, "log_channel")
            if not log_channel_id:
                continue
            log_channel = guild.get_channel(log_channel_id)
            if not log_channel:
                continue

            embed = discord.Embed(
                title="Zaktualizowano profil",
                description=f"{after.mention} zaktualizowal(a) swoj profil.",
                color=discord.Color.purple(),
            )

            if before.name != after.name:
                embed.add_field(name="Nazwa", value=f"`{before.name}` -> `{after.name}`", inline=False)
            if before.display_name != after.display_name:
                embed.add_field(name="Nazwa wyswietlana", value=f"`{before.display_name}` -> `{after.display_name}`", inline=False)
            if before.discriminator != after.discriminator:
                embed.add_field(name="Discriminator", value=f"`{before.discriminator}` -> `{after.discriminator}`", inline=False)
            if before.display_avatar.url != after.display_avatar.url:
                embed.set_image(url=after.display_avatar.url)
                embed.add_field(name="Avatar", value="Zostal zaktualizowany", inline=False)

            if embed.fields:
                await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(OnUserUpdateEvent(bot))
