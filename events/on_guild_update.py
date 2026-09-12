import discord
from discord.ext import commands
import data


class OnGuildUpdateEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        log_channel_id = data.get_guild_setting(before.id, "log_channel")
        if not log_channel_id:
            return
        log_channel = before.get_channel(log_channel_id)
        if not log_channel:
            return

        embed = discord.Embed(
            title="Serwer zaktualizowany",
            color=discord.Color.blue(),
        )

        if before.name != after.name:
            embed.add_field(name="Nazwa", value=f"`{before.name}` -> `{after.name}`", inline=False)
        if before.icon != after.icon:
            embed.set_image(url=after.icon.url if after.icon else "")
            embed.add_field(name="Ikona", value="Zostala zaktualizowana", inline=False)
        if before.owner != after.owner:
            embed.add_field(
                name="Wlasciciel",
                value=f"{before.owner} -> {after.owner}",
                inline=False,
            )
        if before.description != after.description:
            embed.add_field(
                name="Opis",
                value=f"`{before.description}` -> `{after.description}`",
                inline=False,
            )
        if before.mfa_level != after.mfa_level:
            embed.add_field(
                name="Wymagane 2FA",
                value=f"{'Tak' if after.mfa_level else 'Nie'}",
                inline=True,
            )
        if before.verification_level != after.verification_level:
            embed.add_field(
                name="Poziom weryfikacji",
                value=str(after.verification_level),
                inline=True,
            )

        if embed.fields:
            await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(OnGuildUpdateEvent(bot))
