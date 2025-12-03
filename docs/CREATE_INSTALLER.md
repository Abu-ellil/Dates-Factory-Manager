# Creating an Installer for Date Factory Manager

This guide will help you create a professional Windows installer (.exe) for your Date Factory Manager application.

## Quick Start (Automated Method) ⚡

The easiest way to build the installer is using the automated build script:

### Option 1: One-Click Build (Recommended)
1. **Double-click** `BUILD_INSTALLER.bat`
2. Wait for the build process to complete
3. Find your installer in `installer_output\DateFactoryManager_Setup.exe`

### Option 2: Command Line
```bash
python create_installer.py
```

That's it! The script will:
- ✅ Check for Inno Setup (download and install if needed)
- ✅ Check Python dependencies (install if needed)
- ✅ Build the portable application with PyInstaller
- ✅ Compile the installer with Inno Setup
- ✅ Create `DateFactoryManager_Setup.exe` ready for distribution

---

## What the Automated Build Does

### Step 1: Environment Check
- Searches for Inno Setup in common installation paths
- If not found, offers to download and install it automatically
- Checks for required Python packages (PyInstaller, Pillow)
- Installs missing packages automatically

### Step 2: Build Portable Application
- Runs PyInstaller with `app.spec` configuration
- Bundles Python runtime and all dependencies
- Includes templates, static files, and database
- Copies batch files and documentation
- Creates necessary folders (exports, backups)

### Step 3: Compile Installer
- Runs Inno Setup compiler with `installer.iss`
- Creates professional Windows installer
- Adds Start Menu and Desktop shortcuts
- Includes uninstaller
- Supports English and Arabic languages

### Step 4: Validation
- Verifies the installer was created successfully
- Reports file size and location
- Provides next steps

---

## Manual Method (Advanced)

If you prefer to build manually or need more control:

### Prerequisites

1. **Install Pillow** (for icon conversion):
   ```bash
   pip install Pillow
   ```

