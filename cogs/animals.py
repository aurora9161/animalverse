import discord
from discord.ext import commands
import aiohttp
import random

class Animals(commands.Cog):
    """Animal image commands for AnimalVerse"""

    def __init__(self, bot):
        self.bot = bot
        self.session = None
        self.animal_facts = {
            'cat': [
                "Cats can rotate their ears independently!",
                "A cat's purr vibrates at a frequency that may promote bone healing.",
                "Cats have over 20 different vocalizations!",
                "A cat's nose print is unique, like a human fingerprint.",
                "Cats spend about 70% of their lives sleeping!"
            ],
            'dog': [
                "Dogs can understand up to 250 different words and gestures!",
                "Dogs have three eyelids to help keep their eyes moist and protected.",
                "A dog's sense of smell is 10,000 to 100,000 times more sensitive than humans.",
                "Dogs only sweat through the pads of their feet.",
                "Puppies are born without the ability to regulate their body temperature."
            ],
            'fox': [
                "Foxes use the Earth's magnetic field to hunt prey beneath the snow!",
                "A fox's tail is called a brush and helps it balance.",
                "Foxes can hear a mouse squeaking from 100 feet away.",
                "A group of foxes is called a skulk or leash.",
                "Foxes have retractable claws similar to cats!"
            ],
            'duck': [
                "Ducks can sleep with one eye open to watch for predators!",
                "Ducks have waterproof feathers thanks to special glands.",
                "A duck's quack doesn't echo, and no one knows why!",
                "Ducks can see ultraviolet light!",
                "Male ducks are called drakes and females are called hens."
            ],
            'rabbit': [
                "Rabbits can see nearly 360 degrees around them!",
                "A rabbit's teeth never stop growing throughout their life.",
                "Rabbits can jump up to 9 feet in a single leap!",
                "Rabbits are crepuscular, most active at dawn and dusk.",
                "A group of rabbits is called a fluffle or colony!"
            ],
            'raccoon': [
                "Raccoons can open locks with their intelligent paws!",
                "A raccoon's sense of touch is highly developed.",
                "Raccoons wash their food before eating it.",
                "Raccoons have excellent night vision.",
                "A group of raccoons is called a gaze!"
            ],
            'owl': [
                "Owls can turn their heads up to 270 degrees!",
                "Owls have asymmetrical ears to help locate prey.",
                "Owls don't have eyeballs - they have eye tubes!",
                "Most owls are nocturnal hunters.",
                "Owls are found on every continent except Antarctica!"
            ],
            'penguin': [
                "Penguins can swim up to 22 mph underwater!",
                "Penguins' feathers are denser than any other bird's.",
                "Emperor penguins can dive deeper than 1,800 feet!",
                "Penguins are found only in the Southern Hemisphere.",
                "Penguin parents recognize their chick by its unique call!"
            ],
            'panda': [
                "Giant pandas have a pseudo-thumb to help grip bamboo!",
                "Pandas spend 12-16 hours eating bamboo daily.",
                "Baby pandas are about the size of a stick of butter!",
                "Pandas have excellent hearing and smell.",
                "Pandas are one of the rarest animals in the world!"
            ],
            'koala': [
                "Koalas sleep 18-22 hours per day!",
                "Koalas have fingerprints similar to human fingerprints.",
                "Koalas can identify which eucalyptus leaves are safe to eat.",
                "Male koalas have a scent gland on their chest.",
                "Koalas are not actually bears - they're marsupials!"
            ],
            'sloth': [
                "Sloths only descend from trees once a week to defecate!",
                "Sloths move so slowly that algae grows on their fur.",
                "Sloths can rotate their heads up to 270 degrees.",
                "A sloth's metabolism is half that of other mammals.",
                "Sloths are surprisingly good swimmers!"
            ],
            'hedgehog': [
                "Hedgehogs have over 5,000 quills!",
                "Hedgehogs can curl into a ball to protect themselves.",
                "Hedgehogs are immune to certain toxins.",
                "A hedgehog can run 7 mph.",
                "Hedgehogs use their sense of smell to navigate!"
            ],
            'otter': [
                "Otters hold hands while sleeping so they don't drift apart!",
                "Sea otters have the thickest fur of any animal.",
                "Otters are 99% efficient at retaining body heat.",
                "Otters use rocks as tools to crack open shells.",
                "Otters have whiskers that detect vibrations in water!"
            ],
            'squirrel': [
                "Squirrels can't digest cellulose, so they don't eat leaves.",
                "A squirrel's tail is one-third of its body length!",
                "Squirrels can jump 10 times their body length.",
                "Squirrels have excellent memory for buried nuts.",
                "Flying squirrels can glide up to 150 feet!"
            ],
            'deer': [
                "Deer can see nearly 310 degrees around them!",
                "A deer's ears can rotate independently.",
                "Male deer grow new antlers every year.",
                "Deer are ruminants with a four-chambered stomach.",
                "White-tailed deer can run up to 40 mph!"
            ],
            'bear': [
                "Bears can run up to 35 mph despite their size!",
                "A bear's sense of smell is 7 times better than a grizzly's.",
                "Bears can see in color and have good night vision.",
                "Bears stand on their hind legs to smell better.",
                "Bears are one of the few animals that recognize themselves in mirrors!"
            ],
            'wolf': [
                "Wolves have specialized shoulder and leg muscles for hunting.",
                "A wolf pack typically consists of a family unit.",
                "Wolves can hear sounds 6 miles away in winter.",
                "Wolves can run for hours at 5 mph pace.",
                "Each wolf has a unique howl like a human fingerprint!"
            ],
            'eagle': [
                "Eagles can see fish from over 1 mile away!",
                "An eagle's grip strength is 10 times stronger than human grip.",
                "Eagles can fly up to 10,000 feet high.",
                "Eagles mate for life.",
                "An eagle's nest can weigh up to 1 ton!"
            ],
            'dolphin': [
                "Dolphins sleep with one eye open!",
                "Dolphins use echolocation to navigate and hunt.",
                "Dolphins can recognize themselves in mirrors.",
                "Dolphins communicate using clicks and whistles.",
                "Dolphins can swim at speeds up to 20 mph!"
            ]
        }

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

    # ==================== CAT API ====================
    async def fetch_cat_image(self):
        try:
            async with self.session.get('https://api.thecatapi.com/v1/images/search') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data[0]['url']
        except Exception as e:
            print(f"Error fetching cat: {e}")
        return None

    # ==================== DOG API ====================
    async def fetch_dog_image(self):
        try:
            async with self.session.get('https://api.thedogapi.com/v1/images/search') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data[0]['url']
        except Exception as e:
            print(f"Error fetching dog: {e}")
        return None

    # ==================== FOX API ====================
    async def fetch_fox_image(self):
        try:
            async with self.session.get('https://randomfox.ca/floof/') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data['image']
        except Exception as e:
            print(f"Error fetching fox: {e}")
        return None

    # ==================== DUCK API ====================
    async def fetch_duck_image(self):
        try:
            async with self.session.get('https://random-d.uk/api/random') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data['url']
        except Exception as e:
            print(f"Error fetching duck: {e}")
        return None

    # ==================== RABBIT API ====================
    async def fetch_rabbit_image(self):
        try:
            async with self.session.get('https://api.api-ninjas.com/v1/animals?name=rabbit') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data:
                        return data[0].get('picture_link', 'https://images.unsplash.com/photo-1585110396000-c9ffd4d4b3f4')
        except Exception as e:
            print(f"Error fetching rabbit: {e}")
        return 'https://images.unsplash.com/photo-1585110396000-c9ffd4d4b3f4'

    # ==================== RACCOON IMAGE ====================
    async def fetch_raccoon_image(self):
        try:
            async with self.session.get('https://images.unsplash.com/search/photos?query=raccoon') as resp:
                if resp.status == 200:
                    return 'https://images.unsplash.com/photo-1567270762171-79799e56aea1'
        except:
            pass
        return 'https://images.unsplash.com/photo-1567270762171-79799e56aea1'

    # ==================== OWL IMAGE ====================
    async def fetch_owl_image(self):
        return 'https://images.unsplash.com/photo-1540573133985-87b6da97af72'

    # ==================== PENGUIN IMAGE ====================
    async def fetch_penguin_image(self):
        return 'https://images.unsplash.com/photo-1551629146-8d3d89e68da0'

    # ==================== PANDA IMAGE ====================
    async def fetch_panda_image(self):
        return 'https://images.unsplash.com/photo-1525382455947-f319bc05fb35'

    # ==================== KOALA IMAGE ====================
    async def fetch_koala_image(self):
        return 'https://images.unsplash.com/photo-1459262838948-3e2de6c3638f'

    # ==================== SLOTH IMAGE ====================
    async def fetch_sloth_image(self):
        return 'https://images.unsplash.com/photo-1551324894-4f4f1a7f0d6e'

    # ==================== HEDGEHOG IMAGE ====================
    async def fetch_hedgehog_image(self):
        return 'https://images.unsplash.com/photo-1539571696357-5a69c006ae30'

    # ==================== OTTER IMAGE ====================
    async def fetch_otter_image(self):
        return 'https://images.unsplash.com/photo-1591229728215-2a83dbd60066'

    # ==================== SQUIRREL IMAGE ====================
    async def fetch_squirrel_image(self):
        return 'https://images.unsplash.com/photo-1446824653969-c8398aa337df'

    # ==================== DEER IMAGE ====================
    async def fetch_deer_image(self):
        return 'https://images.unsplash.com/photo-1484406566174-9da000fda645'

    # ==================== BEAR IMAGE ====================
    async def fetch_bear_image(self):
        return 'https://images.unsplash.com/photo-1528127269029-c3ee1f0b2c14'

    # ==================== WOLF IMAGE ====================
    async def fetch_wolf_image(self):
        return 'https://images.unsplash.com/photo-1501706362039-c06b2d715385'

    # ==================== EAGLE IMAGE ====================
    async def fetch_eagle_image(self):
        return 'https://images.unsplash.com/photo-1540573133985-87b6da97af72'

    # ==================== DOLPHIN IMAGE ====================
    async def fetch_dolphin_image(self):
        return 'https://images.unsplash.com/photo-1505142468610-359e7d316be0'

    # Dictionary of all animals
    animal_list = {
        'cat': fetch_cat_image,
        'dog': fetch_dog_image,
        'fox': fetch_fox_image,
        'duck': fetch_duck_image,
        'rabbit': fetch_rabbit_image,
        'raccoon': fetch_raccoon_image,
        'owl': fetch_owl_image,
        'penguin': fetch_penguin_image,
        'panda': fetch_panda_image,
        'koala': fetch_koala_image,
        'sloth': fetch_sloth_image,
        'hedgehog': fetch_hedgehog_image,
        'otter': fetch_otter_image,
        'squirrel': fetch_squirrel_image,
        'deer': fetch_deer_image,
        'bear': fetch_bear_image,
        'wolf': fetch_wolf_image,
        'eagle': fetch_eagle_image,
        'dolphin': fetch_dolphin_image,
    }

    # ==================== RANDOM ANIMAL ====================
    @commands.command(name='animal', aliases=['random-animal', 'randomanimal', 'pets'])
    async def prefix_random_animal(self, ctx):
        """Get a random animal image (prefix command)"""
        animal_name = random.choice(list(self.animal_list.keys()))
        fetch_func = self.animal_list[animal_name]
        fact = random.choice(self.animal_facts.get(animal_name, ["Amazing animal!"]))
        
        async with ctx.typing():
            image_url = await fetch_func(self)
            if image_url:
                embed = self.create_animal_embed(animal_name, image_url, fact)
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Could not fetch animal image. Please try again later.")

    @discord.app_commands.command(name='animal', description='Get a random animal image')
    async def slash_random_animal(self, interaction: discord.Interaction):
        """Get a random animal image (slash command)"""
        animal_name = random.choice(list(self.animal_list.keys()))
        fetch_func = self.animal_list[animal_name]
        fact = random.choice(self.animal_facts.get(animal_name, ["Amazing animal!"]))
        
        await interaction.response.defer()
        image_url = await fetch_func(self)
        if image_url:
            embed = self.create_animal_embed(animal_name, image_url, fact)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("❌ Could not fetch animal image. Please try again later.")

    # ==================== SPECIFIC ANIMALS ====================
    async def _send_animal(self, ctx, animal_name: str, aliases: list):
        """Generic animal command sender"""
        fetch_func = self.animal_list.get(animal_name)
        if not fetch_func:
            await ctx.send(f"❌ Animal '{animal_name}' not found!")
            return
        
        async with ctx.typing():
            image_url = await fetch_func(self)
            fact = random.choice(self.animal_facts.get(animal_name, ["Amazing animal!"]))
            if image_url:
                embed = self.create_animal_embed(animal_name, image_url, fact)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Could not fetch {animal_name} image. Please try again later.")

    # Create commands for each animal
    @commands.command(name='cat', aliases=['kitten', 'meow', 'kitty'])
    async def cmd_cat(self, ctx):
        await self._send_animal(ctx, 'cat', ['kitten', 'meow', 'kitty'])

    @commands.command(name='dog', aliases=['doggo', 'woof', 'puppy', 'pupper'])
    async def cmd_dog(self, ctx):
        await self._send_animal(ctx, 'dog', ['doggo', 'woof', 'puppy', 'pupper'])

    @commands.command(name='fox', aliases=['fennec', 'vulpes', 'foxy'])
    async def cmd_fox(self, ctx):
        await self._send_animal(ctx, 'fox', ['fennec', 'vulpes', 'foxy'])

    @commands.command(name='duck', aliases=['quack', 'mallard', 'birdie'])
    async def cmd_duck(self, ctx):
        await self._send_animal(ctx, 'duck', ['quack', 'mallard', 'birdie'])

    @commands.command(name='rabbit', aliases=['bunny', 'hare', 'cottontail'])
    async def cmd_rabbit(self, ctx):
        await self._send_animal(ctx, 'rabbit', ['bunny', 'hare', 'cottontail'])

    @commands.command(name='raccoon', aliases=['trash-panda', 'bandit', 'coon'])
    async def cmd_raccoon(self, ctx):
        await self._send_animal(ctx, 'raccoon', ['trash-panda', 'bandit', 'coon'])

    @commands.command(name='owl', aliases=['owlie', 'hoot', 'birb'])
    async def cmd_owl(self, ctx):
        await self._send_animal(ctx, 'owl', ['owlie', 'hoot', 'birb'])

    @commands.command(name='penguin', aliases=['tux', 'waddle', 'arctic'])
    async def cmd_penguin(self, ctx):
        await self._send_animal(ctx, 'penguin', ['tux', 'waddle', 'arctic'])

    @commands.command(name='panda', aliases=['bamboo', 'giant', 'bear-cat'])
    async def cmd_panda(self, ctx):
        await self._send_animal(ctx, 'panda', ['bamboo', 'giant', 'bear-cat'])

    @commands.command(name='koala', aliases=['eucalyptus', 'fuzzy', 'aussie'])
    async def cmd_koala(self, ctx):
        await self._send_animal(ctx, 'koala', ['eucalyptus', 'fuzzy', 'aussie'])

    @commands.command(name='sloth', aliases=['slow', 'lazy', 'hanging'])
    async def cmd_sloth(self, ctx):
        await self._send_animal(ctx, 'sloth', ['slow', 'lazy', 'hanging'])

    @commands.command(name='hedgehog', aliases=['spiky', 'hedge', 'sonic'])
    async def cmd_hedgehog(self, ctx):
        await self._send_animal(ctx, 'hedgehog', ['spiky', 'hedge', 'sonic'])

    @commands.command(name='otter', aliases=['otter-pop', 'river', 'sea-otter'])
    async def cmd_otter(self, ctx):
        await self._send_animal(ctx, 'otter', ['otter-pop', 'river', 'sea-otter'])

    @commands.command(name='squirrel', aliases=['nutty', 'fluffy', 'acorn'])
    async def cmd_squirrel(self, ctx):
        await self._send_animal(ctx, 'squirrel', ['nutty', 'fluffy', 'acorn'])

    @commands.command(name='deer', aliases=['fawn', 'stag', 'doe'])
    async def cmd_deer(self, ctx):
        await self._send_animal(ctx, 'deer', ['fawn', 'stag', 'doe'])

    @commands.command(name='bear', aliases=['ursine', 'grizzly', 'panda-uncle'])
    async def cmd_bear(self, ctx):
        await self._send_animal(ctx, 'bear', ['ursine', 'grizzly', 'panda-uncle'])

    @commands.command(name='wolf', aliases=['dire', 'pup', 'howler'])
    async def cmd_wolf(self, ctx):
        await self._send_animal(ctx, 'wolf', ['dire', 'pup', 'howler'])

    @commands.command(name='eagle', aliases=['hawk', 'falcon', 'bird-king'])
    async def cmd_eagle(self, ctx):
        await self._send_animal(ctx, 'eagle', ['hawk', 'falcon', 'bird-king'])

    @commands.command(name='dolphin', aliases=['porpoise', 'swimmer', 'aqua-friend'])
    async def cmd_dolphin(self, ctx):
        await self._send_animal(ctx, 'dolphin', ['porpoise', 'swimmer', 'aqua-friend'])

    # Slash commands for each animal
    @discord.app_commands.command(name='cat', description='Get a random cat image')
    async def slash_cat(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self._send_animal(interaction, 'cat', [])

    @discord.app_commands.command(name='dog', description='Get a random dog image')
    async def slash_dog(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self._send_animal(interaction, 'dog', [])

    @discord.app_commands.command(name='animals-list', description='Show all available animals')
    async def slash_animals_list(self, interaction: discord.Interaction):
        animals_text = ', '.join([f'`{a}`' for a in sorted(self.animal_list.keys())])
        embed = discord.Embed(
            title="🐾 Available Animals",
            description=f"Total: {len(self.animal_list)} animals\n\n{animals_text}",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Use /animal to get a random one, or use the specific command!")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Animals(bot))
