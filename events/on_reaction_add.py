import discord
from discord.ext import commands
import data


class OnReactionAddEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        message_id = str(reaction.message.id)
        rr = data.get_reaction_role(message_id)
        if not rr:
            return

        if str(reaction.emoji) != rr["emoji"]:
            return

        guild = reaction.message.guild
        if not guild:
            return

        role = guild.get_role(rr["role_id"])
        if not role:
            return

        try:
            await user.add_roles(role, reason="Reaction role")
            embed = discord.Embed(
                description=f"Nadano ci role {role.mention}.",
                color=discord.Color.green(),
            )
            try:
                await user.send(embed=embed)
            except discord.Forbidden:
                pass
        except discord.Forbidden:
            embed = discord.Embed(
                description="Brak uprawnien do nadania roli.",
                color=discord.Color.red(),
            )
            try:
                await user.send(embed=embed)
            except discord.Forbidden:
                pass


async def setup(bot):
    await bot.add_cog(OnReactionAddEvent(bot))
