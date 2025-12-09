# 🐾 AnimalVerse

> A delightful Discord bot that brings adorable animal images to your server!

[![Discord.py](https://img.shields.io/badge/discord.py-2.3.2-blue)](https://github.com/Rapptz/discord.py)
[![Python](https://img.shields.io/badge/python-3.8+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

## 📋 Features

✨ **Multiple Animal Categories**
- 🐱 Cats - Adorable feline friends
- 🐕 Dogs - Playful puppers and doggos
- 🦊 Foxes - Cunning and cute fox images
- 🦆 Ducks - Quacking ducks and mallards
- 🎲 Random - Get any random animal!

🎯 **Command Support**
- **Prefix Commands** - Use `!` prefix for traditional Discord commands
- **Slash Commands** - Modern `/` commands for easy interaction
- Both command types work identically with full feature parity

📚 **Fun Facts**
- Each animal image comes with an interesting fun fact
- Learn while you enjoy cute animal pictures!

🎨 **Beautiful Embeds**
- Rich Discord embeds with images and information
- Responsive design that looks great on all devices

⚙️ **Professional Architecture**
- **Cogs Structure** - Organized and modular codebase
- **Error Handling** - Graceful error management
- **Async/Await** - Full async support for performance
- **External APIs** - Integrates with multiple animal APIs

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Discord bot token (from [Discord Developer Portal](https://discord.com/developers/applications))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aurora9161/animalverse.git
   cd animalverse
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file**
   ```bash
   cp .env.example .env
   ```

4. **Configure your bot token**
   - Open `.env` file
   - Add your Discord bot token:
     ```
     DISCORD_TOKEN=your_token_here
     BOT_PREFIX=!
     ```

5. **Run the bot**
   ```bash
   python main.py
   ```

## 📖 Commands

### Animal Commands

#### Cats
- **Prefix:** `!cat`, `!kitten`, `!meow`
- **Slash:** `/cat`
- Get a random cat image with fun facts

#### Dogs
- **Prefix:** `!dog`, `!doggo`, `!woof`, `!puppy`
- **Slash:** `/dog`
- Get a random dog image with fun facts

#### Foxes
- **Prefix:** `!fox`, `!fennec`, `!vulpes`
- **Slash:** `/fox`
- Get a random fox image with fun facts

#### Ducks
- **Prefix:** `!duck`, `!quack`, `!mallard`
- **Slash:** `/duck`
- Get a random duck image with fun facts

#### Random Animal
- **Prefix:** `!animal`, `!random-animal`, `!randomanimal`
- **Slash:** `/animal`
- Get a random animal from all categories

### Utility Commands

#### Help
- **Prefix:** `!help`
- **Slash:** `/help`
- Display all available commands

#### Bot Info
- **Prefix:** `!botinfo`
- **Slash:** `/botinfo`
- Show bot statistics and information

#### Ping
- **Prefix:** `!ping`
- **Slash:** `/ping`
- Check bot latency

## 📁 Project Structure

```
animalverse/
├── main.py                 # Main bot file with initialization
├── requirements.txt        # Project dependencies
├── .env.example           # Environment variables template
├── README.md              # This file
├── LICENSE                # MIT License
└── cogs/
    ├── __init__.py        # Cogs package
    ├── animals.py         # Animal commands cog
    └── info.py            # Information commands cog
```

## 🛠️ Technologies Used

- **discord.py** - Discord bot framework
- **aiohttp** - Async HTTP client for API requests
- **python-dotenv** - Environment variable management
- **Multiple Animal APIs:**
  - The Cat API (cats)
  - The Dog API (dogs)
  - Random Fox API (foxes)
  - Random Duck API (ducks)

## 🔧 Configuration

### Environment Variables

Edit `.env` file to customize:

```env
# Discord Bot Token (Required)
DISCORD_TOKEN=your_token_here

# Bot Prefix (Default: !)
BOT_PREFIX=!

# API Keys (Optional, for future enhancements)
CATS_API_KEY=optional
DOGS_API_KEY=optional
```

## 🎯 Development

### Adding New Animal Types

1. Add a fetch function in `cogs/animals.py`:
   ```python
   async def fetch_animal_image(self):
       """Fetch random animal image"""
       # Implementation here
   ```

2. Create command methods (both prefix and slash)
3. Update help embed in `cogs/info.py`

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Use type hints where possible

## 🐛 Troubleshooting

### Bot doesn't respond
- Verify bot token is correct in `.env`
- Check bot has necessary permissions in Discord server
- Ensure bot is online (check Python terminal for errors)

### Commands not appearing
- Try `!help` to verify commands are loaded
- Wait a few seconds after bot startup for slash commands to sync
- Restart bot if slash commands don't appear

### API errors
- Some APIs may have rate limits - bot handles this gracefully
- Check internet connection
- Try again in a few moments

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙌 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new animal types
- Improve documentation
- Submit pull requests

## 🌟 Acknowledgments

- **discord.py** - Amazing Discord bot framework
- **Animal API providers** - For providing free animal images
- **You** - For using AnimalVerse!

## 📞 Support

Need help? Feel free to:
- Create an issue on GitHub
- Check existing documentation
- Review code comments and docstrings

---

**Made with ❤️ by aurora9161**

**Want to add more animals? Star the repo and suggest features!** ⭐
