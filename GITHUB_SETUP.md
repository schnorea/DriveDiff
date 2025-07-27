# GitHub Repository Setup Instructions

## Quick Setup - if you've already created a repository on GitHub

If you've already created the DriveDiff repository on GitHub, run these commands to connect your local repository:

```bash
# Add GitHub remote (replace 'yourusername' with your actual GitHub username)
git remote add origin https://github.com/yourusername/DriveDiff.git

# Push to GitHub
git push -u origin master
```

## Complete Setup - if you haven't created a repository yet

### 1. Create Repository on GitHub

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the repository details:
   - **Repository name**: `DriveDiff`
   - **Description**: `A powerful GUI-based application for comparing directories and SD cards with SHA256 hash verification`
   - **Visibility**: Choose Public or Private
   - **Initialize**: Do NOT check "Add a README file" (we already have one)
   - **gitignore**: None (we already have one)
   - **License**: None (we already have one)
5. Click "Create repository"

### 2. Connect Local Repository to GitHub

After creating the repository on GitHub, you'll see a page with setup instructions. Use the "push an existing repository" section:

```bash
# Add GitHub remote (replace 'yourusername' with your actual GitHub username)
git remote add origin https://github.com/yourusername/DriveDiff.git

# Push to GitHub
git push -u origin master
```

### 3. Verify Upload

1. Refresh your GitHub repository page
2. You should see all the files uploaded
3. The README.md should display as the repository description

## Repository Features to Enable

### 1. Issues
- Go to Settings → Features
- Ensure "Issues" is checked
- This allows users to report bugs and request features

### 2. Discussions (Optional)
- Go to Settings → Features  
- Check "Discussions" if you want community discussions

### 3. Release Creation
After your first push, you can create a release:

1. Go to "Releases" on your repository page
2. Click "Create a new release"
3. Tag version: `v1.0.0`
4. Release title: `DriveDiff v1.0.0 - Initial Release`
5. Describe the release using content from CHANGELOG.md
6. Click "Publish release"

## Repository Settings Recommendations

### Branch Protection (Optional)
For collaborative development:

1. Go to Settings → Branches
2. Add rule for `master` branch
3. Enable "Require pull request reviews before merging"
4. Enable "Require status checks to pass before merging"

### Topics/Tags
Add repository topics for discoverability:

1. Go to Settings → General
2. Add topics: `python`, `gui`, `file-comparison`, `directory-diff`, `tkinter`, `sha256`, `sd-card`, `backup-tool`

## File Overview

Your repository now contains:

### Core Application
- `src/` - Main application source code
- `requirements.txt` - Python dependencies
- `main.py` - Legacy entry point (kept for compatibility)

### Documentation
- `README.md` - Comprehensive project documentation
- `CHANGELOG.md` - Version history and changes
- `CONTRIBUTING.md` - Guidelines for contributors
- `LICENSE` - MIT license file

### Configuration
- `.gitignore` - Git ignore patterns
- `default.yaml` - Default application configuration
- `scan_config.yaml` - User scan configuration

### Development
- `tests/` - Test suite
- `run.sh` / `run.bat` - Convenience scripts

## Next Steps

1. **Create the repository** on GitHub following the instructions above
2. **Push your code** using the git commands provided
3. **Create a release** to mark v1.0.0
4. **Add repository topics** for better discoverability
5. **Share your repository** with others!

## Troubleshooting

### Authentication Issues
If you get authentication errors:

```bash
# Use GitHub CLI (if installed)
gh auth login

# Or configure git with your credentials
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### SSH vs HTTPS
If you prefer SSH over HTTPS:

```bash
# Use SSH URL instead
git remote add origin git@github.com:yourusername/DriveDiff.git
```

## Repository URL
After setup, your repository will be available at:
`https://github.com/yourusername/DriveDiff`

Replace `yourusername` with your actual GitHub username.
