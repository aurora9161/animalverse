import os
import discord
from discord.ext import commands
import asyncio
import logging
from utils import JSONDatabase, GuildSettings
import sys

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
        DISCORD_TOKEN = None

if not DISCORD_TOKEN:
    print("\n❌ FATAL ERROR: DISCORD_TOKEN not found!")
    print("\nFix this by:")
    print("  1. Edit main.py line 13 and set: DISCORD_TOKEN = \"your_token_here\"")
    print("  2. OR create .env file with: DISCORD_TOKEN=your_token_here")
    print("\nGet your token from: https://discord.com/developers/applications\n")
    sys.exit(1)

# ==================== BOT SETTINGS ====================
BOT_PREFIX = "!"                    # Command prefix
BOT_STATUS = "watching 🐾 AnimalVerse"  # Bot status

# ==================== FEATURES ====================
FEATURE_DAILY_ENABLED = True        # Daily animal notifications
FEATURE_STATS_ENABLED = True        # User statistics tracking
FEATURE_SLASH_COMMANDS = True       # Slash commands (/)
FEATURE_DM_SUPPORT = True           # Allow commands in DMs

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

# ==================== BOT OWNER ====================
BOT_OWNER_ID = None                 # Your Discord user ID (no quotes needed) - Example: 123456789

# ==================== END CONFIGURATION ====================

# Setup comprehensive logging
class CustomFormatter(logging.Formatter):
    """Custom formatter with colors"""
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: grey + "[DEBUG] %(message)s" + reset,
        logging.INFO: blue + "[INFO] %(message)s" + reset,
        logging.WARNING: yellow + "[WARN] %(message)s" + reset,
        logging.ERROR: red + "[ERROR] %(message)s" + reset,
        logging.CRITICAL: bold_red + "[CRITICAL] %(message)s" + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

logger = logging.getLogger('AnimalVerse')
logger.setLevel(getattr(logging, LOG_LEVEL))

# Console handler with formatting
console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomFormatter())
logger.addHandler(console_handler)

# File handler
if LOG_FILE:
    try:
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s %(name)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Could not create log file: {e}")

logger.info("\n" + "="*50)
logger.info("📋 AnimalVerse Configuration Loaded")
logger.info("="*50)
logger.info(f"  Prefix: {BOT_PREFIX}")
logger.info(f"  Status: {BOT_STATUS}")
logger.info(f"  Daily Animals: {'✅' if FEATURE_DAILY_ENABLED else '❌'}")
logger.info(f"  Statistics: {'✅' if FEATURE_STATS_ENABLED else '❌'}")
logger.info(f"  Slash Commands: {'✅' if FEATURE_SLASH_COMMANDS else '❌'}")
logger.info(f"  DM Support: {'✅' if FEATURE_DM_SUPPORT else '❌'}")
logger.info(f"  API Keys: Cat={'✅' if CATS_API_KEY else '❌'} Dog={'✅' if DOGS_API_KEY else '❌'}")
logger.info(f"  Database: {DATABASE_DIR}")
logger.info(f"  Log Level: {LOG_LEVEL}")
logger.info("="*50 + "\n")

# Initialize bot with proper error handling
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.guild_messages = True
intents.dm_messages = True  # Enable DMs

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, help_command=commands.DefaultHelpCommand())

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
    'feature_dm': FEATURE_DM_SUPPORT,
    'cache_timeout': CACHE_TIMEOUT,
    'bot_owner_id': BOT_OWNER_ID,
}

# Initialize database with error handling
try:
    db = JSONDatabase(db_dir=DATABASE_DIR)
    guild_settings = GuildSettings(db)
    logger.info(f'💾 Database initialized at {DATABASE_DIR}')
except Exception as e:
    logger.error(f'❌ Failed to initialize database: {e}')
    logger.error('Bot cannot start without database')
    sys.exit(1)

@bot.event
async def on_ready():
    """Bot startup event"""
    try:
        logger.info(f'\n✅ Bot Online: {bot.user}')
        logger.info(f'📋 Bot ID: {bot.user.id}')
        logger.info(f'👥 Guilds: {len(bot.guilds)}')
        logger.info(f'📑 Users: {len(set(bot.get_all_members()))}')
        
        # Set bot status
        try:
            status_text = BOT_STATUS.replace('watching ', '').replace('playing ', '').replace('listening ', '')
            await bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name=status_text
                )
            )
            logger.info(f'💬 Status set: {BOT_STATUS}')
        except Exception as e:
            logger.warning(f'Could not set status: {e}')
        
        # Sync slash commands if enabled
        if FEATURE_SLASH_COMMANDS:
            try:
                synced = await bot.tree.sync()
                logger.info(f'🔄 Synced {len(synced)} slash command(s)')
            except Exception as e:
                logger.warning(f'Error syncing slash commands: {e}')
        else:
            logger.info('⚠️  Slash commands disabled')
        
        if FEATURE_DM_SUPPORT:
            logger.info('💬 DM support: enabled')
        
        logger.info('\n' + '='*50)
        logger.info('Bot is ready! Use commands in Discord or DMs.')
        logger.info('='*50 + '\n')
    except Exception as e:
        logger.error(f'Error in on_ready: {e}')

