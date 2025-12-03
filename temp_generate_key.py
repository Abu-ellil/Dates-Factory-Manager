import sys
sys.path.append('src')
import license_manager

machine_id = '1AED-7CAA-D57F-993E'
client_name = 'Test User'
expiration_date = None

print('='*60)
print('LICENSE KEY GENERATOR')
print('='*60)
print()

# Generate license key
license_key = license_manager.generate_license_key(
    machine_id=machine_id,
    client_name=client_name,
    expiration_date=expiration_date
)

print(f'Machine ID: {machine_id}')
print(f'Client Name: {client_name}')
print(f'Expiration: Lifetime')
print()
print('LICENSE KEY:')
print('='*60)
print(license_key)
print('='*60)
print()

# Verify the key
is_valid, message = license_manager.verify_license_key(license_key, machine_id)

if is_valid:
    print('✓ License key is VALID')
else:
    print(f'✗ License key verification failed: {message}')
