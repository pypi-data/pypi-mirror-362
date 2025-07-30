# 🤖 AI-Powered Git Commit Message Generator

[![PyPI version](https://badge.fury.io/py/ai-commit-generator.svg)](https://badge.fury.io/py/ai-commit-generator)
[![Python Support](https://img.shields.io/pypi/pyversions/ai-commit-generator.svg)](https://pypi.org/project/ai-commit-generator/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/ai-commit-generator)](https://pepy.tech/project/ai-commit-generator)

**Automatically generate conventional commit messages using AI - No backend/frontend required!**

This tool works as a **Git pre-commit hook** that analyzes your staged changes and generates professional commit messages using AI APIs (Groq, OpenRouter, Cohere).

---

## 🚀 Quick Start (2 minutes)

### 1. Install the Package
```bash
# Install from PyPI (recommended)
pip install ai-commit-generator

# Or install from source
pip install git+https://github.com/your-org/ai-commit-generator.git
```

### 2. Get API Key (Free)
- **Groq** (Recommended): https://console.groq.com/keys
- **OpenRouter**: https://openrouter.ai/keys
- **Cohere**: https://dashboard.cohere.ai/api-keys

### 3. Install in Your Project
```bash
# Go to your project
cd /path/to/your/project

# Install the Git hook
ai-commit-generator install

# Add your API key
echo "GROQ_API_KEY=your_key_here" >> .env
```

### 4. Use It
```bash
# Normal Git workflow - AI handles the message!
git add src/components/Button.js
git commit  # ✨ AI generates: "feat(ui): add Button component with hover effects"
```

---

## 📦 Installation Methods

### Method 1: PyPI (Recommended)
```bash
pip install ai-commit-generator
```

### Method 2: From Source
```bash
git clone https://github.com/your-org/ai-commit-generator.git
cd ai-commit-generator
pip install -e .
```

### Method 3: Legacy Bash Script
For the original bash-based installation, see [LEGACY.md](LEGACY.md).

---

## ✨ Features

- **🤖 AI-Powered**: Uses Groq, OpenRouter, or Cohere APIs
- **📝 Conventional Commits**: Automatic `type(scope): description` format
- **⚡ Fast**: < 2 second response time with Groq
- **🔧 Configurable**: Customize prompts, models, and scopes
- **🛡️ Secure**: Only staged changes sent to AI, no data storage
- **🔄 Fallback**: Works even if AI fails
- **🐍 Python Package**: Easy installation and distribution
- **🧪 Testable**: Comprehensive test suite and type hints
- **🎨 Rich CLI**: Beautiful command-line interface with colors

---

## 🎯 Example Output

**Before:**
```bash
git commit -m "fix"
git commit -m "update"
git commit -m "changes"
```

**After:**
```bash
feat(auth): implement JWT token refresh mechanism
fix(api): resolve race condition in user registration  
docs: update README with installation instructions
refactor(utils): optimize date formatting functions
```

---

## 📁 Project Structure

```
ai-commit-generator/
├── README.md                           # This file
├── TEAM_SETUP_GUIDE.md                # Detailed team documentation
├── pyproject.toml                     # Python package configuration
├── src/
│   └── ai_commit_generator/
│       ├── __init__.py                # Package initialization
│       ├── cli.py                     # Command-line interface
│       ├── core.py                    # Main commit generation logic
│       ├── config.py                  # Configuration management
│       ├── api_clients.py             # AI API clients
│       └── git_hook.py                # Git hook management
├── templates/
│   ├── .commitgen.yml                 # Configuration template
│   └── .env.example                   # Environment template
├── tests/                             # Test suite
├── examples/                          # Usage examples
└── legacy/                            # Original bash scripts
    ├── install_hook.sh                # Legacy installer
    └── hooks/
        └── prepare-commit-msg         # Legacy hook script
```

---

## 🖥️ CLI Commands

### Install Hook
```bash
# Install Git hook in current repository
ai-commit-generator install

# Install with configuration files
ai-commit-generator install --config

# Force overwrite existing hook
ai-commit-generator install --force
```

### Manage Installation
```bash
# Check installation status
ai-commit-generator status

# Test with current staged changes
ai-commit-generator test

# Uninstall hook
ai-commit-generator uninstall
```

### Generate Messages
```bash
# Generate message for staged changes
ai-commit-generator generate

# Generate without writing to file (dry run)
ai-commit-generator generate --dry-run

# Generate and save to specific file
ai-commit-generator generate --output commit-msg.txt
```

### Configuration
```bash
# Show current configuration
ai-commit-generator config --show

# Validate configuration
ai-commit-generator config --validate
```

---

## 🔧 Configuration

### Basic Setup (`.env`)
```bash
# Choose one provider
GROQ_API_KEY=gsk_your_key_here
# OPENROUTER_API_KEY=sk-or-your_key_here
# COHERE_API_KEY=your_cohere_key_here
```

### Advanced Setup (`.commitgen.yml`)
```yaml
api:
  provider: groq
  
commit:
  max_chars: 72
  types: [feat, fix, docs, style, refactor, test, chore]
  scopes: [api, ui, auth, db, config]
  
prompt:
  template: |
    Generate a conventional commit message for:
    {{diff}}
```

---

## 🏢 Team Deployment

### Option 1: Shared Network Drive
```bash
# Copy to shared location
cp -r ai-commit-generator /shared/tools/

# Team members install from shared location
/shared/tools/ai-commit-generator/install_hook.sh
```

### Option 2: Internal Git Repository
```bash
# Create internal repo
git init ai-commit-generator
git add .
git commit -m "feat: add AI commit message generator"
git remote add origin https://github.com/your-org/ai-commit-generator.git
git push -u origin main

# Team members clone and install
git clone https://github.com/your-org/ai-commit-generator.git
cd your-project
../ai-commit-generator/install_hook.sh
```

### Option 3: Package Distribution
```bash
# Create distributable package
tar -czf ai-commit-generator.tar.gz ai-commit-generator/

# Team members download and extract
curl -sSL https://your-server/ai-commit-generator.tar.gz | tar -xz
./ai-commit-generator/install_hook.sh
```

---

## 🛠️ Advanced Usage

### Custom Prompts
```yaml
prompt:
  template: |
    You are a senior developer. Generate a commit message for:
    
    {{diff}}
    
    Requirements:
    - Use conventional commits
    - Be specific about business impact
    - Maximum {{max_chars}} characters
```

### Multiple Models
```bash
# Fast and efficient
GROQ_MODEL=llama3-8b-8192

# More detailed
GROQ_MODEL=llama3-70b-8192

# Creative
GROQ_MODEL=mixtral-8x7b-32768
```

### Debug Mode
```bash
DEBUG_ENABLED=true
tail -f .commitgen.log
```

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| "API key not found" | Check `.env` file, ensure correct variable is set |
| "jq: command not found" | Install jq: `brew install jq` or `apt install jq` |
| "Rate limit exceeded" | Wait 1 minute or switch to different provider |
| "Hook not working" | Reinstall: `./install_hook.sh` |

---

## 📊 Provider Comparison

| Provider | Speed | Cost | Models | Best For |
|----------|-------|------|--------|----------|
| **Groq** | ⚡ Very Fast | 🆓 Free | Llama 3, Mixtral | Teams, Daily Use |
| **OpenRouter** | 🐌 Medium | 💰 Paid | Claude, GPT-4 | Premium Quality |
| **Cohere** | ⚖️ Fast | 🆓 Free Tier | Command-R | Enterprise |

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'feat: add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Conventional Commits](https://www.conventionalcommits.org/) specification
- [Groq](https://groq.com/) for fast AI inference
- [OpenRouter](https://openrouter.ai/) for model diversity
- [Cohere](https://cohere.ai/) for enterprise AI

---

**Transform your team's commit messages today! 🚀**
