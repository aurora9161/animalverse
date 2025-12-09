# 🔧 AnimalVerse Configuration Guide

## 🐾 API Keys - Optional or Required?

### 🐳 Answer: **COMPLETELY OPTIONAL!**

✅ **The bot works perfectly fine WITHOUT any API keys!**

- **Cats API Key:** Optional
- **Dogs API Key:** Optional
- **All other animals:** No key needed (uses Unsplash/fallback images)

---

## 🎯 Environment Setup

### Step 1: Copy Environment Template

```bash
cp .env.example .env
```

### Step 2: Add Discord Token (REQUIRED)

```env
DISCORD_TOKEN=your_discord_bot_token_here
```

**Get your token:**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" tab and click "Add Bot"
4. Copy the token under "TOKEN"

### Step 3: (Optional) Add API Keys

If you want premium quality cat/dog images, you can add API keys:

#### Cat API Key (Optional)

```env
CATS_API_KEY=your_cat_api_key
```

**Get your key:**
1. Visit [thecatapi.com](https://thecatapi.com/)
2. Sign up for free
3. Get your API key from the dashboard
4. Add to `.env`

**Benefits:**
- Higher quality cat images
- Premium image collections

#### Dog API Key (Optional)

```env
DOGS_API_KEY=your_dog_api_key
```

**Get your key:**
1. Visit [thedogapi.com](https://thedogapi.com/)
2. Sign up for free
3. Get your API key from the dashboard
4. Add to `.env`

**Benefits:**
- Higher quality dog images
- Breed-specific filtering (future feature)

---

## 🎨 What Happens Without API Keys?

### Without Cats API Key:
- ✅ Still shows random cat images
- ✅ Uses high-quality Unsplash fallback images
- ✅ 100% functional
- ❌ May not have the absolute latest images

### Without Dogs API Key:
- ✅ Still shows random dog images
- ✅ Uses high-quality Unsplash fallback images
- ✅ 100% functional
- ❌ May not have the absolute latest images

### Without Any API Keys:
- ✅ **ALL commands work perfectly**
- ✅ **All 19 animals available**
- ✅ **Daily animals work**
- ✅ **Statistics work**
- ✅ **Nothing is broken**
- ✅ **Just uses fallback Unsplash images**

---

## 📁 Fallback Image System

Every animal has **backup Unsplash images** cached:

```python
FALLBACK_IMAGES = {
    'cat': [5+ high-quality cat images],
    'dog': [5+ high-quality dog images],
    'fox': [3+ high-quality fox images],
    ... 19 animals total
}
```

**Fallback triggers:**
1. API key not provided
2. API is down
3. API timeout (5 second limit)
4. Rate limit exceeded
5. Network error

**Result:** Always shows an image!

---

## 🔐 Bot Permissions Required

For the bot to work properly, give it these Discord permissions:

- ✅ Send Messages
- ✅ Embed Links
- ✅ Attach Files
- ✅ Read Message History
- ✅ Add Reactions (optional)

**In Discord:**
1. Right-click bot → Manage Member
2. Assign a role with these permissions
3. Or manually set permissions in channel settings

---

## 📅 Daily Animals Configuration

### Setup Steps

1. **Set Channel:**
   ```
   !daily channel #animal-updates
   ```

2. **Set Time (24-hour format):**
   ```
   !daily time 08:00    # 8 AM
   !daily time 14:30    # 2:30 PM
   !daily time 23:59    # 11:59 PM
   ```

3. **Select Animals (Optional):**
   ```
   !daily animals set cat dog fox
   !daily animals clear    # Use all animals
   ```

4. **Enable:**
   ```
   !daily enable
   ```

5. **Test:**
   ```
   !daily test
   ```

### View Settings

```
!daily
```

Shows current configuration.

---

## 💾 Database System

### Location

All data stored in `data/` directory:

```
data/
├── guild_settings.json    # Per-guild configs
├── user_stats.json        # User statistics
└── ...
```

### Manual Backup

1. **Backup before updating:**
   ```bash
   cp -r data/ data.backup/
   ```

2. **Restore if needed:**
   ```bash
   rm -r data/
   cp -r data.backup/ data/
   ```

### View Guild Settings

```json
// data/guild_settings.json
{
  "123456789": {
    "daily_animal_enabled": true,
    "daily_animal_channel": 987654321,
    "daily_animal_hour": 8,
    "daily_animal_minute": 0,
    "daily_animal_time": "08:00",
    "animal_types": ["cat", "dog", "fox"],
    "last_daily_animal": "2025-12-09",
    "created_at": "2025-12-09T12:00:00"
  }
}
```

### View User Stats

```json
// data/user_stats.json
{
  "203395068": {
    "commands": {
      "cat": 5,
      "dog": 3,
      "animal": 2
    },
    "favorite_animals": {
      "cat": 5,
      "dog": 3,
      "fox": 1
    }
  }
}
```

---

## 🔍 Troubleshooting

### Bot doesn't respond to commands

**Check:**
1. Bot is online (Discord shows it as active)
2. Bot has Send Messages permission
3. Correct prefix is being used (`!` by default)
4. Check Python terminal for errors

**Fix:**
```bash
python main.py
```

### API errors in logs

**Common:**
- "Cat API error: timeout" → API is slow, fallback used
- "Fox API error: 503" → API is down, fallback used
- "Duck API error: connection" → Network issue, fallback used

**Resolution:**
- All errors are handled gracefully
- Fallback images automatically used
- No action needed!

### Daily animals not sending

**Check:**
1. Daily enabled: `!daily` → "Enabled" should be "Yes"
2. Channel set: `!daily` → Should show channel
3. Time is correct: `!daily` → Should show time
4. Bot has permissions in channel

**Test:**
```
!daily test
```

If test sends, daily is configured correctly.

### Stats not tracking

**Usually works automatically.**

If not:
1. Check `data/user_stats.json` exists
2. Check file permissions
3. Restart bot

---

## 🛠️ Advanced Configuration

### Change Bot Prefix

1. Edit `.env`:
   ```env
   BOT_PREFIX=?
   ```

2. Restart bot

3. New prefix is `?`

### Disable Daily Notifications

Per-guild:
```
!daily disable
```

Temporary:
```
!daily disable
!daily enable
```

### Multiple Bots

1. Create separate `.env` files (not recommended)
2. Or use different Discord tokens in same `.env`
3. Each bot gets own `data/` directory

---

## 📚 Complete .env Template

```env
# ==================== REQUIRED ====================
# Your Discord bot token
DISCORD_TOKEN=your_token_here

# ==================== OPTIONAL ====================
# Bot prefix (default is !)
BOT_PREFIX=!

# Cat API key (optional - bot works without it)
CATS_API_KEY=

# Dog API key (optional - bot works without it)
DOGS_API_KEY=
```

---

## ✅ Verification Checklist

Before running the bot:

- [ ] `.env` file created
- [ ] `DISCORD_TOKEN` is filled in
- [ ] Bot added to test server
- [ ] Bot has required permissions
- [ ] Python 3.8+ installed
- [ ] `pip install -r requirements.txt` run
- [ ] `python main.py` starts without errors
- [ ] `!help` command works

---

## 📧 Need Help?

- 📖 Check README.md for commands
- 🐛 Report bugs on GitHub Issues
- 💬 Ask in GitHub Discussions
- 📚 Review code comments in `cogs/`

---

**Made with ❤️ by aurora9161**
