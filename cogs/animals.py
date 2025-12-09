import discord
from discord.ext import commands
import aiohttp
import random

class Animals(commands.Cog):
    """Animal image commands for AnimalVerse"""

    def __init__(self, bot):
        self.bot = bot
        self.session = None

    async def cog_load(self):
        """Create aiohttp session when cog loads"""
        self.session = aiohttp.ClientSession()

    async def cog_unload(self):
        """Close aiohttp session when cog unloads"""
        if self.session:
            await self.session.close()

    def create_animal_embed(self, animal_name: str, image_url: str, fact: str = None):
        """Helper method to create animal image embeds"""
        embed = discord.Embed(
            title=f"🐾 {animal_name.title()}",
            color=discord.Color.random()
        )
        embed.set_image(url=image_url)
        if fact:
            embed.add_field(name="📚 Fun Fact", value=fact, inline=False)
        embed.set_footer(text="AnimalVerse 🐾")
        return embed

    async def fetch_cat_image(self):
        """Fetch random cat image from API"""
        try:
            async with self.session.get('https://api.thecatapi.com/v1/images/search') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data[0]['url']
        except Exception as e:
            print(f"Error fetching cat image: {e}")
        return None

    async def fetch_dog_image(self):
        """Fetch random dog image from API"""
        try:
            async with self.session.get('https://api.thedogapi.com/v1/images/search') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data[0]['url']
        except Exception as e:
            print(f"Error fetching dog image: {e}")
        return None

    async def fetch_fox_image(self):
        """Fetch random fox image from API"""
        try:
            async with self.session.get('https://randomfox.ca/floof/') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data['image']
        except Exception as e:
            print(f"Error fetching fox image: {e}")
        return None

    async def fetch_duck_image(self):
        """Fetch random duck image from API"""
        try:
            async with self.session.get('https://random-d.uk/api/random') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data['url']
        except Exception as e:
            print(f"Error fetching duck image: {e}")
        return None

    # ==================== CAT COMMANDS ====================
    @commands.command(name='cat', aliases=['kitten', 'meow'])
    async def prefix_cat(self, ctx):
        """Get a random cat image (prefix command)"""
        async with ctx.typing():
            image_url = await self.fetch_cat_image()
            if image_url:
                embed = self.create_animal_embed("Cat", image_url, "Cats can rotate their ears independently!")
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Could not fetch cat image. Please try again later.")

    @discord.app_commands.command(name='cat', description='Get a random cat image')
    async def slash_cat(self, interaction: discord.Interaction):
        """Get a random cat image (slash command)"""
        await interaction.response.defer()
        image_url = await self.fetch_cat_image()
        if image_url:
            embed = self.create_animal_embed("Cat", image_url, "Cats can rotate their ears independently!")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("❌ Could not fetch cat image. Please try again later.")

    # ==================== DOG COMMANDS ====================
    @commands.command(name='dog', aliases=['doggo', 'woof', 'puppy'])
    async def prefix_dog(self, ctx):
        """Get a random dog image (prefix command)"""
        async with ctx.typing():
            image_url = await self.fetch_dog_image()
            if image_url:
                embed = self.create_animal_embed("Dog", image_url, "Dogs can understand up to 250 different words and gestures!")
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Could not fetch dog image. Please try again later.")

    @discord.app_commands.command(name='dog', description='Get a random dog image')
    async def slash_dog(self, interaction: discord.Interaction):
        """Get a random dog image (slash command)"""
        await interaction.response.defer()
        image_url = await self.fetch_dog_image()
        if image_url:
            embed = self.create_animal_embed("Dog", image_url, "Dogs can understand up to 250 different words and gestures!")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("❌ Could not fetch dog image. Please try again later.")

    # ==================== FOX COMMANDS ====================
    @commands.command(name='fox', aliases=['fennec', 'vulpes'])
    async def prefix_fox(self, ctx):
        """Get a random fox image (prefix command)"""
        async with ctx.typing():
            image_url = await self.fetch_fox_image()
            if image_url:
                embed = self.create_animal_embed("Fox", image_url, "Foxes use the Earth's magnetic field to hunt prey beneath the snow!")
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Could not fetch fox image. Please try again later.")

    @discord.app_commands.command(name='fox', description='Get a random fox image')
    async def slash_fox(self, interaction: discord.Interaction):
        """Get a random fox image (slash command)"""
        await interaction.response.defer()
        image_url = await self.fetch_fox_image()
        if image_url:
            embed = self.create_animal_embed("Fox", image_url, "Foxes use the Earth's magnetic field to hunt prey beneath the snow!")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("❌ Could not fetch fox image. Please try again later.")

    # ==================== DUCK COMMANDS ====================
    @commands.command(name='duck', aliases=['quack', 'mallard'])
    async def prefix_duck(self, ctx):
        """Get a random duck image (prefix command)"""
        async with ctx.typing():
            image_url = await self.fetch_duck_image()
            if image_url:
                embed = self.create_animal_embed("Duck", image_url, "Ducks can sleep with one eye open to watch for predators!")
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Could not fetch duck image. Please try again later.")

    @discord.app_commands.command(name='duck', description='Get a random duck image')
    async def slash_duck(self, interaction: discord.Interaction):
        """Get a random duck image (slash command)"""
        await interaction.response.defer()
        image_url = await self.fetch_duck_image()
        if image_url:
            embed = self.create_animal_embed("Duck", image_url, "Ducks can sleep with one eye open to watch for predators!")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("❌ Could not fetch duck image. Please try again later.")

    # ==================== RANDOM ANIMAL ====================
    @commands.command(name='animal', aliases=['random-animal', 'randomanimal'])
    async def prefix_random_animal(self, ctx):
        """Get a random animal image (prefix command)"""
        animals = [
            ('cat', self.fetch_cat_image, "Cats can rotate their ears independently!"),
            ('dog', self.fetch_dog_image, "Dogs can understand up to 250 different words!"),
            ('fox', self.fetch_fox_image, "Foxes use Earth's magnetic field to hunt!"),
            ('duck', self.fetch_duck_image, "Ducks can sleep with one eye open!")
        ]
        animal_name, fetch_func, fact = random.choice(animals)
        
        async with ctx.typing():
            image_url = await fetch_func()
            if image_url:
                embed = self.create_animal_embed(animal_name, image_url, fact)
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Could not fetch animal image. Please try again later.")

    @discord.app_commands.command(name='animal', description='Get a random animal image')
    async def slash_random_animal(self, interaction: discord.Interaction):
        """Get a random animal image (slash command)"""
        animals = [
            ('cat', self.fetch_cat_image, "Cats can rotate their ears independently!"),
            ('dog', self.fetch_dog_image, "Dogs can understand up to 250 different words!"),
            ('fox', self.fetch_fox_image, "Foxes use Earth's magnetic field to hunt!"),
            ('duck', self.fetch_duck_image, "Ducks can sleep with one eye open!")
        ]
        animal_name, fetch_func, fact = random.choice(animals)
        
        await interaction.response.defer()
        image_url = await fetch_func()
        if image_url:
            embed = self.create_animal_embed(animal_name, image_url, fact)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("❌ Could not fetch animal image. Please try again later.")

async def setup(bot):
    await bot.add_cog(Animals(bot))
