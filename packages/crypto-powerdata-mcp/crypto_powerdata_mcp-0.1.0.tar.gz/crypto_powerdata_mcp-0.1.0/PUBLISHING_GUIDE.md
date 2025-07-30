# Publishing Guide - Making crypto-powerdata-mcp Available via uvx

This guide explains how to publish your MCP service to PyPI so users can run it directly with `uvx crypto-powerdata-mcp`.

## 📋 Prerequisites

1. **PyPI Account**: Create account at [pypi.org](https://pypi.org/account/register/)
2. **API Token**: Generate API token at [pypi.org/manage/account/token/](https://pypi.org/manage/account/token/)
3. **GitHub Repository**: Push your code to GitHub
4. **UV Installed**: Install [uv](https://docs.astral.sh/uv/) for package management

## 🚀 Quick Publishing Steps

### 1. Prepare for Publication

```bash
# Run pre-publication checks
python scripts/pre_publish_check.py

# Fix any issues reported by the checks
```

### 2. Bump Version (if needed)

```bash
# Bump patch version (0.1.0 -> 0.1.1)
python scripts/bump_version.py patch

# Bump minor version (0.1.0 -> 0.2.0)
python scripts/bump_version.py minor

# Bump major version (0.1.0 -> 1.0.0)
python scripts/bump_version.py major
```

### 3. Publish to PyPI

```bash
# Automated publishing script
python scripts/publish.py

# Or manual steps:
uv add --dev build twine
uv run python -m build
uv run twine check dist/*
uv run twine upload dist/*
```

### 4. Test Installation

```bash
# Test that users can now run your package
uvx crypto-powerdata-mcp --help

# Test in different modes
uvx crypto-powerdata-mcp --http
```

## 🔄 Automated Publishing with GitHub Actions

### Setup GitHub Secrets

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Add new repository secret:
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI API token (starts with `pypi-`)

### Trigger Automated Publishing

```bash
# Method 1: Create GitHub Release (Recommended)
git tag v0.1.0
git push --tags
# Then create release on GitHub UI

# Method 2: Manual workflow trigger
# Go to Actions tab → Publish to PyPI → Run workflow
```

## 📦 Package Structure for uvx

Your package is already configured correctly for uvx usage:

```
crypto-powerdata-mcp/
├── src/
│   ├── __init__.py
│   ├── cli.py          # CLI entry point
│   ├── main.py         # MCP server logic
│   └── ...
├── pyproject.toml      # Package configuration
├── MANIFEST.in         # File inclusion rules
└── scripts/            # Publishing utilities
```

### Key Configuration in pyproject.toml

```toml
[project.scripts]
crypto-powerdata-mcp = "src.cli:main"  # This enables uvx usage
```

## 🎯 User Experience After Publishing

Once published, users can:

### Direct Usage
```bash
# Run MCP server
uvx crypto-powerdata-mcp

# Run HTTP server
uvx crypto-powerdata-mcp --http

# Run with environment variables
uvx crypto-powerdata-mcp --env OKX_API_KEY=key --env OKX_SECRET_KEY=secret
```

### Claude Desktop Integration
```json
{
  "mcpServers": {
    "crypto-powerdata": {
      "command": "uvx",
      "args": ["crypto-powerdata-mcp"],
      "env": {
        "OKX_API_KEY": "your_key"
      }
    }
  }
}
```

### MCP Studio Integration
```json
{
  "name": "Crypto PowerData MCP",
  "command": "uvx",
  "args": ["crypto-powerdata-mcp"]
}
```

## 🔍 Verification Steps

After publishing, verify everything works:

### 1. Check PyPI Page
- Visit: https://pypi.org/project/crypto-powerdata-mcp/
- Verify description, version, and metadata

### 2. Test Installation
```bash
# Test direct execution
uvx crypto-powerdata-mcp --version

# Test different modes
uvx crypto-powerdata-mcp --help
uvx crypto-powerdata-mcp --http --env HTTP_PORT=8080
```

### 3. Test MCP Integration
```bash
# Test with MCP client
echo '{"method": "tools/list"}' | uvx crypto-powerdata-mcp
```

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**: Check `src/__init__.py` exists and imports are correct
2. **Missing Dependencies**: Verify all dependencies in `pyproject.toml`
3. **CLI Not Working**: Check `[project.scripts]` configuration
4. **Permission Denied**: Verify PyPI API token has correct permissions

### Debug Commands

```bash
# Check package structure
uv run python -m build
tar -tzf dist/*.tar.gz

# Test local installation
pip install dist/*.whl
crypto-powerdata-mcp --help

# Check dependencies
uv tree
```

## 📈 Maintenance

### Regular Updates

1. **Monitor Usage**: Check PyPI download statistics
2. **Update Dependencies**: Keep dependencies current
3. **Version Management**: Use semantic versioning
4. **Documentation**: Keep README and docs updated

### Release Checklist

- [ ] Run pre-publication checks
- [ ] Update version number
- [ ] Update CHANGELOG.md
- [ ] Test locally with uvx
- [ ] Commit and tag release
- [ ] Push to GitHub
- [ ] Create GitHub release
- [ ] Verify PyPI publication
- [ ] Test uvx installation
- [ ] Update documentation

## 🎉 Benefits of uvx Distribution

- ✅ **No Installation Required**: Users don't need to clone repo
- ✅ **Automatic Updates**: uvx uses latest published version
- ✅ **Dependency Isolation**: No conflicts with user's environment
- ✅ **Cross-Platform**: Works on Windows, macOS, Linux
- ✅ **Easy Integration**: Simple MCP client configuration
- ✅ **Professional Distribution**: Standard Python packaging
