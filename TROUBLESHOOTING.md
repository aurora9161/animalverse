# 🐛 AnimalVerse Troubleshooting Guide

## 😱 Quick Fix Checklist

Try these first:

1. **Restart the bot**
   ```bash
   # Press Ctrl+C to stop
   python main.py
   ```

2. **Check Python version**
   ```bash
   python --version  # Should be 3.8+
   ```

3. **Reinstall dependencies**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

4. **Verify bot is online**
   - Check Discord - bot should show as "Online"
   - If offline, check terminal for errors

---

## 👍 Common Issues & Fixes

### Bot Offline / Crashing

**Symptoms:**
- Bot shows as offline in Discord
- Terminal shows errors
- `!help` doesn't work

**Fixes:**

1. **Check Discord token:**
   ```bash
   # .env file
   DISCORD_TOKEN=your_actual_token_here
   # NOT: DISCORD_TOKEN=
   ```

2. **Verify token is correct:**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Select your application
   - Copy token again (maybe it expired)
   - Update `.env`
   - Restart bot

3. **Check for Python errors:**
   ```bash
   python main.py 2>&1 | head -50
   ```
   Look for error messages.

4. **Verify cogs directory exists:**
   ```bash
   ls -la cogs/
   # Should show: __init__.py, animals.py, daily.py, info.py
   ```

5. **Check file permissions:**
   ```bash
   chmod 755 cogs/
   chmod 644 cogs/*.py
   ```

---

### Commands Not Working

**Symptoms:**
- `!help` gives error
- `!cat` gives error
- Commands are ignored

**Fixes:**

1. **Wrong prefix?**
   ```bash
   # Default is !
   # Check .env for correct prefix
   BOT_PREFIX=!
   ```

2. **Verify bot has permissions:**
   - Right-click channel → Permissions
   - Find bot role
   - Enable: Send Messages, Embed Links

3. **Cogs not loading?**
   - Check terminal for loading messages
   - Should show: "✅ Loaded cog: animals.py"
   - If not, check Python syntax errors

4. **Slash commands not appearing?**
   - Wait 10 seconds after bot joins
   - Try typing `/` in chat
   - If still missing, restart bot

---

### Animal Images Not Showing

**Symptoms:**
- `!cat` shows embed with no image
- "Could not fetch image" error
- Black image placeholder

**Fixes:**

1. **API is down (temporary):**
   - Fallback images should appear
   - Wait a moment and retry
   - Check terminal for "API error" messages

2. **No internet connection:**
   - Verify server has internet access
   - Test: `ping google.com`
   - Check firewall settings

3. **API key issues:**
   - API keys are OPTIONAL
   - Leave them blank to use fallback images
   - Fallback images are high-quality!

4. **Timeout issues:**
   - Each API has 5-second timeout
   - If API is slow, fallback used
   - This is normal and expected

**Verify fallback is working:**
```bash
# Check fallback images in logs
python main.py
# Should show fallback URLs when API fails
```

---

### Daily Animals Not Sending

**Symptoms:**
- Daily disabled: `!daily` → "Enabled: No"
- Not sending at scheduled time
- `!daily test` shows error

**Fixes:**

1. **Enable daily animals:**
   ```
   !daily channel #animals
   !daily time 08:00
   !daily enable
   ```

2. **Channel not set:**
   ```
   !daily
   # Should show: "Channel: #channel-name"
   ```
   If not:
   ```
   !daily channel #animals-channel
   ```

3. **Bot doesn't have permissions:**
   - Right-click channel → Permissions
   - Find bot role
   - Enable "Send Messages" and "Embed Links"

4. **Wrong time format:**
   ```
   !daily time 08:00   # Correct (24-hour)
   !daily time 8am     # Wrong
   !daily time 8:00am  # Wrong
   ```

5. **Test if it works:**
   ```
   !daily test
   ```
   Should send a test message immediately.

6. **Check logs for errors:**
   ```bash
   python main.py
   # Look for: "Error in daily animal for guild"
   ```

---

### Bot Lag / Slow Response

**Symptoms:**
- Commands take 5+ seconds to respond
- `!cat` takes very long
- Bot seems frozen

**Fixes:**

1. **Check API latency:**
   - API timeouts are 5 seconds
   - If API is slow, will wait full 5 seconds
   - This is normal!

2. **Reduce bot load:**
   ```
   # Too many daily notifications?
   !daily disable  # Temporarily
   ```

