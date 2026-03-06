# GitHub Setup Instructions

Follow these steps to customize and publish your PhD Deep Read Workflow repository on GitHub.

## Step 1: Customize Placeholders

Replace all placeholders in the repository with your actual information:

### Files to Update:

1. **`README.md`**:
   - All `yourusername` placeholders have been replaced with `heleninsights-dot`
   - All `your-email@example.com` placeholders have been replaced with `heleninsights@gmail.com`

2. **`pyproject.toml`**:
   - `authors` name and email have been updated
   - `project.urls` have been updated with the repository URL

3. **`CONTRIBUTING.md`**:
   - Update references to your repository

4. **`CODE_OF_CONDUCT.md`**:
   - Update enforcement email address

5. **`SECURITY.md`**:
   - Update security contact email

6. **`SKILL.md`**:
   - Update author information if desired

7. **`scripts/__init__.py`**:
   - Update `__author__` and `__email__`

### Quick Search for Placeholders:

```bash
# Find all files containing "yourusername"
grep -r "yourusername" . --include="*.md" --include="*.toml" --include="*.py" --include="*.yaml"

# Find all files containing "example.com"
grep -r "example.com" . --include="*.md" --include="*.toml" --include="*.py" --include="*.yaml"
```

## Step 2: Initialize Git Repository

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit initial version
git commit -m "Initial release: PhD Deep Read Workflow v0.1.6"
```

## Step 3: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `phd-deepread-workflow`
3. Description: "Transform academic PDFs into structured literature notes and critical-thinking canvases for Obsidian"
4. Visibility: Public
5. Initialize with: **DO NOT** add README, .gitignore, or license (we already have them)
6. Click "Create repository"

## Step 4: Connect and Push

```bash
# Add remote repository
git remote add origin https://github.com/heleninsights-dot/phd-deepread-workflow.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 5: Configure Repository Settings

After pushing, configure your repository:

1. **Settings → General**:
   - Update repository description if needed
   - Add topics: `pdf`, `academic`, `obsidian`, `literature-review`, `research`, `workflow`

2. **Settings → Branches**:
   - Add branch protection rule for `main` branch
   - Require pull request reviews before merging
   - Require status checks to pass (set up after GitHub Actions are running)

3. **Settings → Collaborators**:
   - Add team members if applicable

4. **Features**:
   - Enable Issues
   - Enable Discussions
   - Enable Wiki (optional)

## Step 6: Enable GitHub Actions

GitHub Actions will automatically run when you push. The workflow file (`.github/workflows/test.yml`) is already configured.

After your first push, check the Actions tab to ensure tests are running.

## Step 7: Create First Release

Follow the instructions in [PUBLISHING.md](PUBLISHING.md) to create your first release.

## Step 8: Share Your Repository

- Share on social media with hashtags: #PhD #Academic #Obsidian #Research
- Post in relevant communities (Reddit, Discord, forums)
- Consider writing a blog post about your workflow

## Step 9: Maintain and Grow

- Monitor Issues and Discussions
- Review pull requests
- Update dependencies regularly
- Engage with the community

## Troubleshooting

### GitHub Actions Fail
- Check that Tesseract OCR is installed in the workflow (already configured)
- Ensure Python versions are compatible
- Check test files for any missing dependencies

### PyPI Upload Fails
- Ensure you have proper PyPI credentials
- Check package name availability
- Verify `twine` is installed

### Docker Build Fails
- Check Dockerfile syntax
- Ensure base image is available
- Verify system dependencies are installed

## Need Help?

- GitHub Documentation: https://docs.github.com
- Python Packaging Guide: https://packaging.python.org
- Docker Documentation: https://docs.docker.com

---

**Congratulations!** Your PhD Deep Read Workflow is now ready to help researchers worldwide process academic literature more efficiently.