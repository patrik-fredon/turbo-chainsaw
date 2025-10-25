#!/bin/bash

# Fredon Menu Installation Script
# This script installs Fredon Menu on Arch Linux and compatible distributions

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "This script should not be run as root"
        print_info "Please run as a regular user"
        exit 1
    fi
}

# Detect distribution
detect_distro() {
    if [[ -f /etc/arch-release ]]; then
        DISTRO="arch"
    elif [[ -f /etc/debian_version ]]; then
        DISTRO="debian"
    elif [[ -f /etc/fedora-release ]]; then
        DISTRO="fedora"
    elif [[ -f /etc/lsb-release ]]; then
        DISTRO="ubuntu"
    else
        print_warning "Unsupported distribution detected"
        DISTRO="unknown"
    fi
}

# Check dependencies
check_dependencies() {
    print_info "Checking dependencies..."

    local missing_deps=()

    # Check for Python 3.11+
    if command -v python3 >/dev/null; then
        python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        if [[ $(echo "$python_version" | cut -d. -f2) -lt 11 ]]; then
            missing_deps+=("python3.11+")
        fi
    else
        missing_deps+=("python3")
    fi

    # Check for pip
    if ! command -v pip >/dev/null; then
        missing_deps+=("pip")
    fi

    # Check for GTK development libraries
    if [[ "$DISTRO" == "arch" ]]; then
        local gtk_packages=("gtk3" "python-gobject" "python-pillow" "python-watchdog")
        for pkg in "${gtk_packages[@]}"; do
            if ! pacman -Qi "$pkg" >/dev/null 2>&1; then
                missing_deps+=("$pkg")
            fi
        done
    fi

    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        print_error "Missing dependencies: ${missing_deps[*]}"
        print_info "Please install them and try again"
        exit 1
    fi

    print_success "All dependencies found"
}

# Install from source
install_from_source() {
    print_info "Installing Fredon Menu from source..."

    # Create temporary directory
    local temp_dir=$(mktemp -d)
    cd "$temp_dir"

    # Clone repository
    print_info "Cloning repository..."
    git clone https://github.com/patrik-fredon/turbo-chainsaw.git

    cd turbo-chainsaw

    # Create virtual environment
    print_info "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate

    # Install package
    print_info "Installing package..."
    pip install -e .

    # Create symlink
    if [[ -d "$HOME/.local/bin" ]]; then
        ln -sf "$PWD/venv/bin/fredon-menu" "$HOME/.local/bin/fredon-menu"
        print_info "Created symlink in ~/.local/bin/"
    else
        print_warning "~/.local/bin does not exist, please add it to PATH"
    fi

    # Install desktop entry
    if [[ -d "$HOME/.local/share/applications" ]]; then
        mkdir -p "$HOME/.local/share/applications"
        cp packaging/fredon-menu.desktop "$HOME/.local/share/applications/"
        print_info "Installed desktop entry"
    fi

    # Install systemd user service
    if [[ -d "$HOME/.config/systemd/user" ]]; then
        mkdir -p "$HOME/.config/systemd/user"
        cp packaging/fredon-menu.service "$HOME/.config/systemd/user/"
        print_info "Installed systemd user service"
        systemctl --user daemon-reload
    fi

    # Create config directory and default config
    mkdir -p "$HOME/.config/fredon-menu"
    if [[ ! -f "$HOME/.config/fredon-menu/config.json" ]]; then
        cp src/data/default.json "$HOME/.config/fredon-menu/config.json"
        print_info "Created default configuration"
    fi

    # Cleanup
    cd ..
    rm -rf "$temp_dir"

    print_success "Installation completed!"
    print_info "To use Fredon Menu:"
    print_info "1. Make sure ~/.local/bin is in your PATH"
    print_info "2. Run 'fredon-menu --help' for options"
    print_info "3. Add hotkey to your compositor configuration"
}

# Install on Arch Linux using AUR helper
install_arch_aur() {
    print_info "Installing Fredon Menu using AUR..."

    # Check for AUR helpers
    if command -v yay >/dev/null; then
        yay -S fredon-menu-git
    elif command -v paru >/dev/null; then
        paru -S fredon-menu-git
    elif command -v yay-bin >/dev/null; then
        yay-bin -S fredon-menu-git
    else
        print_warning "No AUR helper found"
        print_info "Install yay, paru, or use the source installation"
        install_from_source
        return
    fi

    print_success "Installation completed!"
    print_info "To use Fredon Menu:"
    print_info "1. Add to your Hyprland configuration: bind = \$mainMod, space, exec, fredon-menu"
    print_info "2. Enable the service: systemctl --user enable --now fredon-menu.service"
}

