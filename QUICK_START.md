# 🚀 Quick Start Guide - Date Factory Manager

## Easiest Way to Start Your App

### 🎯 Method 1: Double-Click Start (Recommended)
1. **Go to the `bin` folder**
2. **Double-click `START_SERVER.bat`**
3. The app will automatically:
   - Start the server
   - Open your browser to `http://localhost:5000`
   - Show you the connection details

### 🐍 Method 2: Manual Python Start
1. Open Command Prompt or Terminal
2. Navigate to the project folder:
   ```bash
   cd C:\Users\WH\Desktop\Dates-Factory-Manager-main
   ```
3. Run the app:
   ```bash
   python src/app.py
   ```
4. Open your browser and go to: `http://localhost:5000`

### 📱 Access from Mobile/Other Devices
1. Find your computer's IP address:
   - Open Command Prompt and type: `ipconfig`
   - Look for "IPv4 Address" (e.g., 192.168.1.100)
2. On your mobile device, open browser and go to:
   `http://YOUR-IP-ADDRESS:5000`

## 🔧 Troubleshooting

### If you get errors:
1. **Install requirements first** (only needed once):
   ```bash
   pip install -r requirements.txt
   ```

2. **Make sure Python is installed** (Python 3.8+ required)

3. **Check if port 5000 is available** - if not, change the port in `src/app.py`

## 📁 Important Files
- `bin/START_SERVER.bat` - Easy startup script
- `bin/STOP_SERVER.bat` - Stop the server
- `src/app.py` - Main application file
- `requirements.txt` - Python dependencies

## 💡 Pro Tips
- Keep the Command Prompt window open while using the app
- The app automatically creates backups at 11:59 PM daily
- You can set up Telegram notifications for backups (see `TELEGRAM_SETUP.md`)
- For portable version, use the `.exe` file if available

🎉 **That's it! Your app should now be running and ready to use!**
