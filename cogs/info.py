import discord
from discord import app_commands
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="serverinfo", description="Shows server info")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        await interaction.response.send_message(
            f"Server Name: {guild.name}\n"
            f"Total Members: {guild.member_count}\n"
            f"Server ID: {guild.id}"
        )

async def setup(bot):
    await bot.add_cog(Info(bot))
