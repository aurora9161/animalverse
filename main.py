import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
from utils import JSONDatabase, GuildSettings

# Load environment variables
load_dotenv()

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=os.getenv('BOT_PREFIX', '!'), intents=intents)

# Initialize database
db = JSONDatabase()
guild_settings = GuildSettings(db)

@bot.event
async def on_ready():
    print(f'\n✅ Bot is online as {bot.user}')
    print(f'📊 Bot ID: {bot.user.id}')
    print(f'👥 Guilds: {len(bot.guilds)}')
    try:
        synced = await bot.tree.sync()
        print(f'🔄 Synced {len(synced)} slash commands(s)\n')
    except Exception as e:
        print(f'❌ Error syncing commands: {e}\n')

@bot.event
async def on_guild_join(guild):
    """Initialize guild settings when bot joins a new guild"""
    print(f'📍 Joined guild: {guild.name} (ID: {guild.id})')
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
        await ctx.send(f"❌ I don't have permission to do that: {', '.join(error.missing_perms)}")
    else:
        await ctx.send(f"❌ An error occurred: {str(error)[:100]}")

async def load_cogs():
    """Load all cogs from the cogs directory"""
    cogs_dir = 'cogs'
    if not os.path.exists(cogs_dir):
        os.makedirs(cogs_dir)
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py') and not filename.startswith('_'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'✅ Loaded cog: {filename}')
            except Exception as e:
                print(f'❌ Failed to load {filename}: {e}')

async def main():
    async with bot:
        print('🚀 Starting AnimalVerse bot...')
        print('📁 Loading cogs...\n')
        await load_cogs()
        print('\n📡 Connecting to Discord...\n')
        await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == '__main__':
    asyncio.run(main())
