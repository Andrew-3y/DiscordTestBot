import discord
from discord.ext import commands
from discord import app_commands
import json


def load_approved():
    with open("approved_servers.json", "r") as f:
        return json.load(f)


def is_approved(guild_id):
    return guild_id in load_approved()


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check if the bot is alive.")
    async def ping(self, interaction: discord.Interaction):

        guild = interaction.guild

        if guild is None or not is_approved(guild.id):
            await interaction.response.send_message(
                "This server is not approved. Use /requestaccess.",
                ephemeral=True
            )
            return

        await interaction.response.send_message("Pong!")


async def setup(bot):
    await bot.add_cog(General(bot))
