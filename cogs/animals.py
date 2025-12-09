import discord
from discord.ext import commands
import random
from utils import APIHandler, UserStats
from utils.database import JSONDatabase

class Animals(commands.Cog):
    """Animal image commands for AnimalVerse"""

    def __init__(self, bot):
        self.bot = bot
        self.api_handler = APIHandler()
        self.db = JSONDatabase()
        self.user_stats = UserStats(self.db)
        
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
        """Initialize on cog load"""
        pass

    async def cog_unload(self):
        """Cleanup on cog unload"""
        await self.api_handler.close()

    def create_animal_embed(self, animal_name: str, image_url: str, fact: str = None):
        """Helper method to create animal image embeds"""
        try:
            embed = discord.Embed(
                title=f"🐾 {animal_name.title()}",
                color=discord.Color.random()
            )
            embed.set_image(url=image_url)
            if fact:
                embed.add_field(name="📚 Fun Fact", value=fact, inline=False)
            embed.set_footer(text="AnimalVerse 🐾")
            return embed
        except Exception as e:
            print(f"Error creating embed: {e}")
            return None

    async def _send_animal(self, ctx_or_interaction, animal_name: str):
        """Generic animal command sender with proper error handling"""
        try:
            is_slash = isinstance(ctx_or_interaction, discord.Interaction)
            
            # Determine if it's a valid animal
            valid_animals = list(self.animal_facts.keys())
            if animal_name not in valid_animals:
                error_msg = f"❌ Animal '{animal_name}' not found! Available: {', '.join(valid_animals[:5])}..."
                if is_slash:
                    await ctx_or_interaction.response.send_message(error_msg)
                else:
                    await ctx_or_interaction.send(error_msg)
                return
            
            # Get image based on animal type
            image_url = None
            if animal_name == 'cat':
                image_url = await self.api_handler.get_cat_image()
            elif animal_name == 'dog':
                image_url = await self.api_handler.get_dog_image()
            elif animal_name == 'fox':
                image_url = await self.api_handler.get_fox_image()
            elif animal_name == 'duck':
                image_url = await self.api_handler.get_duck_image()
            else:
                # Static fallback for other animals
                image_url = self.api_handler.get_static_image(animal_name)
            
            if not image_url:
                image_url = self.api_handler.get_static_image(animal_name)
            
            # Get fun fact
            facts = self.animal_facts.get(animal_name, ["Amazing animal!"])
            fact = random.choice(facts)
            
            # Create embed
            embed = self.create_animal_embed(animal_name, image_url, fact)
            if not embed:
                if is_slash:
                    await ctx_or_interaction.response.send_message("❌ Failed to create message.")
                else:
                    await ctx_or_interaction.send("❌ Failed to create message.")
                return
            
            # Send embed
            if is_slash:
                if not ctx_or_interaction.response.is_done():
                    await ctx_or_interaction.response.defer()
                await ctx_or_interaction.followup.send(embed=embed)
            else:
                async with ctx_or_interaction.typing():
                    await ctx_or_interaction.send(embed=embed)
            
            # Track stats
            try:
                user_id = ctx_or_interaction.user.id if is_slash else ctx_or_interaction.author.id
                self.user_stats.add_favorite_animal(user_id, animal_name)
            except Exception as e:
                print(f"Error tracking stats: {e}")
        
        except discord.errors.HTTPException as e:
            print(f"Discord HTTP error: {e}")
            try:
                if is_slash and not ctx_or_interaction.response.is_done():
                    await ctx_or_interaction.response.send_message("❌ Failed to send message (Discord error).", ephemeral=True)
            except:
                pass
        except Exception as e:
            print(f"Unexpected error in _send_animal: {e}")
            try:
                if is_slash:
                    if not ctx_or_interaction.response.is_done():
                        await ctx_or_interaction.response.send_message("❌ An unexpected error occurred.", ephemeral=True)
                else:
                    await ctx_or_interaction.send("❌ An unexpected error occurred.")
            except:
                pass

    # ==================== ANIMAL COMMANDS ====================
    @commands.command(name='cat', aliases=['kitten', 'meow', 'kitty'])
    async def cmd_cat(self, ctx):
        await self._send_animal(ctx, 'cat')

    @commands.command(name='dog', aliases=['doggo', 'woof', 'puppy', 'pupper'])
    async def cmd_dog(self, ctx):
        await self._send_animal(ctx, 'dog')

    @commands.command(name='fox', aliases=['fennec', 'vulpes', 'foxy'])
    async def cmd_fox(self, ctx):
        await self._send_animal(ctx, 'fox')

    @commands.command(name='duck', aliases=['quack', 'mallard', 'birdie'])
    async def cmd_duck(self, ctx):
        await self._send_animal(ctx, 'duck')

    @commands.command(name='rabbit', aliases=['bunny', 'hare', 'cottontail'])
    async def cmd_rabbit(self, ctx):
        await self._send_animal(ctx, 'rabbit')

    @commands.command(name='raccoon', aliases=['trash-panda', 'bandit', 'coon'])
    async def cmd_raccoon(self, ctx):
        await self._send_animal(ctx, 'raccoon')

    @commands.command(name='owl', aliases=['owlie', 'hoot', 'birb'])
    async def cmd_owl(self, ctx):
        await self._send_animal(ctx, 'owl')

    @commands.command(name='penguin', aliases=['tux', 'waddle', 'arctic'])
    async def cmd_penguin(self, ctx):
        await self._send_animal(ctx, 'penguin')

    @commands.command(name='panda', aliases=['bamboo', 'giant', 'bear-cat'])
    async def cmd_panda(self, ctx):
        await self._send_animal(ctx, 'panda')

    @commands.command(name='koala', aliases=['eucalyptus', 'fuzzy', 'aussie'])
    async def cmd_koala(self, ctx):
        await self._send_animal(ctx, 'koala')

    @commands.command(name='sloth', aliases=['slow', 'lazy', 'hanging'])
    async def cmd_sloth(self, ctx):
        await self._send_animal(ctx, 'sloth')

    @commands.command(name='hedgehog', aliases=['spiky', 'hedge', 'sonic'])
    async def cmd_hedgehog(self, ctx):
        await self._send_animal(ctx, 'hedgehog')

    @commands.command(name='otter', aliases=['otter-pop', 'river', 'sea-otter'])
    async def cmd_otter(self, ctx):
        await self._send_animal(ctx, 'otter')

    @commands.command(name='squirrel', aliases=['nutty', 'fluffy', 'acorn'])
    async def cmd_squirrel(self, ctx):
        await self._send_animal(ctx, 'squirrel')

    @commands.command(name='deer', aliases=['fawn', 'stag', 'doe'])
    async def cmd_deer(self, ctx):
        await self._send_animal(ctx, 'deer')

    @commands.command(name='bear', aliases=['ursine', 'grizzly', 'panda-uncle'])
    async def cmd_bear(self, ctx):
        await self._send_animal(ctx, 'bear')

    @commands.command(name='wolf', aliases=['dire', 'pup', 'howler'])
    async def cmd_wolf(self, ctx):
        await self._send_animal(ctx, 'wolf')

    @commands.command(name='eagle', aliases=['hawk', 'falcon', 'bird-king'])
    async def cmd_eagle(self, ctx):
        await self._send_animal(ctx, 'eagle')

    @commands.command(name='dolphin', aliases=['porpoise', 'swimmer', 'aqua-friend'])
    async def cmd_dolphin(self, ctx):
        await self._send_animal(ctx, 'dolphin')

    @commands.command(name='animal', aliases=['random-animal', 'randomanimal', 'pets'])
    async def cmd_random_animal(self, ctx):
        """Get a random animal image (prefix command)"""
        animal_name = random.choice(list(self.animal_facts.keys()))
        await self._send_animal(ctx, animal_name)

    # ==================== SLASH COMMANDS ====================
    @discord.app_commands.command(name='cat', description='Get a random cat image')
    async def slash_cat(self, interaction: discord.Interaction):
        await self._send_animal(interaction, 'cat')

    @discord.app_commands.command(name='dog', description='Get a random dog image')
    async def slash_dog(self, interaction: discord.Interaction):
        await self._send_animal(interaction, 'dog')

    @discord.app_commands.command(name='animal', description='Get a random animal image')
    async def slash_random_animal(self, interaction: discord.Interaction):
        animal_name = random.choice(list(self.animal_facts.keys()))
        await self._send_animal(interaction, animal_name)

    @discord.app_commands.command(name='animals-list', description='Show all available animals')
    async def slash_animals_list(self, interaction: discord.Interaction):
        try:
            animals_text = ', '.join([f'`{a}`' for a in sorted(self.animal_facts.keys())])
            embed = discord.Embed(
                title="🐾 Available Animals",
                description=f"Total: {len(self.animal_facts)} animals\n\n{animals_text}",
                color=discord.Color.blue()
            )
            embed.set_footer(text="Use /animal to get a random one!")
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(f"Error in animals_list: {e}")
            await interaction.response.send_message("❌ Failed to show animals list.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Animals(bot))
