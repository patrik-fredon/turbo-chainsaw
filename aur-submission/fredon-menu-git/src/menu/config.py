"""
Configuration management for Fredon Menu
"""

import json
import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .models import MenuConfig

logger = logging.getLogger(__name__)


class ConfigFileHandler(FileSystemEventHandler):
    """File system event handler for configuration file changes."""

    def __init__(self, config_manager: "ConfigManager"):
        self.config_manager = config_manager

    def on_modified(self, event):
        """Handle file modification events."""
        if not event.is_directory and event.src_path == str(self.config_manager.config_path):
            logger.info(f"Configuration file modified: {event.src_path}")
            self.config_manager.reload_config()


class ConfigManager:
    """Manages loading, saving, and monitoring of configuration files."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.

        Args:
            config_path: Path to configuration file. If None, uses default path.
        """
        if config_path is None:
            config_path = os.path.expanduser("~/.config/fredon-menu/config.json")

        self.config_path = Path(config_path)
        self.fallback_path = Path(__file__).parent / "data" / "default.json"
        self._config: Optional[MenuConfig] = None
        self._observer: Optional[Observer] = None
        self._callbacks: list = []

        # Ensure config directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

    def add_callback(self, callback):
        """Add callback function to be called when configuration changes."""
        self._callbacks.append(callback)

    def remove_callback(self, callback):
        """Remove callback function."""
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def _notify_callbacks(self):
        """Notify all registered callbacks about configuration change."""
        for callback in self._callbacks:
            try:
                callback(self._config)
            except Exception as e:
                logger.error(f"Error in config change callback: {e}")

    def load_config(self) -> MenuConfig:
        """
        Load configuration from file with fallback to default.

        Returns:
            MenuConfig: Loaded configuration

        Raises:
            Exception: If configuration cannot be loaded and fallback fails
        """
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.info(f"Loaded configuration from {self.config_path}")
                self._config = MenuConfig.from_dict(data)
            else:
                logger.warning(f"Configuration file not found: {self.config_path}")
                self._config = self._load_default_config()
                self.save_config()  # Save default config for user

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            logger.info("Loading default configuration")
            self._config = self._load_default_config()

        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            logger.info("Loading default configuration")
            self._config = self._load_default_config()

        return self._config

    def _load_default_config(self) -> MenuConfig:
        """Load default configuration from fallback file."""
        try:
            if self.fallback_path.exists():
                with open(self.fallback_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.info(f"Loaded default configuration from {self.fallback_path}")
                return MenuConfig.from_dict(data)
            else:
                logger.warning("Default configuration file not found, creating minimal config")
                return self._create_minimal_config()
        except Exception as e:
            logger.error(f"Error loading default configuration: {e}")
            return self._create_minimal_config()

    def _create_minimal_config(self) -> MenuConfig:
        """Create a minimal configuration for fallback."""
        return MenuConfig(
            title="Fredon Menu",
            icon="/usr/share/icons/hicolor/256x256/apps/fredon-menu.png",
            quote="Your productivity companion",
            glass_effect=True,
        )

    def save_config(self) -> bool:
        """
        Save current configuration to file.

        Returns:
            bool: True if successful, False otherwise
        """
        if self._config is None:
            logger.error("No configuration to save")
            return False

        try:
            # Create backup of existing config
            if self.config_path.exists():
                backup_path = self.config_path.with_suffix('.json.backup')
                self.config_path.rename(backup_path)
                logger.info(f"Created backup: {backup_path}")

            # Save new configuration
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config.to_dict(), f, indent=2, ensure_ascii=False)

            logger.info(f"Saved configuration to {self.config_path}")
            return True

        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False

    def reload_config(self) -> bool:
        """
        Reload configuration from file.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            old_config = self._config
            self._config = self.load_config()

            # Only notify if configuration actually changed
            if old_config != self._config:
                self._notify_callbacks()
                logger.info("Configuration reloaded and callbacks notified")

            return True

        except Exception as e:
            logger.error(f"Error reloading configuration: {e}")
            return False

    def get_config(self) -> MenuConfig:
        """
        Get current configuration.

        Returns:
            MenuConfig: Current configuration
        """
        if self._config is None:
            self._config = self.load_config()
        return self._config

    def update_config(self, **kwargs) -> bool:
        """
        Update configuration with new values.

        Args:
            **kwargs: Configuration values to update

        Returns:
            bool: True if successful, False otherwise
        """
        if self._config is None:
            self._config = self.load_config()

        try:
            # Update configuration (simplified - in real implementation would be more sophisticated)
            for key, value in kwargs.items():
                if hasattr(self._config, key):
                    setattr(self._config, key, value)

            return self.save_config()

        except Exception as e:
            logger.error(f"Error updating configuration: {e}")
            return False

    def start_monitoring(self):
        """Start monitoring configuration file for changes."""
        if self._observer is not None:
            logger.warning("Configuration monitoring already started")
            return

        try:
            self._observer = Observer()
            event_handler = ConfigFileHandler(self)

            # Watch the directory containing the config file
            self._observer.schedule(
                event_handler,
                str(self.config_path.parent),
                recursive=False
            )

            self._observer.start()
            logger.info(f"Started monitoring configuration file: {self.config_path}")

        except Exception as e:
            logger.error(f"Error starting configuration monitoring: {e}")
            self._observer = None

    def stop_monitoring(self):
        """Stop monitoring configuration file for changes."""
        if self._observer is not None:
            try:
                self._observer.stop()
                self._observer.join(timeout=5)
                logger.info("Stopped configuration file monitoring")
            except Exception as e:
                logger.error(f"Error stopping configuration monitoring: {e}")
            finally:
                self._observer = None

    def __del__(self):
        """Cleanup when object is destroyed."""
        self.stop_monitoring()