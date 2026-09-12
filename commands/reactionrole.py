import discord
from discord.ext import commands
import data


class ReactionroleCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reactionrole")
    @commands.has_permissions(administrator=True)
    async def reactionrole_cmd(self, ctx, message_id: int = None, emoji: str = None, role: discord.Role = None):
        if message_id is None or emoji is None or role is None:
            embed = discord.Embed(
                description=(
                    "Uzycie: `!reactionrole <id_wiadomosci> <emoji> @rola`\n\n"
                    "**Kroki:**\n"
                    "1. Wyslij wiadomosc z info o rolach\n"
                    "2. Skopiuj ID wiadomosci (tryb deweloperski)\n"
                    "3. Uzyj komendy z ID, emoji i rola"
                ),
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

        try:
            message = await ctx.channel.fetch_message(message_id)
        except discord.NotFound:
            embed = discord.Embed(
                description="Nie znaleziono wiadomosci na tym kanale.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        try:
            await message.add_reaction(emoji)
        except discord.HTTPException:
            embed = discord.Embed(
                description="Nie udalo sie dodac reakcji. Sprawdz czy emoji jest prawidlowe.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        data.set_reaction_role(message_id, emoji, role.id)

        embed = discord.Embed(
            title="Reaction role ustawiony",
            description=f"Emoji {emoji} -> {role.mention}\nWiadomosc: [kliknij](https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{message_id})",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)

    @commands.command(name="removereactionrole")
    @commands.has_permissions(administrator=True)
    async def removereactionrole_cmd(self, ctx, message_id: int = None):
        if message_id is None:
            embed = discord.Embed(
                description="Uzycie: `!removereactionrole <id_wiadomosci>`",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        rr = data.get_reaction_role(message_id)
        if not rr:
            embed = discord.Embed(
                description="Nie znaleziono reaction role dla tej wiadomosci.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        data.remove_reaction_role(message_id)
        embed = discord.Embed(
            description="Reaction role zostal usuniety.",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ReactionroleCommand(bot))
