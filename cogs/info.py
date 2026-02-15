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
# Info Cog
# ----------------------------

class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="serverinfo", description="Get information about the server.")
    async def serverinfo(self, interaction: discord.Interaction):

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
