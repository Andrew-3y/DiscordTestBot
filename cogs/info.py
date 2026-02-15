import discord
from discord.ext import commands
from discord import app_commands
import json


def load_approved():
    with open("approved_servers.json", "r") as f:
        return json.load(f)


def is_approved(guild_id):
    return guild_id in load_approved()


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="serverinfo", description="Get information about the server.")
    async def serverinfo(self, interaction: discord.Interaction):

        guild = interaction.guild

        if guild is None or not is_approved(guild.id):
            await interaction.response.send_message(
                "This server is not approved. Use /requestaccess.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"Server Name: {guild.name}\n"
            f"Members: {guild.member_count}\n"
            f"Server ID: {guild.id}"
        )


async def setup(bot):
    await bot.add_cog(Info(bot))
