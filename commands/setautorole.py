import discord
from discord.ext import commands
import data


class SetautoroleCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setautorole")
    @commands.has_permissions(administrator=True)
    async def setautorole_cmd(self, ctx, role: discord.Role = None):
        if role is None:
            embed = discord.Embed(
                description="Uzycie: `!setautorole @rola`\nUzyj `!setautorole off` aby wylaczyc.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        if role >= ctx.guild.me.top_role:
            embed = discord.Embed(
                description="Rola musi byc nizej niz rola bota.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        data.set_guild_setting(ctx.guild.id, "autorole", role.id)
        embed = discord.Embed(
            title="Auto-rola ustawiona",
            description=f"Nowi memberowie otrzymaja role {role.mention}.",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)

    @commands.command(name="removeautorole")
    @commands.has_permissions(administrator=True)
    async def removeautorole_cmd(self, ctx):
        data.set_guild_setting(ctx.guild.id, "autorole", None)
        embed = discord.Embed(
            description="Auto-rola zostala wylaczona.",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(SetautoroleCommand(bot))
