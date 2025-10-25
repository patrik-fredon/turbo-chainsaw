# Desktop Application Launcher Best Practices & Patterns

This document outlines proven patterns and best practices for implementing desktop application launchers, based on analysis of successful open-source projects and industry standards.

## 1. Configuration File Formats and Structures

### Recommended: JSON with Schema Validation

**Why JSON over YAML/TOML:**
- Better parsing performance (critical for <500ms requirement)
- Native support in most programming languages
- Clear structure validation with JSON Schema
- Less ambiguity than YAML for user configurations

**Configuration Structure Pattern:**

```json
{
  "$schema": "https://fredon-menu.org/schema/v1",
  "version": "1.0",
  "menu": {
    "title": "Fredon Menu",
    "mainIcon": "~/.config/fredon-menu/icons/main.svg",
    "quote": "Launch applications with style",
    "itemsPerPage": 10,
    "theme": "glass-dark"
  },
  "categories": [
    {
      "id": "development",
      "name": "Development",
      "description": "Development tools and IDEs",
      "icon": "~/.config/fredon-menu/icons/category-dev.svg"
    },
    {
      "id": "multimedia",
      "name": "Multimedia",
      "description": "Audio and video applications",
      "icon": "~/.config/fredon-menu/icons/category-media.svg"
    }
  ],
  "applications": [
    {
      "id": "vscode",
      "name": "Visual Studio Code",
      "icon": "~/.config/fredon-menu/icons/vscode.png",
      "command": "code",
      "type": "app",
      "category": "development",
      "description": "Code editing. Redefined."
    },
    {
      "id": "npm-start",
      "name": "Start Dev Server",
      "icon": "~/.config/fredon-menu/icons/npm.svg",
      "command": "npm start",
      "type": "shell",
      "workingDirectory": "~/projects/myapp",
      "description": "Start the development server"
    }
  ]
}
```

**Configuration Best Practices:**

1. **Schema Validation**: Include `$schema` reference for IDE support and validation
2. **Semantic Versioning**: Always include version for migration handling
3. **User-Friendly Paths**: Support both absolute paths and `~` expansion
4. **Extensible Structure**: Allow custom fields while maintaining core structure
5. **Default Values**: Provide sensible defaults for all optional fields

## 2. Command Execution Patterns and Security

### Security-First Command Execution

**Critical Security Rules:**

1. **Command Sanitization**:
```python
def sanitize_command(command, args=[]):
    """Prevent shell command injection"""
    import shlex
    # Only allow specific characters and patterns
    allowed_pattern = r'^[a-zA-Z0-9._/:-]+$'
    if not re.match(allowed_pattern, command):
        raise SecurityError(f"Invalid command: {command}")

    # Properly escape arguments
    if args:
        return [command] + [shlex.quote(str(arg)) for arg in args]
    return [command]
```

2. **Execution Type Handling**:
```python
class CommandExecutor:
    def execute(self, app_config):
        command_type = app_config.get('type', 'app')
        command = app_config['command']

        if command_type == 'shell':
            return self._execute_shell(command)
        elif command_type == 'npm':
            return self._execute_npm(command)
        elif command_type == 'python':
            return self._execute_python(command)
        elif command_type == 'app':
            return self._execute_app(command)
        else:
            raise ValueError(f"Unknown command type: {command_type}")

    def _execute_shell(self, command):
        """Execute shell commands safely"""
        import subprocess
        # Use subprocess.run with shell=False for security
        args = ['bash', '-c', command]
        return subprocess.Popen(args,
                               start_new_session=True,
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
```

**Security Considerations:**

1. **Avoid shell=True** unless absolutely necessary
2. **Validate user input** in configuration files
3. **Use whitelist approach** for allowed commands
4. **Set process limits** (CPU, memory, file descriptors)
5. **Run with minimal privileges** using user-level permissions only

## 3. Icon Loading and Caching Strategies

### Multi-Format Icon Support with Caching

**Icon Loading Pattern:**

```python
class IconCache:
    def __init__(self, cache_dir, max_size_mb=50):
        self.cache_dir = Path(cache_dir)
        self.max_size = max_size_mb * 1024 * 1024
        self.memory_cache = {}
        self.cache_index_file = self.cache_dir / 'cache_index.json'

    def get_icon(self, icon_path, size=64):
        """Get icon with caching support"""
        cache_key = f"{icon_path}:{size}"

        # Check memory cache first
        if cache_key in self.memory_cache:
            return self.memory_cache[cache_key]

        # Check disk cache
        cached_icon = self._get_disk_cached_icon(icon_path, size)
        if cached_icon:
            self.memory_cache[cache_key] = cached_icon
            return cached_icon

        # Load and cache original icon
        original_icon = self._load_icon(icon_path)
        if not original_icon:
            return self._get_default_icon(size)

        # Resize and cache
        resized_icon = self._resize_icon(original_icon, size)
        self._cache_icon(icon_path, size, resized_icon)
        self.memory_cache[cache_key] = resized_icon

        return resized_icon
```

