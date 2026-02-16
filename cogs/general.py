import discord
from discord.ext import commands
from discord import app_commands


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def is_approved(self, guild_id: int) -> bool:
        async with self.bot.db.acquire() as conn:
            result = await conn.fetchrow(
                "SELECT guild_id FROM approved_servers WHERE guild_id = $1",
                guild_id
            )
            return result is not None

    @app_commands.command(name="ping", description="Check if the bot is alive.")
    async def ping(self, interaction: discord.Interaction):

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

        await interaction.response.send_message("🏓 Pong!")


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