2. **Download and Install Inno Setup**:
   - Download from: https://jrsoftware.org/isdl.php
   - Install the latest version (it's free)

### Steps

1. **Build the portable version**:
   ```bash
   python build_portable.py
   ```
   This creates the `dist\DateFactoryPortable` folder with all necessary files.

2. **Compile the installer**:
   - Open **Inno Setup Compiler**
   - Click **File → Open** and select `installer.iss`
   - Click **Build → Compile** (or press Ctrl+F9)

3. **Find your installer**:
   - Location: `installer_output\DateFactoryManager_Setup.exe`

---

## Testing the Installer

### Basic Test
1. Navigate to `installer_output` folder
2. Run `DateFactoryManager_Setup.exe`
3. Follow the installation wizard
4. Verify the app launches successfully

### Thorough Test (Recommended)
1. **Test on your development machine**:
   - Install and verify all features work
   - Check desktop and Start Menu shortcuts
   - Test starting and stopping the server

2. **Test on a clean Windows machine** (Critical!):
   - Use a VM or a computer without Python installed
   - This verifies the installer truly bundles everything
   - Install and run the application
   - Verify all features work without Python

3. **Test uninstallation**:
   - Use Windows "Add or Remove Programs"
   - Verify clean removal
   - Check that shortcuts are removed

---

## What the Installer Includes

The final installer bundles:
- ✅ **Python 3.x runtime** (embedded, ~40 MB)
- ✅ **All Python libraries**:
  - Flask (web framework)
  - XlsxWriter (Excel generation)
  - APScheduler (backup scheduling)
  - python-telegram-bot (cloud uploads)
  - openpyxl (Excel reading)
- ✅ **Application files**:
  - Templates and static resources
  - Database (date_factory.db)
  - Configuration files
- ✅ **Utility scripts**:
  - START_SERVER.bat
  - STOP_SERVER.bat
- ✅ **Documentation**:
  - README files
  - User guides
- ✅ **Icons and branding**

**Total size**: Approximately 50-80 MB

---

## Customization

You can customize the installer by editing `installer.iss`:

### Basic Settings
- **Company Name**: Change `MyAppPublisher` on line 9
- **App Version**: Change `MyAppVersion` on line 8
- **Installation Folder**: Modify `DefaultDirName` on line 19

### Advanced Settings
- **Desktop Shortcut**: Line 35 - remove `Flags: unchecked` to enable by default
- **Languages**: Add more languages in the `[Languages]` section
- **File Associations**: Add custom file type associations
- **Custom Actions**: Add pre/post-installation scripts

### Branding
- **Icon**: Replace `icon.ico` with your own icon
- **Wizard Images**: Add custom installer images
- **License Agreement**: Add a license file

---

## What the Installer Does

When users run `DateFactoryManager_Setup.exe`:

1. **Installation Wizard**:
   - Professional Windows installer interface
   - Language selection (English/Arabic)
   - License agreement (if configured)
   - Installation location selection
   - Component selection
   - Desktop shortcut option

2. **File Installation**:
   - Copies all files to `C:\Program Files\Date Factory Manager`
   - Creates necessary folders
   - Sets up database

3. **Shortcuts Creation**:
   - **Start Menu**:
     - Date Factory Manager (launches app)
     - Stop Server (stops the server)
     - Uninstall (removes the app)
   - **Desktop** (optional):
     - Date Factory Manager

4. **Registry Entries**:
   - Adds uninstall information
   - Registers the application

5. **Post-Installation**:
   - Option to launch immediately
   - Opens browser to application

---

## Distribution

After creating the installer, you can distribute the single file:
- **File**: `installer_output\DateFactoryManager_Setup.exe`
- **Size**: ~50-80 MB
- **Distribution methods**:
  - Email (if size permits)
  - File sharing services (Google Drive, Dropbox, etc.)
  - USB drives
  - Network shares
  - Your own website

### End User Experience
Users just need to:
1. Download the installer
2. Run it
3. Follow the wizard
4. Use the desktop or Start Menu shortcut to launch

**No Python or dependencies needed on the target computer!**

---

## Troubleshooting

### Build Fails
- **Check Python version**: Python 3.8+ required
- **Check dependencies**: Run `pip install -r requirements.txt`
- **Check disk space**: Need ~500 MB free for build process
- **Check permissions**: Run as administrator if needed

### Inno Setup Not Found
- The automated script will offer to download it
- Or manually install from: https://jrsoftware.org/isdl.php
- Make sure to install to default location

### PyInstaller Errors
- **Icon errors**: Make sure `icon.ico` exists
- **Import errors**: Check `hiddenimports` in `app.spec`
- **File not found**: Verify all paths in `app.spec` are correct

### Installer Too Large
- Normal size is 50-80 MB (includes Python runtime)
- To reduce size:
  - Remove unused dependencies from `requirements.txt`
  - Exclude unnecessary files in `app.spec`
  - Use UPX compression (already enabled)

### Antivirus Warnings
- Some antivirus software may flag PyInstaller executables
- This is a false positive
- You may need to:
  - Add exception in antivirus
  - Get a code signing certificate (for professional distribution)

---

## Next Steps

After building the installer:

1. **Test thoroughly** (see Testing section above)
2. **Document any special requirements** for your users
3. **Create a distribution plan** (see DISTRIBUTION_GUIDE.md)
4. **Consider code signing** for professional distribution
5. **Set up a download page** or distribution method

---

## Build Time Estimates

- **First build** (with Inno Setup download): ~5-10 minutes
- **Subsequent builds**: ~2-3 minutes
- **Automated build**: Fully hands-off after starting

---

## Support

For issues or questions:
- Check the troubleshooting section above
- Review `DISTRIBUTION_GUIDE.md` for end-user issues
- Check Inno Setup documentation: https://jrsoftware.org/ishelp/
- Check PyInstaller documentation: https://pyinstaller.org/

---

## Version History

- **v1.0**: Initial automated build system
  - Automated Inno Setup installation
  - One-click build process
  - Comprehensive error handling