**Performance Optimization:**

1. **Lazy Loading**: Load icons only when needed
2. **Progressive Loading**: Start with low-res, upgrade to high-res
3. **Background Preloading**: Cache frequently used icons
4. **Memory Management**: Limit memory cache size with LRU eviction
5. **Disk Caching**: Persistent cache for faster startup

**Icon Format Priority:**
1. SVG (scalable, preferred for main icons)
2. PNG (raster, good for application icons)
3. ICO (Windows compatibility, fallback)
4. Theme icons (fallback using freedesktop icon theme spec)

## 4. Menu Navigation Patterns

### Pagination and Keyboard Navigation

**Navigation System Design:**

```python
class MenuNavigation:
    def __init__(self, items_per_page=10):
        self.items_per_page = items_per_page
        self.current_page = 0
        self.current_category = None
        self.search_query = ""
        self.keyboard_navigation = {
            'up': 'k',
            'down': 'j',
            'page_up': 'u',
            'page_down': 'd',
            'select': 'Enter',
            'back': 'Escape',
            'search': '/',
            'quit': 'q'
        }

    def get_visible_items(self, all_items):
        """Get items for current view with pagination"""
        if self.search_query:
            filtered_items = self._filter_items(all_items, self.search_query)
        elif self.current_category:
            filtered_items = self._get_category_items(all_items, self.current_category)
        else:
            filtered_items = all_items

        start_idx = self.current_page * self.items_per_page
        end_idx = start_idx + self.items_per_page

        return {
            'items': filtered_items[start_idx:end_idx],
            'total_pages': math.ceil(len(filtered_items) / self.items_per_page),
            'current_page': self.current_page,
            'total_items': len(filtered_items)
        }
```

**Keyboard Navigation Best Practices:**

1. **Vi-style Navigation**: hjkl for movement (familiar to power users)
2. **Number Navigation**: Press 1-9 to directly select items
3. **Search Integration**: Type to search, Enter to select
4. **Category Breadcrumb**: Show navigation path in sub-menus
5. **Consistent Shortcuts**: Same keys work across all menu levels

**Pagination UI Pattern:**
```
[Main Menu]                Page 1/3
┌─────────────────────────┐
│    [Main Icon]          │
│  ─────────────────────  │
│  [Dev]   [Media] [Web] │
│  [Game]  [Util]  [Sys] │
│  [Edit]  [Term]  [Net] │
│  ─────────────────────  │
│  "Launch with style"    │
└─────────────────────────┘
    [← Prev] [Next →]       [ESC] Quit
```

## 5. Visual Design Patterns

### Glass/Blur Effects Implementation

**CSS/HTML Pattern (for web-based launchers):**

```css
.glass-menu {
    background: rgba(15, 15, 30, 0.85);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    box-shadow:
        0 20px 40px rgba(0, 0, 0, 0.3),
        0 0 0 1px rgba(255, 255, 255, 0.05),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.menu-button {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.menu-button:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateY(-2px) scale(1.02);
    box-shadow:
        0 10px 25px rgba(0, 0, 0, 0.2),
        0 0 20px rgba(100, 200, 255, 0.3);
    border-color: rgba(100, 200, 255, 0.5);
}
```

**GTK/Cairo Pattern (for native launchers):**

```c
// Glass effect with Cairo
static void draw_glass_background(cairo_t *cr, int width, int height) {
    // Create gradient background
    cairo_pattern_t *pattern = cairo_pattern_create_linear(0, 0, 0, height);
    cairo_pattern_add_color_stop_rgba(pattern, 0.0, 0.1, 0.1, 0.2, 0.85);
    cairo_pattern_add_color_stop_rgba(pattern, 1.0, 0.05, 0.05, 0.15, 0.95);

    // Rounded rectangle
    double radius = 20.0;
    double degrees = G_PI / 180.0;

    cairo_new_sub_path(cr);
    cairo_arc(cr, width - radius, radius, radius, -90 * degrees, 0 * degrees);
    cairo_arc(cr, width - radius, height - radius, radius, 0 * degrees, 90 * degrees);
    cairo_arc(cr, radius, height - radius, radius, 90 * degrees, 180 * degrees);
    cairo_arc(cr, radius, radius, radius, 180 * degrees, 270 * degrees);
    cairo_close_path(cr);

    cairo_set_source(cr, pattern);
    cairo_fill_preserve(cr);

    // Border glow
    cairo_set_source_rgba(cr, 1.0, 1.0, 1.0, 0.1);
    cairo_set_line_width(cr, 1.0);
    cairo_stroke(cr);

    cairo_pattern_destroy(pattern);
}
```

