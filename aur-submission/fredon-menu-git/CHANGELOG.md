# Changelog

All notable changes to Fredon Menu will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- 🚀 Initial release of Fredon Menu
- ✨ Modern, customizable application launcher for Hyprland/Wayland
- 🎨 Glass-like visual effects with blur and transparency
- 📱 Centered menu overlay with smooth animations
- 🔧 JSON-based configuration system with real-time monitoring
- 🗂️ Category system for organizing applications
- 📄 Pagination support for large application collections
- 🖼️ Multi-resolution icon support (PNG, SVG, ICO)
- ⌨️ Keyboard navigation support (arrows, escape, backspace)
- 🔒 Secure command execution with whitelist validation
- 📊 Performance optimization with multi-level caching
- 🛡️ Comprehensive error handling and user notifications
- 📦 Complete Arch Linux package (PKGBUILD)
- 🔧 SystemD user service integration
- 📖 Comprehensive documentation and user guides
- 🧪 Extensive test suite for reliability

### Features

#### Core Functionality
- System-wide hotkey integration (default: Super+Space)
- Application launching with support for shell, npm, python, and app commands
- Graceful degradation when configuration files have errors
- Menu positioning that adapts to different screen resolutions
- Prevention of duplicate menu instances

#### Visual Design
- Glass-like background with configurable blur radius and opacity
- Customizable color schemes and typography
- Hover animations and micro-interactions
- Responsive design supporting 1024x768 to 4K resolutions
- Category buttons with distinct styling

#### Configuration Management
- JSON configuration with schema validation
- Real-time configuration monitoring with user notifications
- Automatic fallback to default configuration when needed
- Support for user-specific and system-wide configurations

#### Security & Performance
- Whitelist-based command validation preventing injection attacks
- Icon caching system for fast loading and memory efficiency
- <500ms menu display target
- <50MB idle memory usage
- Secure command execution with timeout protection

### Technical Specifications

#### Dependencies
- Python 3.11+
- GTK3 with gtk-layer-shell for Wayland support
- PyGObject for GTK bindings
- Pillow for image processing
- watchdog for file monitoring

#### Architecture
- Modular design with clear separation of concerns
- Type-safe data models with comprehensive validation
- Event-driven configuration system
- Plugin-ready architecture for future extensions

### Installation Options

#### From Source
```bash
git clone https://github.com/patrik-fredon/fredon-menu.git
cd fredon-menu
sudo python setup.py install
```

#### Arch Linux (AUR)
```bash
yay -S fredon-menu
```

#### Development Installation
```bash
git clone https://github.com/patrik-fredon/fredon-menu.git
cd fredon-menu
python -m venv venv
source venv/bin/activate
pip install -e .
```

### Configuration

Edit `~/.config/fredon-menu/config.json` to customize:

```json
{
  "menu": {
    "title": "Fredon Menu",
    "icon": "/path/to/icon.png",
    "quote": "Your productivity companion",
    "glass_effect": true
  },
  "buttons": [
    {
      "id": "firefox",
      "name": "Firefox",
      "icon": "/usr/share/icons/firefox.png",
      "command": "firefox",
      "type": "app"
    }
  ],
  "categories": [
    {
      "id": "development",
      "name": "Development",
      "icon": "/usr/share/icons/dev.png",
      "description": "Development tools",
      "button_ids": ["vscode", "git"]
    }
  ]
}
```

### Hyprland Integration

Add to `~/.config/hypr/hyprland.conf`:
```ini
bind = $mainMod, space, exec, fredon-menu
```

### Performance Benchmarks

- **Menu Display Time**: <500ms from trigger
- **Icon Loading**: <200ms from cache, <500ms cold start
- **Memory Usage**: <50MB idle, <100MB active
- **Configuration Parsing**: <100ms for typical configurations
- **Animation Frame Rate**: 60fps for hover effects

### Security Features

- Command whitelist validation
- Argument sanitization and escaping
- User permission isolation
- Resource limits enforcement
- Timeout protection for long-running commands

### Accessibility

- High contrast mode support
- Keyboard navigation
- Screen reader compatibility
- Adjustable font sizes
- Focus management

### Known Limitations

- Requires Wayland compositor with gtk-layer-shell support
- Icon themes may vary between systems
- Some command types require specific dependencies

### Support

- **Documentation**: https://fredon-menu.readthedocs.io/
- **Issues**: https://github.com/patrik-fredon/fredon-menu/issues
- **Discussions**: https://github.com/patrik-fredon/fredon-menu/discussions
- **Wiki**: https://github.com/patrik-fredon/fredon-menu/wiki

### Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### License

MIT License - see [LICENSE](LICENSE) file for details.

---

## [Unreleased]

*No unreleased changes yet.*

## [0.9.0] - 2025-10-25 (Development)

### Added
- Initial development milestone
- Core architecture and framework setup