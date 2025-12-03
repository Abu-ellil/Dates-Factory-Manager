"""
Test script to verify and regenerate license keys
"""
import license_manager
import json
import base64

# Get current machine ID
machine_id = license_manager.get_machine_id()
print(f"Current Machine ID: {machine_id}")
print()

# Test the license key you provided
test_key = "eyJtaWQiOiAiMUFFRC03Q0FBLUQ1N0YtOTkzRSIsICJuYW1lIjogIm1hcyIsICJleHAiOiAiMjAyNS0xMi00In0=.254CBDE5C6BCED86"

print("Testing provided license key:")
print(f"Key: {test_key}")

# Decode the payload to see what's inside
try:
    payload_str = test_key.split(".")[0]
    signature = test_key.split(".")[1]
    payload = json.loads(base64.b64decode(payload_str).decode())
    print(f"Decoded payload: {json.dumps(payload, indent=2)}")
    print(f"Provided signature: {signature}")
except Exception as e:
    print(f"Error decoding: {e}")

print()

# Verify the key
is_valid, message = license_manager.verify_license_key(test_key, machine_id)
print(f"Verification result: {is_valid}")
print(f"Message: {message}")
print()

# Generate a new correct license key for this machine
print("Generating new license key for this machine:")
new_key = license_manager.generate_license_key(
    machine_id=machine_id,
    client_name="mas",
    expiration_date="2025-12-04"
)
print(f"New License Key: {new_key}")
print()

# Verify the new key
is_valid, message = license_manager.verify_license_key(new_key, machine_id)
print(f"New key verification: {is_valid}")
print(f"Message: {message}")
print()

# Save the new key
if is_valid:
    license_manager.save_license(new_key)
    print("✓ New license key saved to license.key")
