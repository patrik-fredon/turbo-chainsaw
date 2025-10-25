# AUR Submission Guide for Fredon Menu (turbo-chainsaw repo)

## 🚨 IMPORTANT: Git Versioning Fix

The original PKGBUILD had an issue with versioning when no git tags exist. This has been fixed with a fallback version function that handles this case.

## ✅ Current Status

Your AUR packages are **ready for submission** at:
- `aur-submission/fredon-menu/` (release version)
- `aur-submission/fredon-menu-git/` (git version)

## 📋 Step-by-Step Submission Process

### 1. Create AUR Account
1. Go to: https://aur.archlinux.org/register.php
2. Choose username (recommend: `patrik-fredon`)
3. Add SSH public key to profile
4. Generate SSH key if needed:
   ```bash
   ssh-keygen -t ed25519 -C "your-email@example.com"
   ```

### 2. Submit fredon-menu (Release Version)

```bash
# Clone the AUR repository (first time only)
git clone ssh://aur@aur.archlinux.org/fredon-menu.git
cd fredon-menu

# Copy your package files
cp /path/to/fredon-menu/aur-submission/fredon-menu/* .

# Verify package
namcap PKGBUILD

# Submit to AUR
git add .
git commit -m "Initial release: Fredon Menu v1.0.0

- Modern application launcher for Hyprland/Wayland
- Glass-like visual effects with blur and transparency
- JSON-based configuration with real-time monitoring
- Multi-resolution icon support (PNG, SVG, ICO)
- Category organization and pagination
- Secure command execution with whitelist validation
- SystemD integration and desktop entries
- Comprehensive documentation and examples

Built with Python 3.11+, GTK3, and gtk-layer-shell"

git push origin master
```

### 3. Submit fredon-menu-git (Git Version)

```bash
# Go back and clone git package repository
cd ..
git clone ssh://aur@aur.archlinux.org/fredon-menu-git.git
cd fredon-menu-git

# Copy your package files
cp /path/to/fredon-menu/aur-submission/fredon-menu-git/* .

# Verify package
namcap PKGBUILD

# Test the versioning function works
makepkg -f

# Submit to AUR
git add .
git commit -m "Initial git version: Fredon Menu development branch

- Tracks latest development from main branch
- Automatic versioning with git commit fallback
- For users who want bleeding-edge features
- Always up-to-date with latest improvements

Version function includes fallback for repositories without tags:
- Uses git describe when tags available
- Falls back to commit count + short hash when no tags exist"

git push origin master
```

## 🔧 Package Verification

After submission, test both packages:

```bash
# Test release version
yay -S fredon-menu
fredon-menu --version

# Test git version
yay -S fredon-menu-git
fredon-menu --version
```

## 📦 Package Maintenance

### Regular Updates
1. **Release version**: Update when you create new releases
2. **Git version**: Updates automatically when you push to main branch

### Updating Release Version
```bash
cd fredon-menu
# Update PKGBUILD version number
# Update source checksum
# Update .SRCINFO
git commit -m "Update to v1.1.0"
git push
```

### Responding to Comments
- Check AUR comments regularly
- Fix reported issues promptly
- Engage with community feedback

## 🎯 Best Practices

1. **Start with git version** - easier to maintain
2. **Test thoroughly** on clean systems
3. **Monitor dependencies** - ensure they remain available
4. **Be responsive** to user feedback
5. **Follow AUR guidelines** strictly

## ⚠️ Common Issues

### Git Versioning
- ✅ **Fixed**: Added fallback for repositories without tags
- ✅ **Solution**: Uses commit count + short hash as version

### Dependencies
- Verify all dependencies are in official repositories
- Test installation on fresh Arch system

### Package Quality
- Run `namcap PKGBUILD` to check for issues
- Test with `makepkg -sri` before submitting

## 🚀 Promotion

After submission:
1. Share on Arch Linux forums
2. Post on r/archlinux subreddit
3. Mention in Hyprland communities
4. Add to relevant software lists

## 📞 Support

- AUR package pages for user comments
- GitHub issues for bug reports
- Documentation for user guides

**Your Fredon Menu is ready for AUR submission!** 🎉