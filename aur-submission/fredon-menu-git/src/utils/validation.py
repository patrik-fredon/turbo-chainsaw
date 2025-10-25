"""
Configuration validation utilities for Fredon Menu
"""

import jsonschema
import logging
from typing import Dict, Any, List, Optional
import json
import os

logger = logging.getLogger(__name__)


class ConfigValidationError(Exception):
    """Configuration validation error."""

    def __init__(self, message: str, field: Optional[str] = None,
                 value: Optional[Any] = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(self.message)


class ConfigValidator:
    """Validates configuration against schema and business rules."""

    # JSON schema for configuration validation
    SCHEMA = {
        "type": "object",
        "required": ["menu", "buttons"],
        "properties": {
            "menu": {
                "type": "object",
                "required": ["title", "icon"],
                "properties": {
                    "title": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 100
                    },
                    "icon": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 500
                    },
                    "quote": {
                        "type": "string",
                        "maxLength": 200
                    },
                    "glass_effect": {
                        "type": "boolean"
                    },
                    "theme": {
                        "type": "object",
                        "properties": {
                            "background_opacity": {
                                "type": "number",
                                "minimum": 0.0,
                                "maximum": 1.0
                            },
                            "blur_radius": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 100
                            },
                            "border_radius": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 50
                            },
                            "hover_duration": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 2000
                            },
                            "colors": {
                                "type": "object",
                                "patternProperties": {
                                    "^[a-zA-Z_]+$": {
                                        "type": "string",
                                        "pattern": "^#[0-9a-fA-F]{6}$"
                                    }
                                }
                            },
                            "fonts": {
                                "type": "object",
                                "properties": {
                                    "title_family": {"type": "string"},
                                    "title_size": {
                                        "type": "integer",
                                        "minimum": 8,
                                        "maximum": 72
                                    },
                                    "button_family": {"type": "string"},
                                    "button_size": {
                                        "type": "integer",
                                        "minimum": 8,
                                        "maximum": 48
                                    },
                                    "quote_family": {"type": "string"},
                                    "quote_size": {
                                        "type": "integer",
                                        "minimum": 8,
                                        "maximum": 36
                                    }
                                }
                            }
                        }
                    },
                    "performance": {
                        "type": "object",
                        "properties": {
                            "cache_enabled": {"type": "boolean"},
                            "cache_size_mb": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 1000
                            },
                            "preload_icons": {"type": "boolean"},
                            "lazy_loading": {"type": "boolean"},
                            "max_concurrent_loads": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 20
                            }
                        }
                    }
                }
            },
            "buttons": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "name", "icon", "command", "type"],
                    "properties": {
                        "id": {
                            "type": "string",
                            "pattern": "^[a-zA-Z0-9_-]+$",
                            "minLength": 1,
                            "maxLength": 50
                        },
                        "name": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 50
                        },
                        "icon": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 500
                        },
                        "command": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 500
                        },
                        "type": {
                            "enum": ["shell", "npm", "python", "app"]
                        },
                        "description": {
                            "type": "string",
                            "maxLength": 100
                        },
                        "enabled": {"type": "boolean"},
                        "category_id": {
                            "type": "string",
                            "pattern": "^[a-zA-Z0-9_-]*$",
                            "maxLength": 50
                        },
                        "position": {
                            "type": "integer",
                            "minimum": 0
                        }
                    }
                },
                "minItems": 0,
                "maxItems": 200
            },
            "categories": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "name", "icon", "description"],
                    "properties": {
                        "id": {
                            "type": "string",
                            "pattern": "^[a-zA-Z0-9_-]+$",
                            "minLength": 1,
                            "maxLength": 50
                        },
                        "name": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 30
                        },
                        "icon": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 500
                        },
                        "description": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 100
                        },
                        "button_ids": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "pattern": "^[a-zA-Z0-9_-]+$"
                            },
                            "uniqueItems": True
                        },
                        "enabled": {"type": "boolean"},
                        "position": {
                            "type": "integer",
                            "minimum": 0
                        }
                    }
                },
                "maxItems": 50
            }
        }
    }

    @classmethod
    def validate_config(cls, config_data: Dict[str, Any]) -> List[ConfigValidationError]:
        """
        Validate configuration data against schema and business rules.

        Args:
            config_data: Configuration dictionary to validate

        Returns:
            List[ConfigValidationError]: List of validation errors (empty if valid)
        """
        errors = []

        # Schema validation
        try:
            jsonschema.validate(config_data, cls.SCHEMA)
        except jsonschema.ValidationError as e:
            errors.append(ConfigValidationError(
                message=f"Schema validation failed: {e.message}",
                field=e.absolute_path if hasattr(e, 'absolute_path') else None,
                value=e.instance if hasattr(e, 'instance') else None
            ))
            return errors

        # Business rule validations
        errors.extend(cls._validate_business_rules(config_data))

        return errors

    @classmethod
    def _validate_business_rules(cls, config_data: Dict[str, Any]) -> List[ConfigValidationError]:
        """Validate business rules that go beyond JSON schema."""
        errors = []

        # Validate button uniqueness
        button_ids = set()
        buttons = config_data.get("buttons", [])
        for i, button in enumerate(buttons):
            button_id = button.get("id")
            if button_id in button_ids:
                errors.append(ConfigValidationError(
                    message=f"Duplicate button ID: {button_id}",
                    field=f"buttons[{i}].id",
                    value=button_id
                ))
            else:
                button_ids.add(button_id)

        # Validate category uniqueness
        category_ids = set()
        categories = config_data.get("categories", [])
        for i, category in enumerate(categories):
            category_id = category.get("id")
            if category_id in category_ids:
                errors.append(ConfigValidationError(
                    message=f"Duplicate category ID: {category_id}",
                    field=f"categories[{i}].id",
                    value=category_id
                ))
            else:
                category_ids.add(category_id)

        # Validate category references
        for i, button in enumerate(buttons):
            category_id = button.get("category_id")
            if category_id and category_id not in category_ids:
                errors.append(ConfigValidationError(
                    message=f"Button references non-existent category: {category_id}",
                    field=f"buttons[{i}].category_id",
                    value=category_id
                ))

        # Validate category button references
        for i, category in enumerate(categories):
            button_ids = category.get("button_ids", [])
            for button_id in button_ids:
                if button_id not in {b.get("id") for b in buttons}:
                    errors.append(ConfigValidationError(
                        message=f"Category references non-existent button: {button_id}",
                        field=f"categories[{i}].button_ids",
                        value=button_id
                    ))

        # Validate icon paths
        all_icons = []
        all_icons.append(config_data.get("menu", {}).get("icon"))
        for button in buttons:
            all_icons.append(button.get("icon"))
        for category in categories:
            all_icons.append(category.get("icon"))

        for i, icon_path in enumerate(all_icons):
            if icon_path and not cls._is_valid_icon_path(icon_path):
                errors.append(ConfigValidationError(
                    message=f"Invalid icon path or unsupported format: {icon_path}",
                    field="icon",
                    value=icon_path
                ))

        return errors

    @classmethod
    def _is_valid_icon_path(cls, icon_path: str) -> bool:
        """Check if icon path is valid."""
        if not icon_path:
            return False

        # Check if file exists
        if not os.path.exists(icon_path):
            # Check if it's a theme icon name (no directory separators)
            if '/' not in icon_path and '\\' not in icon_path:
                return True  # Assume theme icon
            return False

        # Check file extension
        valid_extensions = ['.png', '.svg', '.ico', '.jpg', '.jpeg']
        _, ext = os.path.splitext(icon_path.lower())
        return ext in valid_extensions

    @classmethod
    def validate_and_fix_config(cls, config_data: Dict[str, Any]) -> tuple[Dict[str, Any], List[ConfigValidationError]]:
        """
        Validate config and attempt to fix common issues.

        Args:
            config_data: Configuration dictionary

        Returns:
            tuple[Dict[str, Any], List[ConfigValidationError]]: (fixed_config, errors)
        """
        errors = cls.validate_config(config_data)
        fixed_config = config_data.copy()

        # Attempt to fix some common issues
        fixed_errors = []
        for error in errors:
            if cls._attempt_fix(fixed_config, error):
                logger.info(f"Auto-fixed configuration issue: {error.message}")
            else:
                fixed_errors.append(error)

        return fixed_config, fixed_errors

    @classmethod
    def _attempt_fix(cls, config_data: Dict[str, Any], error: ConfigValidationError) -> bool:
        """Attempt to fix a configuration error."""
        field = error.field
        if not field:
            return False

        # Fix missing optional fields with defaults
        if field == "menu.glass_effect" and "glass_effect" not in config_data.get("menu", {}):
            config_data.setdefault("menu", {})["glass_effect"] = True
            return True

        if field == "menu.theme" and "theme" not in config_data.get("menu", {}):
            config_data.setdefault("menu", {})["theme"] = {}
            return True

        # Add more auto-fixes as needed
        return False

    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """Get the JSON schema."""
        return cls.SCHEMA.copy()