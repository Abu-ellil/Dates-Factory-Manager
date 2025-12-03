# 🔑 License Key Generator - Quick Start Guide

## What You Got

A professional GUI application to generate and manage license keys for your Date Factory Manager application.

## 🚀 Two Ways to Use It

### Method 1: Run Directly (Fastest)

**Just double-click:**
```
RUN_LICENSE_KEYGEN.bat
```

That's it! The GUI will open immediately.

### Method 2: Build to EXE (For Distribution)

**Double-click:**
```
BUILD_LICENSE_KEYGEN.bat
```

Wait for the build to complete, then find your executable at:
```
dist\LicenseKeyGenerator.exe
```

You can copy this EXE anywhere and run it without Python!

## 📋 How to Generate a License Key

### Step 1: Get Customer's Machine ID
Your customer runs the Date Factory Manager app and copies their Machine ID.
It looks like: `A1B2-C3D4-E5F6-G7H8`

### Step 2: Fill the Form
1. **Machine ID**: Paste the customer's Machine ID
2. **Client Name**: Enter customer's name (e.g., "Ahmed Mohamed")
3. **Expiration**: 
   - Click "Lifetime" for permanent license
   - OR enter date like: `2026-12-31` for time-limited
4. **Notes**: (Optional) Add any notes like "Premium Package"

### Step 3: Generate
Click the big **"🔑 Generate License Key"** button

### Step 4: Copy & Send
Click **"📋 Copy to Clipboard"** and send the key to your customer!

## 💾 All Keys Are Saved Automatically

Every key you generate is automatically saved to a database. You can:

- **Search**: Type customer name or machine ID in the search box
- **View Details**: Double-click any entry to see full information
- **Export to Excel**: Click "📊 Export to Excel" to save all keys
- **Delete**: Select and click "🗑 Delete" if needed

## 🎯 Features at a Glance

| Feature | Description |
|---------|-------------|
| 🎨 Modern UI | Beautiful dark theme interface |
| 🔐 Secure Keys | Hardware-locked, cryptographically signed |
| 💾 Auto-Save | All keys saved to database automatically |
| 🔍 Search | Find keys by name or machine ID |
| 📊 Export | Export all keys to Excel |
| 📋 Copy | One-click copy to clipboard |
| 🗑️ Manage | View details and delete keys |
| ⏰ Flexible | Lifetime or time-limited licenses |

## 📸 What It Looks Like

```
┌─────────────────────────────────────────────────────┐
│         🔑 License Key Generator                     │
├──────────────────┬──────────────────────────────────┤
│  Generate New    │  Generated Keys History          │
│                  │                                  │
│  Machine ID:     │  [Search box]                    │
│  [____]          │                                  │
│                  │  ID | Client | Machine | Exp    │
│  Client Name:    │  ─────────────────────────────  │
│  [____]          │  1  | Ahmed  | A1B2... | 2026   │
│                  │  2  | Sara   | C3D4... | Life   │
│  Expiration:     │  3  | Omar   | E5F6... | 2025   │
│  [____] Lifetime │                                  │
│                  │  [View] [Export] [Delete]        │
│  Notes:          │                                  │
│  [________]      │                                  │
│                  │                                  │
│  [Generate Key]  │                                  │
│                  │                                  │
│  Generated Key:  │                                  │
│  [Key appears]   │                                  │
│  [Copy]          │                                  │
└──────────────────┴──────────────────────────────────┘
```

## ⚠️ Important Security Notes

### 🔒 Keep This Tool PRIVATE!
- This tool generates VALID license keys
- Only YOU should have access to it
- Don't share the EXE or source code
- Don't upload to public repositories

### 💾 Backup Your Database
The database file `license_keys.db` contains all your generated keys.

**Backup regularly:**
1. Copy `license_keys.db` to a safe location
2. OR use "Export to Excel" feature
3. Store backups securely

## 🆘 Troubleshooting

### GUI doesn't open
- Make sure Python is installed
- Run: `pip install -r requirements.txt`

### "openpyxl not found" when exporting
```bash
pip install openpyxl
```

### Build fails
```bash
pip install pyinstaller
```

### Can't find generated EXE
Look in: `dist\LicenseKeyGenerator.exe`

## 📁 Files Created

```
QQQ/
├── bin/
│   └── license_keygen_gui.py          # Main application
├── license_keys.db                     # Database (auto-created)
├── RUN_LICENSE_KEYGEN.bat             # Quick launcher
├── BUILD_LICENSE_KEYGEN.bat           # Build to EXE
└── dist/
    └── LicenseKeyGenerator.exe        # Standalone EXE (after build)
```

## 🎓 Workflow Example

**Scenario**: Customer "Ahmed" wants to buy your software

1. Ahmed runs your app → Gets Machine ID: `A1B2-C3D4-E5F6-G7H8`
2. Ahmed sends you the Machine ID
3. You open License Key Generator
4. Fill in:
   - Machine ID: `A1B2-C3D4-E5F6-G7H8`
   - Client Name: `Ahmed Mohamed`
   - Expiration: Click "Lifetime"
   - Notes: `Premium Package - Paid $500`
5. Click "Generate License Key"
6. Copy the generated key
7. Send it to Ahmed
8. Ahmed enters the key in your app
9. ✅ Activated!

The key is now saved in your database forever. You can search for "Ahmed" anytime to find his key.

## 🌟 Pro Tips

1. **Use Notes Field**: Add payment info, package type, or any details
2. **Export Regularly**: Backup your keys to Excel monthly
3. **Search is Fast**: Just type any part of name or machine ID
4. **Double-Click**: Fastest way to view full key details
5. **Lifetime vs Dated**: Use lifetime for permanent sales, dated for trials/subscriptions

## 📞 Need Help?

Check the full documentation:
```
docs/LICENSE_KEYGEN_README.md
```

---

**That's it! You're ready to generate license keys! 🎉**

*Remember: Keep this tool secure and private!*
