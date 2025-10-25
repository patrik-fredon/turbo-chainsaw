"""
GTK window implementation for Fredon Menu with Wayland layer shell support
"""

import logging
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GtkLayerShell', '0.1')

from gi.repository import Gtk, Gdk, GLib
from gi.repository import GtkLayerShell

from .models import MenuConfig, MenuState

logger = logging.getLogger(__name__)


class MenuWindow(Gtk.Window):
    """Main menu window with Wayland layer shell integration."""

    def __init__(self, config: MenuConfig):
        """
        Initialize menu window.

        Args:
            config: Menu configuration
        """
        super().__init__(title=config.title)

        self.config = config
        self.current_state = MenuState.MAIN
        self.current_category_id = None
        self.current_page = 0
        self.items_per_page = 10

        # UI components
        self.main_box = None
        self.title_label = None
        self.title_icon = None
        self.buttons_box = None
        self.pagination_box = None
        self.quote_label = None
        self.back_button = None

        # Setup window
        self._setup_window()
        self._setup_layer_shell()
        self._build_ui()
        self._setup_style()

        # Connect signals
        self.connect('key-press-event', self._on_key_press)
        self.connect('focus-out-event', self._on_focus_out)

    def _setup_window(self):
        """Setup basic window properties."""
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)
        self.set_modal(True)

        # Set default size
        self.set_default_size(600, 500)
        self.set_resizable(False)

    def _setup_layer_shell(self):
        """Setup Wayland layer shell integration."""
        try:
            GtkLayerShell.init_for_window(self)
            GtkLayerShell.set_layer(self, GtkLayerShell.Layer.OVERLAY)
            GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, True)
            GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, True)
            GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)
            GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, True)

            # Set margins for centering
            GtkLayerShell.set_margin(self, GtkLayerShell.Edge.LEFT, 100)
            GtkLayerShell.set_margin(self, GtkLayerShell.Edge.RIGHT, 100)
            GtkLayerShell.set_margin(self, GtkLayerShell.Edge.TOP, 50)
            GtkLayerShell.set_margin(self, GtkLayerShell.Edge.BOTTOM, 50)

            # Enable keyboard exclusive mode
            GtkLayerShell.set_keyboard_mode(self, GtkLayerShell.KeyboardMode.EXCLUSIVE)

            logger.info("Wayland layer shell setup successful")

        except Exception as e:
            logger.error(f"Failed to setup Wayland layer shell: {e}")
            # Fallback to regular window if layer shell fails
            self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)

    def _build_ui(self):
        """Build the user interface."""
        # Main container
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.main_box.set_border_width(20)
        self.add(self.main_box)

        # Title section with icon
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        title_box.set_halign(Gtk.Align.CENTER)
        self.main_box.pack_start(title_box, False, False, 0)

        # Title icon
        self.title_icon = Gtk.Image()
        self.title_icon.set_from_icon_name("applications-other", Gtk.IconSize.DIALOG)
        title_box.pack_start(self.title_icon, False, False, 0)

        # Title label
        self.title_label = Gtk.Label(label=self.config.title)
        title_style_context = self.title_label.get_style_context()
        title_style_context.add_class("menu-title")
        title_box.pack_start(self.title_label, False, False, 0)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_box.pack_start(separator, False, False, 0)

        # Buttons container
        self.buttons_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.buttons_box.set_halign(Gtk.Align.CENTER)
        buttons_scroll = Gtk.ScrolledWindow()
        buttons_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        buttons_scroll.set_min_content_height(300)
        buttons_scroll.set_max_content_height(350)
        buttons_scroll.add(self.buttons_box)
        self.main_box.pack_start(buttons_scroll, True, True, 0)

        # Pagination controls
        self.pagination_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.pagination_box.set_halign(Gtk.Align.CENTER)
        self.main_box.pack_start(self.pagination_box, False, False, 0)

        # Back button (initially hidden)
        self.back_button = Gtk.Button(label="← Back")
        self.back_button.set_no_show_all(True)
        self.back_button.connect('clicked', self._on_back_clicked)
        self.pagination_box.pack_start(self.back_button, False, False, 0)

        # Page indicator
        self.page_label = Gtk.Label(label="")
        self.page_label.set_no_show_all(True)
        self.pagination_box.pack_start(self.page_label, True, True, 0)

        # Bottom separator
        bottom_separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_box.pack_start(bottom_separator, False, False, 0)

        # Quote label
        self.quote_label = Gtk.Label(label=self.config.quote or "")
        quote_style_context = self.quote_label.get_style_context()
        quote_style_context.add_class("menu-quote")
        self.quote_label.set_justify(Gtk.Justification.CENTER)
        self.main_box.pack_start(self.quote_label, False, False, 0)

    def _setup_style(self):
        """Setup CSS styling."""
        style_provider = Gtk.CssProvider()

        # Load CSS from file or use default
        css_file = self._get_css_file_path()
        if css_file and css_file.exists():
            try:
                style_provider.load_from_path(str(css_file))
                logger.info(f"Loaded CSS from {css_file}")
            except Exception as e:
                logger.error(f"Failed to load CSS from {css_file}: {e}")
                style_provider.load_from_data(self._get_default_css())
        else:
            style_provider.load_from_data(self._get_default_css())

        # Apply style
        style_context = self.get_style_context()
        style_context.add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Add custom CSS class
        style_context.add_class("menu-window")

    def _get_css_file_path(self):
        """Get path to custom CSS file."""
        import os
        css_paths = [
            os.path.expanduser("~/.config/fredon-menu/style.css"),
            os.path.join(os.path.dirname(__file__), "style.css"),
        ]

        for path in css_paths:
            if os.path.exists(path):
                return path
        return None

    def _get_default_css(self) -> str:
        """Get default CSS styling."""
        return f"""
        .menu-window {{
            background: rgba(26, 26, 26, {self.config.theme.background_opacity});
            border-radius: {self.config.theme.border_radius}px;
            backdrop-filter: blur({self.config.theme.blur_radius}px);
        }}

        .menu-title {{
            color: {self.config.theme.colors['text']};
            font-family: "{self.config.theme.fonts['title_family']}";
            font-size: {self.config.theme.fonts['title_size']}px;
            font-weight: bold;
        }}

        .menu-quote {{
            color: {self.config.theme.colors['text']};
            font-family: "{self.config.theme.fonts['quote_family']}";
            font-size: {self.config.theme.fonts['quote_size']}px;
            font-style: italic;
            opacity: 0.8;
        }}

        .menu-button {{
            background: {self.config.theme.colors['button_bg']};
            color: {self.config.theme.colors['button_text']};
            border: 1px solid {self.config.theme.colors['border']};
            border-radius: {self.config.theme.border_radius}px;
            padding: 12px 16px;
            margin: 2px;
            transition: all {self.config.theme.hover_duration}ms ease;
        }}

        .menu-button:hover {{
            background: {self.config.theme.colors['button_hover']};
            border-color: {self.config.theme.colors['text']};
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }}

        .category-button {{
            background: linear-gradient(135deg, {self.config.theme.colors['button_bg']}, {self.config.theme.colors['button_hover']});
            border: 2px solid {self.config.theme.colors['border']};
        }}

        .category-button:hover {{
            border-color: {self.config.theme.colors['text']};
            transform: scale(1.02);
        }}

        .pagination-button {{
            background: {self.config.theme.colors['button_bg']};
            color: {self.config.theme.colors['button_text']};
            border: 1px solid {self.config.theme.colors['border']};
            border-radius: 6px;
            padding: 6px 12px;
            margin: 0 2px;
        }}

        .pagination-button:hover {{
            background: {self.config.theme.colors['button_hover']};
        }}

        .pagination-button:disabled {{
            opacity: 0.5;
        }}

        .page-indicator {{
            color: {self.config.theme.colors['text']};
            font-family: "{self.config.theme.fonts['button_family']}";
            font-size: {self.config.theme.fonts['button_size']}px;
            opacity: 0.7;
        }}
        """

    def show_main_menu(self):
        """Display the main menu."""
        self.current_state = MenuState.MAIN
        self.current_category_id = None
        self.current_page = 0
        self._update_display()

    def show_category_menu(self, category_id: str):
        """Display a category sub-menu."""
        self.current_state = MenuState.CATEGORY
        self.current_category_id = category_id
        self.current_page = 0
        self._update_display()

    def _update_display(self):
        """Update the display based on current state."""
        # Clear existing buttons
        for child in self.buttons_box.get_children():
            self.buttons_box.remove(child)

        # Get items to display
        if self.current_state == MenuState.MAIN:
            items = self._get_main_menu_items()
        else:
            items = self._get_category_items()

        # Apply pagination
        total_items = len(items)
        total_pages = (total_items + self.items_per_page - 1) // self.items_per_page

        if total_pages > 1:
            start_idx = self.current_page * self.items_per_page
            end_idx = min(start_idx + self.items_per_page, total_items)
            page_items = items[start_idx:end_idx]
        else:
            page_items = items
            total_pages = 1

        # Create buttons
        for item in page_items:
            button = self._create_button(item)
            self.buttons_box.pack_start(button, False, False, 0)

        # Update pagination controls
        self._update_pagination_controls(total_pages)

        # Update title and back button
        if self.current_state == MenuState.CATEGORY:
            category = self.config.get_category_by_id(self.current_category_id)
            if category:
                self.title_label.set_text(category.name)
                self.back_button.show()
        else:
            self.title_label.set_text(self.config.title)
            self.back_button.hide()

        # Show all
        self.show_all()

    def _get_main_menu_items(self):
        """Get items for main menu."""
        items = []

        # Add regular buttons
        main_buttons = self.config.get_main_buttons()
        items.extend(main_buttons)

        # Add category buttons
        for category in self.config.categories:
            if category.enabled:
                items.append(category)

        # Sort by position
        items.sort(key=lambda x: getattr(x, 'position', 0))

        return items

    def _get_category_items(self):
        """Get items for current category."""
        if not self.current_category_id:
            return []

        category_buttons = self.config.get_category_buttons(self.current_category_id)

        # Sort by position
        category_buttons.sort(key=lambda x: x.position)

        return category_buttons

    def _create_button(self, item):
        """Create a button for the given item."""
        from .button import MenuButton
        return MenuButton(item, self.config, self._on_button_clicked)

    def _update_pagination_controls(self, total_pages):
        """Update pagination controls."""
        if total_pages > 1:
            # Previous button
            prev_button = Gtk.Button(label="← Previous")
            prev_button.set_sensitive(self.current_page > 0)
            prev_button.connect('clicked', self._on_prev_page)

            # Page indicator
            page_text = f"Page {self.current_page + 1} of {total_pages}"
            self.page_label.set_text(page_text)
            self.page_label.show()

            # Next button
            next_button = Gtk.Button(label="Next →")
            next_button.set_sensitive(self.current_page < total_pages - 1)
            next_button.connect('clicked', self._on_next_page)

            # Clear existing pagination controls (except back button)
            for child in self.pagination_box.get_children():
                if child != self.back_button:
                    self.pagination_box.remove(child)

            # Add controls
            if self.current_state == MenuState.CATEGORY:
                self.pagination_box.pack_start(prev_button, False, False, 0)
            else:
                self.pagination_box.pack_start(prev_button, False, False, 0)

            self.pagination_box.pack_start(self.page_label, True, True, 0)
            self.pagination_box.pack_start(next_button, False, False, 0)
        else:
            # Hide pagination controls
            self.page_label.hide()
            for child in self.pagination_box.get_children():
                if child != self.back_button:
                    self.pagination_box.remove(child)

    def _on_button_clicked(self, button_item):
        """Handle button click."""
        from .models import Category

        if isinstance(button_item, Category):
            # Category button - show sub-menu
            self.show_category_menu(button_item.id)
        else:
            # Application button - launch and close
            self.hide()
            # Signal to main app to handle command execution
            if hasattr(self, 'command_callback'):
                self.command_callback(button_item)

    def _on_back_clicked(self, button):
        """Handle back button click."""
        self.show_main_menu()

    def _on_prev_page(self, button):
        """Handle previous page click."""
        if self.current_page > 0:
            self.current_page -= 1
            self._update_display()

    def _on_next_page(self, button):
        """Handle next page click."""
        self.current_page += 1
        self._update_display()

    def _on_key_press(self, widget, event):
        """Handle key press events."""
        keyval = event.keyval
        keyname = Gdk.keyval_name(keyval)

        if keyname == 'Escape':
            self.hide()
            return True
        elif keyname == 'Left' or keyname == 'KP_Left':
            if self.current_page > 0:
                self.current_page -= 1
                self._update_display()
            return True
        elif keyname == 'Right' or keyname == 'KP_Right':
            # Check if there's a next page
            if self.current_state == MenuState.MAIN:
                items = self._get_main_menu_items()
            else:
                items = self._get_category_items()

            total_pages = (len(items) + self.items_per_page - 1) // self.items_per_page
            if self.current_page < total_pages - 1:
                self.current_page += 1
                self._update_display()
            return True
        elif keyname == 'BackSpace':
            if self.current_state == MenuState.CATEGORY:
                self.show_main_menu()
            return True

        return False

    def _on_focus_out(self, widget, event):
        """Handle focus out event."""
        # Hide menu when it loses focus
        self.hide()

    def set_command_callback(self, callback):
        """Set callback for command execution."""
        self.command_callback = callback