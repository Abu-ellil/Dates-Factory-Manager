"""
Secure configuration management for Date Factory Manager
Handles environment variables and secure defaults
"""
import os
from datetime import datetime
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    import sys
    
    # Determine base directory
    if getattr(sys, 'frozen', False):
        # If running as compiled exe, look in the temporary folder (sys._MEIPASS)
        # AND the executable folder
        base_dir = Path(sys._MEIPASS)
        exe_dir = Path(sys.executable).parent
        
        # Try loading from temp folder first (bundled file)
        dotenv_path = base_dir / '.env'
        if dotenv_path.exists():
            load_dotenv(dotenv_path)
            
        # Also try loading from executable folder (if user provided one)
        dotenv_local = exe_dir / '.env'
        if dotenv_local.exists():
            load_dotenv(dotenv_local, override=True)
    else:
        # Running as script
        base_dir = Path(__file__).resolve().parent
        dotenv_path = base_dir / '.env'
        if dotenv_path.exists():
            load_dotenv(dotenv_path)
except ImportError:
    # python-dotenv not installed, will use system environment variables only
    pass


def get_app_data_dir():
    """Get the application data directory in AppData"""
    app_data = os.getenv('APPDATA')
    if not app_data:
        app_data = os.path.expanduser('~')
    
    data_dir = os.path.join(app_data, 'DateFactoryManager')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    return data_dir

def get_exports_dir():
    """Get the exports directory in User Documents"""
    try:
        docs_dir = os.path.join(os.path.expanduser('~'), 'Documents')
        exports_dir = os.path.join(docs_dir, 'Date Factory Manager', 'Exports')
        if not os.path.exists(exports_dir):
            os.makedirs(exports_dir, exist_ok=True)
        return exports_dir
    except Exception as e:
        print(f"ERROR in get_exports_dir(): {e}")
        # If Documents directory is not accessible, try current directory
        exports_dir = os.path.join(os.getcwd(), 'exports')
        if not os.path.exists(exports_dir):
            os.makedirs(exports_dir, exist_ok=True)
        return exports_dir

def get_backups_dir():
    """Get the backups directory in User Documents"""
    docs_dir = os.path.join(os.path.expanduser('~'), 'Documents')
    backups_dir = os.path.join(docs_dir, 'Date Factory Manager', 'Backups')
    if not os.path.exists(backups_dir):
        os.makedirs(backups_dir, exist_ok=True)
    return backups_dir

class Config:
    """Application configuration with secure defaults"""
    
    # Data Directory
    DATA_DIR = get_app_data_dir()
    EXPORTS_DIR = get_exports_dir()
    BACKUPS_DIR = get_backups_dir()
    
    # Security Settings
    # HARDCODED KEYS FOR PRODUCTION STABILITY
    # This ensures the license key matches regardless of environment variables
    SECRET_KEY = "DateFactory2025SecureProductionKey!@#"
    
    # License Management
    # This MUST match the key used in generate_license.py
    LICENSE_SECRET_KEY = "DateFactoryLicense2025FixedKey!@#$%"

    # Database Configuration
    DATABASE_PATH = os.environ.get('DATABASE_PATH', os.path.join(DATA_DIR, 'date_factory.db'))

    # Flask Configuration
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')
    
    # Security Headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'"
    }
    
    # Application Settings
    APP_NAME = "Date Factory Manager"
    APP_VERSION = "1.0.0"
    
    # Backup Configuration
    BACKUP_RETENTION_DAYS = int(os.environ.get('BACKUP_RETENTION_DAYS', '30'))
    
    @staticmethod
    def is_production():
        """Check if running in production environment"""
        return Config.FLASK_ENV.lower() == 'production'
    
    @staticmethod
    def get_license_secret_key():
        """Get the secret key for license signing (bytes)"""
        return Config.LICENSE_SECRET_KEY.encode() if isinstance(Config.LICENSE_SECRET_KEY, str) else Config.LICENSE_SECRET_KEY

# Validate required environment variables for production
if Config.is_production():
    required_env_vars = ['SECRET_KEY', 'LICENSE_SECRET_KEY']
    missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"ERROR: Missing required environment variables for production: {missing_vars}")
        print("Please set these variables before running in production mode.")
        
# Export config instance for easy import
config = Config()
