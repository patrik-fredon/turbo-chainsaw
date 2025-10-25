# Implementation Examples and Configuration Templates

This document provides concrete implementation examples, configuration templates, and code patterns for the Fredon Menu launcher based on the best practices research.

## Configuration Examples

### Complete Configuration Template

```json
{
  "$schema": "https://fredon-menu.org/schema/v1",
  "version": "1.0",
  "menu": {
    "title": "Fredon Menu",
    "mainIcon": "~/.config/fredon-menu/icons/fredon-logo.svg",
    "quote": "Launch applications with style and efficiency",
    "itemsPerPage": 10,
    "theme": {
      "name": "glass-dark",
      "blurRadius": 20,
      "opacity": 0.85,
      "primaryColor": "#6495ED",
      "textColor": "#FFFFFF",
      "borderRadius": 20
    },
    "hotkeys": {
      "toggle": "Super+Space",
      "quit": "Escape",
      "search": "/",
      "navigation": {
        "up": "k",
        "down": "j",
        "pageUp": "u",
        "pageDown": "d",
        "select": "Enter",
        "back": "Backspace"
      }
    }
  },
  "categories": [
    {
      "id": "development",
      "name": "Development",
      "description": "Development tools and IDEs",
      "icon": "~/.config/fredon-menu/icons/categories/dev.svg",
      "color": "#4CAF50"
    },
    {
      "id": "multimedia",
      "name": "Multimedia",
      "description": "Audio and video applications",
      "icon": "~/.config/fredon-menu/icons/categories/media.svg",
      "color": "#FF9800"
    },
    {
      "id": "gaming",
      "name": "Gaming",
      "description": "Games and gaming platforms",
      "icon": "~/.config/fredon-menu/icons/categories/gaming.svg",
      "color": "#9C27B0"
    },
    {
      "id": "utilities",
      "name": "Utilities",
      "description": "System utilities and tools",
      "icon": "~/.config/fredon-menu/icons/categories/utilities.svg",
      "color": "#607D8B"
    }
  ],
  "applications": [
    {
      "id": "vscode",
      "name": "Visual Studio Code",
      "icon": "~/.config/fredon-menu/icons/apps/vscode.png",
      "command": "code",
      "type": "app",
      "category": "development",
      "description": "Code editing. Redefined.",
      "keywords": ["editor", "code", "programming"]
    },
    {
      "id": "firefox",
      "name": "Firefox",
      "icon": "~/.config/fredon-menu/icons/apps/firefox.svg",
      "command": "firefox",
      "type": "app",
      "description": "Web browser",
      "keywords": ["browser", "web", "internet"]
    },
    {
      "id": "terminal",
      "name": "Terminal",
      "icon": "~/.config/fredon-menu/icons/apps/terminal.svg",
      "command": "kitty",
      "type": "app",
      "description": "Terminal emulator",
      "keywords": ["terminal", "shell", "command"]
    },
    {
      "id": "spotify",
      "name": "Spotify",
      "icon": "~/.config/fredon-menu/icons/apps/spotify.svg",
      "command": "spotify",
      "type": "app",
      "category": "multimedia",
      "description": "Music streaming",
      "keywords": ["music", "streaming", "audio"]
    },
    {
      "id": "obsidian",
      "name": "Obsidian",
      "icon": "~/.config/fredon-menu/icons/apps/obsidian.png",
      "command": "obsidian",
      "type": "app",
      "category": "development",
      "description": "Knowledge management",
      "keywords": ["notes", "knowledge", "markdown"]
    },
    {
      "id": "npm-dev",
      "name": "NPM Dev Server",
      "icon": "~/.config/fredon-menu/icons/apps/npm.svg",
      "command": "npm run dev",
      "type": "shell",
      "workingDirectory": "~/projects/current",
      "category": "development",
      "description": "Start development server",
      "keywords": ["node", "npm", "development"]
    },
    {
      "id": "steam",
      "name": "Steam",
      "icon": "~/.config/fredon-menu/icons/apps/steam.svg",
      "command": "steam",
      "type": "app",
      "category": "gaming",
      "description": "Gaming platform",
      "keywords": ["games", "gaming", "steam"]
    }
  ]
}
```

### Minimal Configuration Example