@bot.event
async def on_guild_join(guild):
    """Bot joined new guild"""
    try:
        logger.info(f'📝 New guild: {guild.name} ({guild.id}) with {guild.member_count} members')
        guild_settings.initialize_guild(guild.id)
    except Exception as e:
        logger.error(f'Error in on_guild_join: {e}')

@bot.event
async def on_guild_remove(guild):
    """Bot left guild"""
    try:
        logger.info(f'👋 Left guild: {guild.name} ({guild.id})')
    except Exception as e:
        logger.error(f'Error in on_guild_remove: {e}')

@bot.event
async def on_message(message):
    """Handle messages - allow DMs"""
    # Ignore bot messages
    if message.author.bot:
        return
    
    # Process commands (works in both guilds and DMs)
    try:
        await bot.process_commands(message)
    except Exception as e:
        logger.error(f'Error processing message: {e}')

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors in both guilds and DMs"""
    try:
        # Check if in DM
        is_dm = isinstance(ctx.channel, discord.DMChannel)
        
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("🐾 Use `!help` to see all commands.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Missing argument: `{error.param}`")
        elif isinstance(error, commands.MissingPermissions):
            if not is_dm:
                await ctx.send("❌ You don't have permission!")
        elif isinstance(error, commands.BotMissingPermissions):
            if not is_dm:
                perms = ', '.join(error.missing_perms)
                await ctx.send(f"❌ I don't have permission: {perms}")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("❌ This command only works in servers.")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⚠️  Try again in {error.retry_after:.1f}s")
        else:
            logger.error(f'Command error: {type(error).__name__}: {error}')
            await ctx.send(f"❌ Error occurred. Check logs.")
    except discord.errors.Forbidden:
        # Can't send message (likely in DM with no permission)
        logger.warning(f'Cannot send error message to {ctx.author}')
    except Exception as e:
        logger.error(f'Error in on_command_error: {e}')

@bot.event
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    """Handle slash command errors in both guilds and DMs"""
    try:
        if not interaction.response.is_done():
            await interaction.response.send_message(f"❌ Error: {str(error)[:100]}", ephemeral=True)
        logger.error(f'Slash command error: {error}')
    except Exception as e:
        logger.error(f'Error in on_app_command_error: {e}')

async def load_cogs():
    """Load all available cogs"""
    cogs_dir = 'cogs'
    if not os.path.exists(cogs_dir):
        logger.warning(f'🚨 Cogs directory not found, creating: {cogs_dir}')
        os.makedirs(cogs_dir)
    
    # Get all available cogs
    available_cogs = [f[:-3] for f in os.listdir(cogs_dir) if f.endswith('.py') and not f.startswith('_')]
    
    if not available_cogs:
        logger.warning('⚠️  No cogs found to load!')
        return
    
    logger.info(f'\n🔧 Loading cogs: {available_cogs}\n')
    
    failed = []
    for cog_name in available_cogs:
        try:
            await bot.load_extension(f'cogs.{cog_name}')
            logger.info(f'✅ Loaded: {cog_name}')
        except Exception as e:
            logger.error(f'❌ Failed to load {cog_name}: {e}')
            failed.append(cog_name)
    
    if failed:
        logger.warning(f'\n⚠️  {len(failed)} cog(s) failed to load: {failed}\n')
    else:
        logger.info(f'\n✅ All cogs loaded successfully\n')

async def main():
    """Main bot startup"""
    async with bot:
        logger.info('\n🚀 Starting AnimalVerse bot...\n')
        await load_cogs()
        logger.info('\n📡 Connecting to Discord...\n')
        try:
            await bot.start(DISCORD_TOKEN)
        except discord.LoginFailure:
            logger.error('\n❌ Invalid Discord token!')
            logger.error('Check your DISCORD_TOKEN in main.py or .env\n')
            sys.exit(1)
        except discord.ConnectionClosed:
            logger.error('\n❌ Connection to Discord closed!')
            sys.exit(1)
        except Exception as e:
            logger.error(f'\n❌ Fatal error: {e}\n')
            sys.exit(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('\n👋 Bot shutting down gracefully...\n')
    except Exception as e:
        logger.critical(f'\n❌ Fatal startup error: {e}\n')
        sys.exit(1)
