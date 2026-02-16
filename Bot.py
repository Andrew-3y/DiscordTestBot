import discord
from discord.ext import commands
import asyncpg
import os
import asyncio

TOKEN = os.getenv("TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

if TOKEN is None:
    raise ValueError("TOKEN is not set.")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set.")

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    bot.db = await asyncpg.create_pool(DATABASE_URL)

    async with bot.db.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS approved_servers (
                guild_id BIGINT PRIMARY KEY
            )
        """)

    await bot.tree.sync()
    print("Slash commands synced.")

async def load_extensions():
    await bot.load_extension("cogs.access")
    await bot.load_extension("cogs.general")
    await bot.load_extension("cogs.info")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())
