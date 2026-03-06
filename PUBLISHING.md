# Publishing Guide

This document describes how to publish and distribute the PhD Deep Read Workflow.

## GitHub Repository

### Initial Setup

1. **Create a new repository** on GitHub:
   - Repository name: `phd-deepread-workflow`
   - Description: "Transform academic PDFs into structured literature notes and critical-thinking canvases for Obsidian"
   - Visibility: Public
   - License: MIT
   - Add .gitignore: Python
   - Add README: Yes

2. **Push local repository**:
```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial release: PhD Deep Read Workflow v0.1.6"

# Add remote repository
git remote add origin https://github.com/heleninsights-dot/phd-deepread-workflow.git
git branch -M main
git push -u origin main
```

3. **Configure repository settings**:
   - Enable Issues and Discussions
   - Set up branch protection rules for `main` branch
   - Add repository topics: `pdf`, `academic`, `obsidian`, `literature-review`, `research`, `workflow`
   - Update repository description and website if needed

## Python Package Distribution

### Prerequisites

```bash
# Install build tools
pip install --upgrade build twine
```

### Building Packages

```bash
# Build source distribution and wheel
python -m build

# Verify the packages
twine check dist/*
```

### Publishing to PyPI

#### Test PyPI (for testing)

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ phd-deepread-workflow
```

#### Production PyPI

```bash
# Upload to PyPI
twine upload dist/*
```

### Version Management

1. Update version in `pyproject.toml`:
```toml
version = "0.1.6"
```

2. Update `CHANGELOG.md` with new version section

3. Create a git tag:
```bash
git tag -a v0.1.6 -m "Release v0.1.6"
git push origin v0.1.6
```

4. Create a GitHub Release:
   - Go to Repository → Releases → Draft New Release
   - Tag: `v0.1.6`
   - Title: "PhD Deep Read Workflow v0.1.6"
   - Description: Copy from CHANGELOG.md
   - Upload `dist/*` files as assets

## Claude Code Skill Distribution

### Option 1: Direct Installation

Users can install directly from GitHub:

```bash
git clone https://github.com/heleninsights-dot/phd-deepread-workflow.git
cp -r phd-deepread-workflow ~/.claude/skills/phd-deepread
```

### Option 2: Skill Repository (Future)

Consider creating a dedicated skill repository or submitting to Claude Code skill registry when available.

## Docker Distribution

### Build and Push to Docker Hub

```bash
# Build the image
docker build -t heleninsights-dot/phd-deepread-workflow:latest .

# Tag for version
docker tag heleninsights-dot/phd-deepread-workflow:latest heleninsights-dot/phd-deepread-workflow:v0.1.6

# Push to Docker Hub
docker push heleninsights-dot/phd-deepread-workflow:latest
docker push heleninsights-dot/phd-deepread-workflow:v0.1.6
```

### Update docker-compose.yml

Update image reference in `docker-compose.yml`:
```yaml
image: heleninsights-dot/phd-deepread-workflow:latest
```

## Documentation

### GitHub Pages

The repository includes MkDocs configuration for documentation:

```bash
# Install docs dependencies
pip install mkdocs mkdocs-material

# Build docs locally
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

### Read the Docs (Alternative)

Set up Read the Docs integration:
1. Connect repository to Read the Docs
2. Configure `.readthedocs.yaml`
3. Enable automatic builds

## Marketing and Promotion

### Social Media

- Twitter/X: Announce the release with hashtags #PhD #Academic #Obsidian #Research
- Reddit: Share in r/obsidian, r/academic, r/PhD
- Discord: Share in Obsidian and academic communities

### Academic Platforms

- Share on research platforms like ResearchGate, Academia.edu
- Consider writing a blog post about the workflow
- Present at academic conferences or workshops

## Maintenance

### Regular Updates

1. **Monthly**: Update dependencies
2. **Quarterly**: Review and update documentation
3. **As needed**: Address issues and feature requests

### Community Management

- Monitor GitHub Issues and Discussions
- Respond to questions within 48 hours
- Review and merge pull requests
- Acknowledge contributors

## Legal Considerations

- Ensure all dependencies are properly licensed (MIT compatible)
- Attribute third-party tools in README.md
- Include license files for bundled assets
- Consider adding a Contributor License Agreement (CLA)

---

## Quick Checklist

### Before Release
- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md`
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Build packages locally

### Release Day
- [ ] Push final commit
- [ ] Create git tag
- [ ] Build and upload to PyPI
- [ ] Create GitHub Release
- [ ] Update Docker Hub images
- [ ] Announce on social media

### Post-Release
- [ ] Monitor for issues
- [ ] Respond to feedback
- [ ] Plan next release

---

**Remember**: Open-source projects thrive on community engagement. Be responsive, welcoming, and appreciative of contributions!