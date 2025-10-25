# Configuration API Contract

**Version**: 1.0
**Date**: 2025-10-25
**Purpose**: Define configuration management interface and validation rules

## Configuration File Contract

### File Location
```
Primary:   ~/.config/fredon-menu/config.json
Fallback:  /usr/share/fredon-menu/default.json
Schema:    /usr/share/fredon-menu/config.schema.json
```

### Configuration Structure

```yaml
# Fredon Menu Configuration Schema
menu:
  title: string              # Menu display title (required)
  icon: string               # Main icon path (required, PNG/SVG/ICO)
  quote: string              # Bottom quote text (optional)
  glass_effect: boolean      # Enable visual effects (default: true)
  theme: ThemeConfig         # Visual appearance settings

buttons:
  - id: string               # Unique identifier (required, pattern: ^[a-zA-Z0-9_-]+$)
    name: string             # Display name (required, max 50 chars)
    icon: string             # Icon file path (required)
    command: string          # Command to execute (required, max 500 chars)
    type: enum               # shell|npm|python|app (required)
    description: string      # Tooltip description (optional, max 100 chars)
    enabled: boolean         # Button active state (default: true)
    category_id: string      # Category assignment (optional)
    position: integer        # Display order (default: append)

categories:
  - id: string               # Unique identifier (required)
    name: string             # Category name (required, max 30 chars)
    icon: string             # Category icon path (required)
    description: string      # Category description (required, max 100 chars)
    button_ids:              # Associated button IDs (optional)
      - string
    enabled: boolean         # Category active state (default: true)
    position: integer        # Display order (default: append)
```

### Theme Configuration

```yaml
theme:
  background_opacity: float  # 0.0-1.0 (default: 0.9)
  blur_radius: integer       # Glass blur pixels (default: 20)
  border_radius: integer     # Button corner radius (default: 12)
  hover_duration: integer    # Animation duration ms (default: 200)
  colors:
    background: string       # Hex color (default: "#1a1a1a")
    text: string            # Hex color (default: "#ffffff")
    button_bg: string       # Hex color (default: "#2a2a2a")
    button_hover: string    # Hex color (default: "#3a3a3a")
    button_text: string     # Hex color (default: "#ffffff")
    border: string          # Hex color (default: "#4a4a4a")
  fonts:
    title_family: string    # Font family (default: "sans-serif")
    title_size: integer     # Title font size (default: 24)
    button_family: string   # Button font family (default: "sans-serif")
    button_size: integer    # Button font size (default: 14)
    quote_family: string    # Quote font family (default: "serif")
    quote_size: integer     # Quote font size (default: 12)
```

## Validation Rules

### Input Validation

```python
class ValidationRules:
    """Configuration validation constraints."""

    # String length limits
    MAX_TITLE_LENGTH = 100
    MAX_BUTTON_NAME_LENGTH = 50
    MAX_COMMAND_LENGTH = 500
    MAX_DESCRIPTION_LENGTH = 100
    MAX_CATEGORY_NAME_LENGTH = 30

    # Configuration size limits
    MAX_BUTTONS = 200
    MAX_CATEGORIES = 50
    BUTTONS_PER_PAGE = 10

    # File size limits
    MAX_CONFIG_FILE_SIZE = 1024 * 1024  # 1MB
    MAX_ICON_FILE_SIZE = 1024 * 512     # 512KB

    # Performance limits
    MAX_STARTUP_TIME_MS = 500
    MAX_ICON_LOAD_TIME_MS = 1000
```

### Security Validation

```python
class SecurityRules:
    """Command execution security constraints."""

    # Blocked characters in commands
    BLOCKED_CHARACTERS = [';', '&', '|', '`', '$', '(', ')', '<', '>', '"', "'"]

    # Allowed command prefixes
    ALLOWED_COMMAND_PREFIXES = [
        '/usr/bin/', '/usr/local/bin/', '/bin/', '/snap/bin/',
        'npm ', 'python ', 'python3 ', 'flatpak ', 'xdg-open '
    ]

    # Blocked command names
    BLOCKED_COMMANDS = [
        'rm', 'sudo', 'su', 'passwd', 'chmod', 'chown',
        'dd', 'mkfs', 'fdisk', 'mount', 'umount'
    ]
