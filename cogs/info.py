import discord
from discord.ext import commands
from datetime import datetime

class Info(commands.Cog):
    """Information and help commands for AnimalVerse"""

    def __init__(self, bot):
        self.bot = bot

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
            "`!cat` - Get a random cat\n"
            "`!dog` - Get a random dog\n"
            "`!fox` - Get a random fox\n"
            "`!duck` - Get a random duck\n"
            "`!animal` - Get a random animal\n"
            "`!help` - Show this help message\n"
            "`!botinfo` - Show bot information"
        )
        embed.add_field(name="📄 Prefix Commands (📇 use ! prefix)", value=prefix_commands, inline=False)

        # Slash Commands
        slash_commands = (
            "`/cat` - Get a random cat\n"
            "`/dog` - Get a random dog\n"
            "`/fox` - Get a random fox\n"
            "`/duck` - Get a random duck\n"
            "`/animal` - Get a random animal\n"
            "`/help` - Show this help message\n"
            "`/botinfo` - Show bot information"
        )
        embed.add_field(name="📱 Slash Commands (/ prefix)", value=slash_commands, inline=False)

        footer_text = "Want more animals? Suggest them on GitHub!"
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
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        embed.set_footer(text="Made with ❤️ by your favorite developer")
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
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        embed.set_footer(text="Made with ❤️ by your favorite developer")
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

async def setup(bot):
    await bot.add_cog(Info(bot))
