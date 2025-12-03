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
    # Get the directory where this config file is located
    basedir = Path(__file__).resolve().parent
    dotenv_path = basedir / '.env'
    if dotenv_path.exists():
        load_dotenv(dotenv_path)
except ImportError:
    # python-dotenv not installed, will use system environment variables only
    pass


class Config:
    """Application configuration with secure defaults"""
    
    # Security Settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        # Generate a secure random key for this session
        # In production, this should always come from environment variables
        import secrets
        SECRET_KEY = secrets.token_urlsafe(32)
        print("WARNING: Using generated SECRET_KEY. Set SECRET_KEY environment variable in production!")

    # Database Configuration
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'date_factory.db')

    # Flask Configuration
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')

    # License Management
    LICENSE_SECRET_KEY = os.environ.get('LICENSE_SECRET_KEY')
    if not LICENSE_SECRET_KEY:
        # Use SECRET_KEY as fallback for license signing
        LICENSE_SECRET_KEY = SECRET_KEY
        print("WARNING: Using SECRET_KEY for license signing. Set LICENSE_SECRET_KEY in production!")
        # For development, use a fixed key to avoid signature issues
        if FLASK_ENV.lower() != 'production':
            LICENSE_SECRET_KEY = "test_secret_key_12345"
            print("INFO: Using fixed development license key")
    
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
