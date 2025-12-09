import discord
from discord.ext import commands, tasks
import random
from datetime import datetime, time as dt_time, timedelta
from utils import JSONDatabase, GuildSettings
import asyncio

class DailyAnimal(commands.Cog):
    """Daily animal notifications for servers"""

    def __init__(self, bot):
        self.bot = bot
        self.db = JSONDatabase()
        self.guild_settings = GuildSettings(self.db)
        self.daily_loop.start()
        self.session = None

    async def cog_load(self):
        """Initialize on cog load"""
        import aiohttp
        self.session = aiohttp.ClientSession()

    async def cog_unload(self):
        """Cleanup on cog unload"""
        self.daily_loop.cancel()
        if self.session:
            await self.session.close()

    @tasks.loop(minutes=1)
    async def daily_loop(self):
        """Main loop for daily animals - checks every minute"""
        try:
            now = datetime.now()
            
            for guild in self.bot.guilds:
                try:
                    await self._check_and_send_daily(guild, now)
                except Exception as e:
                    print(f"Error in daily animal for guild {guild.id}: {e}")
        except Exception as e:
            print(f"Error in daily loop: {e}")

    @daily_loop.before_loop
    async def before_daily_loop(self):
        """Wait for bot to be ready before starting loop"""
        await self.bot.wait_until_ready()

    async def _check_and_send_daily(self, guild: discord.Guild, now: datetime) -> None:
        """Check if daily animal should be sent for this guild"""
        self.guild_settings.initialize_guild(guild.id)
        settings = self.guild_settings.get_settings(guild.id)
        
        # Check if daily animal is enabled
        if not settings.get('daily_animal_enabled', False):
            return
        
        # Get channel
        channel_id = settings.get('daily_animal_channel')
        if not channel_id:
            return
        
        channel = guild.get_channel(int(channel_id))
        if not channel:
            return
        
        # Check if it's time to send
        target_hour = settings.get('daily_animal_hour', 8)
        target_minute = settings.get('daily_animal_minute', 0)
        
        # Check if current time matches target time
        if now.hour != target_hour or now.minute != target_minute:
            return
        
        # Check if already sent today
        last_sent = settings.get('last_daily_animal')
        today = now.strftime('%Y-%m-%d')
        
        if last_sent == today:
            return  # Already sent today
        
        # Send daily animal
        await self._send_daily_animal(channel, guild.id, settings)
        
        # Update last sent time
        self.guild_settings.set_setting(guild.id, 'last_daily_animal', today)

    async def _send_daily_animal(self, channel: discord.TextChannel, guild_id: int, settings: dict) -> None:
        """Send daily animal to channel"""
        try:
            # Get available animals
            animal_types = settings.get('animal_types', [])
            if not animal_types:
                # Use all available animals
                animal_types = ['cat', 'dog', 'fox', 'duck', 'rabbit', 'raccoon', 'owl', 
                               'penguin', 'panda', 'koala', 'sloth', 'hedgehog', 'otter', 
                               'squirrel', 'deer', 'bear', 'wolf', 'eagle', 'dolphin']
            
            animal_name = random.choice(animal_types)
            
            # Get animal cog for fetching image
            animal_cog = self.bot.get_cog('Animals')
            if not animal_cog:
                await channel.send("❌ Animal cog not loaded!")
                return
            
            # Fetch image
            fetch_func = animal_cog.animal_list.get(animal_name)
            if not fetch_func:
                await channel.send(f"❌ Animal '{animal_name}' not found!")
                return
            
            image_url = await fetch_func(animal_cog)
            if not image_url:
                await channel.send("❌ Failed to fetch animal image.")
                return
            
            # Get fun fact
            facts = animal_cog.animal_facts.get(animal_name, ["Amazing animal!"])
            fact = random.choice(facts)
            
            # Create embed
            embed = discord.Embed(
                title=f"🐾 Daily Animal - {animal_name.title()}",
                color=discord.Color.gold()
            )
            embed.set_image(url=image_url)
            embed.add_field(name="📚 Fun Fact", value=fact, inline=False)
            embed.add_field(name="⏰ Daily Reminder", value="You received this message because daily animals are enabled!", inline=False)
            embed.set_footer(text="AnimalVerse 🐾 Daily")
            
            await channel.send(embed=embed)
            
        except Exception as e:
            print(f"Error sending daily animal: {e}")
            try:
                await channel.send(f"❌ Error sending daily animal: {str(e)[:100]}")
            except:
                pass

    @commands.group(name='daily', invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def daily_group(self, ctx):
        """Daily animal configuration commands"""
        settings = self.guild_settings.get_settings(ctx.guild.id)
        
        embed = discord.Embed(
            title="🐾 Daily Animal Settings",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="✅ Enabled",
            value="Yes" if settings.get('daily_animal_enabled') else "No",
            inline=True
        )
        embed.add_field(
            name="#홟 Channel",
            value=f"<#{settings.get('daily_animal_channel')}>" if settings.get('daily_animal_channel') else "Not set",
            inline=True
        )
        embed.add_field(
            name="⏰ Time",
            value=f"{settings.get('daily_animal_time', '08:00')}",
            inline=True
        )
        
        animal_types = settings.get('animal_types', [])
        if animal_types:
            embed.add_field(
                name="🐾 Animals",
                value=f"{len(animal_types)} specific: {', '.join(animal_types[:3])}{'...' if len(animal_types) > 3 else ''}",
                inline=False
            )
        else:
            embed.add_field(
                name="🐾 Animals",
                value="All 20+ animals (random each day)",
                inline=False
            )
        
        embed.add_field(
            name="📍 Commands",
            value="`!daily enable` - Enable daily animals\n"
                  "`!daily disable` - Disable daily animals\n"
                  "`!daily channel #channel` - Set channel\n"
                  "`!daily time HH:MM` - Set time (24-hour format)\n"
                  "`!daily animals list` - Show animals\n"
                  "`!daily animals set cat dog` - Set specific animals\n"
                  "`!daily animals clear` - Use all animals",
            inline=False
        )
        
        await ctx.send(embed=embed)

    @daily_group.command(name='enable')
    @commands.has_permissions(administrator=True)
    async def daily_enable(self, ctx):
        """Enable daily animals"""
        self.guild_settings.initialize_guild(ctx.guild.id)
        
        if self.guild_settings.get_setting(ctx.guild.id, 'daily_animal_channel') is None:
            embed = discord.Embed(
                title="⚠️ Setup Required",
                description="Please set a channel first using `!daily channel #channel`",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return
        
        self.guild_settings.set_setting(ctx.guild.id, 'daily_animal_enabled', True)
        
        embed = discord.Embed(
            title="✅ Daily Animals Enabled",
            description="Daily animals have been enabled for this server!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @daily_group.command(name='disable')
    @commands.has_permissions(administrator=True)
    async def daily_disable(self, ctx):
        """Disable daily animals"""
        self.guild_settings.set_setting(ctx.guild.id, 'daily_animal_enabled', False)
        
        embed = discord.Embed(
            title="❌ Daily Animals Disabled",
            description="Daily animals have been disabled for this server.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    @daily_group.command(name='channel')
    @commands.has_permissions(administrator=True)
    async def daily_channel(self, ctx, channel: discord.TextChannel):
        """Set the channel for daily animals"""
        self.guild_settings.initialize_guild(ctx.guild.id)
        self.guild_settings.set_setting(ctx.guild.id, 'daily_animal_channel', channel.id)
        
        embed = discord.Embed(
            title="📱 Channel Set",
            description=f"Daily animals will be sent to {channel.mention}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @daily_group.command(name='time')
    @commands.has_permissions(administrator=True)
    async def daily_time(self, ctx, time_str: str):
        """Set the time for daily animals (24-hour format HH:MM)"""
        try:
            parts = time_str.split(':')
            if len(parts) != 2:
                raise ValueError("Invalid format")
            
            hour = int(parts[0])
            minute = int(parts[1])
            
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError("Invalid time")
            
            self.guild_settings.set_setting(ctx.guild.id, 'daily_animal_hour', hour)
            self.guild_settings.set_setting(ctx.guild.id, 'daily_animal_minute', minute)
            self.guild_settings.set_setting(ctx.guild.id, 'daily_animal_time', time_str)
            
            embed = discord.Embed(
                title="⏰ Time Set",
                description=f"Daily animals will be sent at {time_str}",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Invalid Time Format",
                description="Please use HH:MM format (e.g., 14:30 for 2:30 PM)",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @daily_group.group(name='animals')
    @commands.has_permissions(administrator=True)
    async def daily_animals(self, ctx):
        """Manage which animals can appear in daily messages"""
        pass

    @daily_animals.command(name='list')
    async def animals_list(self, ctx):
        """List currently selected animals for daily messages"""
        animals = self.guild_settings.get_setting(ctx.guild.id, 'animal_types', [])
        
        if not animals:
            embed = discord.Embed(
                title="🐾 Daily Animals",
                description="All 20+ animals are available (random each day)\n\n"
                           "Available: cat, dog, fox, duck, rabbit, raccoon, owl, penguin, "
                           "panda, koala, sloth, hedgehog, otter, squirrel, deer, bear, wolf, eagle, dolphin",
                color=discord.Color.blue()
            )
        else:
            embed = discord.Embed(
                title="🐾 Daily Animals",
                description=f"**Selected Animals ({len(animals)}):**\n" + ", ".join(f"`{a}`" for a in animals),
                color=discord.Color.blue()
            )
        
        await ctx.send(embed=embed)

    @daily_animals.command(name='set')
    async def animals_set(self, ctx, *animals):
        """Set specific animals for daily messages"""
        if not animals:
            embed = discord.Embed(
                title="❌ No animals provided",
                description="Usage: `!daily animals set cat dog fox`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        animal_list = list(animals)
        self.guild_settings.set_setting(ctx.guild.id, 'animal_types', animal_list)
        
        embed = discord.Embed(
            title="✅ Animals Set",
            description=f"Daily animals limited to: {', '.join(f'`{a}`' for a in animal_list)}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @daily_animals.command(name='clear')
    async def animals_clear(self, ctx):
        """Clear animal selection (use all animals)"""
        self.guild_settings.set_setting(ctx.guild.id, 'animal_types', [])
        
        embed = discord.Embed(
            title="✅ Animals Cleared",
            description="Daily animals will now include all 20+ animals",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @daily_group.command(name='test')
    @commands.has_permissions(administrator=True)
    async def daily_test(self, ctx):
        """Send a test daily animal message now"""
        self.guild_settings.initialize_guild(ctx.guild.id)
        settings = self.guild_settings.get_settings(ctx.guild.id)
        
        channel_id = settings.get('daily_animal_channel')
        if not channel_id:
            embed = discord.Embed(
                title="❌ No Channel Set",
                description="Please set a channel first using `!daily channel #channel`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        channel = ctx.guild.get_channel(int(channel_id))
        if not channel:
            embed = discord.Embed(
                title="❌ Channel Not Found",
                description="The configured channel was not found.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        try:
            await self._send_daily_animal(channel, ctx.guild.id, settings)
            embed = discord.Embed(
                title="✅ Test Sent",
                description=f"Test daily animal sent to {channel.mention}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to send test: {str(e)[:100]}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(DailyAnimal(bot))
