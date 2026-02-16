import discord
from discord.ext import commands
import asyncpg
import os
import asyncio

# ----------------------------
# Environment Variables
# ----------------------------

TOKEN = os.getenv("TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

if TOKEN is None:
    raise ValueError("TOKEN is not set in environment variables.")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in environment variables.")

# ----------------------------
# Bot Setup
# ----------------------------

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",  # Not used (slash only), but required
    intents=intents
)

# ----------------------------
# Events
# ----------------------------

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # Connect to PostgreSQL
    bot.db = await asyncpg.create_pool(DATABASE_URL)

    # Create table if it doesn't exist
    async with bot.db.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS approved_servers (
                guild_id BIGINT PRIMARY KEY
            )
        """)

    # Sync slash commands
    await bot.tree.sync()
    print("Slash commands synced.")


# ----------------------------
# Load Cogs
# ----------------------------

async def load_extensions():
    await bot.load_extension("cogs.access")
    await bot.load_extension("cogs.general")
    await bot.load_extension("cogs.info")
    await bot.load_extension("cogs.poll")  # Remove if you didn't create poll


# ----------------------------
# Main Entry
# ----------------------------

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


asyncio.run(main())
