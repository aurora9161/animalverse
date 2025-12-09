import discord
from discord.ext import commands
from datetime import datetime
from utils import JSONDatabase, UserStats, GuildSettings

class Info(commands.Cog):
    """Information and help commands for AnimalVerse"""

    def __init__(self, bot):
        self.bot = bot
        self.db = JSONDatabase()
        self.user_stats = UserStats(self.db)
        self.guild_settings = GuildSettings(self.db)

    def create_help_embed(self):
        """Create a comprehensive help embed"""
        embed = discord.Embed(
            title="🐾 AnimalVerse - Help & Commands",
            description="Get adorable animal images with AnimalVerse!",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )

        # Prefix Commands
        prefix_commands = (
            "`!cat` `!dog` `!fox` `!duck` `!rabbit` `!raccoon` `!owl` `!penguin`\n"
            "`!panda` `!koala` `!sloth` `!hedgehog` `!otter` `!squirrel` `!deer` `!bear`\n"
            "`!wolf` `!eagle` `!dolphin` - Get specific animal\n"
            "`!animal` - Get random animal\n"
            "`!help` - Show this help message\n"
            "`!botinfo` - Show bot information\n"
            "`!ping` - Check bot latency\n"
            "`!stats` - View your stats"
        )
        embed.add_field(name="📄 Prefix Commands (use ! prefix)", value=prefix_commands, inline=False)

        # Slash Commands
        slash_commands = (
            "`/cat` `!dog` `!fox` `!duck` ... - Get specific animal\n"
            "`/animal` - Get random animal\n"
            "`/animals-list` - Show all available animals\n"
            "`/help` - Show help\n"
            "`/botinfo` - Show bot info\n"
            "`/ping` - Check latency\n"
            "`/stats` - View your stats"
        )
        embed.add_field(name="📱 Slash Commands (/ prefix)", value=slash_commands, inline=False)

        # Daily Commands
        daily_commands = (
            "`!daily` - Show settings\n"
            "`!daily enable` - Enable daily animals\n"
            "`!daily disable` - Disable daily animals\n"
            "`!daily channel #channel` - Set channel\n"
            "`!daily time HH:MM` - Set time (24-hour)\n"
            "`!daily animals set cat dog` - Select animals\n"
            "`!daily test` - Send test message"
        )
        embed.add_field(name="🏓 Daily Animal Commands", value=daily_commands, inline=False)

        footer_text = "AnimalVerse v2.0 - Daily Animal Support!"
        embed.set_footer(text=footer_text)

        return embed

    @commands.command(name='help')
    async def prefix_help(self, ctx):
        """Show help information (prefix command)"""
        embed = self.create_help_embed()
        await ctx.send(embed=embed)

    @discord.app_commands.command(name='help', description='Show help and available commands')
    async def slash_help(self, interaction: discord.Interaction):
        """Show help information (slash command)"""
        embed = self.create_help_embed()
        await interaction.response.send_message(embed=embed)

    @commands.command(name='botinfo')
    async def prefix_botinfo(self, ctx):
        """Show bot information (prefix command)"""
        embed = discord.Embed(
            title="🐾 AnimalVerse Bot Info",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        embed.add_field(name="Bot Name", value=self.bot.user.name, inline=True)
        embed.add_field(name="Bot ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="Guilds", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Users", value=sum(g.member_count for g in self.bot.guilds if g.member_count), inline=True)
        embed.add_field(name="discord.py Version", value=discord.__version__, inline=True)
        embed.add_field(name="Prefix", value="!", inline=True)
        embed.add_field(name="\u2728 Features", value="20+ Animals | Daily Messages | Statistics | Slash Commands", inline=False)
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        embed.set_footer(text="Made with ❤️ by aurora9161")
        await ctx.send(embed=embed)

    @discord.app_commands.command(name='botinfo', description='Show bot information')
    async def slash_botinfo(self, interaction: discord.Interaction):
        """Show bot information (slash command)"""
        embed = discord.Embed(
            title="🐾 AnimalVerse Bot Info",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        embed.add_field(name="Bot Name", value=self.bot.user.name, inline=True)
        embed.add_field(name="Bot ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="Guilds", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Users", value=sum(g.member_count for g in self.bot.guilds if g.member_count), inline=True)
        embed.add_field(name="discord.py Version", value=discord.__version__, inline=True)
        embed.add_field(name="Prefix", value="!", inline=True)
        embed.add_field(name="\u2728 Features", value="20+ Animals | Daily Messages | Statistics | Slash Commands", inline=False)
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        embed.set_footer(text="Made with ❤️ by aurora9161")
        await interaction.response.send_message(embed=embed)

    @commands.command(name='ping')
    async def prefix_ping(self, ctx):
        """Check bot latency (prefix command)"""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Bot latency: **{latency}ms**",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    @discord.app_commands.command(name='ping', description='Check bot latency')
    async def slash_ping(self, interaction: discord.Interaction):
        """Check bot latency (slash command)"""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Bot latency: **{latency}ms**",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)

    @commands.command(name='stats')
    async def prefix_stats(self, ctx):
        """Show user statistics (prefix command)"""
        stats = self.user_stats.get_stats(ctx.author.id)
        commands_used = stats.get('commands', {})
        total_commands = sum(commands_used.values())
        favorite_animal = self.user_stats.get_favorite_animal(ctx.author.id)
        
        embed = discord.Embed(
            title="📊 Your Statistics",
            color=discord.Color.purple(),
            timestamp=datetime.now()
        )
        embed.add_field(name="Total Commands", value=total_commands, inline=True)
        embed.add_field(name="Favorite Animal", value=favorite_animal.title() if favorite_animal else "None yet", inline=True)
        
        if commands_used:
            top_commands = sorted(commands_used.items(), key=lambda x: x[1], reverse=True)[:5]
            commands_text = "\n".join([f"`{cmd}` - {count} times" for cmd, count in top_commands])
            embed.add_field(name="Top Commands", value=commands_text, inline=False)
        
        embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else None)
        await ctx.send(embed=embed)

    @discord.app_commands.command(name='stats', description='View your statistics')
    async def slash_stats(self, interaction: discord.Interaction):
        """Show user statistics (slash command)"""
        stats = self.user_stats.get_stats(interaction.user.id)
        commands_used = stats.get('commands', {})
        total_commands = sum(commands_used.values())
        favorite_animal = self.user_stats.get_favorite_animal(interaction.user.id)
        
        embed = discord.Embed(
            title="📊 Your Statistics",
            color=discord.Color.purple(),
            timestamp=datetime.now()
        )
        embed.add_field(name="Total Commands", value=total_commands, inline=True)
        embed.add_field(name="Favorite Animal", value=favorite_animal.title() if favorite_animal else "None yet", inline=True)
        
        if commands_used:
            top_commands = sorted(commands_used.items(), key=lambda x: x[1], reverse=True)[:5]
            commands_text = "\n".join([f"`{cmd}` - {count} times" for cmd, count in top_commands])
            embed.add_field(name="Top Commands", value=commands_text, inline=False)
        
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else None)
        await interaction.response.send_message(embed=embed)

    @commands.command(name='serverinfo')
    async def prefix_serverinfo(self, ctx):
        """Show server information (prefix command)"""
        settings = self.guild_settings.get_settings(ctx.guild.id)
        
        embed = discord.Embed(
            title=f"🏛️ {ctx.guild.name} Info",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.add_field(name="Guild ID", value=ctx.guild.id, inline=True)
        embed.add_field(name="Members", value=ctx.guild.member_count, inline=True)
        embed.add_field(name="Owner", value=ctx.guild.owner.mention if ctx.guild.owner else "Unknown", inline=True)
        embed.add_field(
            name="🐾 Daily Animals",
            value="Enabled" if settings.get('daily_animal_enabled') else "Disabled",
            inline=True
        )
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        await ctx.send(embed=embed)

    @discord.app_commands.command(name='serverinfo', description='Show server information')
    async def slash_serverinfo(self, interaction: discord.Interaction):
        """Show server information (slash command)"""
        settings = self.guild_settings.get_settings(interaction.guild.id)
        
        embed = discord.Embed(
            title=f"🏛️ {interaction.guild.name} Info",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.add_field(name="Guild ID", value=interaction.guild.id, inline=True)
        embed.add_field(name="Members", value=interaction.guild.member_count, inline=True)
        embed.add_field(name="Owner", value=interaction.guild.owner.mention if interaction.guild.owner else "Unknown", inline=True)
        embed.add_field(
            name="🐾 Daily Animals",
            value="Enabled" if settings.get('daily_animal_enabled') else "Disabled",
            inline=True
        )
        embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))
