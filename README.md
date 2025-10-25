# Fredon Menu

A modern, customizable application launcher for Arch Linux with Hyprland and Wayland support.

## Features

- **Glass-like visual effects** with blur and transparency
- **Configurable buttons** via JSON configuration file
- **Category organization** for grouping applications
- **Pagination support** for large application collections
- **Multi-resolution icons** with automatic scaling
- **Real-time configuration monitoring** with user notifications
- **System-wide hotkey** integration (default: Super+Space)
- **Graceful error handling** with user-friendly messages

## System Requirements

- Arch Linux (updated)
- Wayland with Hyprland compositor
- Python 3.11+
- GTK3 with gtk-layer-shell support

## Quick Start

1. **Install dependencies**:
   ```bash
   sudo pacman -S python python-gobject gtk3 gtk-layer-shell gdk-pixbuf2 python-pillow
   ```

2. **Clone and install**:
   ```bash
   git clone https://github.com/your-username/fredon-menu.git
   cd fredon-menu
   sudo python setup.py install
   ```

3. **Configure**:
   ```bash
   mkdir -p ~/.config/fredon-menu
   cp src/data/default.json ~/.config/fredon-menu/config.json
   ```

4. **Add hotkey to Hyprland** (in `~/.config/hypr/hyprland.conf`):
   ```ini
   bind = $mainMod, space, exec, fredon-menu
   ```

5. **Launch**: Press Super+Space to display the menu

## Configuration

Edit `~/.config/fredon-menu/config.json` to customize your menu:

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
  ]
}
```

## Development

1. **Setup development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

2. **Run in development mode**:
   ```bash
   python src/main.py --dev
   ```

3. **Run tests**:
   ```bash
   pytest tests/
   ```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Support

- **Issues**: https://github.com/patrik-fredon/fredon-menu/issues
- **Documentation**: https://fredon-menu.readthedocs.io/
- **Discussions**: https://github.com/patrik-fredon/fredon-menu/discussions