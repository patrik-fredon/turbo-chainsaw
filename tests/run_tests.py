#!/usr/bin/env python3
"""
Test runner for Fredon Menu
"""

import sys
import os
import unittest
import tempfile
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def run_tests():
    """Run all tests."""
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1

def create_test_config():
    """Create a test configuration for integration tests."""
    test_config = {
        "menu": {
            "title": "Fredon Menu Test",
            "icon": "/usr/share/icons/hicolor/256x256/apps/fredon-menu.png",
            "quote": "Test configuration for development",
            "glass_effect": True,
            "theme": {
                "background_opacity": 0.9,
                "blur_radius": 20,
                "border_radius": 12,
                "hover_duration": 200,
                "colors": {
                    "background": "#1a1a1a",
                    "text": "#ffffff",
                    "button_bg": "#2a2a2a",
                    "button_hover": "#3a3a3a",
                    "button_text": "#ffffff",
                    "border": "#4a4a4a"
                },
                "fonts": {
                    "title_family": "sans-serif",
                    "title_size": 24,
                    "button_family": "sans-serif",
                    "button_size": 14,
                    "quote_family": "serif",
                    "quote_size": 12
                }
            },
            "performance": {
                "cache_enabled": True,
                "cache_size_mb": 10,
                "preload_icons": False,
                "lazy_loading": True,
                "max_concurrent_loads": 2
            }
        },
        "buttons": [
            {
                "id": "test-echo",
                "name": "Echo Test",
                "icon": "/usr/share/icons/hicolor/256x256/apps/utilities-terminal.png",
                "command": "echo 'Hello from Fredon Menu!'",
                "type": "shell",
                "description": "Test command that outputs a message",
                "enabled": True,
                "position": 0
            },
            {
                "id": "test-date",
                "name": "Show Date",
                "icon": "/usr/share/icons/hicolor/256x256/apps/calendar.png",
                "command": "date",
                "type": "shell",
                "description": "Display current date and time",
                "enabled": True,
                "position": 1
            }
        ],
        "categories": [
            {
                "id": "test-category",
                "name": "Test Category",
                "icon": "/usr/share/icons/hicolor/256x256/apps/folder.png",
                "description": "Category for testing purposes",
                "button_ids": [],
                "enabled": True,
                "position": 0
            }
        ]
    }

    # Create temporary config directory
    temp_dir = tempfile.mkdtemp(prefix='fredon-menu-test-')
    config_file = os.path.join(temp_dir, 'config.json')

    import json
    with open(config_file, 'w') as f:
        json.dump(test_config, f, indent=2)

    return config_file, temp_dir

def cleanup_test_config(temp_dir):
    """Clean up test configuration."""
    import shutil
    try:
        shutil.rmtree(temp_dir)
    except:
        pass

if __name__ == '__main__':
    # Set up environment for tests
    os.environ['FREDON_MENU_TEST_MODE'] = '1'

    # Create test configuration
    test_config_file, temp_dir = create_test_config()
    os.environ['FREDON_MENU_TEST_CONFIG'] = test_config_file

    try:
        # Run tests
        exit_code = run_tests()
        sys.exit(exit_code)
    finally:
        # Cleanup
        cleanup_test_config(temp_dir)