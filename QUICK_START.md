# 🚀 AnimalVerse Quick Start

**Get your bot running in 5 minutes!**

---

## 📟 Step 1: Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Go to "Bot" tab → "Add Bot"
4. Under TOKEN, click "Copy"
5. Keep this token safe!

---

## 💾 Step 2: Setup Bot Files

```bash
# Clone repo
git clone https://github.com/aurora9161/animalverse.git
cd animalverse

# Create environment file
cp .env.example .env

# Edit .env and paste your token
# DISCORD_TOKEN=your_token_here
```

---

## 📻 Step 3: Install & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run bot
python main.py
```

**You should see:**
```
✅ Bot is online as YourBotName
📱 Loaded cog: animals.py
📱 Loaded cog: daily.py
📱 Loaded cog: info.py
🔄 Synced X slash commands
```

---

## 🐾 Step 4: Invite Bot to Server

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your application
3. Go to OAuth2 → URL Generator
4. Select scopes:
   - `bot`
   - `applications.commands`
5. Select permissions:
   - Send Messages
   - Embed Links
   - Read Message History
6. Copy generated URL
7. Paste in browser
8. Select your server
9. Click Authorize

---

## 🏓 Step 5: Test Commands

In your Discord server:

```
!help                    # Show all commands
!cat                     # Get a cat image
!dog                     # Get a dog image
!animal                  # Get random animal
/animal                  # Slash version
!stats                   # Your statistics
```

**You should see beautiful animal images!** 🐾

---

## 📅 Step 6: Setup Daily Animals (Optional)

```
!daily channel #animals         # Set channel
!daily time 08:00               # Set time (8 AM)
!daily enable                   # Enable
!daily test                     # Send test
```

Now you'll get a daily animal at 8 AM!

---

## ❓ API Keys? Optional!

**The bot works WITHOUT any API keys!**

To add API keys (optional):
1. Get free key from [thecatapi.com](https://thecatapi.com/)
2. Get free key from [thedogapi.com](https://thedogapi.com/)
3. Add to `.env`:
   ```
   CATS_API_KEY=your_key
   DOGS_API_KEY=your_key
   ```

---

## 📝 All Commands

### Animal Commands
```
!cat !dog !fox !duck !rabbit !raccoon !owl !penguin
!panda !koala !sloth !hedgehog !otter !squirrel !deer
!bear !wolf !eagle !dolphin
```

### Utility
```
!help                  # Show this
!botinfo              # Bot information
!ping                 # Check latency
!stats                # Your stats
!serverinfo           # Server info
```

### Daily Setup
```
!daily                           # Show settings
!daily enable / disable          # Toggle
!daily channel #channel          # Set channel
!daily time HH:MM                # Set time
!daily animals set cat dog       # Select animals
!daily animals clear             # Use all
!daily test                      # Send test
```

---

## 🐛 Issues?

**Check these first:**

1. Bot is online (check Discord)
2. Bot has Send Messages permission
3. Using correct prefix (`!` by default)
4. Python is running (check terminal)

**For detailed help:**
- 📖 [README.md](README.md) - Full overview
- 🔧 [CONFIGURATION.md](CONFIGURATION.md) - Advanced setup
- 🐛 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Fix issues

---

## 🌟 Next Steps

- ✅ Invite more people to test
- ✅ Setup daily animals
- ✅ Check `!stats` to see usage
- ✅ Add optional API keys for better images
- ✅ Star the repo! ⭐

---

## 📞 Need Help?

- GitHub Issues: https://github.com/aurora9161/animalverse/issues
- Check TROUBLESHOOTING.md for common problems
- Review code comments in `cogs/`

---

**That's it! Your bot is ready!** 🎉

**Made with ❤️ by aurora9161**
