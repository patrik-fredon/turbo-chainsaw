# AUR Submission Instructions

## Prerequisites

1. **AUR Account**: Create an account at https://aur.archlinux.org/register.php
2. **SSH Keys**: Add your SSH public key to your AUR profile
3. **Git**: Ensure git is installed and configured

## Package 1: fredon-menu (Release Version)

### 1. Clone the AUR repository
```bash
git clone ssh://aur@aur.archlinux.org/fredon-menu.git
cd fredon-menu
```

### 2. Add your package files
```bash
# Copy from aur-submission directory
cp /path/to/fredon-menu/aur-submission/fredon-menu/* .
```

### 3. Review files before submission
- Check PKGBUILD: `namcap PKGBUILD`
- Check .SRCINFO: Ensure it's properly generated
- Verify dependencies and paths

### 4. Commit and push
```bash
git add .
git commit -m "Initial release of fredon-menu v1.0.0"
git push origin master
```

## Package 2: fredon-menu-git (Git Version)

### 1. Clone the AUR repository
```bash
git clone ssh://aur@aur.archlinux.org/fredon-menu-git.git
cd fredon-menu-git
```

### 2. Add your package files
```bash
# Copy from aur-submission directory
cp /path/to/fredon-menu/aur-submission/fredon-menu-git/* .
```

### 3. Review files before submission
- Check PKGBUILD: `namcap PKGBUILD`
- Check .SRCINFO: Ensure it matches PKGBUILD
- Verify git source URL is correct

### 4. Commit and push
```bash
git add .
git commit -m "Initial git version of fredon-menu"
git push origin master
```

## Important Notes

1. **Package Naming**: Follow AUR conventions
2. **Dependencies**: Ensure all dependencies are correct
3. **Versioning**: Use semantic versioning for release package
4. **Documentation**: Include proper package description
5. **Maintenance**: Be prepared to maintain both packages

## Post-Submission

1. **Monitor Comments**: Respond to user feedback and issues
2. **Update Regularly**: Keep packages updated with new releases
3. **Test Thoroughly**: Ensure packages install and work correctly
4. **Engage Community**: Participate in AUR discussions

## Verification

After submission, test installation:
```bash
# Release version
yay -S fredon-menu

# Git version
yay -S fredon-menu-git
```