```json
{
  "$schema": "https://fredon-menu.org/schema/v1",
  "version": "1.0",
  "menu": {
    "title": "Simple Menu",
    "mainIcon": "~/.config/fredon-menu/icons/menu.svg",
    "quote": "Quick launcher"
  },
  "applications": [
    {
      "id": "browser",
      "name": "Web Browser",
      "icon": "firefox",
      "command": "firefox",
      "type": "app"
    },
    {
      "id": "terminal",
      "name": "Terminal",
      "icon": "terminal",
      "command": "kitty",
      "type": "app"
    }
  ]
}
```

## Core Implementation Patterns

### Configuration Manager Implementation

```python
import json
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class MenuConfig:
    title: str = "Fredon Menu"
    main_icon: str = ""
    quote: str = ""
    items_per_page: int = 10
    theme: Dict[str, Any] = field(default_factory=dict)
    hotkeys: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Category:
    id: str
    name: str
    description: str = ""
    icon: str = ""
    color: str = ""

@dataclass
class Application:
    id: str
    name: str
    icon: str
    command: str
    type: str = "app"
    category: Optional[str] = None
    description: str = ""
    keywords: list = field(default_factory=list)
    working_directory: Optional[str] = None

class ConfigurationManager:
    def __init__(self, config_path: str = None):
        self.config_path = config_path or self._get_default_config_path()
        self._config_cache = None
        self._last_modified = 0
        self.logger = logging.getLogger(__name__)

    def _get_default_config_path(self) -> str:
        return str(Path("~/.config/fredon-menu/config.json").expanduser())

    def load_config(self) -> tuple[MenuConfig, list[Category], list[Application]]:
        """Load and validate configuration"""
        if self._config_changed():
            self._reload_config()

        return self._config_cache

    def _config_changed(self) -> bool:
        """Check if configuration file has been modified"""
        try:
            current_mtime = os.path.getmtime(self.config_path)
            if current_mtime > self._last_modified:
                self._last_modified = current_mtime
                return True
        except FileNotFoundError:
            self.logger.warning(f"Config file not found: {self.config_path}")
            return True  # Force reload to create default config
        return False

    def _reload_config(self):
        """Reload configuration from file"""
        try:
            config_data = self._load_config_file()
            validated_config = self._validate_and_normalize(config_data)
            self._config_cache = self._parse_config(validated_config)
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            self._config_cache = self._get_default_config()

    def _load_config_file(self) -> Dict[str, Any]:
        """Load raw configuration from file"""
        if not os.path.exists(self.config_path):
            self.logger.info("Creating default configuration")
            return self._create_default_config_data()

        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _validate_and_normalize(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate configuration structure and normalize values"""
        # Ensure required sections exist
        config_data.setdefault('menu', {})
        config_data.setdefault('categories', [])
        config_data.setdefault('applications', [])

        # Normalize menu configuration
        menu_config = config_data['menu']
        menu_config.setdefault('title', 'Fredon Menu')
        menu_config.setdefault('mainIcon', '')
        menu_config.setdefault('quote', '')
        menu_config.setdefault('itemsPerPage', 10)

        # Normalize paths
        if menu_config.get('mainIcon'):
            menu_config['mainIcon'] = os.path.expanduser(menu_config['mainIcon'])

        # Normalize categories
        for category in config_data['categories']:
            if 'icon' in category:
                category['icon'] = os.path.expanduser(category['icon'])

        # Normalize applications
        for app in config_data['applications']:
            if 'icon' in app:
                app['icon'] = os.path.expanduser(app['icon'])
            if 'workingDirectory' in app:
                app['workingDirectory'] = os.path.expanduser(app['workingDirectory'])

        return config_data

    def _parse_config(self, config_data: Dict[str, Any]) -> tuple[MenuConfig, list[Category], list[Application]]:
        """Parse configuration data into data classes"""
        # Parse menu config
        menu_data = config_data['menu']
        menu_config = MenuConfig(
            title=menu_data.get('title', 'Fredon Menu'),
            main_icon=menu_data.get('mainIcon', ''),
            quote=menu_data.get('quote', ''),
            items_per_page=menu_data.get('itemsPerPage', 10),
            theme=menu_data.get('theme', {}),
            hotkeys=menu_data.get('hotkeys', {})
        )

        # Parse categories
        categories = [
            Category(
                id=cat['id'],
                name=cat['name'],
                description=cat.get('description', ''),
                icon=cat.get('icon', ''),
                color=cat.get('color', '')
            )
            for cat in config_data['categories']
        ]

        # Parse applications
        applications = [
            Application(
                id=app['id'],
                name=app['name'],
                icon=app['icon'],
                command=app['command'],
                type=app.get('type', 'app'),
                category=app.get('category'),
                description=app.get('description', ''),
                keywords=app.get('keywords', []),
                working_directory=app.get('workingDirectory')
            )
            for app in config_data['applications']
        ]

        return menu_config, categories, applications

    def _create_default_config_data(self) -> Dict[str, Any]:
        """Create default configuration data"""
        default_config = {
            "$schema": "https://fredon-menu.org/schema/v1",
            "version": "1.0",
            "menu": {
                "title": "Fredon Menu",
                "mainIcon": "",
                "quote": "Launch applications with style",
                "itemsPerPage": 10
            },
            "categories": [],
            "applications": []
        }

        # Save default config
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)

        return default_config

    def _get_default_config(self) -> tuple[MenuConfig, list[Category], list[Application]]:
        """Get default configuration when loading fails"""
        return MenuConfig(), [], []
```

