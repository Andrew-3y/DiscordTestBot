import discord
from discord.ext import commands
from discord import app_commands
import json
import os


# ----------------------------
# Environment Variables
# ----------------------------

OWNER_SERVERS = os.getenv("OWNER_SERVERS", "")
OWNER_SERVER_IDS = [
    int(server_id.strip())
    for server_id in OWNER_SERVERS.split(",")
    if server_id.strip().isdigit()
]


# ----------------------------
# Approval System
# ----------------------------

def load_approved():
    try:
        with open("approved_servers.json", "r") as f:
            return json.load(f)
    except:
        return []


def is_approved(guild_id: int) -> bool:
    # Automatically approve owner servers
    if guild_id in OWNER_SERVER_IDS:
        return True

    return guild_id in load_approved()


# ----------------------------
# General Cog
# ----------------------------

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check if the bot is alive.")
    async def ping(self, interaction: discord.Interaction):

        if interaction.guild is None:
            await interaction.response.send_message(
                "Use this command inside a server.",
                ephemeral=True
            )
            return

        if not is_approved(interaction.guild.id):
            await interaction.response.send_message(
                "This server is not approved. Use /requestaccess.",
                ephemeral=True
            )
            return

        await interaction.response.send_message("🏓 Pong!")


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
