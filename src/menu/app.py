"""
Main application class for Fredon Menu
"""

import logging
import signal
import sys
import argparse
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, GLib, Gdk

from .models import MenuConfig, Button
from .config import ConfigManager
from .window import MenuWindow
from .launcher import CommandLauncher, ExecutionResult

logger = logging.getLogger(__name__)


class FredonMenu:
    """Main Fredon Menu application."""

    def __init__(self, config_path: str = None, debug: bool = False):
        """
        Initialize Fredon Menu application.

        Args:
            config_path: Path to configuration file
            debug: Enable debug logging
        """
        self.debug = debug
        self.setup_logging(debug)

        # Initialize components
        self.config_manager = ConfigManager(config_path)
        self.command_launcher = CommandLauncher()
        self.window = None
        self.is_running = False

        # Load configuration
        try:
            self.config = self.config_manager.load_config()
            logger.info("Configuration loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            sys.exit(1)

        # Setup configuration monitoring
        self.config_manager.add_callback(self._on_config_changed)
        self.config_manager.start_monitoring()

    def setup_logging(self, debug: bool = False):
        """Setup logging configuration."""
        level = logging.DEBUG if debug else logging.INFO

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)

        # File handler (if not debug)
        if not debug:
            try:
                import os
                log_dir = os.path.expanduser("~/.local/share/fredon-menu")
                os.makedirs(log_dir, exist_ok=True)
                log_file = os.path.join(log_dir, "fredon-menu.log")

                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(logging.INFO)
                file_handler.setFormatter(formatter)
                logging.getLogger().addHandler(file_handler)
            except Exception as e:
                logger.error(f"Failed to setup file logging: {e}")

        # Configure root logger
        logging.getLogger().setLevel(level)
        logging.getLogger().addHandler(console_handler)

    def _on_config_changed(self, config: MenuConfig):
        """Handle configuration changes."""
        logger.info("Configuration changed, updating application")
        self.config = config

        # Update window if it exists
        if self.window:
            self.window.config = config
            self.window._setup_style()  # Update styling
            self.window._update_display()  # Refresh display

    def show_menu(self):
        """Display the menu."""
        if not self.window:
            self.window = MenuWindow(self.config)
            self.window.set_command_callback(self._on_button_clicked)

        try:
            self.window.show_all()
            self.window.present()
            self.window.grab_focus()
            logger.info("Menu displayed")
        except Exception as e:
            logger.error(f"Failed to show menu: {e}")
            self._show_error_notification("Failed to display menu")

    def hide_menu(self):
        """Hide the menu."""
        if self.window:
            try:
                if self.window.get_visible():
                    self.window.hide()
                    logger.info("Menu hidden")
            except Exception as e:
                logger.error(f"Failed to hide menu: {e}")

    def toggle_menu(self):
        """Toggle menu visibility."""
        if self.window and self.window.get_visible():
            self.hide_menu()
        else:
            self.show_menu()

    def _on_button_clicked(self, item):
        """Handle button click."""
        from .models import Category

        if isinstance(item, Category):
            # Category items are handled by the window
            pass
        else:
            # Execute command for button
            self._execute_command(item)

    def _execute_command(self, button: Button):
        """Execute command associated with button."""
        logger.info(f"Executing command: {button.type.value} - {button.command}")

        try:
            result = self.command_launcher.execute_command(
                button.command,
                button.type
            )

            if result.success:
                logger.info(f"Command executed successfully: {button.name}")
                # Show notification without blocking
                try:
                    self._show_success_notification(f"Launched: {button.name}")
                except Exception as e:
                    logger.warning(f"Failed to show success notification: {e}")
            else:
                logger.error(f"Command execution failed: {result.error}")
                try:
                    self._show_error_notification(
                        f"Failed to launch {button.name}: {result.error}"
                    )
                except Exception as e:
                    logger.warning(f"Failed to show error notification: {e}")

        except Exception as e:
            logger.error(f"Unexpected error executing command: {e}")
            try:
                self._show_error_notification(
                    f"Unexpected error launching {button.name}: {e}"
                )
            except Exception as notification_error:
                logger.warning(f"Failed to show error notification: {notification_error}")

    def _show_success_notification(self, message: str):
        """Show success notification."""
        try:
            # Try to use libnotify if available
            try:
                import gi
                gi.require_version('Notify', '0.7')
                from gi.repository import Notify

                if not Notify.is_initted():
                    Notify.init("Fredon Menu")

                notification = Notify.Notification.new(
                    "Fredon Menu",
                    message,
                    "dialog-information"
                )
                notification.show()

            except ImportError:
                logger.info(f"Success: {message}")

        except Exception as e:
            logger.error(f"Failed to show notification: {e}")

    def _show_error_notification(self, message: str):
        """Show error notification."""
        try:
            # Try to use libnotify if available
            try:
                import gi
                gi.require_version('Notify', '0.7')
                from gi.repository import Notify

                if not Notify.is_initted():
                    Notify.init("Fredon Menu")

                notification = Notify.Notification.new(
                    "Fredon Menu - Error",
                    message,
                    "dialog-error"
                )
                notification.show()

            except ImportError:
                logger.error(f"Error: {message}")

        except Exception as e:
            logger.error(f"Failed to show notification: {e}")

    def run(self):
        """Run the application."""
        try:
            self.is_running = True

            # Setup signal handlers
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)

            # Create and show menu
            self.show_menu()

            # Run GTK main loop
            Gtk.main()

        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        except Exception as e:
            logger.error(f"Application error: {e}")
            self._show_error_notification(f"Application error: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Cleanup application resources."""
        logger.info("Cleaning up application")

        try:
            if self.window:
                self.window.destroy()
                self.window = None

            if self.config_manager:
                self.config_manager.stop_monitoring()

            # Save icon cache
            try:
                from ..utils.cache import IconCacheManager
                cache = IconCacheManager()
                cache.save_cache()
            except ImportError:
                # Import failed, skip cache saving
                logger.warning("Could not import IconCacheManager for cache cleanup")

        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

        self.is_running = False

    def _signal_handler(self, signum, frame):
        """Handle system signals."""
        logger.info(f"Received signal {signum}")
        if self.is_running:
            Gtk.main_quit()

    def quit(self):
        """Quit the application."""
        if self.is_running:
            Gtk.main_quit()


def create_argument_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Fredon Menu - Modern application launcher for Hyprland/Wayland",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  fredon-menu                    # Show menu with default config
  fredon-menu --config custom.json  # Use custom configuration
  fredon-menu --debug              # Enable debug logging
  fredon-menu --version           # Show version information
        """
    )

    parser.add_argument(
        "--config", "-c",
        help="Path to configuration file",
        metavar="PATH"
    )

    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug logging"
    )

    parser.add_argument(
        "--version", "-v",
        action="store_true",
        help="Show version information and exit"
    )

    parser.add_argument(
        "--toggle", "-t",
        action="store_true",
        help="Toggle menu visibility (for existing instance)"
    )

    return parser


def main():
    """Main entry point."""
    parser = create_argument_parser()
    args = parser.parse_args()

    # Show version and exit
    if args.version:
        from . import __version__
        print(f"Fredon Menu v{__version__}")
        sys.exit(0)

    # Toggle existing instance
    if args.toggle:
        try:
            # Try to communicate with existing instance
            import os
            import signal
            pid_file = os.path.expanduser("~/.config/fredon-menu/fredon-menu.pid")

            if os.path.exists(pid_file):
                with open(pid_file, 'r') as f:
                    pid = int(f.read().strip())
                os.kill(pid, signal.SIGUSR1)
                print("Toggled existing Fredon Menu instance")
                sys.exit(0)
            else:
                print("No existing Fredon Menu instance found")
                sys.exit(1)
        except Exception as e:
            print(f"Failed to toggle existing instance: {e}")
            sys.exit(1)

    # Create and run application
    try:
        app = FredonMenu(config_path=args.config, debug=args.debug)

        # Write PID file
        try:
            import os
            pid_dir = os.path.expanduser("~/.config/fredon-menu")
            os.makedirs(pid_dir, exist_ok=True)
            pid_file = os.path.join(pid_dir, "fredon-menu.pid")

            with open(pid_file, 'w') as f:
                f.write(str(os.getpid()))

            # Cleanup PID file on exit
            import atexit
            def cleanup_pid():
                try:
                    os.remove(pid_file)
                except:
                    pass
            atexit.register(cleanup_pid)

        except Exception as e:
            logger.warning(f"Failed to write PID file: {e}")

        app.run()

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()