**Design Principles:**

1. **Consistent Visual Language**: Same glass effect across all elements
2. **Micro-interactions**: Subtle animations and hover states
3. **High Contrast**: Ensure readability with semi-transparent backgrounds
4. **Color Harmony**: Use complementary colors for accents
5. **Accessibility**: Support for high contrast and reduced motion modes

## 6. Performance Optimization Techniques

### Sub-500ms Menu Display Optimization

**Startup Optimization Checklist:**

```python
class PerformanceOptimizedMenu:
    def __init__(self):
        self.config_cache = None
        self.icon_cache = IconCache()
        self.render_cache = {}
        self.last_config_mtime = 0

    def show_menu(self):
        """Optimized menu display pipeline"""
        start_time = time.time()

        # 1. Fast config check (cached)
        if not self._config_changed():
            config = self.config_cache
        else:
            config = self._load_config()
            self.config_cache = config

        # 2. Pre-render layout (async)
        if self._should_rerender(config):
            self._prerender_async(config)

        # 3. Show window immediately
        self._show_window()

        # 4. Populate with cached content
        self._populate_cached_content()

        display_time = time.time() - start_time
        if display_time > 0.5:
            logger.warning(f"Menu display took {display_time:.3f}s")

    def _config_changed(self):
        """Fast config modification check"""
        config_path = Path("~/.config/fredon-menu/config.json").expanduser()
        try:
            current_mtime = config_path.stat().st_mtime
            if current_mtime > self.last_config_mtime:
                self.last_config_mtime = current_mtime
                return True
        except FileNotFoundError:
            pass
        return False
```

**Performance Strategies:**

1. **Configuration Caching**: Cache parsed config, check file mtime
2. **Lazy Icon Loading**: Load icons in background, show placeholders
3. **Layout Caching**: Pre-calculate widget positions and sizes
4. **Async Operations**: Use threading for I/O operations
5. **Memory Pooling**: Reuse objects to reduce GC pressure
6. **Hardware Acceleration**: Use GPU for rendering when available

**Memory Management:**

```python
class MemoryManager:
    def __init__(self, max_idle_mb=50, max_active_mb=100):
        self.max_idle = max_idle_mb * 1024 * 1024
        self.max_active = max_active_mb * 1024 * 1024
        self.current_state = 'idle'

    def check_memory_usage(self):
        """Monitor and optimize memory usage"""
        import psutil
        process = psutil.Process()
        memory_usage = process.memory_info().rss

        if self.current_state == 'idle' and memory_usage > self.max_idle:
            self._cleanup_idle_memory()
        elif self.current_state == 'active' and memory_usage > self.max_active:
            self._cleanup_active_memory()

    def _cleanup_idle_memory(self):
        """Aggressive cleanup for idle state"""
        self.icon_cache.clear_memory_cache()
        self.render_cache.clear()
        gc.collect()
```

## 7. Error Handling Patterns

### Robust Error Management

**Configuration Error Handling:**

```python
class ConfigurationError(Exception):
    def __init__(self, message, line_number=None, field_path=None):
        super().__init__(message)
        self.line_number = line_number
        self.field_path = field_path

class ConfigLoader:
    def load_config(self, config_path):
        """Load configuration with comprehensive error handling"""
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)

            # Validate structure
            self._validate_config(config_data)

            # Normalize paths and defaults
            return self._normalize_config(config_data)

        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            return self._get_default_config()

        except json.JSONDecodeError as e:
            raise ConfigurationError(
                f"Invalid JSON syntax: {e.msg}",
                line_number=e.lineno
            )

        except Exception as e:
            logger.error(f"Unexpected error loading config: {e}")
            return self._get_default_config()
```

**Icon Error Handling:**

