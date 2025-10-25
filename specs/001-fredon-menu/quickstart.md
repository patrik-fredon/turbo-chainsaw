# Quickstart Guide: Fredon Menu

**Version**: 1.0
**Date**: 2025-10-25
**Purpose**: Get Fredon Menu running on Arch Linux with Hyprland in minutes

## System Requirements

### Minimum Requirements
- **Operating System**: Arch Linux (updated)
- **Display Server**: Wayland with Hyprland compositor
- **Python**: Version 3.11 or higher
- **Memory**: 512MB RAM minimum
- **Storage**: 100MB disk space
- **Graphics**: Hardware acceleration recommended

### Required Dependencies
```bash
# Core runtime dependencies
python>=3.11
gtk3>=3.24
gtk-layer-shell>=0.8
python-gobject>=3.42
gdk-pixbuf2>=2.42

# Optional dependencies for enhanced features
python-pillow>=9.0           # Image processing
python-watchdog>=2.1         # Configuration file monitoring
libnotify>=0.8               # Notification support
```

## Installation

### Method 1: Arch Linux Package (Recommended)

```bash
# Install from AUR (when available)
yay -S fredon-menu

# Or using paru
paru -S fredon-menu

# Enable and start the user service
systemctl --user enable --now fredon-menu.service
```

### Method 2: Manual Installation

```bash
# Clone the repository
git clone https://github.com/patrik-fredon/fredon-menu.git
cd fredon-menu

# Install dependencies
sudo pacman -S python python-gobject gtk3 gtk-layer-shell gdk-pixbuf2

# Install the application
sudo python setup.py install

# Copy default configuration
mkdir -p ~/.config/fredon-menu
cp data/default.json ~/.config/fredon-menu/config.json

# Install desktop entry
sudo cp packaging/fredon-menu.desktop /usr/share/applications/

# Install SystemD user service
mkdir -p ~/.config/systemd/user/
cp packaging/fredon-menu.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now fredon-menu.service
```

### Method 3: Development Installation

```bash
# Clone for development
git clone https://github.com/patrik-fredon/fredon-menu.git
cd fredon-menu

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -e .
pip install -r requirements-dev.txt

# Run in development mode
python src/main.py --dev
```

## Initial Configuration

### Default Configuration

After installation, a default configuration is created at `~/.config/fredon-menu/config.json`:

```json
{
  "menu": {
    "title": "Fredon Menu",
    "icon": "/usr/share/icons/hicolor/256x256/apps/fredon-menu.png",
    "quote": "Your productivity companion",
    "glass_effect": true,
    "theme": {
      "background_opacity": 0.9,
      "blur_radius": 20,
      "border_radius": 12,
      "hover_duration": 200,
      "colors": {
        "background": "#1a1a1a",
        "text": "#ffffff",
        "button_bg": "#2a2a2a",
        "button_hover": "#3a3a3a",
        "button_text": "#ffffff",
        "border": "#4a4a4a"
      },
      "fonts": {
        "title_family": "sans-serif",
        "title_size": 24,
        "button_family": "sans-serif",
        "button_size": 14,
        "quote_family": "serif",
        "quote_size": 12
      }
    }
  },
  "buttons": [
    {
      "id": "firefox",
      "name": "Firefox",
      "icon": "/usr/share/icons/hicolor/256x256/apps/firefox.png",
      "command": "firefox",
      "type": "app",
      "description": "Web Browser",
      "enabled": true,
      "position": 0
    },
    {
      "id": "terminal",
      "name": "Terminal",
      "icon": "/usr/share/icons/hicolor/256x256/apps/Alacritty.png",
      "command": "alacritty",
      "type": "shell",
      "description": "Terminal Emulator",
      "enabled": true,
      "position": 1
    }
  ],
  "categories": [],
  "performance": {
    "cache_enabled": true,
    "cache_size_mb": 50,
    "preload_icons": true,
    "lazy_loading": true,
    "max_concurrent_loads": 5
  }
}
```

### Hyprland Integration

Add the following to your `~/.config/hypr/hyprland.conf`:

```ini
# Fredon Menu keybinding
bind = $mainMod, space, exec, fredon-menu

# Optional: Animation for menu appearance
animation = workspaces, 1, 2, default
animation = windows, 1, 3, popin 80%
```

Replace `$mainMod` with your main modifier (usually `SUPER`).

## First Launch

### Testing Installation

1. **Launch from Terminal**:
```bash
fredon-menu
```

2. **Launch using Keybinding**:
Press your configured hotkey (default: Super + Space)

3. **Expected Behavior**:
- Menu appears centered on screen
- Glass-like background with blur effect
- Two default buttons: Firefox and Terminal
- Quote displayed at bottom
- Menu closes after launching an application

### Verifying Functionality

