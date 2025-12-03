# How to Distribute Date Factory Manager

This guide explains how to distribute your Date Factory Manager application to end users.

## What You'll Distribute

A single file: **`DateFactoryManager_Setup.exe`**

This installer includes:
- ✅ Python 3.x runtime (embedded)
- ✅ All required libraries (Flask, XlsxWriter, APScheduler, etc.)
- ✅ Application files and database
- ✅ Templates and static resources
- ✅ Start/Stop server scripts
- ✅ Application icons

**File size**: Approximately 50-80 MB

---

## System Requirements for End Users

### Minimum Requirements
- **Operating System**: Windows 7 or later (Windows 10/11 recommended)
- **RAM**: 2 GB minimum, 4 GB recommended
- **Disk Space**: 200 MB for installation
- **Processor**: Any modern CPU (1 GHz or faster)
- **Network**: Not required for basic operation (required for Telegram backup features)

### Important Notes
- ❌ **No Python installation required**
- ❌ **No additional software needed**
- ✅ **Works on clean Windows installations**
- ✅ **Portable - can be installed on any Windows PC**

---

## Distribution Methods

### 1. Direct Download
- Upload `DateFactoryManager_Setup.exe` to a file hosting service:
  - Google Drive
  - Dropbox
  - OneDrive
  - Your own website
- Share the download link with users

### 2. USB Drive
- Copy `DateFactoryManager_Setup.exe` to a USB drive
- Distribute physically to users
- Users can run directly from USB or copy to their computer

### 3. Network Share
- Place the installer on a shared network folder
- Users can access and install from the network

---

## Installation Instructions for End Users

### Step 1: Download the Installer
- Download `DateFactoryManager_Setup.exe` from the provided link or location

### Step 2: Run the Installer
1. Double-click `DateFactoryManager_Setup.exe`
2. If Windows SmartScreen appears, click "More info" → "Run anyway"
   - This is normal for new applications
3. Click "Yes" if User Account Control (UAC) prompts appear

### Step 3: Follow the Installation Wizard
1. **Welcome Screen**: Click "Next"
2. **License Agreement**: Accept and click "Next"
3. **Installation Location**: 
   - Default: `C:\Program Files\Date Factory Manager`
   - Or choose a custom location
4. **Select Components**: Keep defaults, click "Next"
5. **Start Menu Folder**: Keep default, click "Next"
6. **Additional Tasks**: 
   - ✅ Check "Create a desktop icon" (recommended)
   - Click "Next"
7. **Ready to Install**: Click "Install"
8. **Completing Setup**: 
   - ✅ Check "Launch Date Factory Manager" to start immediately
   - Click "Finish"

---

## Using the Application

### Starting the Server

**Method 1: Desktop Shortcut**
- Double-click the "Date Factory Manager" icon on your desktop

**Method 2: Start Menu**
- Click Start → All Programs → Date Factory Manager → Date Factory Manager

**Method 3: Manual**
- Navigate to installation folder
- Double-click `START_SERVER.bat`

### What Happens When You Start
1. A console window opens showing server status
2. Your default web browser opens automatically to `http://localhost:5000`
3. The application dashboard appears

### Accessing from Other Devices
To access from mobile phones or other computers on the same network:
1. Find your computer's IP address:
   - Open Command Prompt (cmd)
   - Type: `ipconfig`
   - Look for "IPv4 Address" (e.g., 192.168.1.100)
2. On other devices, open browser and go to:
   - `http://YOUR-IP-ADDRESS:5000`
   - Example: `http://192.168.1.100:5000`

### Stopping the Server

**Method 1: Start Menu**
- Start → All Programs → Date Factory Manager → Stop Server

**Method 2: Console Window**
- Close the console window that opened when you started the server

**Method 3: Manual**
- Navigate to installation folder
- Double-click `STOP_SERVER.bat`

---

## Uninstallation

### Method 1: Windows Settings (Recommended)
1. Open Windows Settings
2. Go to "Apps" or "Apps & Features"
3. Find "Date Factory Manager" in the list
4. Click "Uninstall"
5. Follow the prompts

### Method 2: Start Menu
1. Start → All Programs → Date Factory Manager
2. Click "Uninstall Date Factory Manager"
3. Follow the prompts

### Method 3: Control Panel
1. Open Control Panel
2. Go to "Programs and Features"
3. Find "Date Factory Manager"
4. Click "Uninstall"
5. Follow the prompts

### What Gets Removed
- ✅ Application files
- ✅ Desktop shortcut
- ✅ Start Menu entries
- ✅ Registry entries

### What Gets Kept (Optional)
During uninstallation, you may be asked if you want to keep:
- Database files (your data)
- Export files
- Backup files

Choose "Yes" to keep your data if you plan to reinstall later.

---

## Troubleshooting

### Installer Won't Run
**Problem**: Windows blocks the installer
**Solution**: 
1. Right-click the installer
2. Select "Properties"
3. Check "Unblock" at the bottom
4. Click "Apply" → "OK"
5. Try running again

### Port 5000 Already in Use
**Problem**: Another application is using port 5000
**Solution**:
1. Close other applications that might use port 5000
2. Restart your computer
3. Try starting the server again

### Browser Doesn't Open Automatically
**Problem**: Browser doesn't open when starting server
**Solution**:
1. Wait for the console window to show "Server running"
2. Manually open your browser
3. Go to `http://localhost:5000`

### Can't Access from Other Devices
**Problem**: Mobile/other computers can't connect
**Solution**:
1. Check that both devices are on the same network
2. Verify the IP address is correct
3. Check Windows Firewall:
   - Allow Python through firewall
   - Or temporarily disable firewall to test

### Application Won't Start
**Problem**: Nothing happens when clicking the shortcut
**Solution**:
1. Try running as Administrator:
   - Right-click shortcut
   - Select "Run as administrator"
2. Check if antivirus is blocking it
3. Reinstall the application

---

## Support Information

### Getting Help
If users encounter issues:
1. Check the troubleshooting section above
2. Verify system requirements are met
3. Try reinstalling the application
4. Contact your IT support or the application provider

### Reporting Issues
When reporting issues, provide:
- Windows version (e.g., Windows 10, Windows 11)
- Error messages (if any)
- Steps to reproduce the problem
- Screenshots (if applicable)

---

## Security Notes

### Antivirus Warnings
Some antivirus software may flag the installer because:
- It's a new/unknown application
- It bundles Python runtime
- It creates executable files

**This is normal**. The application is safe. You may need to:
1. Add an exception in your antivirus
2. Temporarily disable antivirus during installation
3. Contact your IT department for approval

### Windows SmartScreen
Windows SmartScreen may show a warning because:
- The application doesn't have a digital signature
- It's not widely distributed yet

**This is normal**. Click "More info" → "Run anyway" to proceed.

---

## Updates

### Installing Updates
When a new version is released:
1. Download the new installer
2. Run it - it will automatically update the existing installation
3. Your data will be preserved

### Backup Before Updating
Recommended steps:
1. Stop the server
2. Copy the database file (`date_factory.db`) to a safe location
3. Install the update
4. Verify everything works
5. Delete the backup if successful

---

## License and Terms

[Add your license information here]

---

## Contact Information

[Add your contact information here]
- Email: your-email@example.com
- Website: www.yourwebsite.com
- Support: support@yourwebsite.com
