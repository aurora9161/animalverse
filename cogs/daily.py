import discord
from discord.ext import commands, tasks
import random
from datetime import datetime
from utils import JSONDatabase, GuildSettings

class DailyAnimal(commands.Cog):
    """Daily animal notifications for servers"""

    def __init__(self, bot):
        self.bot = bot
        self.db = JSONDatabase()
        self.guild_settings = GuildSettings(self.db)
        self.daily_loop.start()

    async def cog_unload(self):
        """Cleanup on cog unload"""
        self.daily_loop.cancel()

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
        try:
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
            if not channel or not isinstance(channel, discord.TextChannel):
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
        except Exception as e:
            print(f"Error in _check_and_send_daily: {e}")

    async def _send_daily_animal(self, channel: discord.TextChannel, guild_id: int, settings: dict) -> None:
        """Send daily animal to channel"""
        try:
            # Check bot permissions
            if not channel.permissions_for(channel.guild.me).send_messages:
                print(f"Bot doesn't have send_messages permission in {channel.id}")
                return
            
            # Get available animals
            animal_types = settings.get('animal_types', [])
            if not animal_types:
                animal_types = ['cat', 'dog', 'fox', 'duck', 'rabbit', 'raccoon', 'owl', 
                               'penguin', 'panda', 'koala', 'sloth', 'hedgehog', 'otter', 
                               'squirrel', 'deer', 'bear', 'wolf', 'eagle', 'dolphin']
            
            animal_name = random.choice(animal_types)
            
            # Get animal cog for fetching image
            animal_cog = self.bot.get_cog('Animals')
            if not animal_cog:
                print("Animals cog not loaded")
                return
            
            # Get API handler
            from utils import APIHandler
            api_handler = getattr(animal_cog, 'api_handler', None)
            if not api_handler:
                print("API handler not found in Animals cog")
                return
            
            # Fetch image
            image_url = None
            if animal_name == 'cat':
                image_url = await api_handler.get_cat_image()
            elif animal_name == 'dog':
                image_url = await api_handler.get_dog_image()
            elif animal_name == 'fox':
                image_url = await api_handler.get_fox_image()
            elif animal_name == 'duck':
                image_url = await api_handler.get_duck_image()
            else:
                image_url = api_handler.get_static_image(animal_name)
            
            if not image_url:
                image_url = api_handler.get_static_image(animal_name)
            
            # Get fun fact
            animal_facts = getattr(animal_cog, 'animal_facts', {})
            facts = animal_facts.get(animal_name, ["Amazing animal!"])
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
            
        except discord.errors.Forbidden:
            print(f"No permission to send message in {channel.id}")
        except discord.errors.HTTPException as e:
            print(f"Discord HTTP error in daily send: {e}")
        except Exception as e:
            print(f"Error sending daily animal: {e}")

    @commands.group(name='daily', invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def daily_group(self, ctx):
        """Daily animal configuration commands"""
        try:
            self.guild_settings.initialize_guild(ctx.guild.id)
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
                name="#️ Channel",
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
                    value="All 19 animals (random each day)",
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
                      "`!daily animals clear` - Use all animals\n"
                      "`!daily test` - Send test message",
                inline=False
            )
            
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in daily_group: {e}")
            await ctx.send(f"❌ Error: {str(e)[:100]}")

    @daily_group.command(name='enable')
    @commands.has_permissions(administrator=True)
    async def daily_enable(self, ctx):
        """Enable daily animals"""
        try:
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
        except Exception as e:
            print(f"Error in daily_enable: {e}")
            await ctx.send(f"❌ Error: {str(e)[:100]}")

    @daily_group.command(name='disable')
    @commands.has_permissions(administrator=True)
    async def daily_disable(self, ctx):
        """Disable daily animals"""
        try:
            self.guild_settings.set_setting(ctx.guild.id, 'daily_animal_enabled', False)
            
            embed = discord.Embed(
                title="❌ Daily Animals Disabled",
                description="Daily animals have been disabled for this server.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in daily_disable: {e}")
            await ctx.send(f"❌ Error: {str(e)[:100]}")

    @daily_group.command(name='channel')
    @commands.has_permissions(administrator=True)
    async def daily_channel(self, ctx, channel: discord.TextChannel):
        """Set the channel for daily animals"""
        try:
            # Check bot permissions
            if not channel.permissions_for(ctx.guild.me).send_messages:
                embed = discord.Embed(
                    title="❌ Permission Error",
                    description=f"I don't have permission to send messages in {channel.mention}",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            
            self.guild_settings.initialize_guild(ctx.guild.id)
            self.guild_settings.set_setting(ctx.guild.id, 'daily_animal_channel', channel.id)
            
            embed = discord.Embed(
                title="📱 Channel Set",
                description=f"Daily animals will be sent to {channel.mention}",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in daily_channel: {e}")
            await ctx.send(f"❌ Error: {str(e)[:100]}")

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
        except ValueError:
            embed = discord.Embed(
                title="❌ Invalid Time Format",
                description="Please use HH:MM format (e.g., 14:30 for 2:30 PM)",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in daily_time: {e}")
            await ctx.send(f"❌ Error: {str(e)[:100]}")

    @daily_group.group(name='animals')
    @commands.has_permissions(administrator=True)
    async def daily_animals(self, ctx):
        """Manage which animals can appear in daily messages"""
        pass

    @daily_animals.command(name='list')
    async def animals_list(self, ctx):
        """List currently selected animals for daily messages"""
        try:
            animals = self.guild_settings.get_setting(ctx.guild.id, 'animal_types', [])
            
            if not animals:
                embed = discord.Embed(
                    title="🐾 Daily Animals",
                    description="All 19 animals are available (random each day)\n\n"
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
        except Exception as e:
            print(f"Error in animals_list: {e}")
            await ctx.send(f"❌ Error: {str(e)[:100]}")

    @daily_animals.command(name='set')
    async def animals_set(self, ctx, *animals):
        """Set specific animals for daily messages"""
        try:
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
        except Exception as e:
            print(f"Error in animals_set: {e}")
            await ctx.send(f"❌ Error: {str(e)[:100]}")

    @daily_animals.command(name='clear')
    async def animals_clear(self, ctx):
        """Clear animal selection (use all animals)"""
        try:
            self.guild_settings.set_setting(ctx.guild.id, 'animal_types', [])
            
            embed = discord.Embed(
                title="✅ Animals Cleared",
                description="Daily animals will now include all 19 animals",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in animals_clear: {e}")
            await ctx.send(f"❌ Error: {str(e)[:100]}")

    @daily_group.command(name='test')
    @commands.has_permissions(administrator=True)
    async def daily_test(self, ctx):
        """Send a test daily animal message now"""
        try:
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
            if not channel or not isinstance(channel, discord.TextChannel):
                embed = discord.Embed(
                    title="❌ Channel Not Found",
                    description="The configured channel was not found.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            
            # Check permissions
            if not channel.permissions_for(ctx.guild.me).send_messages:
                embed = discord.Embed(
                    title="❌ Permission Error",
                    description=f"I don't have permission to send messages in {channel.mention}",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            
            await self._send_daily_animal(channel, ctx.guild.id, settings)
            
            embed = discord.Embed(
                title="✅ Test Sent",
                description=f"Test daily animal sent to {channel.mention}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in daily_test: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to send test: {str(e)[:100]}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(DailyAnimal(bot))
