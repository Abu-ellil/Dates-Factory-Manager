"""
Test script to check what's causing the internal server error
"""
import sys
import traceback

try:
    print("Testing license check...")
    import license_manager
    
    # Check license
    is_valid = license_manager.check_license()
    print(f"License valid: {is_valid}")
    
    if is_valid:
        stored_key = license_manager.load_license()
        machine_id = license_manager.get_machine_id()
        is_valid, message = license_manager.verify_license_key(stored_key, machine_id)
        print(f"Verification: {is_valid}")
        print(f"Message: {message}")
    
    print("\nTesting Flask app import...")
    from app import app
    print("✓ App imported successfully")
    
    print("\nTesting routes...")
    with app.test_client() as client:
        # Test root
        print("Testing GET /")
        response = client.get('/')
        print(f"Status: {response.status_code}")
        if response.status_code >= 400:
            print(f"Response: {response.data.decode()[:500]}")
        
        # Test activate page
        print("\nTesting GET /activate")
        response = client.get('/activate')
        print(f"Status: {response.status_code}")
        if response.status_code >= 400:
            print(f"Response: {response.data.decode()[:500]}")
            
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
