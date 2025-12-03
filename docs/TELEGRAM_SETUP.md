# 🤖 Telegram Bot Setup Guide

## Overview
This guide will help you set up a Telegram bot to receive daily backup files automatically.

## Step 1: Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Start a chat and send `/newbot`
3. Follow the instructions:
   - Choose a name for your bot (e.g., "Date Factory Manager")
   - Choose a username (must end with 'bot', e.g., "date_factory_bot")
4. **BotFather will give you a TOKEN** - Copy this token!
   - Example: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

## Step 2: Get Your Chat ID

1. Search for **@userinfobot** on Telegram
2. Start a chat with it
3. It will send you your **Chat ID** - Copy this number!
   - Example: `987654321`

## Step 3: Configure the Application

### Option A: Using Environment Variables (Recommended)

**Windows (PowerShell):**
```powershell
$env:TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
$env:TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"
```

**Windows (Command Prompt):**
```cmd
set TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
set TELEGRAM_CHAT_ID=YOUR_CHAT_ID_HERE
```

### Option B: Edit the Code Directly

Open `cloud_upload.py` and replace:
```python
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID_HERE')
```

With your actual values:
```python
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '123456789:ABCdefGHIjklMNOpqrsTUVwxyz')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '987654321')
```

## Step 4: Test the Setup

Run the test script:
```bash
python cloud_upload.py
```

If configured correctly, you should receive a test file on Telegram!

## Step 5: Start the Application

Once configured, restart your Flask application:
```bash
python app.py
```

The application will now:
- ✅ Create a backup every day at 11:59 PM
- ✅ Send the backup file to your Telegram automatically
- ✅ Keep the last 30 days of backups locally

## Troubleshooting

### "Telegram bot token not configured!"
- Make sure you've set the environment variables or edited the code
- Restart your terminal/PowerShell after setting environment variables

### "Telegram error: Unauthorized"
- Check that your bot token is correct
- Make sure there are no extra spaces in the token

### "Chat not found"
- Verify your Chat ID is correct
- Make sure you've started a conversation with your bot first (send `/start` to your bot)

## Security Notes

⚠️ **Never share your bot token publicly!**
- Don't commit it to Git
- Don't share screenshots containing it
- If exposed, use @BotFather to revoke and create a new token

## Alternative: Google Drive

If you prefer Google Drive instead of Telegram, you can:
1. Use the Google Drive API (requires more setup)
2. Or manually download backups from the `backups/` folder and upload to Drive

The Telegram method is recommended for its simplicity and instant notifications.
