# License Management Guide

## Overview
The installer `DateFactoryManager_Setup.exe` is now configured for production distribution.
- **Clean Install**: It does NOT include any license key.
- **Secure**: It includes a fixed secret key for verification.
- **Hardware Locked**: Each installation requires a unique key.

## How to License New Customers

### 1. Customer Steps
1. **Install**: Run the installer on their computer.
2. **Open**: Launch the app. It will show the "Activation Required" screen.
3. **Send ID**: Ask them to send you the **Machine ID** shown (e.g., `1AED-7CAA-D57F-993E`).

### 2. Your Steps (Developer)
1. Open your project folder on your computer.
2. Run the generator:
   ```bash
   python src/generate_license.py
   ```
3. Enter the **Machine ID** they sent you.
4. Enter their name (e.g., "Al-Nakhil Farm").
5. Choose expiration (e.g., 1 year).
6. Copy the **Generated License Key**.

### 3. Activation
1. Send the key to the customer.
2. They paste it into the app and click "Activate".
3. The app is now fully functional!

---

## Technical Details

- **Secret Key**: `DateFactoryLicense2025FixedKey!@#$%` (Stored in bundled .env)
- **License File**: `license.key` (Created on customer's PC after activation)
- **Database**: `date_factory.db` (Included empty or with sample data)

## Troubleshooting

- **"Invalid Signature"**: 
  - Ensure you used the correct Machine ID.
  - Ensure they copied the key exactly (no spaces).
  - Ensure you haven't changed the `LICENSE_SECRET_KEY` in `.env`.

- **"Internal Server Error"**:
  - The new installer fixes this by including all templates and static files.
