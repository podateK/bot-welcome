import discord
from discord.ext import commands


class ServerstatsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverstats", aliases=["stats", "serverinfo"])
    async def serverstats_cmd(self, ctx):
        guild = ctx.guild

        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        roles = len(guild.roles) - 1
        online = sum(1 for m in guild.members if m.status != discord.Status.offline)
        bots = sum(1 for m in guild.members if m.bot)

        embed = discord.Embed(
            title=f"Statystyki - {guild.name}",
            color=discord.Color.blurple(),
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(name="Wlasciciel", value=guild.owner.mention if guild.owner else "Nieznany", inline=True)
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Utworzony", value=f"<t:{int(guild.created_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Czlonkowie", value=f"{guild.member_count}", inline=True)
        embed.add_field(name="Boty", value=str(bots), inline=True)
        embed.add_field(name="Online", value=str(online), inline=True)
        embed.add_field(name="Kanaly tekstowe", value=str(text_channels), inline=True)
        embed.add_field(name="Kanaly glosowe", value=str(voice_channels), inline=True)
        embed.add_field(name="Kategorie", value=str(categories), inline=True)
        embed.add_field(name="Role", value=str(roles), inline=True)
        embed.add_field(name="Emoji", value=f"{len(guild.emojis)}/{guild.emoji_limit}", inline=True)
        embed.add_field(name="Boosty", value=f"{guild.premium_subscription_count} (poziom {guild.premium_tier})", inline=True)

        if guild.description:
            embed.add_field(name="Opis", value=guild.description, inline=False)

        embed.set_footer(text=f"Zapytane przez {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ServerstatsCommand(bot))