# Install on Debian/Ubuntu
install_debian() {
    print_info "Installing Fredon Menu on Debian/Ubuntu..."

    # Update package list
    print_info "Updating package lists..."
    sudo apt-get update

    # Install dependencies
    print_info "Installing dependencies..."
    sudo apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        python3-gi \
        python3-cairo \
        python3-pil \
        gir1.2-gtk-3.0 \
        gir1.2-gdkpixbuf-2.0 \
        libgtk-3-dev

    # Install from source
    install_from_source
}

# Installation instructions for other distributions
install_generic() {
    print_info "Generic installation instructions for $DISTRO:"
    print_info ""
    print_info "1. Install Python 3.11+ and development tools"
    print_info "2. Install GTK3 development libraries and Python GObject"
    print_info "3. Install Pillow: pip install Pillow"
    print_info "4. Install watchdog: pip install watchdog"
    print_info ""
    print_info "Then run the source installation:"
    print_info "  git clone https://github.com/patrik-fredon/turbo-chainsaw.git"
    print_info "  cd fredon-menu"
    print_info "  python3 -m venv venv"
    print_info "  source venv/bin/activate"
    print_info "  pip install -e ."
    print_info "  sudo ln -sf venv/bin/fredon-menu /usr/local/bin/fredon-menu"
}

# Show post-installation instructions
show_post_install() {
    echo ""
    print_success "Fredon Menu has been installed!"
    echo ""
    print_info "Post-installation steps:"
    echo ""
    print_info "1. 🎯 Configure your compositor:"
    print_info "   Add to ~/.config/hypr/hyprland.conf:"
    print_info "   bind = \$mainMod, space, exec, fredon-menu"
    echo ""
    print_info "2. ⚙️ Enable the service (optional):"
    print_info "   systemctl --user enable --now fredon-menu.service"
    echo ""
    print_info "3. 🔧 Configure applications:"
    print_info "   Edit ~/.config/fredon-menu/config.json"
    print_info "   Add your favorite applications and categories"
    echo ""
    print_info "4. 🚀 Launch the menu:"
    print_info "   Press Super+Space (or your configured hotkey)"
    echo ""
    print_info "5. 📖 Get help:"
    print_info "   fredon-menu --help"
    print_info "   fredon-menu --version"
    echo ""
    print_info "Documentation: https://fredon-menu.readthedocs.io/"
    print_info "Issues: https://github.com/patrik-fredon/turbo-chainsaw/issues"
}

# Main installation function
main() {
    echo "🚀 Fredon Menu Installation Script"
    echo "=================================="
    echo ""

    check_root
    detect_distro
    check_dependencies

    echo ""
    print_info "Detected distribution: $DISTRO"
    echo ""

    # Choose installation method
    if [[ "$DISTRO" == "arch" ]]; then
        echo "Installation methods:"
        echo "1) Install from AUR (recommended)"
        echo "2) Install from source"
        echo "3) Cancel"
        echo ""
        read -p "Choose installation method (1-3): " choice

        case $choice in
            1)
                install_arch_aur
                ;;
            2)
                install_from_source
                ;;
            3)
                print_info "Installation cancelled"
                exit 0
                ;;
            *)
                print_error "Invalid choice"
                exit 1
                ;;
        esac
    elif [[ "$DISTRO" == "debian" || "$DISTRO" == "ubuntu" ]]; then
        install_debian
    else
        install_generic
    fi

    show_post_install
}

# Parse command line arguments
case "${1:-}" in
    --help|-h)
        echo "Fredon Menu Installation Script"
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --source, -s   Install from source only"
        echo "  --aur, -a     Install from AUR only (Arch Linux)"
        echo ""
        exit 0
        ;;
    --source|-s)
        check_root
        detect_distro
        check_dependencies
        install_from_source
        show_post_install
        ;;
    --aur|-a)
        check_root
        if [[ "$DISTRO" != "arch" ]]; then
            print_error "AUR installation is only available on Arch Linux"
            exit 1
        fi
        check_dependencies
        install_arch_aur
        show_post_install
        ;;
    *)
        main
        ;;
esac
