import discord
from discord.ext import commands
import data


class OnReactionRemoveEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
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
            await user.remove_roles(role, reason="Reaction role usuniety")
            embed = discord.Embed(
                description=f"Zabrano ci role {role.mention}.",
                color=discord.Color.orange(),
            )
            try:
                await user.send(embed=embed)
            except discord.Forbidden:
                pass
        except discord.Forbidden:
            pass


async def setup(bot):
    await bot.add_cog(OnReactionRemoveEvent(bot))
