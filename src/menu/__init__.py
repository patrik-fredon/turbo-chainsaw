"""
Fredon Menu - A modern, customizable application launcher for Hyprland/Wayland
"""

__version__ = "1.0.0"
__author__ = "Fredon Menu Team"
__email__ = "contact@fredon-menu.org"
__description__ = "A modern, customizable application launcher for Hyprland/Wayland"

# Export main classes and functions
from .app import FredonMenu, main
from .models import MenuConfig, Button, Category
from .config import ConfigManager
from .window import MenuWindow
from .button import MenuButton

__all__ = [
    "FredonMenu",
    "main",
    "MenuConfig",
    "Button",
    "Category",
    "ConfigManager",
    "MenuWindow",
    "MenuButton",
]