import discord
from discord.ext import commands
from discord import app_commands
import json
import os

APPROVED_FILE = "approved_servers.json"
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# Read owner servers from environment variable
OWNER_SERVERS = os.getenv("OWNER_SERVERS", "")
OWNER_SERVER_IDS = [
    int(server_id.strip())
    for server_id in OWNER_SERVERS.split(",")
    if server_id.strip().isdigit()
]


def load_approved():
    try:
        with open(APPROVED_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_approved(data):
    with open(APPROVED_FILE, "w") as f:
        json.dump(data, f, indent=4)


def is_approved(guild_id: int) -> bool:
    # Automatically approve owner servers
    if guild_id in OWNER_SERVER_IDS:
        return True

    return guild_id in load_approved()


class Access(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="requestaccess",
        description="Request access to use this bot."
    )
    async def requestaccess(self, interaction: discord.Interaction):

        guild = interaction.guild

        if guild is None:
            await interaction.response.send_message(
                "This command must be used inside a server.",
                ephemeral=True
            )
            return

        if is_approved(guild.id):
            await interaction.response.send_message(
                "This server is already approved.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            "Access request sent to the bot owner.",
            ephemeral=True
        )

        try:
            owner = await self.bot.fetch_user(OWNER_ID)

            if owner:
                await owner.send(
                    f"🔔 Access Request\n\n"
                    f"Server Name: {guild.name}\n"
                    f"Server ID: {guild.id}\n\n"
                    f"Use `/approve {guild.id}` to approve."
                )
        except Exception as e:
            print("Failed to DM owner:", e)

    @app_commands.command(
        name="approve",
        description="Approve a server."
    )
    async def approve(self, interaction: discord.Interaction, server_id: str):

        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message(
                "You are not authorized.",
                ephemeral=True
            )
            return

        approved = load_approved()
        server_id_int = int(server_id)

        if server_id_int not in approved:
            approved.append(server_id_int)
            save_approved(approved)

        await interaction.response.send_message(
            f"Server {server_id} approved.",
            ephemeral=True
        )

    @app_commands.command(
        name="deny",
        description="Deny a server."
    )
    async def deny(self, interaction: discord.Interaction, server_id: str):

        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message(
                "You are not authorized.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"Server {server_id} denied.",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Access(bot))