### Secure Command Executor

```python
import subprocess
import shlex
import logging
import re
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class ExecutionResult:
    success: bool
    process: Optional[subprocess.Popen] = None
    error_message: Optional[str] = None

class SecurityError(Exception):
    """Raised when a security violation is detected"""
    pass

class CommandExecutor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._allowed_command_patterns = [
            r'^[a-zA-Z0-9._/:-]+$',
            r'^npm\s+',
            r'^python\s+',
            r'^python3\s+',
            r'^node\s+'
        ]

    def execute(self, application: Application) -> ExecutionResult:
        """Execute application command securely"""
        try:
            # Validate command security
            self._validate_command(application.command, application.type)

            # Build command based on type
            command_parts = self._build_command(application)

            # Execute with appropriate method
            process = self._execute_command(command_parts, application)

            return ExecutionResult(success=True, process=process)

        except SecurityError as e:
            error_msg = f"Security violation: {e}"
            self.logger.error(error_msg)
            return ExecutionResult(success=False, error_message=error_msg)

        except Exception as e:
            error_msg = f"Execution failed: {e}"
            self.logger.error(error_msg)
            return ExecutionResult(success=False, error_message=error_msg)

    def _validate_command(self, command: str, command_type: str):
        """Validate command for security"""
        # Check for dangerous patterns
        dangerous_patterns = [
            r'[;&|`$()]',  # Shell metacharacters
            r'\.\./',      # Directory traversal
            r'~/.*\.\./',  # Home directory traversal
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, command):
                raise SecurityError(f"Dangerous pattern detected: {pattern}")

        # Validate against allowed patterns
        command_allowed = False
        for pattern in self._allowed_command_patterns:
            if re.match(pattern, command):
                command_allowed = True
                break

        if not command_allowed and command_type not in ['shell']:
            raise SecurityError(f"Command not allowed: {command}")

    def _build_command(self, application: Application) -> List[str]:
        """Build command parts based on application type"""
        command = application.command
        command_type = application.type

        if command_type == 'app':
            return [command]

        elif command_type == 'shell':
            # For shell commands, use bash -c for consistency
            return ['bash', '-c', command]

        elif command_type == 'npm':
            return ['npm', 'run', command]

        elif command_type == 'python':
            return ['python3', command]

        elif command_type == 'python':
            return ['python', command]

        else:
            raise ValueError(f"Unknown command type: {command_type}")

    def _execute_command(self, command_parts: List[str], application: Application) -> subprocess.Popen:
        """Execute command with proper environment and working directory"""
        env = os.environ.copy()
        cwd = None

        # Set working directory if specified
        if application.working_directory:
            cwd = os.path.expanduser(application.working_directory)
            if not os.path.exists(cwd):
                self.logger.warning(f"Working directory does not exist: {cwd}")
                cwd = None

        try:
            process = subprocess.Popen(
                command_parts,
                cwd=cwd,
                env=env,
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL
            )

            # Check if process started successfully
            import time
            time.sleep(0.1)  # Small delay to check immediate failure

            if process.poll() is not None:
                raise RuntimeError(f"Process exited immediately with code {process.returncode}")

            return process

        except FileNotFoundError:
            raise RuntimeError(f"Command not found: {command_parts[0]}")
        except PermissionError:
            raise RuntimeError(f"Permission denied: {command_parts[0]}")
```

### Icon Management System

```python
import os
import logging
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
from PIL import Image, ImageDraw
import cairosvg
from dataclasses import dataclass

