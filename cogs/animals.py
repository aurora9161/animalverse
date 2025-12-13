import discord
from discord.ext import commands
import random
import logging
from utils import APIHandler, UserStats
from utils.database import JSONDatabase

logger = logging.getLogger('AnimalVerse')

class Animals(commands.Cog):
    """Animal image commands for AnimalVerse"""

    def __init__(self, bot):
        self.bot = bot
        self.api_handler = APIHandler()
        self.db = JSONDatabase()
        self.user_stats = UserStats(self.db)
        self.request_count = {}  # Track requests per user
        
        # Animals that use static images (Unsplash fallbacks)
        self.static_image_animals = {'sloth', 'otter', 'squirrel', 'panda', 'koala', 'rabbit', 'penguin', 'owl'}
        # Animals with API support
        self.api_animals = {'cat', 'dog', 'fox', 'duck'}
        # Animals using Wikimedia/Wildlife API
        self.wildlife_animals = {'bear', 'deer', 'eagle', 'dolphin', 'wolf', 'raccoon', 'hedgehog'}
        
        self.animal_facts = {
            'cat': [
                "Cats can rotate their ears independently!",
                "A cat's purr vibrates at a frequency that may promote bone healing.",
                "Cats have over 20 different vocalizations!",
                "A cat's nose print is unique, like a human fingerprint.",
                "Cats spend about 70% of their lives sleeping!",
                "Cats have a special collarbone that allows them to squeeze through tight spaces.",
                "A cat's brain is biologically more similar to a human brain than a dog's brain is."
            ],
            'dog': [
                "Dogs can understand up to 250 different words and gestures!",
                "Dogs have three eyelids to help keep their eyes moist and protected.",
                "A dog's sense of smell is 10,000 to 100,000 times more sensitive than humans.",
                "Dogs only sweat through the pads of their feet.",
                "Puppies are born without the ability to regulate their body temperature.",
                "A dog's sense of hearing is about four times better than humans.",
                "Dogs have an incredible sense of time and can sense when their owner is coming home."
            ],
            'fox': [
                "Foxes use the Earth's magnetic field to hunt prey beneath the snow!",
                "A fox's tail is called a brush and helps it balance.",
                "Foxes can hear a mouse squeaking from 100 feet away.",
                "A group of foxes is called a skulk or leash.",
                "Foxes have retractable claws similar to cats!",
                "Foxes can see in the dark almost as well as cats can.",
                "Arctic foxes have thick fur on the soles of their feet to keep them warm."
            ],
            'duck': [
                "Ducks can sleep with one eye open to watch for predators!",
                "Ducks have waterproof feathers thanks to special glands.",
                "A duck's quack doesn't echo, and no one knows why!",
                "Ducks can see ultraviolet light!",
                "Male ducks are called drakes and females are called hens.",
                "Ducks have excellent color vision and can see ultraviolet colors.",
                "A duck's tongue has touch sensors that help them find food."
            ],
            'rabbit': [
                "Rabbits can see nearly 360 degrees around them!",
                "A rabbit's teeth never stop growing throughout their life.",
                "Rabbits can jump up to 9 feet in a single leap!",
                "Rabbits are crepuscular, most active at dawn and dusk.",
                "A group of rabbits is called a fluffle or colony!",
                "Rabbits purr when they're happy, just like cats!",
                "Rabbits can sleep with their eyes open!"
            ],
            'raccoon': [
                "Raccoons can open locks with their intelligent paws!",
                "A raccoon's sense of touch is highly developed.",
                "Raccoons wash their food before eating it.",
                "Raccoons have excellent night vision.",
                "A group of raccoons is called a gaze!",
                "Raccoons are one of the smartest wild animals.",
                "Raccoons have black markings on their face that reduce glare, like a football player's eye black."
            ],
            'owl': [
                "Owls can turn their heads up to 270 degrees!",
                "Owls have asymmetrical ears to help locate prey.",
                "Owls don't have eyeballs - they have eye tubes!",
                "Most owls are nocturnal hunters.",
                "Owls are found on every continent except Antarctica!",
                "An owl's eyes are about the same size as human eyes.",
                "Owls have excellent hearing and can hunt in complete darkness."
            ],
            'penguin': [
                "Penguins can swim up to 22 mph underwater!",
                "Penguins' feathers are denser than any other bird's.",
                "Emperor penguins can dive deeper than 1,800 feet!",
                "Penguins are found only in the Southern Hemisphere.",
                "Penguin parents recognize their chick by its unique call!",
                "Penguins can hold their breath for up to 7 minutes.",
                "A group of penguins in water is called a raft, on land a waddle."
            ],
            'panda': [
                "Giant pandas have a pseudo-thumb to help grip bamboo!",
                "Pandas spend 12-16 hours eating bamboo daily.",
                "Baby pandas are about the size of a stick of butter!",
                "Pandas have excellent hearing and smell.",
                "Pandas are one of the rarest animals in the world!",
                "Pandas are actually carnivores but eat bamboo as 99% of their diet.",
                "Baby pandas are born pink and blind!"
            ],
            'koala': [
                "Koalas sleep 18-22 hours per day!",
                "Koalas have fingerprints similar to human fingerprints.",
                "Koalas can identify which eucalyptus leaves are safe to eat.",
                "Male koalas have a scent gland on their chest.",
                "Koalas are not actually bears - they're marsupials!",
                "Koalas get 90% of their water from eucalyptus leaves.",
                "A koala's closest living relative is the wombat!"
            ],
            'sloth': [
                "Sloths only descend from trees once a week to defecate!",
                "Sloths move so slowly that algae grows on their fur.",
                "Sloths can rotate their heads up to 270 degrees.",
                "A sloth's metabolism is half that of other mammals.",
                "Sloths are surprisingly good swimmers!",
                "Sloths have a 40-hour digestive cycle.",
                "A sloth's arm span is longer than its body height."
            ],
            'hedgehog': [
                "Hedgehogs have over 5,000 quills!",
                "Hedgehogs can curl into a ball to protect themselves.",
                "Hedgehogs are immune to certain toxins.",
                "A hedgehog can run 7 mph.",
                "Hedgehogs use their sense of smell to navigate!",
                "Hedgehogs have poor eyesight but excellent hearing.",
                "Hedgehogs are lactose intolerant!"
            ],
            'otter': [
                "Otters hold hands while sleeping so they don't drift apart!",
                "Sea otters have the thickest fur of any animal.",
                "Otters are 99% efficient at retaining body heat.",
                "Otters use rocks as tools to crack open shells.",
                "Otters have whiskers that detect vibrations in water!",
                "Otters have a metabolism so fast they must eat 25% of their body weight daily.",
                "Sea otters can hold their breath for 5-8 minutes."
            ],
            'squirrel': [
                "Squirrels can't digest cellulose, so they don't eat leaves.",
                "A squirrel's tail is one-third of its body length!",
                "Squirrels can jump 10 times their body length.",
                "Squirrels have excellent memory for buried nuts.",
                "Flying squirrels can glide up to 150 feet!",
                "Squirrels have sharp claws that help them grip tree bark.",
                "Squirrels can rotate their back feet 180 degrees!"
            ],
            'deer': [
                "Deer can see nearly 310 degrees around them!",
                "A deer's ears can rotate independently.",
                "Male deer grow new antlers every year.",
                "Deer are ruminants with a four-chambered stomach.",
                "White-tailed deer can run up to 40 mph!",
                "Deer have excellent night vision.",
                "A deer's eyes are so positioned that it can see behind itself!"
            ],
            'bear': [
                "Bears can run up to 35 mph despite their size!",
                "A bear's sense of smell is 7 times better than a grizzly's.",
                "Bears can see in color and have good night vision.",
                "Bears stand on their hind legs to smell better.",
                "Bears are one of the few animals that recognize themselves in mirrors!",
                "Bears have excellent memory and can remember food sources for years.",
                "Bears are actually considered very curious and intelligent animals!"
            ],
            'wolf': [
                "Wolves have specialized shoulder and leg muscles for hunting.",
                "A wolf pack typically consists of a family unit.",
                "Wolves can hear sounds 6 miles away in winter.",
                "Wolves can run for hours at 5 mph pace.",
                "Each wolf has a unique howl like a human fingerprint!",
                "Wolves are incredibly social animals with complex communication.",
                "A wolf's jaw can exert 1,500 PSI of pressure!"
            ],
            'eagle': [
                "Eagles can see fish from over 1 mile away!",
                "An eagle's grip strength is 10 times stronger than human grip.",
                "Eagles can fly up to 10,000 feet high.",
                "Eagles mate for life.",
                "An eagle's nest can weigh up to 1 ton!",
                "Eagles have eyesight 8 times stronger than humans.",
                "Bald eagles can reach speeds of 100 mph in a dive!"
            ],
            'dolphin': [
                "Dolphins sleep with one eye open!",
                "Dolphins use echolocation to navigate and hunt.",
                "Dolphins can recognize themselves in mirrors.",
                "Dolphins communicate using clicks and whistles.",
                "Dolphins can swim at speeds up to 20 mph!",
                "Dolphins are among the most intelligent animals on Earth.",
                "Dolphins have been observed playing and using tools!"
            ]
        }

    async def cog_load(self):
        """Initialize on cog load"""
        logger.info('Animals cog loaded')

    async def cog_unload(self):
        """Cleanup on cog unload"""
        try:
            await self.api_handler.close()
            logger.info('Animals cog unloaded')
        except Exception as e:
            logger.error(f'Error unloading Animals cog: {e}')

    def create_animal_embed(self, animal_name: str, image_url: str, fact: str = None) -> discord.Embed:
        """Create animal image embeds with better styling"""
        try:
            # Color mapping for different animals
            color_map = {
                'cat': discord.Color.orange(),
                'dog': discord.Color.dark_gold(),
                'fox': discord.Color.from_rgb(255, 127, 0),
                'duck': discord.Color.blue(),
                'rabbit': discord.Color.from_rgb(255, 192, 203),
                'raccoon': discord.Color.dark_gray(),
                'owl': discord.Color.darker_gray(),
                'penguin': discord.Color.dark_blue(),
                'panda': discord.Color.lighter_gray(),
                'koala': discord.Color.dark_gray(),
                'sloth': discord.Color.from_rgb(139, 69, 19),
                'hedgehog': discord.Color.from_rgb(160, 82, 45),
                'otter': discord.Color.from_rgb(101, 67, 33),
                'squirrel': discord.Color.from_rgb(165, 42, 42),
                'deer': discord.Color.from_rgb(139, 69, 19),
                'bear': discord.Color.from_rgb(139, 69, 19),
                'wolf': discord.Color.dark_gray(),
                'eagle': discord.Color.dark_gold(),
                'dolphin': discord.Color.blue()
            }
            
            color = color_map.get(animal_name, discord.Color.random())
            
            embed = discord.Embed(
                title=f"🐾 {animal_name.title()}",
                color=color
            )
            embed.set_image(url=image_url)
            
            if fact:
                embed.add_field(name="📚 Fun Fact", value=fact, inline=False)
            
            embed.set_footer(text="AnimalVerse v2.2 🐾 | Use !help for more commands")
            return embed
        except Exception as e:
            logger.error(f"Error creating embed: {e}")
            return None

    async def _send_animal(self, ctx_or_interaction, animal_name: str):
        """Generic animal command sender with proper error handling"""
        try:
            is_slash = isinstance(ctx_or_interaction, discord.Interaction)
            user_id = ctx_or_interaction.user.id if is_slash else ctx_or_interaction.author.id
            
            # Validate animal
            valid_animals = list(self.animal_facts.keys())
            if animal_name not in valid_animals:
                error_msg = f"❌ Unknown animal! Available: {', '.join(valid_animals[:8])}..."
                if is_slash:
                    await ctx_or_interaction.response.send_message(error_msg, ephemeral=True)
                else:
                    await ctx_or_interaction.send(error_msg)
                return
            
            # Defer response for slash commands
            if is_slash and not ctx_or_interaction.response.is_done():
                await ctx_or_interaction.response.defer()
            
            # Get image based on animal type
            image_url = None
            if animal_name == 'cat':
                image_url = await self.api_handler.get_cat_image(self.bot.config.get('cats_api_key', ''))
            elif animal_name == 'dog':
                image_url = await self.api_handler.get_dog_image(self.bot.config.get('dogs_api_key', ''))
            elif animal_name == 'fox':
                image_url = await self.api_handler.get_fox_image()
            elif animal_name == 'duck':
                image_url = await self.api_handler.get_duck_image()
            elif animal_name in self.wildlife_animals:
                # Use Wikimedia API for wildlife animals
                image_url = await self.api_handler.get_wildlife_image(animal_name)
            else:
                # Use static images for remaining animals
                image_url = self.api_handler.get_static_image(animal_name)
            
            # Fallback if image fetch failed
            if not image_url:
                image_url = self.api_handler.get_static_image(animal_name)
            
            # Get fact
            facts = self.animal_facts.get(animal_name, ["Amazing animal!"])
            fact = random.choice(facts)
            
            # Create embed
            embed = self.create_animal_embed(animal_name, image_url, fact)
            if not embed:
                raise Exception("Failed to create embed")
            
            # Send message
            if is_slash:
                await ctx_or_interaction.followup.send(embed=embed)
            else:
                async with ctx_or_interaction.typing():
                    await ctx_or_interaction.send(embed=embed)
            
            # Track stats
            try:
                self.user_stats.add_favorite_animal(user_id, animal_name)
            except Exception as e:
                logger.debug(f"Error tracking stats: {e}")
        
        except discord.errors.HTTPException as e:
            logger.error(f"Discord HTTP error: {e}")
            try:
                if is_slash:
                    if not ctx_or_interaction.response.is_done():
                        await ctx_or_interaction.response.send_message("❌ Discord error. Try again.", ephemeral=True)
                    else:
                        await ctx_or_interaction.followup.send("❌ Discord error. Try again.")
            except:
                pass
        except Exception as e:
            logger.error(f"Error in _send_animal: {e}")
            try:
                error_msg = "❌ An error occurred. Try again later."
                if is_slash:
                    if not ctx_or_interaction.response.is_done():
                        await ctx_or_interaction.response.send_message(error_msg, ephemeral=True)
                    else:
                        await ctx_or_interaction.followup.send(error_msg)
                else:
                    await ctx_or_interaction.send(error_msg)
            except:
                pass

    # ==================== PREFIX ANIMAL COMMANDS ====================
    @commands.command(name='cat', aliases=['kitten', 'meow', 'kitty'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_cat(self, ctx):
        """Get a cute cat image! 🐱"""
        await self._send_animal(ctx, 'cat')

    @commands.command(name='dog', aliases=['doggo', 'woof', 'puppy', 'pupper'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_dog(self, ctx):
        """Get an adorable dog image! 🐕"""
        await self._send_animal(ctx, 'dog')

    @commands.command(name='fox', aliases=['fennec', 'vulpes', 'foxy'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_fox(self, ctx):
        """Get a foxy fox image! 🦊"""
        await self._send_animal(ctx, 'fox')

    @commands.command(name='duck', aliases=['quack', 'mallard', 'birdie'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_duck(self, ctx):
        """Get a cute duck image! 🦆"""
        await self._send_animal(ctx, 'duck')

    @commands.command(name='rabbit', aliases=['bunny', 'hare', 'cottontail'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_rabbit(self, ctx):
        """Get a fluffy rabbit image! 🐰"""
        await self._send_animal(ctx, 'rabbit')

    @commands.command(name='raccoon', aliases=['trash-panda', 'bandit', 'coon'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_raccoon(self, ctx):
        """Get a clever raccoon image! 🦝"""
        await self._send_animal(ctx, 'raccoon')

    @commands.command(name='owl', aliases=['owlie', 'hoot', 'birb'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_owl(self, ctx):
        """Get a wise owl image! 🦉"""
        await self._send_animal(ctx, 'owl')

    @commands.command(name='penguin', aliases=['tux', 'waddle', 'arctic'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_penguin(self, ctx):
        """Get a fancy penguin image! 🐧"""
        await self._send_animal(ctx, 'penguin')

    @commands.command(name='panda', aliases=['bamboo', 'giant', 'bear-cat'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_panda(self, ctx):
        """Get a gentle panda image! 🐼"""
        await self._send_animal(ctx, 'panda')

    @commands.command(name='koala', aliases=['eucalyptus', 'fuzzy', 'aussie'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_koala(self, ctx):
        """Get a sleepy koala image! 🐨"""
        await self._send_animal(ctx, 'koala')

    @commands.command(name='sloth', aliases=['slow', 'lazy', 'hanging'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_sloth(self, ctx):
        """Get a chill sloth image! 🦥"""
        await self._send_animal(ctx, 'sloth')

    @commands.command(name='hedgehog', aliases=['spiky', 'hedge', 'sonic'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_hedgehog(self, ctx):
        """Get a spiky hedgehog image! 🦔"""
        await self._send_animal(ctx, 'hedgehog')

    @commands.command(name='otter', aliases=['otter-pop', 'river', 'sea-otter'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_otter(self, ctx):
        """Get a playful otter image! 🦦"""
        await self._send_animal(ctx, 'otter')

    @commands.command(name='squirrel', aliases=['nutty', 'fluffy', 'acorn'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_squirrel(self, ctx):
        """Get a nutty squirrel image! 🐿️"""
        await self._send_animal(ctx, 'squirrel')

    @commands.command(name='deer', aliases=['fawn', 'stag', 'doe'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_deer(self, ctx):
        """Get a graceful deer image! 🦌"""
        await self._send_animal(ctx, 'deer')

    @commands.command(name='bear', aliases=['ursine', 'grizzly', 'panda-uncle'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_bear(self, ctx):
        """Get a mighty bear image! 🐻"""
        await self._send_animal(ctx, 'bear')

    @commands.command(name='wolf', aliases=['dire', 'pup', 'howler'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_wolf(self, ctx):
        """Get a fierce wolf image! 🐺"""
        await self._send_animal(ctx, 'wolf')

    @commands.command(name='eagle', aliases=['hawk', 'falcon', 'bird-king'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_eagle(self, ctx):
        """Get a majestic eagle image! 🦅"""
        await self._send_animal(ctx, 'eagle')

    @commands.command(name='dolphin', aliases=['porpoise', 'swimmer', 'aqua-friend'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_dolphin(self, ctx):
        """Get a smart dolphin image! 🐬"""
        await self._send_animal(ctx, 'dolphin')

    @commands.command(name='animal', aliases=['random-animal', 'randomanimal', 'pets', 'random'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cmd_random_animal(self, ctx):
        """Get a random animal image! 🎲"""
        animal_name = random.choice(list(self.animal_facts.keys()))
        await self._send_animal(ctx, animal_name)

    # ==================== SLASH COMMANDS ====================
    @discord.app_commands.command(name='cat', description='🐱 Get a random cat image')
    @discord.app_commands.checks.cooldown(1, 2, key=lambda i: (i.user.id))
    async def slash_cat(self, interaction: discord.Interaction):
        """Get a cute cat image! 🐱"""
        await self._send_animal(interaction, 'cat')

    @discord.app_commands.command(name='dog', description='🐕 Get a random dog image')
    @discord.app_commands.checks.cooldown(1, 2, key=lambda i: (i.user.id))
    async def slash_dog(self, interaction: discord.Interaction):
        """Get an adorable dog image! 🐕"""
        await self._send_animal(interaction, 'dog')

    @discord.app_commands.command(name='animal', description='🎲 Get a random animal image')
    @discord.app_commands.checks.cooldown(1, 2, key=lambda i: (i.user.id))
    async def slash_random_animal(self, interaction: discord.Interaction):
        """Get a random animal image! 🎲"""
        animal_name = random.choice(list(self.animal_facts.keys()))
        await self._send_animal(interaction, animal_name)

    @discord.app_commands.command(name='animals-list', description='📋 Show all available animals')
    async def slash_animals_list(self, interaction: discord.Interaction):
        """Show all available animals"""
        try:
            animals = sorted(self.animal_facts.keys())
            # Split into chunks for readability
            chunks = [animals[i:i+5] for i in range(0, len(animals), 5)]
            description = "\n".join([f"🐾 {', '.join(f'`{a}`' for a in chunk)}" for chunk in chunks])
            
            embed = discord.Embed(
                title="🐾 Available Animals",
                description=f"Total: **{len(animals)}** animals\n\n{description}",
                color=discord.Color.blue()
            )
            embed.add_field(name="💡 Tip", value="Use `/animal` for random, or `/cat`, `/dog` for specific animals!", inline=False)
            embed.set_footer(text="AnimalVerse v2.2 🐾")
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            logger.error(f"Error in animals_list: {e}")
            await interaction.response.send_message("❌ Failed to show animals list.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Animals(bot))
