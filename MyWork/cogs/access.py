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
        await interaction.response.defer(ephemeral=True)

        if interaction.guild is None:
            await interaction.followup.send("Use this inside a server.")
            return

        if await self.is_approved(interaction.guild.id):
            await interaction.followup.send("This server is already approved.")
            return

        owner = await self.bot.fetch_user(OWNER_ID)
        if owner:
            await owner.send(
                f"🚨 **Access Request**\n"
                f"**Server:** {interaction.guild.name}\n"
                f"**ID:** {interaction.guild.id}"
            )
        
        await interaction.followup.send("Access request sent to bot owner.")

    @app_commands.command(name="approve", description="Approve a server.")
    async def approve(self, interaction: discord.Interaction, server_id: str):
        await interaction.response.defer(ephemeral=True)

        if interaction.user.id != OWNER_ID:
            await interaction.followup.send("Not authorized.")
            return

        try:
            guild_id = int(server_id)
            async with self.bot.db.acquire() as conn:
                await conn.execute(
                    "INSERT INTO approved_servers (guild_id) VALUES ($1) ON CONFLICT DO NOTHING",
                    guild_id
                )
            await interaction.followup.send(f"Server {guild_id} approved.")
        except Exception as e:
            await interaction.followup.send(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(Access(bot))