import os
import discord
from discord.ext import commands
import asyncio
import logging
from utils import JSONDatabase, GuildSettings

# ==================== CONFIGURATION ====================
# All configuration here - .env file is OPTIONAL
# You can put DISCORD_TOKEN here directly or use .env

# Discord Bot Token - PUT HERE or in .env
DISCORD_TOKEN = "your_token_here_or_leave_empty_to_use_env"

# If empty above, will try to load from .env
if not DISCORD_TOKEN or DISCORD_TOKEN == "your_token_here_or_leave_empty_to_use_env":
    try:
        from dotenv import load_dotenv
        load_dotenv()
        DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    except:
        pass

if not DISCORD_TOKEN:
    raise ValueError("\n❌ DISCORD_TOKEN not found!\nEither:\n1. Put token in main.py line 10\n2. Create .env file with DISCORD_TOKEN=your_token")

# ==================== BOT SETTINGS ====================
BOT_PREFIX = "!"                    # Command prefix
BOT_STATUS = "watching 🐾 AnimalVerse"  # Bot status

# ==================== FEATURES ====================
FEATURE_DAILY_ENABLED = True        # Daily animal notifications
FEATURE_STATS_ENABLED = True        # User statistics tracking
FEATURE_SLASH_COMMANDS = True       # Slash commands (/)

# ==================== DATABASE ====================
DATABASE_DIR = "data"               # Where to save JSON files

# ==================== LOGGING ====================
LOG_LEVEL = "INFO"                  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "bot.log"                # Log file path

# ==================== API KEYS (OPTIONAL) ====================
# Leave empty strings to use fallback images
CATS_API_KEY = ""                   # From thecatapi.com
DOGS_API_KEY = ""                   # From thedogapi.com

# ==================== PERFORMANCE ====================
API_TIMEOUT = 5                     # API timeout in seconds
API_CALL_DELAY = 0.1                # Delay between API calls
CACHE_TIMEOUT = 3600                # Cache duration in seconds
MAX_CONCURRENT_REQUESTS = 5         # Max parallel API requests

# ==================== COGS TO LOAD ====================
LOAD_COGS = ["animals", "daily", "info"]  # Which cogs to load, or None for all

# ==================== BOT OWNER ====================
BOT_OWNER_ID = None                 # Your Discord user ID (optional)

# ==================== END CONFIGURATION ====================

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE) if LOG_FILE else logging.NullHandler()
    ]
)

logger = logging.getLogger('AnimalVerse')
logger.info(f"\n📋 AnimalVerse Configuration:")
logger.info(f"  Prefix: {BOT_PREFIX}")
logger.info(f"  Status: {BOT_STATUS}")
logger.info(f"  Daily: {'✅' if FEATURE_DAILY_ENABLED else '❌'}")
logger.info(f"  Stats: {'✅' if FEATURE_STATS_ENABLED else '❌'}")
logger.info(f"  Slash Commands: {'✅' if FEATURE_SLASH_COMMANDS else '❌'}")
logger.info(f"  Database: {DATABASE_DIR}")
logger.info(f"  API Keys: Cat={'✅' if CATS_API_KEY else '❌'} Dog={'✅' if DOGS_API_KEY else '❌'}")

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

# Store configuration in bot for cogs to access
bot.config = {
    'prefix': BOT_PREFIX,
    'status': BOT_STATUS,
    'cats_api_key': CATS_API_KEY,
    'dogs_api_key': DOGS_API_KEY,
    'api_timeout': API_TIMEOUT,
    'database_dir': DATABASE_DIR,
    'feature_daily': FEATURE_DAILY_ENABLED,
    'feature_stats': FEATURE_STATS_ENABLED,
    'feature_slash': FEATURE_SLASH_COMMANDS,
    'cache_timeout': CACHE_TIMEOUT,
    'bot_owner_id': BOT_OWNER_ID,
}

# Initialize database
db = JSONDatabase(database_dir=DATABASE_DIR)
guild_settings = GuildSettings(db)

@bot.event
async def on_ready():
    logger.info(f'\n✅ Bot is online as {bot.user}')
    logger.info(f'📍 Bot ID: {bot.user.id}')
    logger.info(f'👥 Guilds: {len(bot.guilds)}')
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=BOT_STATUS.replace('watching ', '').replace('playing ', '').replace('listening ', '')
        )
    )
    
    # Sync slash commands if enabled
    if FEATURE_SLASH_COMMANDS:
        try:
            synced = await bot.tree.sync()
            logger.info(f'🔄 Synced {len(synced)} slash command(s)')
        except Exception as e:
            logger.error(f'Error syncing commands: {e}')
    else:
        logger.info('⚠️  Slash commands disabled')

@bot.event
async def on_guild_join(guild):
    logger.info(f'📝 Joined guild: {guild.name} (ID: {guild.id})')
    guild_settings.initialize_guild(guild.id)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found! Use `!help` to see all commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing argument: {error.param}")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command!")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(f"❌ I don't have permission: {', '.join(error.missing_perms)}")
    else:
        logger.error(f"Command error: {error}")
        await ctx.send(f"❌ An error occurred: {str(error)[:100]}")

async def load_cogs():
    """Load cogs"""
    cogs_dir = 'cogs'
    if not os.path.exists(cogs_dir):
        os.makedirs(cogs_dir)
    
    available_cogs = [f[:-3] for f in os.listdir(cogs_dir) if f.endswith('.py') and not f.startswith('_')]
    
    # Determine which cogs to load
    cogs_to_load = LOAD_COGS if LOAD_COGS else available_cogs
    
    logger.info(f'\n🔧 Loading cogs: {cogs_to_load}')
    
    for cog_name in cogs_to_load:
        try:
            await bot.load_extension(f'cogs.{cog_name}')
            logger.info(f'✅ Loaded cog: {cog_name}')
        except Exception as e:
            logger.error(f'❌ Failed to load {cog_name}: {e}')

async def main():
    async with bot:
        logger.info('\n🚀 Starting AnimalVerse bot...\n')
        await load_cogs()
        logger.info('\n📡 Connecting to Discord...\n')
        await bot.start(DISCORD_TOKEN)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('\n👋 Bot shutting down...')
    except Exception as e:
        logger.critical(f'Fatal error: {e}')
