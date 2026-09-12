import discord
from discord.ext import commands
import data


class SetgoodbyeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setgoodbye")
    @commands.has_permissions(administrator=True)
    async def setgoodbye_cmd(self, ctx, *, text: str = None):
        if text is None:
            embed = discord.Embed(
                description="Uzycie: `!setgoodbye <wiadomosc>`\n"
                "Dostepne zmienne: `{user}`, `{server}`",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        data.set_guild_setting(ctx.guild.id, "goodbye_msg", text)

        embed = discord.Embed(
            title="Wiadomosc pozegnalna ustawiona",
            description=f"Nowa wiadomosc:\n{text}",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)

    @commands.command(name="setgoodbyechannel")
    @commands.has_permissions(administrator=True)
    async def setgoodbyechannel_cmd(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            embed = discord.Embed(
                description="Uzycie: `!setgoodbyechannel #kanal`",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        data.set_guild_setting(ctx.guild.id, "goodbye_channel", channel.id)
        embed = discord.Embed(
            description=f"Kanal pozegnalny ustawiony na {channel.mention}.",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(SetgoodbyeCommand(bot))
