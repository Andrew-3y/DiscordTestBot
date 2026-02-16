import discord
from discord.ext import commands
import asyncpg
import os
import asyncio
from dotenv import load_dotenv

# Load local .env file if it exists (for local testing)
load_dotenv()

TOKEN = os.getenv("TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# --- CRITICAL FIX FOR RAILWAY/ASYNCPG ---
# asyncpg requires "postgresql://" but Railway often provides "postgres://"
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
# ----------------------------------------

if not TOKEN:
    raise ValueError("TOKEN is not set.")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set.")

intents = discord.Intents.default()
# If you need to read messages or see members, ensure these are enabled:
# intents.message_content = True 
# intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

async def setup_database():
    """Initializes the database pool and creates the table."""
    try:
        bot.db = await asyncpg.create_pool(DATABASE_URL)
        print("✅ Database pool created.")
        
        async with bot.db.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS approved_servers (
                    guild_id BIGINT PRIMARY KEY
                )
            """)
        print("✅ Database table verified.")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise e

async def load_extensions():
    """Loads all cogs from the cogs folder."""
    initial_extensions = [
        "cogs.access",
        "cogs.general",
        "cogs.info",
        "cogs.poll"
    ]
    
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"✅ Loaded extension: {extension}")
        except Exception as e:
            print(f"❌ Failed to load extension {extension}: {e}")

@bot.event
async def on_ready():
    print(f"---")
    print(f"Logged in as {bot.user}")
    print(f"ID: {bot.user.id}")
    print(f"---")

async def main():
    async with bot:
        # 1. Connect to DB first
        await setup_database()
        
        # 2. Load commands
        await load_extensions()
        
        # 3. Sync slash commands
        print("Syncing slash commands...")
        await bot.tree.sync()
        print("✅ Slash commands synced.")
        
        # 4. Start the bot
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass