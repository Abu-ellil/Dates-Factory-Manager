"""
Server-only launcher for Date Factory Manager
Runs the Flask server without opening browser or console status messages
"""

# Monkey patch webbrowser to prevent browser opening
import webbrowser
webbrowser.open = lambda *args, **kwargs: None

# Import the full app after patching webbrowser
from app import app

if __name__ == '__main__':
    # Run server silently - no console startup messages
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
