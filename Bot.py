import discord
from discord.ext import commands
import asyncpg
import os
import asyncio

TOKEN = os.getenv("TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

if not TOKEN:
    raise ValueError("TOKEN is not set.")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set.")

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

async def setup_database():
    bot.db = await asyncpg.create_pool(DATABASE_URL)

    async with bot.db.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS approved_servers (
                guild_id BIGINT PRIMARY KEY
            )
        """)

async def load_extensions():
    await bot.load_extension("cogs.access")
    await bot.load_extension("cogs.general")
    await bot.load_extension("cogs.info")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def main():
    async with bot:
        await setup_database()
        await load_extensions()

        # Proper slash command sync
        await bot.tree.sync()
        print("Slash commands synced.")

        await bot.start(TOKEN)

asyncio.run(main())
