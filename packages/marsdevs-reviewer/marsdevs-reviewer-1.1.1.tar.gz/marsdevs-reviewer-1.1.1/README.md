# MarsDevs Code Reviewer

> 🔍 AI-powered pre-commit hook that learns your codebase conventions and ensures consistent, high-quality code

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🚀 What is MarsDevs Code Reviewer?

MarsDevs Code Reviewer is an intelligent Git pre-commit hook that automatically reviews your staged changes against your repository's existing coding patterns. Unlike generic linters, it **learns from your codebase** to enforce your team's specific conventions.

### Key Benefits

✅ **Zero Configuration** - Automatically learns from your existing code  
✅ **Repository-Specific** - Enforces YOUR conventions, not generic rules  
✅ **Interactive Fixes** - Accept or reject suggested changes  
✅ **Fast Reviews** - Smart caching for instant re-reviews  
✅ **Non-Intrusive** - Only reviews new changes, not existing code  
✅ **Machine Learning** - Learns from your decisions to reduce API calls over time  

---

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- Git repository
- [Anthropic API key](https://console.anthropic.com)

### Install from PyPI

```bash
pip install marsdevs-reviewer
```

### Set up your API key

```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
export ANTHROPIC_API_KEY='sk-ant-...'
```

### Enable in your repository

```bash
cd your-project
marsdevs-reviewer install
```

That's it! 🎉 MarsDevs will now review all your commits automatically.

---

## 🎯 How It Works

<details>
<summary><b>Click to see how MarsDevs learns your conventions</b></summary>

1. **Analyzes Your Repository** - Finds similar files to understand patterns
2. **Reads Config Files** - Checks `.editorconfig`, `.eslintrc`, `pyproject.toml`, etc.
3. **Reviews Only Changes** - Focuses on new/modified lines in staged files
4. **Suggests Fixes** - Provides corrections that match your codebase style

</details>

### Example Review Session

```bash
$ git commit -m "Add user authentication"

Running MarsDevs Code Reviewer...
📋 Analyzing repository coding conventions...
🔍 Reviewing staged changes against repository conventions...

Found 2 convention issue(s) to review...

------------------------------------------------------------
ISSUE: CONVENTION
File: src/auth.py
Lines: 23-23

Convention Violated: Use project's logging pattern
Example from Codebase:
    logger.info(f"User {user_id} logged in")

Description: Using print() instead of logger
Explanation: Other auth modules use logger.info for consistency

--- Current Code ---
print(f"User {user_id} authenticated")

--- Suggested Fix ---
logger.info(f"User {user_id} authenticated")
------------------------------------------------------------

Apply this fix? (y)es / (n)o / (s)kip all / (q)uit: y
✅ Fix applied successfully!
```

---

## 🛠️ Commands

| Command | Description |
|---------|-------------|
| `marsdevs-reviewer install` | Install pre-commit hook in current repo |
| `marsdevs-reviewer uninstall` | Remove pre-commit hook |
| `marsdevs-reviewer review` | Manually review staged changes |
| `marsdevs-reviewer stats` | Show learning statistics |
| `marsdevs-reviewer clear-cache` | Clear the review cache |
| `marsdevs-reviewer export-learning` | Export learned conventions |
| `marsdevs-reviewer reset-learning` | Reset learning data |
| `marsdevs-reviewer --help` | Show help message |

---

## 🧠 Learning System

MarsDevs learns from your decisions to improve over time:

- **Accepted fixes** increase pattern confidence
- **Rejected fixes** decrease pattern confidence  
- **High confidence patterns** (>70%) skip API calls
- **Learning data** stored locally in `.marsdevs/` directory

Check your learning progress:
```bash
marsdevs-reviewer stats
```

## ⚙️ Configuration

### Skipped Files

By default, these file types are skipped:
- Documentation: `.md`, `.txt`
- Config files: `.json`, `.yml`, `.yaml`, `.toml`
- Lock files: `package-lock.json`, `*.lock`
- Media: `.jpg`, `.png`, `.gif`, `.svg`

### Bypass Review

Need to skip the review temporarily?

```bash
git commit --no-verify -m "Emergency hotfix"
```

### Debug Mode

Having issues? Enable debug mode:

```bash
export MARSDEVS_DEBUG=1
export MARSDEVS_LOG_LEVEL=DEBUG
git commit -m "Debug commit"
```

---

## 🐛 Troubleshooting

<details>
<summary><b>MarsDevs is not running on commit</b></summary>

```bash
# Check if hook is installed
ls -la .git/hooks/pre-commit

# Make hook executable
chmod +x .git/hooks/pre-commit

# Check Git hooks path
git config core.hooksPath
```
</details>

<details>
<summary><b>Import or command not found errors</b></summary>

```bash
# Verify installation
pip show marsdevs-reviewer

# Reinstall
pip install --upgrade marsdevs-reviewer

# Check Python path
which python3
which marsdevs-reviewer
```
</details>

<details>
<summary><b>API connection issues</b></summary>

```bash
# Verify API key is set
echo $ANTHROPIC_API_KEY

# Test API connection
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```
</details>

---

## 👨‍💻 Development

<details>
<summary><b>Setting up for development</b></summary>

```bash
# Clone and setup
git clone https://github.com/marsdevs/marsdevs-reviewer
cd marsdevs-reviewer
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Run tests
python -m pytest tests/ -v

# Enable debug logging
export MARSDEVS_DEBUG=1
```
</details>

<details>
<summary><b>Project structure</b></summary>

```
marsdevs_reviewer/
├── __init__.py          # Package metadata
├── reviewer.py          # Core review logic
├── cli.py              # Command-line interface
├── debug.py            # Debug utilities
└── learning/           # Machine learning system
    ├── __init__.py
    ├── learning_manager.py    # Manages persistent storage
    ├── convention_extractor.py # Extracts patterns
    ├── pattern_matcher.py     # Matches against learned patterns
    └── models.py             # Data structures
```
</details>

<details>
<summary><b>Adding new features</b></summary>

```python
# Add new review check in reviewer.py
def review_code_with_conventions(diff, files, conventions_context):
    prompt = f"""...existing prompt...
    
    6. **Security Issues**: Check for exposed secrets or API keys
    """

# Add new CLI command in cli.py
def stats_command():
    """Show review statistics."""
    # Implementation

# Register in main()
parser.add_argument('command', 
    choices=['install', 'uninstall', 'review', 'clear-cache', 'stats'])
```
</details>

---

## 📝 Publishing to PyPI

<details>
<summary><b>Release checklist</b></summary>

1. **Update version** in `__init__.py`, `setup.py`, and `pyproject.toml`
2. **Run tests**: `python -m pytest tests/`
3. **Build package**: `python -m build`
4. **Test on TestPyPI**: `python -m twine upload --repository testpypi dist/*`
5. **Release**: `python -m twine upload dist/*`
6. **Tag release**: `git tag -a v1.1.0 -m "Release v1.1.0"`
</details>

---

## 🤝 Contributing

We welcome contributions! Here's how to help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Ensure tests pass (`python -m pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Anthropic's Claude API](https://www.anthropic.com)
- Inspired by the need for repository-specific code standards
- Thanks to all contributors and early testers

---

<p align="center">
  <b>🌟 Star this repo if you find it helpful!</b><br>
  <a href="https://github.com/marsdevs/marsdevs-reviewer/issues">Report Bug</a> •
  <a href="https://github.com/marsdevs/marsdevs-reviewer/issues">Request Feature</a> •
  <a href="https://github.com/marsdevs/marsdevs-reviewer/discussions">Discussions</a>
</p>