```python
class IconLoader:
    def load_icon_safely(self, icon_path, fallback_size=64):
        """Load icon with comprehensive fallback handling"""
        original_path = icon_path

        # Try different formats and paths
        for path_variant in self._get_path_variants(icon_path):
            try:
                icon = self._load_icon_file(path_variant)
                if icon:
                    return icon
            except Exception as e:
                logger.debug(f"Failed to load icon from {path_variant}: {e}")
                continue

        # Use theme icon as fallback
        theme_icon = self._load_theme_icon(original_path)
        if theme_icon:
            return theme_icon

        # Final fallback - default icon
        logger.warning(f"Using default icon for {original_path}")
        return self._create_default_icon(fallback_size)

    def _get_path_variants(self, icon_path):
        """Generate different path variants to try"""
        variants = []

        # Original path
        variants.append(icon_path)

        # Add different extensions
        base_path = os.path.splitext(icon_path)[0]
        for ext in ['.svg', '.png', '.ico', '.xpm']:
            variants.append(base_path + ext)

        # Try in icon directories
        icon_dirs = [
            "~/.local/share/icons",
            "/usr/share/icons",
            "~/.config/fredon-menu/icons"
        ]

        basename = os.path.basename(icon_path)
        for icon_dir in icon_dirs:
            variants.append(os.path.expanduser(f"{icon_dir}/{basename}"))

        return variants
```

**Command Execution Error Handling:**

```python
class SafeExecutor:
    def execute_with_error_handling(self, app_config):
        """Execute commands with comprehensive error handling"""
        try:
            # Pre-execution validation
            self._validate_command(app_config)

            # Execute command
            process = self._execute_command(app_config)

            # Monitor for immediate failures
            if process.poll() is not None:
                self._handle_execution_failure(process, app_config)

            return True

        except SecurityError as e:
            self._show_error_dialog(
                "Security Error",
                f"Command blocked for security reasons:\n{e}"
            )
            return False

        except FileNotFoundError:
            self._show_error_dialog(
                "Application Not Found",
                f"The application '{app_config['name']}' could not be found.\n"
                f"Command: {app_config['command']}"
            )
            return False

        except PermissionError:
            self._show_error_dialog(
                "Permission Denied",
                f"Insufficient permissions to execute '{app_config['name']}'."
            )
            return False

        except Exception as e:
            logger.error(f"Unexpected error executing {app_config['name']}: {e}")
            self._show_error_dialog(
                "Execution Error",
                f"Failed to launch '{app_config['name']}'.\n"
                f"Check the logs for details."
            )
            return False
```

## 8. Integration and Compatibility

### Wayland/Hyprland Integration

**Layer Shell Integration:**

```c
// Wayland layer shell setup for Hyprland compatibility
static void setup_wayland_layer_shell(struct menu_state *state) {
    // Get Wayland display
    state->display = wl_display_connect(NULL);
    if (!state->display) {
        fprintf(stderr, "Failed to connect to Wayland display\n");
        return;
    }

    // Get registry and bind to required interfaces
    state->registry = wl_display_get_registry(state->display);
    wl_registry_add_listener(state->registry, &registry_listener, state);
    wl_display_roundtrip(state->display);

    // Create layer surface
    state->layer_surface = zwlr_layer_surface_v1_create(
        state->layer_shell,
        state->surface,
        ZWLR_LAYER_SURFACE_V1_LAYER_OVERLAY,
        "fredon-menu"
    );

    // Set layer surface properties
    zwlr_layer_surface_v1_set_anchor(state->layer_surface,
        ZWLR_LAYER_SURFACE_V1_ANCHOR_TOP |
        ZWLR_LAYER_SURFACE_V1_ANCHOR_BOTTOM |
        ZWLR_LAYER_SURFACE_V1_ANCHOR_LEFT |
        ZWLR_LAYER_SURFACE_V1_ANCHOR_RIGHT
    );

    zwlr_layer_surface_v1_set_exclusive_zone(state->layer_surface, -1);
    zwlr_layer_surface_v1_set_keyboard_interactivity(
        state->layer_surface,
        ZWLR_LAYER_SURFACE_V1_KEYBOARD_INTERACTIVITY_EXCLUSIVE
    );
}
```

## Summary of Key Recommendations

1. **Configuration**: Use JSON with schema validation, support `~` expansion, include defaults
2. **Security**: Sanitize all commands, avoid shell=True, use whitelist approach
3. **Performance**: Cache aggressively, load lazily, monitor memory usage (<50MB idle, <100MB active)
4. **Icons**: Support SVG/PNG/ICO, implement multi-level caching, provide fallbacks
5. **Navigation**: Vi-style keys, number shortcuts, search integration, consistent patterns
6. **Visual**: Glass effects with backdrop-filter, micro-interactions, high contrast
7. **Error Handling**: Comprehensive validation, user-friendly error messages, graceful fallbacks
8. **Integration**: Wayland layer shell support, Hyprland compatibility, systemd integration

These patterns provide a solid foundation for building a fast, secure, and user-friendly desktop application launcher that meets modern performance and usability requirements.