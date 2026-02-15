import discord
from discord.ext import commands
from discord import app_commands
import json


def load_approved():
    with open("approved_servers.json", "r") as f:
        return json.load(f)


def is_approved(guild_id: int) -> bool:
    return guild_id in load_approved()


class Poll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="poll", description="Create a simple yes/no poll.")
    @app_commands.describe(question="The question for the poll")
    async def poll(self, interaction: discord.Interaction, question: str):

        if interaction.guild is None:
            await interaction.response.send_message(
                "Use this command inside a server.",
                ephemeral=True
            )
            return

        if not is_approved(interaction.guild.id):
            await interaction.response.send_message(
                "This server is not approved. Use /requestaccess first.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="📊 Poll",
            description=question
        )
        embed.set_footer(text=f"Requested by {interaction.user}")

        await interaction.response.send_message(embed=embed)

        message = await interaction.original_response()
        await message.add_reaction("👍")
        await message.add_reaction("👎")


async def setup(bot: commands.Bot):
    await bot.add_cog(Poll(bot))
