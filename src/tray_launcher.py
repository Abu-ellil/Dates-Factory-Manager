"""
System Tray Launcher for Date Factory Manager
Runs the Flask server in the background with a system tray icon
"""
import sys
import os
import webbrowser
import threading
import socket
from pathlib import Path

# Try to import pystray and PIL
try:
    import pystray
    from pystray import MenuItem as item
    from PIL import Image, ImageDraw
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pystray", "Pillow"])
    import pystray
    from pystray import MenuItem as item
    from PIL import Image, ImageDraw

# Import Flask app
from app import app, init_db

class ServerManager:
    def __init__(self):
        self.server_thread = None
        self.is_running = False
        self.host = '127.0.0.1'
        self.port = 5000
        
    def start_server(self):
        """Start the Flask server in a background thread"""
        if not self.is_running:
            # Initialize database
            init_db()
            
            # Start server in thread
            self.server_thread = threading.Thread(
                target=lambda: app.run(host=self.host, port=self.port, debug=False, use_reloader=False),
                daemon=True
            )
            self.server_thread.start()
            self.is_running = True
            
            # Wait a moment for server to start
            threading.Timer(1.5, self.open_browser).start()
    
    def open_browser(self):
        """Open the application in the default browser"""
        if self.is_running:
            webbrowser.open(f'http://{self.host}:{self.port}')
    
    def is_port_in_use(self):
        """Check if the port is already in use"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((self.host, self.port)) == 0

def create_icon_image():
    """Create a simple icon for the system tray"""
    # Create a 64x64 image with a factory/building icon
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color='#2563eb')
    dc = ImageDraw.Draw(image)
    
    # Draw a simple factory building
    # Base
    dc.rectangle([10, 35, 54, 54], fill='#1e40af', outline='white')
    
    # Chimney
    dc.rectangle([20, 20, 28, 35], fill='#1e40af', outline='white')
    dc.rectangle([36, 15, 44, 35], fill='#1e40af', outline='white')
    
    # Smoke
    dc.ellipse([18, 10, 26, 18], fill='#94a3b8')
    dc.ellipse([34, 5, 42, 13], fill='#94a3b8')
    
    # Windows
    for x in [16, 26, 36, 46]:
        for y in [40, 48]:
            dc.rectangle([x, y, x+4, y+3], fill='#fbbf24')
    
    return image

class TrayApp:
    def __init__(self):
        self.server = ServerManager()
        self.icon = None
        
    def on_open_browser(self, icon, item):
        """Open the application in browser"""
        self.server.open_browser()
    
    def on_quit(self, icon, item):
        """Quit the application"""
        icon.stop()
        sys.exit(0)
    
    def create_menu(self):
        """Create the system tray menu"""
        return pystray.Menu(
            item('Open Date Factory Manager', self.on_open_browser, default=True),
            item('Quit', self.on_quit)
        )
    
    def run(self):
        """Run the system tray application"""
        # Start the server
        self.server.start_server()
        
        # Create and run the system tray icon
        icon_image = create_icon_image()
        self.icon = pystray.Icon(
            "DateFactoryManager",
            icon_image,
            "Date Factory Manager",
            self.create_menu()
        )
        
        self.icon.run()

def main():
    """Main entry point"""
    # Change to the script directory
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        os.chdir(os.path.dirname(sys.executable))
    else:
        # Running as script
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create and run the tray app
    app = TrayApp()
    app.run()

if __name__ == '__main__':
    main()
