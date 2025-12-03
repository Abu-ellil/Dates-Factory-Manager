"""
GUI Launcher for Date Factory Manager
Provides a graphical interface to start and stop the Flask server
"""
import sys
import os
import subprocess
import threading
import time
import socket
import webbrowser
from pathlib import Path

# Try to import tkinter first
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except ImportError:
    print("Installing tkinter...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "maturin"])
    import tkinter as tk
    from tkinter import ttk, messagebox

class ServerLauncherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Date Factory Manager - Server Control")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Set window icon if available
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'build_tools', 'icon.ico')
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.path.dirname(__file__), 'server_launcher_gui.py')  # fallback
        try:
            self.root.iconbitmap(icon_path)
        except:
            pass

        # Server process management
        self.server_process = None
        self.is_server_running = False

        # Color scheme
        self.bg_color = "#1a1a2e"
        self.secondary_bg = "#16213e"
        self.accent_color = "#0f3460"
        self.highlight_color = "#e94560"
        self.text_color = "#ffffff"
        self.success_color = "#00ff88"
        self.warning_color = "#ffa500"

        self.root.configure(bg=self.bg_color)

        self.setup_ui()
        self.check_server_status()

        # Start status monitoring
        self.monitor_thread = threading.Thread(target=self.monitor_server_status, daemon=True)
        self.monitor_thread.start()

    def setup_ui(self):
        """Setup the user interface"""
        # Header
        header_frame = tk.Frame(self.root, bg=self.highlight_color, height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🏭 Date Factory Manager",
            font=("Segoe UI", 24, "bold"),
            bg=self.highlight_color,
            fg=self.text_color
        )
        title_label.pack(pady=20)

        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Server Control Panel
        control_panel = tk.Frame(main_container, bg=self.secondary_bg, relief=tk.RAISED, bd=2)
        control_panel.pack(fill=tk.X, pady=(0, 20))

        self.setup_control_panel(control_panel)

        # Status Panel
        status_panel = tk.Frame(main_container, bg=self.secondary_bg, relief=tk.RAISED, bd=2)
        status_panel.pack(fill=tk.X, pady=(0, 20))

        self.setup_status_panel(status_panel)

        # Logs Panel
        logs_panel = tk.Frame(main_container, bg=self.secondary_bg, relief=tk.RAISED, bd=2)
        logs_panel.pack(fill=tk.BOTH, expand=True)

        self.setup_logs_panel(logs_panel)

    def setup_control_panel(self, parent):
        """Setup the server control panel"""
        # Title
        title = tk.Label(
            parent,
            text="🚀 Server Control",
            font=("Segoe UI", 16, "bold"),
            bg=self.secondary_bg,
            fg=self.text_color
        )
        title.pack(pady=15)

        # Control buttons frame
        btn_frame = tk.Frame(parent, bg=self.secondary_bg)
        btn_frame.pack(pady=10)

        # Start Server Button
        self.start_btn = tk.Button(
            btn_frame,
            text="▶️ Start Server",
            command=self.start_server,
            bg=self.success_color,
            fg="#000000",
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            height=2,
            width=15
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)

        # Stop Server Button
        self.stop_btn = tk.Button(
            btn_frame,
            text="⏹️ Stop Server",
            command=self.stop_server,
            bg=self.highlight_color,
            fg=self.text_color,
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            height=2,
            width=15,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=10)

        # Access Application Button
        self.access_btn = tk.Button(
            btn_frame,
            text="🌐 Open App",
            command=self.open_application,
            bg=self.accent_color,
            fg=self.text_color,
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            height=2,
            width=15,
            state=tk.DISABLED
        )
        self.access_btn.pack(side=tk.LEFT, padx=10)

        # Quit Button
        quit_btn = tk.Button(
            btn_frame,
            text="❌ Quit",
            command=self.quit_application,
            bg=self.warning_color,
            fg="#000000",
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            height=2,
            width=15
        )
        quit_btn.pack(side=tk.RIGHT, padx=10)

    def setup_status_panel(self, parent):
        """Setup the status panel"""
        # Title
        title = tk.Label(
            parent,
            text="📊 Server Status",
            font=("Segoe UI", 16, "bold"),
            bg=self.secondary_bg,
            fg=self.text_color
        )
        title.pack(pady=15)

        # Status grid
        status_grid = tk.Frame(parent, bg=self.secondary_bg)
        status_grid.pack(pady=10, padx=20, fill=tk.X)

        # Server Status
        status_frame = tk.Frame(status_grid, bg=self.secondary_bg)
        status_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            status_frame,
            text="Server Status:",
            font=("Segoe UI", 12),
            bg=self.secondary_bg,
            fg=self.text_color,
            anchor="w"
        ).pack(side=tk.LEFT)

        self.status_label = tk.Label(
            status_frame,
            text="❌ Stopped",
            font=("Segoe UI", 12, "bold"),
            bg=self.secondary_bg,
            fg=self.highlight_color,
            anchor="w"
        )
        self.status_label.pack(side=tk.RIGHT)

        # Server URL
        url_frame = tk.Frame(status_grid, bg=self.secondary_bg)
        url_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            url_frame,
            text="Server URL:",
            font=("Segoe UI", 12),
            bg=self.secondary_bg,
            fg=self.text_color,
            anchor="w"
        ).pack(side=tk.LEFT)

        self.url_label = tk.Label(
            url_frame,
            text="http://localhost:5000",
            font=("Segoe UI", 12),
            bg=self.secondary_bg,
            fg=self.success_color,
            anchor="w"
        )
        self.url_label.pack(side=tk.RIGHT)

        # Mobile Access
        mobile_frame = tk.Frame(status_grid, bg=self.secondary_bg)
        mobile_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            mobile_frame,
            text="Mobile Access:",
            font=("Segoe UI", 12),
            bg=self.secondary_bg,
            fg=self.text_color,
            anchor="w"
        ).pack(side=tk.LEFT)

        self.mobile_label = tk.Label(
            mobile_frame,
            text="http://<IP>:5000",
            font=("Segoe UI", 12),
            bg=self.secondary_bg,
            fg=self.warning_color,
            anchor="w"
        )
        self.mobile_label.pack(side=tk.RIGHT)

    def setup_logs_panel(self, parent):
        """Setup the logs panel"""
        # Title
        title = tk.Label(
            parent,
            text="📝 Server Logs",
            font=("Segoe UI", 16, "bold"),
            bg=self.secondary_bg,
            fg=self.text_color
        )
        title.pack(pady=15)

        # Logs frame
        logs_frame = tk.Frame(parent, bg=self.accent_color, relief=tk.SUNKEN, bd=2)
        logs_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Scrollbars
        vsb = ttk.Scrollbar(logs_frame, orient="vertical")

        # Configure style
        style = ttk.Style()
        style.configure("CustomText.TText",
                       background=self.accent_color,
                       foreground=self.text_color,
                       fieldbackground=self.accent_color,
                       borderwidth=0)

        self.logs_text = tk.Text(
            logs_frame,
            font=("Courier New", 10),
            bg=self.accent_color,
            fg=self.text_color,
            relief=tk.FLAT,
            padx=10,
            pady=8,
            wrap=tk.WORD,
            yscrollcommand=vsb.set
        )
        self.logs_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        vsb.config(command=self.logs_text.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.logs_text.insert(tk.END, "Welcome to Date Factory Manager Server Launcher!\n")
        self.logs_text.insert(tk.END, "Click 'Start Server' to launch the application.\n\n")
        self.logs_text.config(state=tk.DISABLED)

    def log_message(self, message):
        """Add a message to the logs"""
        self.logs_text.config(state=tk.NORMAL)
        timestamp = time.strftime("%H:%M:%S")
        self.logs_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.logs_text.see(tk.END)
        self.logs_text.config(state=tk.DISABLED)

    def get_local_ip(self):
        """Get local IP address"""
        try:
            # Create a socket and connect to external server to get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "unknown"

    def is_port_in_use(self, port=5000):
        """Check if port is in use"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0

    def check_server_status(self):
        """Check current server status"""
        self.is_server_running = self.is_port_in_use(5000)
        self.update_ui_status()

    def monitor_server_status(self):
        """Monitor server status in background"""
        while True:
            old_status = self.is_server_running
            self.is_server_running = self.is_port_in_use(5000)

            if old_status != self.is_server_running:
                self.root.after(0, self.update_ui_status)

            time.sleep(2)

    def update_ui_status(self):
        """Update UI based on server status"""
        if self.is_server_running:
            self.status_label.config(text="✅ Running", fg=self.success_color)
            self.start_btn.config(state=tk.DISABLED, bg=self.secondary_bg, fg=self.text_color)
            self.stop_btn.config(state=tk.NORMAL)
            self.access_btn.config(state=tk.NORMAL)

            # Update mobile access IP
            local_ip = self.get_local_ip()
            self.mobile_label.config(text=f"http://{local_ip}:5000")
        else:
            self.status_label.config(text="❌ Stopped", fg=self.highlight_color)
            self.start_btn.config(state=tk.NORMAL, bg=self.success_color, fg="#000000")
            self.stop_btn.config(state=tk.DISABLED)
            self.access_btn.config(state=tk.DISABLED)
            self.mobile_label.config(text="http://<IP>:5000", fg=self.warning_color)

    def start_server(self):
        """Start the Flask server"""
        if self.is_server_running:
            messagebox.showwarning("Warning", "Server is already running!")
            return

        self.log_message("Starting Date Factory Manager server...")

        try:
            # Get the server_only.py path (runs without browser/console output)
            server_path = os.path.join(os.path.dirname(__file__), 'server_only.py')

            if not os.path.exists(server_path):
                # Fallback to app.py if server_only.py doesn't exist
                server_path = os.path.join(os.path.dirname(__file__), 'app.py')

            # Start server process
            self.server_process = subprocess.Popen(
                [sys.executable, server_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.path.dirname(server_path),
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            self.log_message("Server process started successfully")
            self.log_message("Waiting for server to initialize...")

            # Wait a moment for server to start
            time.sleep(3)
            self.check_server_status()

            if self.is_server_running:
                self.log_message("Server is now running and ready!")
                self.log_message("You can now open the application in your browser.")
            else:
                self.log_message("Warning: Server may not have started properly")
                # Don't kill process yet, give it more time

        except Exception as e:
            self.log_message(f"Error starting server: {str(e)}")
            messagebox.showerror("Error", f"Failed to start server:\n{str(e)}")

    def stop_server(self):
        """Stop the Flask server"""
        if not self.is_server_running:
            messagebox.showwarning("Warning", "Server is not running!")
            return

        self.log_message("Stopping server...")

        try:
            if os.name == 'nt':  # Windows
                # On Windows, use taskkill to force terminate processes listening on port 5000
                import subprocess
                result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, timeout=10)

                # Find the process using port 5000
                lines = result.stdout.split('\n')
                for line in lines:
                    if ':5000 ' in line and 'LISTENING' in line:
                        # Extract PID from the line (last column)
                        parts = line.split()
                        if len(parts) >= 5:
                            pid = parts[-1].strip()
                            try:
                                # Force kill the process
                                subprocess.run(['taskkill', '/PID', pid, '/F'], check=True, timeout=10)
                                self.log_message(f"Successfully terminated process {pid}")
                                break
                            except subprocess.CalledProcessError as e:
                                self.log_message(f"Failed to kill process {pid}: {e}")

                # Also try to terminate our stored process if available
                if self.server_process and self.server_process.poll() is None:
                    self.server_process.kill()
                    self.log_message("Force-killed stored process")

            else:  # Unix-like systems
                if self.server_process and self.server_process.poll() is None:
                    import signal
                    self.server_process.terminate()
                    time.sleep(2)
                    if self.server_process.poll() is None:
                        self.server_process.kill()
                        self.log_message("Server force-killed")

            self.server_process = None
            self.log_message("Server stopped successfully")

            # Update status
            time.sleep(1)
            self.check_server_status()

        except Exception as e:
            self.log_message(f"Error stopping server: {str(e)}")
            messagebox.showerror("Error", f"Failed to stop server:\n{str(e)}")

    def open_application(self):
        """Open the application in browser"""
        if not self.is_server_running:
            messagebox.showwarning("Warning", "Server is not running!")
            return

        try:
            webbrowser.open("http://localhost:5000")
            self.log_message("Opened application in default browser")
        except Exception as e:
            self.log_message(f"Error opening browser: {str(e)}")

    def quit_application(self):
        """Quit the application"""
        if self.is_server_running:
            if messagebox.askyesno("Confirm Quit",
                "The server is still running. Stop it before quitting?"):
                self.stop_server()

        self.log_message("Goodbye!")
        self.root.quit()
        self.root.destroy()

    def on_closing(self):
        """Handle window closing"""
        self.quit_application()

def main():
    """Main entry point"""
    # Change to the src directory
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        os.chdir(os.path.dirname(sys.executable))
    else:
        # Running as script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)

    root = tk.Tk()
    app = ServerLauncherGUI(root)

    # Handle window close event
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    root.mainloop()

if __name__ == "__main__":
    main()
