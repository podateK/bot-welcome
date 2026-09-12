import discord
from discord.ext import commands
import data


class SetwelcomeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setwelcome")
    @commands.has_permissions(administrator=True)
    async def setwelcome_cmd(self, ctx, *, text: str = None):
        if text is None:
            embed = discord.Embed(
                description="Uzycie: `!setwelcome <wiadomosc>`\n"
                "Dostepne zmienne: `{user}`, `{server}`",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        data.set_guild_setting(ctx.guild.id, "welcome_msg", text)

        embed = discord.Embed(
            title="Wiadomosc powitalna ustawiona",
            description=f"Nowa wiadomosc:\n{text}",
            color=discord.Color.green(),
        )
        embed.set_footer(text="Uzyj !welcomecard aby zobaczyc podglad.")
        await ctx.send(embed=embed)

    @commands.command(name="setwelcomechannel")
    @commands.has_permissions(administrator=True)
    async def setwelcomechannel_cmd(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            embed = discord.Embed(
                description="Uzycie: `!setwelcomechannel #kanal`",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        data.set_guild_setting(ctx.guild.id, "welcome_channel", channel.id)
        embed = discord.Embed(
            description=f"Kanal powitalny ustawiony na {channel.mention}.",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(SetwelcomeCommand(bot))