@dataclass
class IconCacheEntry:
    path: str
    size: int
    last_modified: float
    data: Any

class IconManager:
    def __init__(self, cache_dir: str = None, max_memory_mb: int = 50):
        self.cache_dir = Path(cache_dir or "~/.cache/fredon-menu/icons").expanduser()
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.memory_cache: Dict[str, IconCacheEntry] = {}
        self.cache_index_file = self.cache_dir / 'cache_index.json'

        self.logger = logging.getLogger(__name__)

        # Icon search paths
        self.icon_paths = [
            "~/.local/share/icons",
            "/usr/share/icons",
            "/usr/share/pixmaps",
            "~/.config/fredon-menu/icons"
        ]

        self._load_cache_index()

    def get_icon(self, icon_path: str, size: int = 64) -> Optional[Any]:
        """Get icon with caching support"""
        cache_key = self._get_cache_key(icon_path, size)

        # Check memory cache first
        if cache_key in self.memory_cache:
            entry = self.memory_cache[cache_key]
            if self._is_cache_valid(entry):
                return entry.data
            else:
                del self.memory_cache[cache_key]

        # Check disk cache
        disk_cache_path = self._get_disk_cache_path(icon_path, size)
        if disk_cache_path.exists():
            cached_data = self._load_from_disk_cache(disk_cache_path)
            if cached_data:
                self._add_to_memory_cache(cache_key, icon_path, size, cached_data)
                return cached_data

        # Load and process original icon
        original_icon = self._load_original_icon(icon_path)
        if original_icon:
            resized_icon = self._resize_icon(original_icon, size)

            # Cache the result
            self._save_to_disk_cache(disk_cache_path, resized_icon)
            self._add_to_memory_cache(cache_key, icon_path, size, resized_icon)

            return resized_icon

        # Fallback to default icon
        return self._create_default_icon(size)

    def _get_cache_key(self, icon_path: str, size: int) -> str:
        """Generate cache key for icon"""
        return f"{icon_path}:{size}"

    def _get_disk_cache_path(self, icon_path: str, size: int) -> Path:
        """Get disk cache file path"""
        # Create safe filename from icon path
        safe_name = hashlib.md5(icon_path.encode()).hexdigest()
        return self.cache_dir / f"{safe_name}_{size}.png"

    def _load_original_icon(self, icon_path: str) -> Optional[Any]:
        """Load original icon file"""
        expanded_path = os.path.expanduser(icon_path)

        # Try direct path first
        if os.path.exists(expanded_path):
            return self._load_icon_file(expanded_path)

        # Try icon theme lookup
        theme_icon = self._lookup_theme_icon(icon_path)
        if theme_icon:
            return self._load_icon_file(theme_icon)

        # Try different extensions
        base_path = os.path.splitext(expanded_path)[0]
        for ext in ['.svg', '.png', '.ico', '.xpm']:
            test_path = base_path + ext
            if os.path.exists(test_path):
                return self._load_icon_file(test_path)

        return None

    def _load_icon_file(self, file_path: str) -> Optional[Any]:
        """Load icon from file path"""
        try:
            if file_path.endswith('.svg'):
                # Convert SVG to PNG
                png_data = cairosvg.svg2png(url=file_path)
                return Image.open(io.BytesIO(png_data))
            else:
                return Image.open(file_path)
        except Exception as e:
            self.logger.debug(f"Failed to load icon {file_path}: {e}")
            return None

    def _lookup_theme_icon(self, icon_name: str) -> Optional[str]:
        """Look up icon in system theme"""
        # This would implement freedesktop icon theme lookup
        # For now, return None
        return None

    def _resize_icon(self, original_icon: Any, size: int) -> Any:
        """Resize icon to specified size"""
        try:
            # Convert to RGBA if needed
            if original_icon.mode != 'RGBA':
                original_icon = original_icon.convert('RGBA')

            # Resize with high quality
            resized = original_icon.resize((size, size), Image.Resampling.LANCZOS)
            return resized
        except Exception as e:
            self.logger.error(f"Failed to resize icon: {e}")
            return self._create_default_icon(size)

    def _create_default_icon(self, size: int) -> Any:
        """Create default icon when original fails to load"""
        try:
            # Create a simple rounded square as default
            image = Image.new('RGBA', (size, size), (100, 100, 100, 200))
            draw = ImageDraw.Draw(image)

            # Draw rounded rectangle
            margin = size // 8
            draw.rounded_rectangle(
                [margin, margin, size - margin, size - margin],
                radius=size // 6,
                fill=(150, 150, 150, 200)
            )

            # Add simple question mark
            font_size = size // 2
            draw.text(
                (size // 2, size // 2),
                "?",
                fill=(255, 255, 255, 255),
                anchor="mm"
            )

            return image
        except Exception as e:
            self.logger.error(f"Failed to create default icon: {e}")
            # Return a simple colored square as last resort
            return Image.new('RGBA', (size, size), (128, 128, 128, 255))

    def _add_to_memory_cache(self, cache_key: str, icon_path: str, size: int, data: Any):
        """Add icon to memory cache"""
        # Check memory usage and clean if needed
        self._cleanup_memory_cache()

        entry = IconCacheEntry(
            path=icon_path,
            size=size,
            last_modified=os.path.getmtime(icon_path) if os.path.exists(icon_path) else 0,
            data=data
        )

        self.memory_cache[cache_key] = entry

    def _cleanup_memory_cache(self):
        """Clean memory cache if it exceeds size limit"""
        # Estimate memory usage (rough approximation)
        estimated_size = len(self.memory_cache) * 1024 * 64  # Assume 64KB per icon

        if estimated_size > self.max_memory_bytes:
            # Remove oldest entries (simple LRU)
            # For now, just clear half the cache
            entries_to_remove = len(self.memory_cache) // 2
            keys_to_remove = list(self.memory_cache.keys())[:entries_to_remove]

            for key in keys_to_remove:
                del self.memory_cache[key]

    def _is_cache_valid(self, entry: IconCacheEntry) -> bool:
        """Check if cache entry is still valid"""
        if not os.path.exists(entry.path):
            return False

        current_mtime = os.path.getmtime(entry.path)
        return current_mtime <= entry.last_modified

    def _load_from_disk_cache(self, cache_path: Path) -> Optional[Any]:
        """Load icon from disk cache"""
        try:
            return Image.open(cache_path)
        except Exception as e:
            self.logger.debug(f"Failed to load from disk cache {cache_path}: {e}")
            return None

    def _save_to_disk_cache(self, cache_path: Path, icon_data: Any):
        """Save icon to disk cache"""
        try:
            icon_data.save(cache_path, 'PNG')
        except Exception as e:
            self.logger.debug(f"Failed to save to disk cache {cache_path}: {e}")

    def _load_cache_index(self):
        """Load cache index from disk"""
        # This would load metadata about cached icons
        # For now, keep it simple
        pass
```

## Menu Rendering Patterns

### Glass Effect CSS (for web-based implementation)

```css
/* Glass menu container */
.fredon-menu {
    background: rgba(10, 10, 20, 0.85);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    box-shadow:
        0 25px 50px rgba(0, 0, 0, 0.4),
        0 0 0 1px rgba(255, 255, 255, 0.05),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
    overflow: hidden;
    min-width: 400px;
    max-width: 600px;
    animation: menuAppear 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes menuAppear {
    from {
        opacity: 0;
        transform: scale(0.9) translateY(20px);
        filter: blur(10px);
    }
    to {
        opacity: 1;
        transform: scale(1) translateY(0);
        filter: blur(0);
    }
}

/* Menu header with main icon */
.menu-header {
    text-align: center;
    padding: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.main-icon {
    width: 80px;
    height: 80px;
    margin-bottom: 10px;
    filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
    transition: transform 0.3s ease;
}

.main-icon:hover {
    transform: scale(1.05) rotate(5deg);
}

/* Button styles */
.menu-button {
    display: flex;
    align-items: center;
    padding: 12px 16px;
    margin: 6px 12px;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    color: white;
    text-decoration: none;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.menu-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    transition: left 0.5s ease;
}

.menu-button:hover::before {
    left: 100%;
}

.menu-button:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateY(-2px) scale(1.02);
    box-shadow:
        0 10px 25px rgba(0, 0, 0, 0.2),
        0 0 20px rgba(100, 200, 255, 0.3);
    border-color: rgba(100, 200, 255, 0.5);
}

.menu-button:active {
    transform: translateY(0) scale(0.98);
    transition: all 0.1s ease;
}

.button-icon {
    width: 32px;
    height: 32px;
    margin-right: 12px;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.1);
    padding: 4px;
}

.button-text {
    flex: 1;
    font-size: 14px;
    font-weight: 500;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

/* Category button variant */
.category-button {
    background: linear-gradient(135deg, rgba(100, 200, 255, 0.1), rgba(150, 100, 255, 0.1));
    border: 1px solid rgba(150, 200, 255, 0.3);
}

.category-button:hover {
    background: linear-gradient(135deg, rgba(100, 200, 255, 0.2), rgba(150, 100, 255, 0.2));
    border-color: rgba(150, 200, 255, 0.6);
}

/* Pagination controls */
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 16px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    gap: 12px;
}

.page-button {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 8px 16px;
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 12px;
}

.page-button:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-1px);
}

