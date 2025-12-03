"""
Server-only launcher for Date Factory Manager
Runs the Flask server without opening browser or console status messages
"""
from flask import Flask
from database import get_connection
import os

# Create a very minimal Flask app for server-only use
app = Flask(__name__)

if __name__ == '__main__':
    # Run server silently - no browser, no console messages
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
