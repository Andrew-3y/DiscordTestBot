import discord
from discord.ext import commands
from discord import app_commands

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_approved(self, guild_id: int) -> bool:
        """Queries the Postgres database for server approval status."""
        async with self.bot.db.acquire() as conn:
            result = await conn.fetchrow(
                "SELECT guild_id FROM approved_servers WHERE guild_id = $1",
                guild_id
            )
            return result is not None

    @app_commands.command(name="poll", description="Create a simple yes/no poll.")
    @app_commands.describe(question="The question for the poll")
    async def poll(self, interaction: discord.Interaction, question: str):
        if interaction.guild is None:
            await interaction.response.send_message("Use this command inside a server.", ephemeral=True)
            return

        # Check database for server approval
        if not await self.is_approved(interaction.guild.id):
            await interaction.response.send_message(
                "This server is not approved. Use /requestaccess first.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="📊 Poll",
            description=question,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Requested by {interaction.user}")

        await interaction.response.send_message(embed=embed)
        
        # Add reactions to the response
        message = await interaction.original_response()
        await message.add_reaction("👍")
        await message.add_reaction("👎")

async def setup(bot):
    await bot.add_cog(Poll(bot))