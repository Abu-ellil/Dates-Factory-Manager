import platform
import uuid
import hashlib
import hmac
import base64
import json
import os
from datetime import datetime

# SECRET KEY - CHANGE THIS FOR YOUR PRODUCTION RELEASE!
# This key is used to sign the licenses. Keep it safe.
SECRET_KEY = b"DATE_FACTORY_MANAGER_SECRET_KEY_2025_SECURE"

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
        
        if signature != expected_signature:
            return False, "Invalid signature"
            
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

def save_license(license_key):
    """Saves the license key to a file."""
    with open("license.key", "w") as f:
        f.write(license_key)

def load_license():
    """Loads the license key from file."""
    if os.path.exists("license.key"):
        with open("license.key", "r") as f:
            return f.read().strip()
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
