import discord
from discord.ext import commands
from discord import app_commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_approved(self, guild_id: int) -> bool:
        async with self.bot.db.acquire() as conn:
            result = await conn.fetchrow(
                "SELECT guild_id FROM approved_servers WHERE guild_id = $1",
                guild_id
            )
            return result is not None

    @app_commands.command(name="ping", description="Check if bot is alive.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.defer()

        if interaction.guild is None:
            await interaction.followup.send("Use inside a server.")
            return

        if not await self.is_approved(interaction.guild.id):
            await interaction.followup.send("Server not approved.", ephemeral=True)
            return

        await interaction.followup.send("🏓 Pong!")

async def setup(bot):
    await bot.add_cog(General(bot))