.page-button:disabled {
    opacity: 0.3;
    cursor: not-allowed;
}

.page-info {
    color: rgba(255, 255, 255, 0.7);
    font-size: 12px;
    min-width: 60px;
    text-align: center;
}

/* Menu footer with quote */
.menu-footer {
    text-align: center;
    padding: 16px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    font-style: italic;
    color: rgba(255, 255, 255, 0.6);
    font-size: 13px;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

/* Search input */
.search-input {
    width: calc(100% - 24px);
    margin: 12px;
    padding: 12px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    color: white;
    font-size: 14px;
    outline: none;
    transition: all 0.2s ease;
}

.search-input::placeholder {
    color: rgba(255, 255, 255, 0.5);
}

.search-input:focus {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(100, 200, 255, 0.5);
    box-shadow: 0 0 15px rgba(100, 200, 255, 0.2);
}

/* Keyboard navigation hint */
.keyboard-hint {
    position: absolute;
    bottom: 8px;
    right: 8px;
    font-size: 10px;
    color: rgba(255, 255, 255, 0.4);
    background: rgba(0, 0, 0, 0.3);
    padding: 4px 8px;
    border-radius: 4px;
}

/* Responsive design */
@media (max-width: 480px) {
    .fredon-menu {
        min-width: 320px;
        margin: 20px;
    }

    .menu-button {
        padding: 10px 12px;
        margin: 4px 8px;
    }

    .button-icon {
        width: 28px;
        height: 28px;
    }

    .main-icon {
        width: 60px;
        height: 60px;
    }
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

@media (prefers-contrast: high) {
    .fredon-menu {
        background: rgba(0, 0, 0, 0.95);
        border: 2px solid white;
    }

    .menu-button {
        background: rgba(255, 255, 255, 0.2);
        border: 2px solid white;
    }
}
```

## Performance Monitoring Implementation

```python
import time
import psutil
import logging
from typing import Dict, Any
from dataclasses import dataclass, field
from threading import Thread, Event

@dataclass
class PerformanceMetrics:
    startup_time: float = 0.0
    config_load_time: float = 0.0
    icon_load_time: float = 0.0
    render_time: float = 0.0
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    frame_rate: float = 0.0

class PerformanceMonitor:
    def __init__(self):
        self.metrics = PerformanceMetrics()
        self.startup_start_time = None
        self.logger = logging.getLogger(__name__)
        self.monitoring = False
        self.monitor_thread = None
        self.stop_event = Event()

    def start_startup_timing(self):
        """Start timing the application startup"""
        self.startup_start_time = time.time()
        self.monitoring = True
        self.monitor_thread = Thread(target=self._monitor_performance, daemon=True)
        self.monitor_thread.start()

    def finish_startup_timing(self):
        """Finish timing and log startup metrics"""
        if self.startup_start_time:
            total_time = time.time() - self.startup_start_time
            self.metrics.startup_time = total_time

            self.logger.info(f"Startup completed in {total_time:.3f}s")
            self._log_performance_summary()

            # Stop monitoring
            self.stop_event.set()
            self.monitoring = False

    def time_config_load(self):
        """Context manager for timing config loading"""
        return PerformanceTimer(self, 'config_load_time')

    def time_icon_load(self):
        """Context manager for timing icon loading"""
        return PerformanceTimer(self, 'icon_load_time')

    def time_render(self):
        """Context manager for timing rendering"""
        return PerformanceTimer(self, 'render_time')

    def _monitor_performance(self):
        """Monitor system performance in background"""
        process = psutil.Process()

        while not self.stop_event.is_set():
            try:
                # Memory usage
                memory_info = process.memory_info()
                self.metrics.memory_usage_mb = memory_info.rss / 1024 / 1024

                # CPU usage
                self.metrics.cpu_usage_percent = process.cpu_percent()

                # Check for performance warnings
                self._check_performance_warnings()

                time.sleep(0.5)  # Monitor every 500ms

            except Exception as e:
                self.logger.debug(f"Performance monitoring error: {e}")
                break

    def _check_performance_warnings(self):
        """Check for performance issues and log warnings"""
        # Memory warnings
        if self.metrics.memory_usage_mb > 100:
            self.logger.warning(f"High memory usage: {self.metrics.memory_usage_mb:.1f}MB")

        # CPU warnings
        if self.metrics.cpu_usage_percent > 50:
            self.logger.warning(f"High CPU usage: {self.metrics.cpu_usage_percent:.1f}%")

    def _log_performance_summary(self):
        """Log comprehensive performance summary"""
        self.logger.info("=== Performance Summary ===")
        self.logger.info(f"Total startup time: {self.metrics.startup_time:.3f}s")
        self.logger.info(f"Config load time: {self.metrics.config_load_time:.3f}s")
        self.logger.info(f"Icon load time: {self.metrics.icon_load_time:.3f}s")
        self.logger.info(f"Render time: {self.metrics.render_time:.3f}s")
        self.logger.info(f"Memory usage: {self.metrics.memory_usage_mb:.1f}MB")
        self.logger.info(f"CPU usage: {self.metrics.cpu_usage_percent:.1f}%")

        # Performance targets check
        self._check_performance_targets()

    def _check_performance_targets(self):
        """Check if performance targets are met"""
        targets_met = True

        if self.metrics.startup_time > 0.5:
            self.logger.warning(f"Startup time target missed: {self.metrics.startup_time:.3f}s > 0.5s")
            targets_met = False

        if self.metrics.memory_usage_mb > 50:
            self.logger.warning(f"Memory target missed: {self.metrics.memory_usage_mb:.1f}MB > 50MB")
            targets_met = False

        if targets_met:
            self.logger.info("All performance targets met! ✓")

@dataclass
class PerformanceTimer:
    monitor: PerformanceMonitor
    metric_name: str

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start_time
        setattr(self.monitor.metrics, self.metric_name, elapsed)
```

## Integration Scripts

### SystemD Service Integration

```ini
# ~/.config/systemd/user/fredon-menu.service
[Unit]
Description=Fredon Menu Application Launcher
Documentation=https://github.com/patrik-fredon/fredon-menu
PartOf=graphical-session.target
After=graphical-session.target

[Service]
Type=simple
ExecStart=/usr/local/bin/fredon-menu --daemon
Restart=on-failure
RestartSec=5
Environment=DISPLAY=:1
Environment=WAYLAND_DISPLAY=wayland-1

# Security settings
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
ProtectKernelTunables=true
ProtectControlGroups=true
RestrictRealtime=true

[Install]
WantedBy=default.target
```

### Desktop Entry for Wayland Integration

```desktop
# ~/.local/share/applications/fredon-menu.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=Fredon Menu
Comment=Fast, customizable application launcher
Exec=fredon-menu --toggle
Icon=fredon-menu
Terminal=false
StartupNotify=false
Categories=Utility;System;
Keywords=launcher;menu;applications;quick;launch;
MimeType=
Actions=Configure;About;

[Desktop Action Configure]
Name=Configure
Exec=fredon-menu --config

[Desktop Action About]
Name=About
Exec=fredon-menu --about
```

### Hyprland Keybind Configuration

```haskell
# ~/.config/hypr/hyprland.conf
# Fredon Menu keybindings

# Toggle menu with Super+Space
bind = $mainMod, Space, exec, fredon-menu --toggle

# Alternative keybindings
bind = $mainMod, Return, exec, fredon-menu --toggle
bind = ALT, F1, exec, fredon-menu --toggle

# Window rules for menu
windowrule = float, ^(fredon-menu)$
windowrule = center, ^(fredon-menu)$
windowrule = noborder, ^(fredon-menu)$
windowrule = noshadow, ^(fredon-menu)$
windowrule = opaque, ^(fredon-menu)$
windowrule = nofocus, ^(fredon-menu)$
windowrule = pin, ^(fredon-menu)$
```

These implementation examples provide a solid foundation for building the Fredon Menu launcher with all the required features, security considerations, and performance optimizations. The code is modular, well-structured, and follows the best practices identified in the research phase.