import os
from telegram import Bot
from telegram.error import TelegramError
import asyncio

# Configuration - You need to set these values
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID_HERE')

async def send_file_to_telegram(file_path, caption=None):
    """
    Send a file to Telegram
    
    Args:
        file_path: Path to the file to send
        caption: Optional caption for the file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if TELEGRAM_BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
            print("⚠️ Telegram bot token not configured!")
            print("📝 To enable Telegram upload:")
            print("   1. Create a bot with @BotFather on Telegram")
            print("   2. Get your bot token")
            print("   3. Get your chat ID (use @userinfobot)")
            print("   4. Set environment variables:")
            print("      - TELEGRAM_BOT_TOKEN=your_token")
            print("      - TELEGRAM_CHAT_ID=your_chat_id")
            return False
        
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        with open(file_path, 'rb') as file:
            await bot.send_document(
                chat_id=TELEGRAM_CHAT_ID,
                document=file,
                caption=caption or f"📊 Date Factory Backup - {os.path.basename(file_path)}"
            )
        
        print(f"✅ File sent to Telegram successfully: {file_path}")
        return True
        
    except TelegramError as e:
        print(f"❌ Telegram error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error sending file: {e}")
        return False

def upload_backup(file_path):
    """
    Synchronous wrapper for sending backup to Telegram
    """
    try:
        asyncio.run(send_file_to_telegram(file_path))
    except Exception as e:
        print(f"❌ Upload failed: {e}")

if __name__ == '__main__':
    # Test upload
    print("Testing Telegram upload...")
    print("This will fail if you haven't configured the bot token and chat ID")
    
    # Create a test file
    test_file = 'test_upload.txt'
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write('This is a test file from Date Factory Manager')
    
    upload_backup(test_file)
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
