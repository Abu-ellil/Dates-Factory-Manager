"""
Test the activation flow
"""
import license_manager

# Get machine ID
machine_id = license_manager.get_machine_id()
print(f"Machine ID: {machine_id}")
print()

# Load the saved license
saved_license = license_manager.load_license()
print(f"Saved License Key: {saved_license}")
print()

# Check if license is valid
is_valid = license_manager.check_license()
print(f"License Valid: {is_valid}")
print()

if is_valid:
    print("✓ ✓ ✓ APP IS ACTIVATED! ✓ ✓ ✓")
    print()
    print("You can now run the app and it should work without asking for activation.")
else:
    print("✗ License is still invalid")
    print()
    print("Verifying the saved license:")
    is_valid, message = license_manager.verify_license_key(saved_license, machine_id)
    print(f"Result: {is_valid}")
    print(f"Message: {message}")
