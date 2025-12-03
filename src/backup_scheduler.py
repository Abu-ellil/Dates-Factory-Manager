from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
from export import export_to_excel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_backup():
    """Create daily backup of database as Excel file"""
    try:
        # Create backups directory if it doesn't exist
        if not os.path.exists('backups'):
            os.makedirs('backups')
        
        # Generate filename with date
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f'backup_{date_str}.xlsx'
        filepath = os.path.join('backups', filename)
        
        # Export to Excel
        export_to_excel(filepath)
        
        print(f"✅ Backup created successfully: {filepath}")
        
        # Upload to Telegram
        try:
            from cloud_upload import upload_backup
            upload_backup(filepath)
        except Exception as e:
            print(f"⚠️ Telegram upload skipped: {e}")
        
        # Clean old backups (keep last 30 days)
        cleanup_old_backups()
        
        return filepath
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return None

def cleanup_old_backups(days_to_keep=30):
    """Delete backups older than specified days"""
    try:
        if not os.path.exists('backups'):
            return
        
        import time
        current_time = time.time()
        days_in_seconds = days_to_keep * 24 * 60 * 60
        
        for filename in os.listdir('backups'):
            filepath = os.path.join('backups', filename)
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getmtime(filepath)
                if file_age > days_in_seconds:
                    os.remove(filepath)
                    print(f"🗑️ Deleted old backup: {filename}")
    except Exception as e:
        print(f"⚠️ Cleanup error: {e}")

def start_scheduler():
    """Start the backup scheduler"""
    scheduler = BackgroundScheduler()
    
    # Schedule daily backup at 11:59 PM
    scheduler.add_job(
        create_backup,
        'cron',
        hour=23,
        minute=59,
        id='daily_backup'
    )
    
    scheduler.start()
    print("⏰ Backup scheduler started - Daily backup at 11:59 PM")
    
    return scheduler

if __name__ == '__main__':
    # Test backup creation
    create_backup()
