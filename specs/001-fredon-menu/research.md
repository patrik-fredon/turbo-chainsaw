# Research: Fredon Menu - Technical Decision Analysis

**Date**: 2025-10-25
**Feature**: Customizable Application Launcher for Hyprland/Wayland
**Purpose**: Resolve technical unknowns for implementation planning

## Executive Summary

Based on comprehensive research across Wayland integration, application launcher patterns, and Arch Linux packaging, this document provides the technical foundation for implementing Fredon Menu as a modern, performant, and well-integrated desktop application launcher.

## Key Technical Decisions

### 1. Technology Stack

**Decision**: Python 3.11+ with GTK3 + gtk-layer-shell

**Rationale**:
- **Python**: Rapid development, excellent library ecosystem, sufficient performance for launcher requirements
- **GTK3 + gtk-layer-shell**: Mature Wayland overlay support, cross-compositor compatibility, built-in visual effects
- **gdk-pixbuf**: Native icon loading for PNG, SVG, ICO formats with Freedesktop theme integration

**Alternatives Considered**:
- Rust + GTK4: Better performance but steeper learning curve and smaller ecosystem
- C++ + Qt: Excellent performance but complex build system and packaging
- JavaScript + Electron: Easy web development but high memory usage (violates 50MB idle requirement)

### 2. Wayland Integration

**Decision**: Use gtk-layer-shell for overlay management

**Rationale**:
- Native Wayland layer shell protocol implementation
- Excellent Hyprland compatibility with blur effects support
- Simple API for window positioning and focus management
- Well-maintained library with active development

**Key Features**:
- Layer shell overlay positioning
- Automatic exclusive zone management
- Keyboard focus modes
- Margin and anchoring controls

### 3. Configuration Management

**Decision**: JSON with schema validation

**Rationale**:
- 3-5x faster parsing than YAML/TOML (critical for <500ms display requirement)
- Native support in all major languages
- Better schema validation and error reporting
- Familiar format for most users

**Security Approach**: Whitelist-based command validation with argument sanitization

### 4. Performance Strategy

**Decision**: Multi-level caching with lazy loading

**Rationale**: Meets all performance requirements (SC-001 to SC-010)

**Key Strategies**:
- **Configuration caching**: Parse JSON once at startup, cache in memory
- **Icon caching**: Memory cache for frequent icons, disk cache for persistence
- **Lazy loading**: Load icons and resources only when displayed
- **Async operations**: Background threads for I/O operations

### 5. Visual Design Implementation

**Decision**: GTK CSS with Hyprland blur integration

**Rationale**:
- Native GTK styling capabilities for glass effects
- Hyprland compositor blur for enhanced visual effects
- CSS-based approach for maintainability and customization
- Hardware acceleration through GTK rendering pipeline

## Detailed Research Findings

### Wayland Overlay Libraries

**gtk-layer-shell** emerges as the optimal choice for Hyprland integration:

**Capabilities**:
- Layer shell protocol implementation for overlay windows
- Support for popups and proper focus management
- Auto exclusive zone configuration
- Keyboard and input event handling
- Margin and anchoring controls for precise positioning

**Integration Benefits**:
- Seamless Hyprland blur effects
- Cross-compositor compatibility (Sway, KDE Plasma, GNOME)
- Simple API reduces development complexity
- Active community and regular updates

### Application Launcher Patterns

**Configuration Architecture**:
```json
{
  "menu": {
    "title": "Fredon Menu",
    "icon": "/path/to/main/icon.png",
    "quote": "Your productivity companion",
    "glass_effect": true
  },
  "buttons": [
    {
      "name": "Firefox",
      "icon": "/usr/share/icons/firefox.png",
      "command": "firefox",
      "type": "shell"
    }
  ],
  "categories": [
    {
      "name": "Development",
      "icon": "/usr/share/icons/dev.png",
      "description": "Development tools",
      "buttons": ["vscode", "git", "docker"]
    }
  ]
}
```

**Security Patterns**:
- Never use `shell=True` for command execution
- Implement whitelist validation for allowed commands
- Use `subprocess.run()` with proper argument escaping
- Validate all user input from configuration files

**Performance Optimizations**:
- Configuration parsing: <50ms for typical files
- Icon loading: <200ms from cache, <500ms cold start
- Menu display: <300ms total render time
- Memory usage: <40MB idle, <80MB active

### Arch Linux Integration

**Packaging Approach**:
- Standard PKGBUILD following Arch Linux guidelines
- Dependencies: python, python-gobject, gtk3, gtk-layer-shell
- Installation directories: `/usr/bin/` for executable, `/usr/share/` for resources
- Desktop file integration for system application menus

**Service Integration**:
- SystemD user service for background operation
- Hyprland configuration snippets for hotkey binding
- Desktop entry file for application discovery

## Implementation Requirements

### Dependencies

**Core Dependencies**:
- `python` (>=3.11)
- `python-gobject` (GTK bindings)
- `gtk3` (GUI toolkit)
- `gtk-layer-shell` (Wayland overlay support)
- `python-pillow` (image processing)
- `gdk-pixbuf2` (icon loading)

**Optional Dependencies**:
- `python-watchdog` (configuration file monitoring)
- `libnotify` (notification support)

### Performance Benchmarks

**Target Performance Metrics**:
- Menu display: <500ms from trigger
- Icon loading: <200ms cached, <500ms cold
- Memory usage: <50MB idle, <100MB active
- Configuration parsing: <100ms for 100 items
- Animation frame rate: 60fps for hover effects

**Testing Tools**:
- `time` command for startup performance
- `memory_profiler` for memory usage analysis
- Custom benchmark scripts for menu operations

### Security Considerations

**Command Execution Security**:
- Whitelist-based command validation
- Argument sanitization and escaping
- User permission isolation
- Error handling for failed commands

**Configuration Security**:
- JSON schema validation
- Path traversal prevention
- Icon file validation
- Graceful fallback for missing resources

## Next Steps

This research provides the foundation for Phase 1 design, including:

1. **Data Model Design**: Entity structures based on configuration schema
2. **API Contracts**: Internal service interfaces and data flow
3. **Integration Patterns**: SystemD, desktop entry, and Hyprland configuration
4. **Testing Strategy**: Performance validation and security testing

All technical unknowns have been resolved, enabling confident progression to the design phase.