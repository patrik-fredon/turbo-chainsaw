"""
Data models for Fredon Menu configuration and state management
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from enum import Enum
import json


class CommandType(Enum):
    """Supported command execution types."""
    SHELL = "shell"
    NPM = "npm"
    PYTHON = "python"
    APP = "app"


class IconFormat(Enum):
    """Supported icon formats."""
    PNG = "png"
    SVG = "svg"
    ICO = "ico"
    FALLBACK = "fallback"


class MenuState(Enum):
    """Menu display states."""
    MAIN = "main"
    CATEGORY = "category"
    HIDDEN = "hidden"


@dataclass
class ThemeConfig:
    """Visual appearance settings."""
    background_opacity: float = 0.9
    blur_radius: int = 20
    border_radius: int = 12
    hover_duration: int = 200
    colors: Dict[str, str] = field(default_factory=lambda: {
        "background": "#1a1a1a",
        "text": "#ffffff",
        "button_bg": "#2a2a2a",
        "button_hover": "#3a3a3a",
        "button_text": "#ffffff",
        "border": "#4a4a4a",
    })
    fonts: Dict[str, Any] = field(default_factory=lambda: {
        "title_family": "sans-serif",
        "title_size": 24,
        "button_family": "sans-serif",
        "button_size": 14,
        "quote_family": "serif",
        "quote_size": 12,
    })


@dataclass
class PerformanceConfig:
    """Performance optimization settings."""
    cache_enabled: bool = True
    cache_size_mb: int = 50
    preload_icons: bool = True
    lazy_loading: bool = True
    max_concurrent_loads: int = 5


@dataclass
class IconCache:
    """Cached icon data."""
    data: bytes
    format: IconFormat
    size: tuple[int, int]
    last_modified: float


@dataclass
class Button:
    """Represents an application launch button."""
    id: str
    name: str
    icon: str
    command: str
    type: CommandType
    description: Optional[str] = None
    enabled: bool = True
    category_id: Optional[str] = None
    position: int = 0
    icon_cache: Optional[IconCache] = None

    def __post_init__(self):
        """Validate button data after initialization."""
        if not self.id:
            raise ValueError("Button ID is required")
        if not self.name:
            raise ValueError("Button name is required")
        if not self.command:
            raise ValueError("Button command is required")
        if not isinstance(self.type, CommandType):
            self.type = CommandType(self.type)

    def to_dict(self) -> Dict[str, Any]:
        """Convert button to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "command": self.command,
            "type": self.type.value,
            "description": self.description,
            "enabled": self.enabled,
            "category_id": self.category_id,
            "position": self.position,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Button":
        """Create button from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            icon=data["icon"],
            command=data["command"],
            type=CommandType(data["type"]),
            description=data.get("description"),
            enabled=data.get("enabled", True),
            category_id=data.get("category_id"),
            position=data.get("position", 0),
        )


@dataclass
class Category:
    """Represents a button category for organization."""
    id: str
    name: str
    icon: str
    description: str
    button_ids: List[str] = field(default_factory=list)
    enabled: bool = True
    position: int = 0

    def __post_init__(self):
        """Validate category data after initialization."""
        if not self.id:
            raise ValueError("Category ID is required")
        if not self.name:
            raise ValueError("Category name is required")
        if not self.description:
            raise ValueError("Category description is required")

    def to_dict(self) -> Dict[str, Any]:
        """Convert category to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "description": self.description,
            "button_ids": self.button_ids,
            "enabled": self.enabled,
            "position": self.position,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Category":
        """Create category from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            icon=data["icon"],
            description=data["description"],
            button_ids=data.get("button_ids", []),
            enabled=data.get("enabled", True),
            position=data.get("position", 0),
        )


@dataclass
class MenuConfig:
    """Top-level configuration structure for the entire menu system."""
    title: str
    icon: str
    quote: Optional[str] = None
    glass_effect: bool = True
    theme: ThemeConfig = field(default_factory=ThemeConfig)
    buttons: List[Button] = field(default_factory=list)
    categories: List[Category] = field(default_factory=list)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)

    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.title:
            raise ValueError("Menu title is required")
        if not self.icon:
            raise ValueError("Menu icon is required")

    def get_button_by_id(self, button_id: str) -> Optional[Button]:
        """Get button by ID."""
        for button in self.buttons:
            if button.id == button_id:
                return button
        return None

    def get_category_by_id(self, category_id: str) -> Optional[Category]:
        """Get category by ID."""
        for category in self.categories:
            if category.id == category_id:
                return category
        return None

    def get_main_buttons(self) -> List[Button]:
        """Get buttons that appear on the main menu (not in categories)."""
        return [button for button in self.buttons
                if button.enabled and button.category_id is None]

    def get_category_buttons(self, category_id: str) -> List[Button]:
        """Get buttons for a specific category."""
        return [button for button in self.buttons
                if button.enabled and button.category_id == category_id]

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary for JSON serialization."""
        return {
            "menu": {
                "title": self.title,
                "icon": self.icon,
                "quote": self.quote,
                "glass_effect": self.glass_effect,
                "theme": {
                    "background_opacity": self.theme.background_opacity,
                    "blur_radius": self.theme.blur_radius,
                    "border_radius": self.theme.border_radius,
                    "hover_duration": self.theme.hover_duration,
                    "colors": self.theme.colors,
                    "fonts": self.theme.fonts,
                },
                "performance": {
                    "cache_enabled": self.performance.cache_enabled,
                    "cache_size_mb": self.performance.cache_size_mb,
                    "preload_icons": self.performance.preload_icons,
                    "lazy_loading": self.performance.lazy_loading,
                    "max_concurrent_loads": self.performance.max_concurrent_loads,
                },
            },
            "buttons": [button.to_dict() for button in self.buttons],
            "categories": [category.to_dict() for category in self.categories],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MenuConfig":
        """Create configuration from dictionary."""
        menu_data = data.get("menu", {})

        theme_data = menu_data.get("theme", {})
        theme = ThemeConfig(
            background_opacity=theme_data.get("background_opacity", 0.9),
            blur_radius=theme_data.get("blur_radius", 20),
            border_radius=theme_data.get("border_radius", 12),
            hover_duration=theme_data.get("hover_duration", 200),
            colors=theme_data.get("colors", {}),
            fonts=theme_data.get("fonts", {}),
        )

        performance_data = menu_data.get("performance", {})
        performance = PerformanceConfig(
            cache_enabled=performance_data.get("cache_enabled", True),
            cache_size_mb=performance_data.get("cache_size_mb", 50),
            preload_icons=performance_data.get("preload_icons", True),
            lazy_loading=performance_data.get("lazy_loading", True),
            max_concurrent_loads=performance_data.get("max_concurrent_loads", 5),
        )

        return cls(
            title=menu_data.get("title", "Fredon Menu"),
            icon=menu_data.get("icon", ""),
            quote=menu_data.get("quote"),
            glass_effect=menu_data.get("glass_effect", True),
            theme=theme,
            performance=performance,
            buttons=[Button.from_dict(b) for b in data.get("buttons", [])],
            categories=[Category.from_dict(c) for c in data.get("categories", [])],
        )