import discord
from discord.ext import commands
from discord import app_commands
import os

OWNER_ID = int(os.getenv("OWNER_ID", "0"))


class Access(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_approved(self, guild_id: int) -> bool:
        async with self.bot.db.acquire() as conn:
            result = await conn.fetchrow(
                "SELECT guild_id FROM approved_servers WHERE guild_id = $1",
                guild_id
            )
            return result is not None

    @app_commands.command(name="requestaccess", description="Request access to use this bot.")
    async def requestaccess(self, interaction: discord.Interaction):

        guild = interaction.guild

        if guild is None:
            await interaction.response.send_message(
                "Use this command inside a server.",
                ephemeral=True
            )
            return

        if await self.is_approved(guild.id):
            await interaction.response.send_message(
                "This server is already approved.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            "Access request sent to the bot owner.",
            ephemeral=True
        )

        owner = await self.bot.fetch_user(OWNER_ID)
        if owner:
            await owner.send(
                f"Access Request:\n"
                f"Server: {guild.name}\n"
                f"ID: {guild.id}"
            )

    @app_commands.command(name="approve", description="Approve a server.")
    async def approve(self, interaction: discord.Interaction, server_id: str):

        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message(
                "Not authorized.",
                ephemeral=True
            )
            return

        guild_id = int(server_id)

        async with self.bot.db.acquire() as conn:
            await conn.execute(
                "INSERT INTO approved_servers (guild_id) VALUES ($1) ON CONFLICT DO NOTHING",
                guild_id
            )

        await interaction.response.send_message(
            f"Server {guild_id} approved.",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Access(bot))
