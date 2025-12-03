import platform
import uuid
import hashlib
import hmac
import base64
import json
import os
from datetime import datetime

# Security: Secret key now managed through config.py
from config import config
SECRET_KEY = config.get_license_secret_key()

def get_machine_id():
    """
    Generates a unique ID for the current machine.
    Combines MAC address and Hostname.
    """
    mac = uuid.getnode()
    hostname = platform.node()
    system = platform.system()
    
    # Combine hardware info
    machine_info = f"{mac}-{hostname}-{system}"
    
    # Hash it to make it a nice string
    machine_id = hashlib.sha256(machine_info.encode()).hexdigest()[:16].upper()
    
    # Format as XXXX-XXXX-XXXX-XXXX
    return "-".join([machine_id[i:i+4] for i in range(0, len(machine_id), 4)])

def generate_license_key(machine_id, client_name="User", expiration_date=None):
    """
    Generates a signed license key for a specific machine ID.
    
    Args:
        machine_id (str): The unique ID of the client machine.
        client_name (str): Name of the client (optional metadata).
        expiration_date (str): 'YYYY-MM-DD' or None for lifetime.
    """
    payload = {
        "mid": machine_id,
        "name": client_name,
        "exp": expiration_date
    }
    
    # Create payload string
    payload_str = base64.b64encode(json.dumps(payload).encode()).decode()
    
    # Create signature
    signature = hmac.new(SECRET_KEY, payload_str.encode(), hashlib.sha256).hexdigest()[:16].upper()
    
    # Combine: PAYLOAD.SIGNATURE
    license_key = f"{payload_str}.{signature}"
    return license_key

def verify_license_key(license_key, machine_id):
    """
    Verifies if a license key is valid for this machine.
    
    Returns:
        tuple: (is_valid, message/payload)
    """
    try:
        if "." not in license_key:
            return False, "Invalid key format"
            
        payload_str, signature = license_key.split(".")
        
        # Verify signature
        expected_signature = hmac.new(SECRET_KEY, payload_str.encode(), hashlib.sha256).hexdigest()[:16].upper()
        
        # DEBUG LOGGING
        print(f"DEBUG: Checking Key: {license_key}")
        print(f"DEBUG: Using Secret Key (first 5 chars): {str(SECRET_KEY)[:5]}...")
        print(f"DEBUG: Expected Signature: {expected_signature}")
        print(f"DEBUG: Actual Signature:   {signature}")
        
        if signature != expected_signature:
            return False, f"Invalid signature (Expected: {expected_signature}, Got: {signature})"
            
        # Decode payload
        payload = json.loads(base64.b64decode(payload_str).decode())
        
        # Check Machine ID
        if payload["mid"] != machine_id:
            return False, "License not for this machine"
            
        # Check Expiration
        if payload["exp"]:
            exp_date = datetime.strptime(payload["exp"], "%Y-%m-%d")
            if datetime.now() > exp_date:
                return False, "License expired"
                
        return True, payload
        
    except Exception as e:
        return False, f"Error verifying key: {str(e)}"

def get_license_file_path():
    """Get the path to the license file in AppData"""
    app_data = os.getenv('APPDATA')
    if not app_data:
        app_data = os.path.expanduser('~')
    
    app_dir = os.path.join(app_data, 'DateFactoryManager')
    if not os.path.exists(app_dir):
        os.makedirs(app_dir, exist_ok=True)
        
    return os.path.join(app_dir, 'license.key')

def save_license(license_key):
    """Saves the license key to a file in AppData."""
    try:
        license_path = get_license_file_path()
        with open(license_path, "w") as f:
            f.write(license_key)
        return True
    except Exception as e:
        print(f"Error saving license: {e}")
        raise e

def load_license():
    """Loads the license key from file."""
    # 1. Try AppData (new standard location)
    try:
        license_path = get_license_file_path()
        if os.path.exists(license_path):
            with open(license_path, "r") as f:
                return f.read().strip()
    except Exception:
        pass

    # 2. Fallback: Try script directory (legacy/portable)
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        license_path = os.path.join(script_dir, "license.key")
        if os.path.exists(license_path):
            with open(license_path, "r") as f:
                return f.read().strip()
    except Exception:
        pass
    
    # 3. Fallback: Current directory
    if os.path.exists("license.key"):
        try:
            with open("license.key", "r") as f:
                return f.read().strip()
        except Exception:
            pass
    
    return None

def check_license():
    """
    Checks if a valid license exists for this machine.
    Returns True if valid, False otherwise.
    """
    stored_key = load_license()
    if not stored_key:
        return False
        
    machine_id = get_machine_id()
    is_valid, _ = verify_license_key(stored_key, machine_id)
    return is_valid
