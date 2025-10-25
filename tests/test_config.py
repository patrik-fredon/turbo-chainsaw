"""
Configuration management tests for Fredon Menu
"""

import unittest
import tempfile
import json
import os
from pathlib import Path

from src.menu.models import MenuConfig, Button, Category, CommandType
from src.menu.config import ConfigManager
from src.utils.validation import ConfigValidator, ConfigValidationError


class TestMenuConfig(unittest.TestCase):
    """Test MenuConfig model."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_config = {
            "menu": {
                "title": "Test Menu",
                "icon": "/path/to/icon.png",
                "quote": "Test quote",
                "glass_effect": True
            },
            "buttons": [
                {
                    "id": "test-button",
                    "name": "Test Button",
                    "icon": "/path/to/button.png",
                    "command": "echo hello",
                    "type": "shell",
                    "enabled": True,
                    "position": 0
                }
            ],
            "categories": []
        }

    def test_menu_config_creation(self):
        """Test MenuConfig creation."""
        config = MenuConfig.from_dict(self.valid_config)

        self.assertEqual(config.title, "Test Menu")
        self.assertEqual(config.icon, "/path/to/icon.png")
        self.assertEqual(config.quote, "Test quote")
        self.assertTrue(config.glass_effect)
        self.assertEqual(len(config.buttons), 1)

    def test_button_creation(self):
        """Test Button creation."""
        button_data = {
            "id": "test-button",
            "name": "Test Button",
            "icon": "/path/to/button.png",
            "command": "echo hello",
            "type": "shell"
        }

        button = Button.from_dict(button_data)

        self.assertEqual(button.id, "test-button")
        self.assertEqual(button.name, "Test Button")
        self.assertEqual(button.command, "echo hello")
        self.assertEqual(button.type, CommandType.SHELL)

    def test_category_creation(self):
        """Test Category creation."""
        category_data = {
            "id": "test-category",
            "name": "Test Category",
            "icon": "/path/to/category.png",
            "description": "Test category description",
            "button_ids": ["button1", "button2"]
        }

        category = Category.from_dict(category_data)

        self.assertEqual(category.id, "test-category")
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.description, "Test category description")
        self.assertEqual(category.button_ids, ["button1", "button2"])

    def test_get_main_buttons(self):
        """Test getting main menu buttons."""
        config = MenuConfig.from_dict(self.valid_config)

        main_buttons = config.get_main_buttons()
        self.assertEqual(len(main_buttons), 1)
        self.assertEqual(main_buttons[0].id, "test-button")

    def test_get_category_buttons(self):
        """Test getting category buttons."""
        config_data = self.valid_config.copy()
        config_data["categories"] = [{
            "id": "test-category",
            "name": "Test Category",
            "icon": "/path/to/category.png",
            "description": "Test description",
            "button_ids": []
        }]
        config_data["buttons"][0]["category_id"] = "test-category"

        config = MenuConfig.from_dict(config_data)

        category_buttons = config.get_category_buttons("test-category")
        self.assertEqual(len(category_buttons), 1)
        self.assertEqual(category_buttons[0].id, "test-button")

    def test_to_dict_conversion(self):
        """Test conversion to dictionary."""
        config = MenuConfig.from_dict(self.valid_config)
        dict_data = config.to_dict()

        self.assertIn("menu", dict_data)
        self.assertIn("buttons", dict_data)
        self.assertIn("categories", dict_data)
        self.assertEqual(dict_data["menu"]["title"], "Test Menu")


class TestConfigValidator(unittest.TestCase):
    """Test configuration validation."""

    def test_valid_config(self):
        """Test validation of valid configuration."""
        config = {
            "menu": {
                "title": "Test Menu",
                "icon": "/path/to/icon.png"
            },
            "buttons": [],
            "categories": []
        }

        errors = ConfigValidator.validate_config(config)
        self.assertEqual(len(errors), 0)

    def test_invalid_config_missing_required(self):
        """Test validation of config with missing required fields."""
        config = {
            "menu": {
                "title": "Test Menu"
                # Missing icon
            },
            "buttons": [],
            "categories": []
        }

        errors = ConfigValidator.validate_config(config)
        self.assertGreater(len(errors), 0)

        # Check for specific error about missing icon
        icon_error = next((e for e in errors if "icon" in str(e.field)), None)
        self.assertIsNotNone(icon_error)

    def test_duplicate_button_ids(self):
        """Test validation of duplicate button IDs."""
        config = {
            "menu": {
                "title": "Test Menu",
                "icon": "/path/to/icon.png"
            },
            "buttons": [
                {
                    "id": "duplicate-id",
                    "name": "Button 1",
                    "icon": "/path/to/icon1.png",
                    "command": "echo 1",
                    "type": "shell"
                },
                {
                    "id": "duplicate-id",
                    "name": "Button 2",
                    "icon": "/path/to/icon2.png",
                    "command": "echo 2",
                    "type": "shell"
                }
            ],
            "categories": []
        }

        errors = ConfigValidator.validate_config(config)
        self.assertGreater(len(errors), 0)

        # Check for duplicate ID error
        duplicate_error = next((e for e in errors if "duplicate" in e.message.lower()), None)
        self.assertIsNotNone(duplicate_error)


class TestConfigManager(unittest.TestCase):
    """Test configuration manager."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "test_config.json")

        self.test_config = {
            "menu": {
                "title": "Test Menu",
                "icon": "/path/to/icon.png",
                "quote": "Test quote"
            },
            "buttons": [
                {
                    "id": "test-button",
                    "name": "Test Button",
                    "icon": "/path/to/button.png",
                    "command": "echo hello",
                    "type": "shell"
                }
            ],
            "categories": []
        }

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_load_config_from_file(self):
        """Test loading configuration from file."""
        # Write test config file
        with open(self.config_path, 'w') as f:
            json.dump(self.test_config, f)

        config_manager = ConfigManager(self.config_path)
        config = config_manager.load_config()

        self.assertEqual(config.title, "Test Menu")
        self.assertEqual(len(config.buttons), 1)

    def test_load_config_missing_file(self):
        """Test loading configuration when file doesn't exist."""
        config_manager = ConfigManager(self.config_path)
        config = config_manager.load_config()

        # Should load minimal config
        self.assertIsNotNone(config)
        self.assertEqual(config.title, "Fredon Menu")  # Default title

    def test_save_config(self):
        """Test saving configuration to file."""
        config_manager = ConfigManager(self.config_path)
        config = MenuConfig.from_dict(self.test_config)
        config_manager._config = config

        result = config_manager.save_config()
        self.assertTrue(result)

        # Verify file was created
        self.assertTrue(os.path.exists(self.config_path))

        # Verify content
        with open(self.config_path, 'r') as f:
            saved_data = json.load(f)

        self.assertEqual(saved_data["menu"]["title"], "Test Menu")

    def test_reload_config(self):
        """Test reloading configuration."""
        config_manager = ConfigManager(self.config_path)

        # Save initial config
        config = MenuConfig.from_dict(self.test_config)
        config_manager._config = config
        config_manager.save_config()

        # Modify file
        modified_config = self.test_config.copy()
        modified_config["menu"]["title"] = "Modified Menu"

        with open(self.config_path, 'w') as f:
            json.dump(modified_config, f)

        # Reload
        result = config_manager.reload_config()
        self.assertTrue(result)

        # Verify change was detected
        reloaded_config = config_manager.get_config()
        self.assertEqual(reloaded_config.title, "Modified Menu")


if __name__ == '__main__':
    unittest.main()