3. **Check database size:**
   ```bash
   ls -lh data/
   # If files are huge (>100MB), something is wrong
   ```

4. **Monitor resource usage:**
   ```bash
   # Linux/Mac
   top -p $(pgrep -f "python main.py")
   
   # Windows
   tasklist /v | grep python
   ```

---

### Database Issues

**Symptoms:**
- `!stats` shows no data
- Guild settings disappeared
- "Permission Error" when using !daily

**Fixes:**

1. **Verify database files exist:**
   ```bash
   ls -la data/
   # Should show: guild_settings.json, user_stats.json
   ```

2. **Check file permissions:**
   ```bash
   chmod 644 data/*.json
   chmod 755 data/
   ```

3. **Backup and reset database:**
   ```bash
   cp -r data/ data.backup/
   rm data/*.json
   # Bot will recreate on next run
   python main.py
   ```

4. **Verify JSON is valid:**
   ```bash
   python -m json.tool data/guild_settings.json
   # Should not show errors
   ```

---

### Permission Errors

**Symptoms:**
- "Bot missing permissions" errors
- Can't set daily channel
- `!daily test` fails

**Fixes:**

1. **Check server permissions:**
   - Right-click bot → Manage Member
   - Assign admin role
   - Or manually enable permissions

2. **Check channel permissions:**
   - Right-click channel → Permissions
   - Find bot role
   - Enable all needed permissions

3. **Verify bot role position:**
   - Bot role must be ABOVE target channel's role
   - Server Settings → Roles
   - Drag bot role higher

4. **Specific permissions needed:**
   - Send Messages
   - Embed Links
   - Read Message History
   - (Add Reactions - optional)

---

### Slash Commands Issues

**Symptoms:**
- `/animal` doesn't appear
- "/" shows no suggestions
- Slash commands not working

**Fixes:**

1. **Wait for bot to sync:**
   - After bot starts, wait 10 seconds
   - Slash commands sync automatically

2. **Manual resync:**
   ```bash
   # Restart bot
   python main.py
   ```

3. **Check bot has "applications.commands" scope:**
   - [Discord Developer Portal](https://discord.com/developers/applications)
   - Select app → OAuth2 → Scopes
   - Check "applications.commands"

4. **Verify bot permissions:**
   - Bot needs "Use Slash Commands" permission
   - Usually enabled by default

---

## 📣 Error Messages Explained

### "discord.ext.commands.CommandNotFound"
**Meaning:** Command not recognized
**Fix:** Check spelling, correct prefix

### "discord.errors.Forbidden"
**Meaning:** Bot doesn't have permission
**Fix:** Give bot required permissions

### "asyncio.TimeoutError"
**Meaning:** API took too long (>5s)
**Fix:** Automatic - fallback image used

### "aiohttp.ClientError"
**Meaning:** Network/API connection error
**Fix:** Automatic - fallback image used

### "json.JSONDecodeError"
**Meaning:** Database file corrupted
**Fix:** Reset database (see above)

### "discord.errors.HTTPException"
**Meaning:** Discord API error
**Fix:** Usually temporary - retry

---

## 📌 Log Analysis

**To view detailed logs:**
```bash
python main.py 2>&1 | tee bot.log
# Logs saved to bot.log
```

**Look for:**
- "✅ Loaded cog" = Good
- "❌ Failed to load" = Problem
- "Error fetching cat" = API issue (OK)
- "Error in daily loop" = Daily feature issue

---

## 🐛 Report a Bug

If none of the above fixes work:

1. **Collect information:**
   ```bash
   python --version
   pip list | grep discord
   python main.py 2>&1 | head -100
   ```

2. **Create GitHub Issue:**
   - Go to [AnimalVerse Issues](https://github.com/aurora9161/animalverse/issues)
   - Click "New Issue"
   - Describe problem
   - Paste logs/errors
   - System info (OS, Python version)

3. **Include:**
   - Error message (full text)
   - Command that triggered it
   - When it happens
   - Python version
   - OS (Windows/Mac/Linux)

---

## 🔓 Getting Help

**Documentation:**
- 📖 [README.md](README.md) - Overview
- 🔧 [CONFIGURATION.md](CONFIGURATION.md) - Setup & Config
- 🐛 [This file](TROUBLESHOOTING.md) - Troubleshooting

**Community:**
- GitHub Issues - Bug reports
- GitHub Discussions - General help
- Code comments - How things work

---

**Made with ❤️ by aurora9161**

*Last updated: December 2025*
