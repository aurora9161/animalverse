import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import logging
from utils import JSONDatabase, GuildSettings

# Load environment variables
load_dotenv()

# ==================== CONFIGURATION FROM .ENV ====================

# Required
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
if not DISCORD_TOKEN:
    raise ValueError("❌ DISCORD_TOKEN not found in .env file!")

# Bot Settings
BOT_PREFIX = os.getenv('BOT_PREFIX', '!')
BOT_STATUS = os.getenv('BOT_STATUS', 'watching 🐾 AnimalVerse')

# API Keys (Optional)
CATS_API_KEY = os.getenv('CATS_API_KEY', '')
DOGS_API_KEY = os.getenv('DOGS_API_KEY', '')

# Daily Animals
DEFAULT_DAILY_TIME = os.getenv('DEFAULT_DAILY_TIME', '08:00')
ENABLE_DAILY_BY_DEFAULT = os.getenv('ENABLE_DAILY_BY_DEFAULT', 'false').lower() == 'true'

# Animal Selection
DEFAULT_ANIMALS = os.getenv('DEFAULT_ANIMALS', '').split(',') if os.getenv('DEFAULT_ANIMALS') else []
API_CALL_DELAY = float(os.getenv('API_CALL_DELAY', '0.1'))
API_TIMEOUT = int(os.getenv('API_TIMEOUT', '5'))

# Database
DATABASE_DIR = os.getenv('DATABASE_DIR', 'data')
AUTO_BACKUP_DB = os.getenv('AUTO_BACKUP_DB', 'true').lower() == 'true'

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'bot.log')

# Features
FEATURE_DAILY_ENABLED = os.getenv('FEATURE_DAILY_ENABLED', 'true').lower() == 'true'
FEATURE_STATS_ENABLED = os.getenv('FEATURE_STATS_ENABLED', 'true').lower() == 'true'
FEATURE_SLASH_COMMANDS = os.getenv('FEATURE_SLASH_COMMANDS', 'true').lower() == 'true'
MAX_DAILY_ANIMALS = int(os.getenv('MAX_DAILY_ANIMALS', '19'))

# Performance
LOAD_COGS_LIST = os.getenv('LOAD_COGS', '').split(',') if os.getenv('LOAD_COGS') else None
CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', '3600'))
MAX_CONCURRENT_REQUESTS = int(os.getenv('MAX_CONCURRENT_REQUESTS', '5'))

# Optional
BOT_OWNER_ID = os.getenv('BOT_OWNER_ID', '')
SUPPORT_SERVER = os.getenv('SUPPORT_SERVER', 'https://github.com/aurora9161/animalverse')
SOURCE_CODE_URL = os.getenv('SOURCE_CODE_URL', 'https://github.com/aurora9161/animalverse')

# ==================== LOGGING SETUP ====================

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE) if LOG_FILE else logging.NullHandler()
    ]
)

logger = logging.getLogger('AnimalVerse')
logger.info(f"\n📋 AnimalVerse Configuration Loaded:")
logger.info(f"  Prefix: {BOT_PREFIX}")
logger.info(f"  Status: {BOT_STATUS}")
logger.info(f"  Daily Animals: {'✅ Enabled' if FEATURE_DAILY_ENABLED else '❌ Disabled'}")
logger.info(f"  Statistics: {'✅ Enabled' if FEATURE_STATS_ENABLED else '❌ Disabled'}")
logger.info(f"  Slash Commands: {'✅ Enabled' if FEATURE_SLASH_COMMANDS else '❌ Disabled'}")
logger.info(f"  API Keys: Cat={'✅' if CATS_API_KEY else '❌'} Dog={'✅' if DOGS_API_KEY else '❌'}")
logger.info(f"  Database: {DATABASE_DIR}")

# ==================== BOT INITIALIZATION ====================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

# Store configuration in bot for access in cogs
bot.config = {
    'prefix': BOT_PREFIX,
    'status': BOT_STATUS,
    'cats_api_key': CATS_API_KEY,
    'dogs_api_key': DOGS_API_KEY,
    'default_daily_time': DEFAULT_DAILY_TIME,
    'enable_daily_by_default': ENABLE_DAILY_BY_DEFAULT,
    'default_animals': DEFAULT_ANIMALS,
    'api_timeout': API_TIMEOUT,
    'database_dir': DATABASE_DIR,
    'feature_daily': FEATURE_DAILY_ENABLED,
    'feature_stats': FEATURE_STATS_ENABLED,
    'feature_slash': FEATURE_SLASH_COMMANDS,
    'max_daily_animals': MAX_DAILY_ANIMALS,
    'cache_timeout': CACHE_TIMEOUT,
    'bot_owner_id': BOT_OWNER_ID,
    'support_server': SUPPORT_SERVER,
    'source_code': SOURCE_CODE_URL,
}

# Initialize database
db = JSONDatabase(database_dir=DATABASE_DIR)
guild_settings = GuildSettings(db)

@bot.event
async def on_ready():
    logger.info(f'\n✅ Bot is online as {bot.user}')
    logger.info(f'📋 Bot ID: {bot.user.id}')
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
        logger.info('⚠️  Slash commands disabled in config')

@bot.event
async def on_guild_join(guild):
    logger.info(f'📍 Joined guild: {guild.name} (ID: {guild.id})')
    guild_settings.initialize_guild(guild.id)
    
    # Apply default daily settings if enabled
    if ENABLE_DAILY_BY_DEFAULT:
        logger.info(f'🐾 Applying default daily settings to {guild.name}')

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
    """Load cogs based on configuration"""
    cogs_dir = 'cogs'
    if not os.path.exists(cogs_dir):
        os.makedirs(cogs_dir)
    
    available_cogs = [f[:-3] for f in os.listdir(cogs_dir) if f.endswith('.py') and not f.startswith('_')]
    
    # Determine which cogs to load
    if LOAD_COGS_LIST:
        cogs_to_load = [c.strip() for c in LOAD_COGS_LIST if c.strip()]
    else:
        cogs_to_load = available_cogs
    
    # Filter by feature flags
    if not FEATURE_DAILY_ENABLED and 'daily' in cogs_to_load:
        logger.info('⚠️  Skipping daily cog (disabled in config)')
        cogs_to_load.remove('daily')
    
    if not FEATURE_STATS_ENABLED and 'info' in cogs_to_load:
        logger.info('⚠️  Skipping info cog (disabled in config)')
        cogs_to_load.remove('info')
    
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
