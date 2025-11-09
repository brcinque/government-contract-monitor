#!/usr/bin/env python3
"""
Launch dashboard - run this to start the web interface
"""

from dashboard_webapp import app
import webbrowser
import time
import threading
import sys

def open_browser():
    """Open browser after a short delay"""
    time.sleep(2)
    webbrowser.open('http://127.0.0.1:8080')

def main():
    print("=== Government Contract Monitor Dashboard ===")
    print("Starting web server...")
    print("Dashboard URL: http://127.0.0.1:8080")
    print("Press Ctrl+C to stop the server")
    print()
    
    # Open browser automatically
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Start Flask app
        app.run(debug=False, host='127.0.0.1', port=8080)
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Dashboard failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
