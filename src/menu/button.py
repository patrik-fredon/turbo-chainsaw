"""
Menu button widget implementation for Fredon Menu
"""

import logging
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, GdkPixbuf, GLib

from .models import Button, Category

try:
    from ..utils.cache import IconCacheManager
except ImportError:
    # Fallback for running without proper package structure
    try:
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from utils.cache import IconCacheManager
    except ImportError:
        # If all else fails, create a dummy cache manager
        logger.warning("Could not import IconCacheManager, using fallback")
        class IconCacheManager:
            def get_gdk_pixbuf(self, icon_path, size=(48, 48)):
                return None

logger = logging.getLogger(__name__)


class MenuButton(Gtk.Button):
    """Custom menu button with icon and text."""

    def __init__(self, item, config, callback=None):
        """
        Initialize menu button.

        Args:
            item: Button or Category object
            config: Menu configuration
            callback: Click callback function
        """
        super().__init__()

        self.item = item
        self.config = config
        self.callback = callback
        self.icon_cache = IconCacheManager()

        # UI components
        self.content_box = None
        self.icon_image = None
        self.name_label = None
        self.description_label = None

        # Setup button
        self._setup_button()
        self._build_ui()
        self._load_icon()

        # Connect signals
        self.connect('clicked', self._on_clicked)
        self.connect('enter-notify-event', self._on_enter)
        self.connect('leave-notify-event', self._on_leave)

    def _setup_button(self):
        """Setup button properties."""
        self.set_relief(Gtk.ReliefStyle.NONE)
        self.set_can_focus(False)

        # Add appropriate CSS class
        style_context = self.get_style_context()
        if isinstance(self.item, Category):
            style_context.add_class("category-button")
        else:
            style_context.add_class("menu-button")

    def _build_ui(self):
        """Build the button UI."""
        # Horizontal content box
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.content_box.set_border_width(8)
        self.add(self.content_box)

        # Icon
        self.icon_image = Gtk.Image()
        self.icon_image.set_size_request(48, 48)
        self.content_box.pack_start(self.icon_image, False, False, 0)

        # Text container
        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.content_box.pack_start(text_box, True, True, 0)

        # Name label
        self.name_label = Gtk.Label(label=self.item.name)
        name_style_context = self.name_label.get_style_context()
        name_style_context.add_class("button-name")
        self.name_label.set_halign(Gtk.Align.START)
        self.name_label.set_justify(Gtk.Justification.LEFT)
        text_box.pack_start(self.name_label, False, False, 0)

        # Description label (if available)
        if hasattr(self.item, 'description') and self.item.description:
            self.description_label = Gtk.Label(label=self.item.description)
            desc_style_context = self.description_label.get_style_context()
            desc_style_context.add_class("button-description")
            self.description_label.set_halign(Gtk.Align.START)
            self.description_label.set_justify(Gtk.Justification.LEFT)
            self.description_label.set_line_wrap(True)
            self.description_label.set_max_width_chars(40)
            text_box.pack_start(self.description_label, False, False, 0)

        # Category indicator (for category buttons)
        if isinstance(self.item, Category):
            category_indicator = Gtk.Label(label="▶")
            category_indicator.set_halign(Gtk.Align.END)
            category_indicator.set_valign(Gtk.Align.CENTER)
            category_indicator.set_opacity(0.7)
            self.content_box.pack_start(category_indicator, False, False, 0)

    def _load_icon(self):
        """Load and set the button icon."""
        try:
            # Get GDK pixbuf from cache
            pixbuf = self.icon_cache.get_gdk_pixbuf(self.item.icon, (48, 48))

            if pixbuf:
                self.icon_image.set_from_pixbuf(pixbuf)
            else:
                # Use fallback icon
                self.icon_image.set_from_icon_name("image-missing", Gtk.IconSize.LARGE_TOOLBAR)
                logger.warning(f"Failed to load icon: {self.item.icon}")

        except Exception as e:
            logger.error(f"Error loading icon for {self.item.name}: {e}")
            self.icon_image.set_from_icon_name("image-missing", Gtk.IconSize.LARGE_TOOLBAR)

    def _on_clicked(self, button):
        """Handle button click."""
        if self.callback:
            self.callback(self.item)

    def _on_enter(self, widget, event):
        """Handle mouse enter event."""
        # Additional hover effects if needed
        pass

    def _on_leave(self, widget, event):
        """Handle mouse leave event."""
        # Additional hover effects if needed
        pass

    def update_icon(self, icon_path: str):
        """Update the button icon."""
        self.item.icon = icon_path
        self._load_icon()

    def set_enabled(self, enabled: bool):
        """Set button enabled state."""
        super().set_sensitive(enabled)
        if not enabled:
            self.set_opacity(0.5)
        else:
            self.set_opacity(1.0)


class AnimatedMenuButton(MenuButton):
    """Menu button with animation support."""

    def __init__(self, item, config, callback=None):
        """Initialize animated menu button."""
        self.animation_timeout = None
        super().__init__(item, config, callback)

    def _on_enter(self, widget, event):
        """Handle mouse enter with animation."""
        super()._on_enter(widget, event)

        # Start hover animation
        if self.animation_timeout:
            GLib.source_remove(self.animation_timeout)

        self.animation_timeout = GLib.timeout_add(
            self.config.theme.hover_duration // 4,
            self._animate_hover_in
        )

    def _on_leave(self, widget, event):
        """Handle mouse leave with animation."""
        super()._on_leave(widget, event)

        # Start hover out animation
        if self.animation_timeout:
            GLib.source_remove(self.animation_timeout)

        self.animation_timeout = GLib.timeout_add(
            self.config.theme.hover_duration // 4,
            self._animate_hover_out
        )

    def _animate_hover_in(self):
        """Animate hover in effect."""
        # Simple opacity animation
        current_opacity = self.get_opacity()
        if current_opacity < 1.0:
            new_opacity = min(1.0, current_opacity + 0.1)
            self.set_opacity(new_opacity)
            return True  # Continue animation
        return False  # Stop animation

    def _animate_hover_out(self):
        """Animate hover out effect."""
        # Simple opacity animation
        current_opacity = self.get_opacity()
        if current_opacity > 0.8:
            new_opacity = max(0.8, current_opacity - 0.1)
            self.set_opacity(new_opacity)
            return True  # Continue animation
        return False  # Stop animation