✅ **Menu Display**: Menu appears within 500ms of trigger
✅ **Button Interaction**: Buttons show hover effects
✅ **Application Launch**: Applications launch successfully
✅ **Visual Effects**: Glass blur effect visible
✅ **Menu Close**: Menu closes after application launch

## Configuration Customization

### Adding Applications

Edit `~/.config/fredon-menu/config.json` to add your applications:

```json
{
  "buttons": [
    {
      "id": "code",
      "name": "VS Code",
      "icon": "/usr/share/icons/hicolor/256x256/apps/code.png",
      "command": "code",
      "type": "app",
      "description": "Code Editor",
      "enabled": true,
      "position": 2
    },
    {
      "id": "files",
      "name": "Files",
      "icon": "/usr/share/icons/hicolor/256x256/apps/org.gnome.Nautilus.png",
      "command": "nautilus",
      "type": "app",
      "description": "File Manager",
      "enabled": true,
      "position": 3
    }
  ]
}
```

### Creating Categories

Organize applications into categories:

```json
{
  "categories": [
    {
      "id": "development",
      "name": "Development",
      "icon": "/usr/share/icons/hicolor/256x256/apps/utilities-terminal.png",
      "description": "Development Tools",
      "button_ids": ["code", "git", "docker"],
      "enabled": true,
      "position": 0
    },
    {
      "id": "multimedia",
      "name": "Multimedia",
      "icon": "/usr/share/icons/hicolor/256x256/apps/multimedia.png",
      "description": "Audio & Video Applications",
      "button_ids": ["vlc", "audacious", "obs"],
      "enabled": true,
      "position": 1
    }
  ]
}
```

### Customizing Appearance

Modify theme settings to match your desktop:

```json
{
  "menu": {
    "theme": {
      "background_opacity": 0.85,
      "blur_radius": 25,
      "colors": {
        "background": "#0a0a0a",
        "button_bg": "#1a1a1a",
        "button_hover": "#2a2a2a"
      },
      "fonts": {
        "title_family": "JetBrains Mono",
        "button_size": 16
      }
    }
  }
}
```

### NPM and Python Scripts

Add development scripts:

```json
{
  "buttons": [
    {
      "id": "npm-dev",
      "name": "Start Dev Server",
      "icon": "/home/user/projects/myapp/dev-icon.png",
      "command": "dev",
      "type": "npm",
      "description": "Start development server",
      "enabled": true,
      "position": 10
    },
    {
      "id": "python-backup",
      "name": "Run Backup",
      "icon": "/home/user/scripts/backup-icon.png",
      "command": "/home/user/scripts/backup.py",
      "type": "python",
      "description": "Execute backup script",
      "enabled": true,
      "position": 11
    }
  ]
}
```

## Troubleshooting

### Common Issues

**Menu doesn't appear**:
```bash
# Check if service is running
systemctl --user status fredon-menu.service

# Check Wayland display
echo $WAYLAND_DISPLAY

# Manual launch for debugging
fredon-menu --verbose
```

**Icons not displaying**:
```bash
# Update icon cache
gtk-update-icon-cache /usr/share/icons/hicolor/

# Check icon paths
ls -la /usr/share/icons/hicolor/256x256/apps/

# Verify icon format
file /path/to/icon.png
```

**Applications not launching**:
```bash
# Check executable exists
which firefox

# Test command manually
firefox -new-window

# Check permissions
ls -la /usr/bin/firefox
```

**Performance issues**:
```bash
# Check memory usage
ps aux | grep fredon-menu

# Monitor startup time
time fredon-menu

# Check configuration
fredon-menu --validate-config
```

### Debug Mode

Enable verbose logging for troubleshooting:

```bash
# Run with debug output
fredon-menu --debug --verbose

# Check logs
journalctl --user -u fredon-menu.service -f

# Validate configuration
fredon-menu --validate-config
```

### Getting Help

- **GitHub Issues**: https://github.com/patrik-fredon/fredon-menu/issues
- **Arch Linux Forum**: https://bbs.archlinux.org/
- **Hyprland Discord**: https://discord.gg/hyprland
- **Documentation**: https://fredon-menu.readthedocs.io/

## Next Steps

1. **Customize Configuration**: Add your favorite applications
2. **Organize Categories**: Group related applications
3. **Personalize Theme**: Match your desktop aesthetics
4. **Set Keybindings**: Configure comfortable hotkeys
5. **Explore Features**: Pagination, search, advanced configurations

Congratulations! You now have Fredon Menu running on your Arch Linux system with Hyprland. 🎉

## Performance Tips

- **SSD Storage**: Keeps icon loading fast
- **GPU Acceleration**: Enables smooth animations
- **Sufficient RAM**: Prevents swapping during operation
- **Optimized Icons**: Use appropriately sized icon files
- **Regular Updates**: Keep system and application current

Enjoy your new application launcher!