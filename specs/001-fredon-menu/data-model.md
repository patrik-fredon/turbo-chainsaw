# Data Model: Fredon Menu - Customizable Application Launcher

**Date**: 2025-10-25
**Purpose**: Define data structures and validation rules for menu configuration and application state
**Based on**: [Feature Specification](spec.md) and [Research Findings](research.md)

## Core Data Entities

### 1. Menu Configuration

```python
class MenuConfig:
    """Top-level configuration structure for the entire menu system."""

    title: str                 # Menu display title
    icon: str                 # Path to main menu icon
    quote: str                # Bottom quote text
    glass_effect: bool        # Enable glass visual effects
    theme: ThemeConfig        # Visual theme settings
    buttons: List[Button]     # Main menu buttons
    categories: List[Category] # Category definitions
    performance: PerformanceConfig # Performance settings
```

### 2. Button Entity

```python
class Button:
    """Represents an application launch button."""

    id: str                   # Unique identifier
    name: str                 # Display name
    icon: str                 # Icon file path
    command: str              # Command to execute
    type: CommandType         # shell | npm | python | app
    description: Optional[str] # Tooltip description
    enabled: bool             # Whether button is active
    category_id: Optional[str] # Category assignment (None = main menu)
    position: int             # Display order
    icon_cache: Optional[IconCache] # Cached icon data
```

### 3. Category Entity

```python
class Category:
    """Represents a button category for organization."""

    id: str                   # Unique identifier
    name: str                 # Category display name
    icon: str                 # Category icon path
    description: str          # Category description
    button_ids: List[str]     # Associated button IDs
    enabled: bool             # Whether category is active
    position: int             # Display order
    style: CategoryStyle      # Visual styling
```

### 4. Theme Configuration

```python
class ThemeConfig:
    """Visual appearance settings."""

    background_opacity: float # Background transparency (0.0-1.0)
    blur_radius: int          # Glass blur effect radius
    border_radius: int        # Button corner radius
    hover_duration: int       # Hover animation duration (ms)
    button_size: ButtonSize   # Button dimensions
    colors: ColorScheme       # Color palette
    fonts: FontConfig         # Typography settings
```

### 5. Performance Configuration

```python
class PerformanceConfig:
    """Performance optimization settings."""

    cache_enabled: bool       # Enable icon caching
    cache_size_mb: int        # Maximum cache size in MB
    preload_icons: bool       # Preload icons on startup
    lazy_loading: bool        # Load resources on demand
    max_concurrent_loads: int # Concurrent icon loading limit
```

## Enumerations and Types

### Command Types

```python
class CommandType(Enum):
    SHELL = "shell"           # Execute via system shell
    NPM = "npm"               # Run npm script
    PYTHON = "python"         # Execute Python script
    APP = "app"               # Launch desktop application
```

### Button States

```python
class ButtonState(Enum):
    NORMAL = "normal"         # Default state
    HOVER = "hover"           # Mouse hover
    PRESSED = "pressed"       # Mouse pressed
    DISABLED = "disabled"     # Button disabled
```

### Icon Formats

```python
class IconFormat(Enum):
    PNG = "png"               # PNG image format
    SVG = "svg"               # Scalable Vector Graphics
    ICO = "ico"               # Windows icon format
    FALLBACK = "fallback"     # Default fallback icon
```

## Data Validation Rules

### Configuration Validation

```python
class ConfigValidator:
    """Validates configuration data against schema rules."""

    def validate_menu_config(config: dict) -> ValidationResult:
        """Validate entire menu configuration."""

    def validate_button(button: dict) -> ValidationResult:
        """Validate individual button configuration."""
        # Required fields: id, name, command, type
        # Icon path must exist or be valid default
        # Command must be safe executable
        # Type must be valid CommandType

    def validate_category(category: dict) -> ValidationResult:
        """Validate category configuration."""
        # Required fields: id, name, description
        # Icon path must exist or be valid default
        # button_ids must reference existing buttons

    def validate_theme(theme: dict) -> ValidationResult:
        """Validate theme configuration."""
        # Opacity values within 0.0-1.0 range
        # Color values in valid hex format
        # Font sizes within reasonable bounds
```

### Security Validation

```python
class SecurityValidator:
    """Validates security aspects of configuration."""

    def validate_command(command: str, command_type: CommandType) -> bool:
        """Validate command is safe to execute."""
        # Check for dangerous characters
        # Validate against command whitelist
        # Prevent shell injection

    def validate_path(path: str, allowed_dirs: List[str]) -> bool:
        """Validate file path is within allowed directories."""
        # Prevent directory traversal
        # Check path exists and is readable
        # Validate file extension
```

## State Management

### Application State

