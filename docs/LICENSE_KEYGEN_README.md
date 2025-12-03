# License Key Generator GUI

A professional GUI application for generating and managing license keys for the Date Factory Manager application.

## Features

✨ **Modern GUI Interface**
- Beautiful dark theme design
- Intuitive and user-friendly layout
- Professional appearance

🔑 **License Key Generation**
- Generate hardware-locked license keys
- Support for lifetime and time-limited licenses
- Custom client names and notes
- Machine ID validation

💾 **Database Storage**
- All generated keys are automatically saved to SQLite database
- Complete history of all generated keys
- Search functionality by client name or machine ID
- View detailed information for each key

📊 **Export Capabilities**
- Export all keys to Excel format
- Formatted spreadsheet with all details
- Easy sharing and backup

🗑️ **Key Management**
- View full details of any generated key
- Delete keys when needed
- Copy keys to clipboard with one click

## Installation

### Option 1: Run from Source

1. Install required dependencies:
```bash
pip install openpyxl
```

2. Run the application:
```bash
python bin/license_keygen_gui.py
```

### Option 2: Build Executable

1. Run the build script:
```bash
BUILD_LICENSE_KEYGEN.bat
```

2. The executable will be created in the `dist` folder:
```
dist/LicenseKeyGenerator.exe
```

3. Double-click the executable to run the application.

## Usage

### Generating a License Key

1. **Enter Machine ID**: The customer's unique machine ID (format: XXXX-XXXX-XXXX-XXXX)
   - Customer can get their Machine ID by running the main application

2. **Enter Client Name**: The name of the customer/client

3. **Set Expiration Date** (Optional):
   - Leave empty or click "Lifetime" for permanent licenses
   - Or enter a date in YYYY-MM-DD format for time-limited licenses

4. **Add Notes** (Optional): Any additional information about this license

5. **Click "Generate License Key"**: The key will be generated and displayed

6. **Copy to Clipboard**: Click the copy button to copy the key for sending to the customer

### Viewing History

- All generated keys appear in the right panel
- Use the search box to find specific keys by client name or machine ID
- Double-click any entry to view full details
- Click "View Details" button to see complete information

### Exporting Keys

1. Click "Export to Excel" button
2. Choose save location
3. Excel file will contain all generated keys with full details

### Managing Keys

- **View Details**: Double-click or select and click "View Details"
- **Delete**: Select a key and click "Delete" (confirmation required)
- **Copy Key**: In details view, click "Copy License Key" button

## Database

All generated keys are stored in:
```
license_keys.db
```

This database contains:
- Machine ID
- Client Name
- Expiration Date
- License Key
- Generation Timestamp
- Notes

**⚠️ IMPORTANT**: Keep this database file secure and backed up!

## Security Notes

🔒 **Keep This Tool Private!**
- This tool can generate valid license keys
- Only authorized personnel should have access
- Do not distribute the executable or source code
- Keep the SECRET_KEY in `license_manager.py` confidential

🔐 **Backup Recommendations**
- Regularly backup `license_keys.db`
- Export keys to Excel for additional backup
- Store backups in a secure location

## How Customers Use Their License

1. Customer runs the Date Factory Manager application
2. Application shows their Machine ID
3. Customer sends you their Machine ID
4. You generate a license key using this tool
5. You send the license key to the customer
6. Customer enters the key in the application
7. Application validates and activates

## Troubleshooting

### "openpyxl not found" error
Install the required library:
```bash
pip install openpyxl
```

### Build fails
Make sure PyInstaller is installed:
```bash
pip install pyinstaller
```

### Database locked error
Close any other instances of the application

### Key generation fails
- Verify Machine ID format (XXXX-XXXX-XXXX-XXXX)
- Check date format if using expiration (YYYY-MM-DD)
- Ensure client name is not empty

## Technical Details

- **Framework**: Python Tkinter
- **Database**: SQLite3
- **License System**: HMAC-SHA256 signed keys with hardware locking
- **Export Format**: Excel (.xlsx) using openpyxl

## File Structure

```
QQQ/
├── bin/
│   └── license_keygen_gui.py      # Main GUI application
├── src/
│   └── license_manager.py         # License generation/validation logic
├── BUILD_LICENSE_KEYGEN.bat       # Build script for creating EXE
├── license_keys.db                # Database of generated keys (created on first run)
└── dist/
    └── LicenseKeyGenerator.exe    # Built executable (after build)
```

## Version

Version: 1.0.0
Created: December 2025

---

**© Date Factory Manager - License Key Generator**
*Keep this tool secure and confidential!*
