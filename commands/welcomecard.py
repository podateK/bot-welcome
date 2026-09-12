import discord
from discord.ext import commands
import data


class WelcomecardCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="welcomecard")
    async def welcomecard_cmd(self, ctx):
        welcome_msg = data.get_guild_setting(
            ctx.guild.id, "welcome_msg", "Witamy na serwerze {user}!"
        )
        autorole_id = data.get_guild_setting(ctx.guild.id, "autorole")
        autorole = ctx.guild.get_role(autorole_id) if autorole_id else None

        embed = discord.Embed(
            title="Podglad karty powitalnej",
            color=discord.Color.blurple(),
        )
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.add_field(
            name="Wiadomosc",
            value=welcome_msg.format(user=ctx.author.mention, server=ctx.guild.name),
            inline=False,
        )
        if autorole:
            embed.add_field(name="Auto-rola", value=autorole.mention, inline=True)
        else:
            embed.add_field(name="Auto-rola", value="Wylaczona", inline=True)

        embed.add_field(
            name="Kanal powitalny",
            value=f"<#{data.get_guild_setting(ctx.guild.id, 'welcome_channel', ctx.guild.system_channel.id)}>",
            inline=True,
        )
        embed.set_footer(text="Uzyj !setwelcome aby zmienic wiadomosc.")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(WelcomecardCommand(bot))