```python
class ApplicationState:
    """Runtime application state."""

    current_menu: MenuType    # main | category
    current_category_id: Optional[str]
    current_page: int         # For pagination
    button_states: Dict[str, ButtonState]
    menu_visible: bool
    last_activity: datetime
    error_state: Optional[ErrorState]
```

### Cache State

```python
class CacheState:
    """Icon and resource cache state."""

    icon_cache: Dict[str, IconCache]
    cache_size_bytes: int
    cache_hits: int
    cache_misses: int
    last_cleanup: datetime
```

## JSON Schema Definition

### Configuration Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Fredon Menu Configuration",
  "type": "object",
  "required": ["menu", "buttons"],
  "properties": {
    "menu": {
      "type": "object",
      "required": ["title", "icon"],
      "properties": {
        "title": {"type": "string", "minLength": 1, "maxLength": 100},
        "icon": {"type": "string", "format": "uri"},
        "quote": {"type": "string", "maxLength": 200},
        "glass_effect": {"type": "boolean", "default": true},
        "theme": {"$ref": "#/definitions/ThemeConfig"}
      }
    },
    "buttons": {
      "type": "array",
      "items": {"$ref": "#/definitions/Button"},
      "minItems": 1,
      "maxItems": 200
    },
    "categories": {
      "type": "array",
      "items": {"$ref": "#/definitions/Category"},
      "maxItems": 50
    }
  },
  "definitions": {
    "Button": {
      "type": "object",
      "required": ["id", "name", "command", "type"],
      "properties": {
        "id": {"type": "string", "pattern": "^[a-zA-Z0-9_-]+$"},
        "name": {"type": "string", "minLength": 1, "maxLength": 50},
        "icon": {"type": "string", "format": "uri"},
        "command": {"type": "string", "minLength": 1, "maxLength": 500},
        "type": {"enum": ["shell", "npm", "python", "app"]},
        "description": {"type": "string", "maxLength": 100},
        "enabled": {"type": "boolean", "default": true},
        "category_id": {"type": "string"},
        "position": {"type": "integer", "minimum": 0}
      }
    },
    "Category": {
      "type": "object",
      "required": ["id", "name", "description"],
      "properties": {
        "id": {"type": "string", "pattern": "^[a-zA-Z0-9_-]+$"},
        "name": {"type": "string", "minLength": 1, "maxLength": 30},
        "icon": {"type": "string", "format": "uri"},
        "description": {"type": "string", "maxLength": 100},
        "button_ids": {"type": "array", "items": {"type": "string"}},
        "enabled": {"type": "boolean", "default": true},
        "position": {"type": "integer", "minimum": 0}
      }
    }
  }
}
```

## Data Flow Patterns

### Configuration Loading Flow

```
1. Read JSON file from ~/.config/fredon-menu/config.json
2. Parse JSON with schema validation
3. Validate security constraints (command safety, path validation)
4. Load and cache icons referenced in configuration
5. Initialize application state
6. Build UI components from validated data
```

### Button Click Flow

```
1. User clicks button
2. Retrieve button configuration from state
3. Validate command safety
4. Execute command based on type:
   - shell: subprocess.run(command)
   - npm: subprocess.run(["npm", "run", command])
   - python: subprocess.run(["python", command])
   - app: subprocess.run(command)
5. Handle execution result
6. Close menu
```

### Category Navigation Flow

```
1. User clicks category button
2. Filter buttons by category_id
3. Update current_menu state to category
4. Update current_category_id
5. Reset pagination to page 0
6. Render category view with back button
7. Handle back button click to return to main menu
```

## Error Handling

### Configuration Errors

```python
class ConfigError(Exception):
    """Base class for configuration errors."""
    pass

class ValidationError(ConfigError):
    """Schema validation failed."""
    pass

class SecurityError(ConfigError):
    """Security validation failed."""
    pass

class FileError(ConfigError):
    """File access error."""
    pass
```

### Error Recovery

- **Missing Configuration**: Load default configuration and show user-friendly error
- **Invalid JSON**: Show specific validation error with line numbers
- **Missing Icons**: Use fallback icons and log warning
- **Command Execution Failures**: Show error dialog with troubleshooting information
- **Security Violations**: Disable problematic button and show security warning

## Performance Considerations

### Caching Strategy

- **Configuration Cache**: Parse JSON once and cache in memory
- **Icon Cache**: Two-level caching (memory + disk) with LRU eviction
- **Validation Cache**: Cache validation results for unchanged configurations
- **State Cache**: Maintain application state for quick menu show/hide

### Memory Management

- **Lazy Loading**: Load icons only when needed
- **Object Pooling**: Reuse button widgets for pagination
- **Cache Limits**: Enforce maximum cache sizes to prevent memory bloat
- **Cleanup**: Periodic cleanup of unused cache entries

This data model provides a robust foundation for implementing the Fredon Menu with clear separation of concerns, comprehensive validation, and performance optimization strategies.