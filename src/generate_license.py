"""
License Key Generator for Date Factory Manager
Use this script to generate valid license keys for clients
"""
import license_manager
import sys
from datetime import datetime, timedelta

def main():
    print("=" * 60)
    print("Date Factory Manager - License Key Generator")
    print("=" * 60)
    print()
    
    # Get current machine ID
    machine_id = license_manager.get_machine_id()
    print(f"Current Machine ID: {machine_id}")
    print()
    
    # Get client name
    client_name = input("Enter client name (default: 'User'): ").strip() or "User"
    
    # Get expiration date
    print("\nExpiration options:")
    print("1. Lifetime (no expiration)")
    print("2. 1 month")
    print("3. 6 months")
    print("4. 1 year")
    print("5. Custom date")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    expiration_date = None
    if choice == "2":
        expiration_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    elif choice == "3":
        expiration_date = (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d")
    elif choice == "4":
        expiration_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    elif choice == "5":
        expiration_date = input("Enter expiration date (YYYY-MM-DD): ").strip()
    
    print()
    print("-" * 60)
    print("Generating license key...")
    print("-" * 60)
    
    # Generate license key
    license_key = license_manager.generate_license_key(
        machine_id=machine_id,
        client_name=client_name,
        expiration_date=expiration_date
    )
    
    print(f"\nMachine ID: {machine_id}")
    print(f"Client Name: {client_name}")
    print(f"Expiration: {expiration_date if expiration_date else 'Lifetime'}")
    print()
    print("LICENSE KEY:")
    print("=" * 60)
    print(license_key)
    print("=" * 60)
    print()
    
    # Verify the key
    is_valid, message = license_manager.verify_license_key(license_key, machine_id)
    
    if is_valid:
        print("✓ License key is VALID")
        
        # Ask to save
        save = input("\nSave this license key to license.key? (y/n): ").strip().lower()
        if save == 'y':
            license_manager.save_license(license_key)
            print("✓ License key saved successfully!")
    else:
        print(f"✗ License key verification failed: {message}")
    
    print()

if __name__ == "__main__":
    main()
