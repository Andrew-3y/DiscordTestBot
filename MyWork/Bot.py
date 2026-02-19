import discord
from discord.ext import commands
import asyncpg
import os
import asyncio
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

TOKEN = os.getenv("TOKEN")
raw_url = os.getenv("DATABASE_URL")

# --- CRITICAL FIX FOR RAILWAY/ASYNCPG ---
if raw_url and raw_url.startswith("postgres://"):
    DATABASE_URL = raw_url.replace("postgres://", "postgresql://", 1)
else:
    DATABASE_URL = raw_url

# Standard Intents
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

async def setup_database():
    """Initializes the database pool with retry logic."""
    if not DATABASE_URL:
        print("❌ ERROR: DATABASE_URL is missing.")
        return

    for i in range(5):
        try:
            bot.db = await asyncio.wait_for(asyncpg.create_pool(DATABASE_URL), timeout=10.0)
            print("✅ Database pool created successfully.")
            
            async with bot.db.acquire() as conn:
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS approved_servers (
                        guild_id BIGINT PRIMARY KEY
                    )
                """)
            print("✅ Database tables verified.")
            return
        except Exception as e:
            print(f"⚠️ Connection attempt {i+1} failed: {e}. Retrying in 3s...")
            await asyncio.sleep(3)
    
    raise Exception("❌ Could not connect to the database after 5 attempts.")

@bot.event
async def on_ready():
    print(f"---")
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    
    # Sync Slash Commands here to avoid MissingApplicationID error
    try:
        print("Syncing slash commands...")
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")
    
    print(f"Status: Online and Ready")
    print(f"---")

async def load_extensions():
    """Loads all command modules from the cogs folder."""
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

async def main():
    async with bot:
        # Step 1: Connect to database
        await setup_database()
        
        # Step 2: Load Cogs
        await load_extensions()
        
        # Step 3: Start the bot (on_ready will handle the sync)
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is shutting down...")