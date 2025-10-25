#!/usr/bin/env python3
"""
Test script to verify button click behavior
"""
import time
import threading
from src.menu.app import FredonMenu

def test_button_click():
    """Test button click closing behavior"""
    print("Testing button click behavior...")

    # Create app instance
    app = FredonMenu(debug=True)

    def run_menu():
        """Run menu in background thread"""
        time.sleep(1)  # Wait for setup
        app.show_menu()
        time.sleep(5)  # Show for 5 seconds
        app.hide_menu()
        app.quit()

    # Start menu in background
    menu_thread = threading.Thread(target=run_menu, daemon=True)
    menu_thread.start()

    # Run main loop
    try:
        app.run()
    except KeyboardInterrupt:
        print("Test interrupted")
        app.quit()

if __name__ == "__main__":
    test_button_click()