```

## Error Responses

### Validation Errors

```yaml
# Schema validation error response
error:
  type: "validation_error"
  message: "Configuration validation failed"
  details:
    field: "buttons[0].command"
    rule: "MAX_COMMAND_LENGTH_EXCEEDED"
    value: "this command is way too long and exceeds the maximum allowed length"
    expected: "maximum 500 characters"
    line: 15
    column: 25
```

### Security Errors

```yaml
# Security validation error response
error:
  type: "security_error"
  message: "Command blocked for security reasons"
  details:
    field: "buttons[2].command"
    rule: "BLOCKED_CHARACTER_FOUND"
    value: "rm -rf /"
    blocked_character: ";"
    suggestion: "Use safe commands only"
```

### File Errors

```yaml
# File access error response
error:
  type: "file_error"
  message: "Unable to access configuration file"
  details:
    path: "/home/user/.config/fredon-menu/config.json"
    error: "Permission denied"
    suggestion: "Check file permissions or run with appropriate user"
```

## Configuration Loading API

### Load Configuration

```python
def load_config(config_path: str = None) -> ConfigResult:
    """
    Load and validate configuration file.

    Args:
        config_path: Optional custom config path

    Returns:
        ConfigResult containing:
        - success: boolean
        - config: MenuConfig (if successful)
        - errors: List[ValidationError] (if failed)
        - warnings: List[ValidationWarning]

    Error handling:
    - File not found -> Load default configuration
    - Parse error -> Return specific validation error
    - Schema validation -> Return field-specific errors
    - Security validation -> Block unsafe configurations
    """
```

### Validate Configuration

```python
def validate_config(config_data: dict) -> ValidationResult:
    """
    Validate configuration against schema and security rules.

    Args:
        config_data: Raw configuration dictionary

    Returns:
        ValidationResult containing:
        - valid: boolean
        - errors: List[ValidationError]
        - warnings: List[ValidationWarning]
        - sanitized_config: dict (if valid)
    """
```

### Save Configuration

```python
def save_config(config: MenuConfig, path: str) -> SaveResult:
    """
    Save configuration to file with validation.

    Args:
        config: Validated configuration object
        path: Target file path

    Returns:
        SaveResult containing:
        - success: boolean
        - backup_path: str (if backup created)
        - errors: List[SaveError]

    Safety features:
    - Create backup before overwriting
    - Atomic write operation
    - Validate before saving
    - Restore backup on failure
    """
```

## Icon Management API

### Load Icon

```python
def load_icon(icon_path: str, size: tuple = (64, 64)) -> IconResult:
    """
    Load and cache icon with fallback handling.

    Args:
        icon_path: Path to icon file
        size: Desired icon size (width, height)

    Returns:
        IconResult containing:
        - success: boolean
        - icon_data: bytes (if successful)
        - format: IconFormat (PNG, SVG, ICO)
        - fallback_used: boolean
        - cache_hit: boolean

    Features:
    - Multi-format support (PNG, SVG, ICO)
    - Automatic size scaling
    - Fallback to default icon
    - Memory and disk caching
    - Progressive loading
    """
```

### Cache Management

```python
def manage_cache(cache_config: CacheConfig) -> CacheResult:
    """
    Manage icon cache with size limits and cleanup.

    Args:
        cache_config: Cache configuration settings

    Returns:
        CacheResult containing:
        - cache_size_mb: float
        - cache_hits: int
        - cache_misses: int
        - cleanup_performed: boolean
        - space_freed_mb: float

    Features:
    - LRU eviction policy
    - Size-based cleanup
    - Hit/miss statistics
    - Automatic cleanup on startup
    """
```

## Performance Monitoring

### Metrics Collection

```python
class PerformanceMetrics:
    """Configuration loading performance metrics."""

    config_load_time_ms: float      # Total config load time
    validation_time_ms: float       # Schema validation time
    icon_load_time_ms: float        # Icon loading time
    cache_hit_rate: float           # Cache efficiency
    memory_usage_mb: float          # Current memory usage
    startup_time_ms: float          # Total application startup time
```

### Performance Targets

```yaml
targets:
  config_load_time_ms: <= 100      # Configuration parsing
  validation_time_ms: <= 50        # Schema validation
  icon_load_time_ms: <= 200        # From cache
  icon_cold_load_ms: <= 500        # From disk
  total_startup_ms: <= 500         # Application ready
  memory_usage_mb: <= 50           # Idle memory usage
  cache_hit_rate: >= 0.8           # Cache efficiency
```

This contract defines the complete configuration management interface with comprehensive validation, security rules, error handling, and performance requirements for the Fredon Menu application.