import discord
from discord.ext import commands
from discord import app_commands


class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def is_approved(self, guild_id: int) -> bool:
        async with self.bot.db.acquire() as conn:
            result = await conn.fetchrow(
                "SELECT guild_id FROM approved_servers WHERE guild_id = $1",
                guild_id
            )
            return result is not None

    @app_commands.command(name="serverinfo", description="Get information about the server.")
    async def serverinfo(self, interaction: discord.Interaction):

        if interaction.guild is None:
            await interaction.response.send_message(
                "Use this command inside a server.",
                ephemeral=True
            )
            return

        if not await self.is_approved(interaction.guild.id):
            await interaction.response.send_message(
                "This server is not approved. Use /requestaccess.",
                ephemeral=True
            )
            return

        guild = interaction.guild

        embed = discord.Embed(
            title="📊 Server Information",
            color=discord.Color.blue()
        )

        embed.add_field(name="Server Name", value=guild.name, inline=False)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Server ID", value=guild.id, inline=True)

        if guild.owner:
            embed.add_field(name="Owner", value=str(guild.owner), inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))
