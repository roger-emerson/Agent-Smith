# Documentation Index

Complete guide to all AgentSmith documentation.

## 📚 Getting Started

### For New Users
1. **[README.md](README.md)** - Project overview and quick start
2. **[SETUP.md](SETUP.md)** - Detailed setup instructions
3. **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
4. **[docs/GMAIL_SETUP.md](docs/GMAIL_SETUP.md)** - Gmail API configuration

### First Steps
```
README.md → SETUP.md → GMAIL_SETUP.md → Launch web_gui.py
```

## 🖥️ Using the Application

### Web Interface
- **[GUI_README.md](GUI_README.md)** - Complete web GUI documentation
  - Features overview
  - How to use each tab
  - Tips and tricks
  - Troubleshooting

### Command Line
- **[README_SCRIPTS.md](README_SCRIPTS.md)** - All scripts explained
  - launch_web_gui.sh
  - stop_web_gui.sh
  - verify_security.sh
  - Example scripts usage

## 🔧 Technical Documentation

### Architecture
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design
  - Component overview
  - Data flow
  - API interactions

### Concepts
- **[docs/AGENT_CONCEPTS.md](docs/AGENT_CONCEPTS.md)** - AI agent theory
  - What are agents?
  - Perception-thought-action loop
  - Design patterns

### Source Code
- `src/agent.py` - Main email agent class
- `src/gmail_helper.py` - Gmail API wrapper
- `src/prompts.py` - AI prompts
- `web_gui.py` - Web interface
- `examples/` - Example scripts

## 🔒 Security

### Essential Reading
- **[SECURITY.md](SECURITY.md)** - Security best practices ⚠️ READ THIS!
  - What NOT to commit
  - Protecting credentials
  - If credentials are exposed
  - Security tools

### Before Committing
- **[PRE_COMMIT_CHECKLIST.md](PRE_COMMIT_CHECKLIST.md)** - Pre-commit checks
  - Required checks
  - What to verify
  - How to fix issues

### Cleanup Summary
- **[CLEANUP_SUMMARY.md](CLEANUP_SUMMARY.md)** - Repository cleanup log
  - Files removed
  - Files added
  - Security improvements

## 🚀 Advanced Topics

### Next Steps
- **[docs/NEXT_STEPS.md](docs/NEXT_STEPS.md)** - Beyond basics
  - Advanced features
  - Custom workflows
  - Integration ideas

### Development
- Contributing guidelines (coming soon)
- Testing procedures (coming soon)
- API documentation (coming soon)

## 📋 Quick Reference

### Common Tasks

| Task | Document |
|------|----------|
| Install and setup | [SETUP.md](SETUP.md) |
| Launch web GUI | [GUI_README.md](GUI_README.md) |
| Run examples | [README_SCRIPTS.md](README_SCRIPTS.md) |
| Configure Gmail | [docs/GMAIL_SETUP.md](docs/GMAIL_SETUP.md) |
| Check security | [SECURITY.md](SECURITY.md) |
| Before commit | [PRE_COMMIT_CHECKLIST.md](PRE_COMMIT_CHECKLIST.md) |
| Troubleshooting | [GUI_README.md](GUI_README.md#troubleshooting) |

### By Role

**End User:**
1. README.md
2. SETUP.md
3. GUI_README.md

**Developer:**
1. docs/ARCHITECTURE.md
2. docs/AGENT_CONCEPTS.md
3. Source code in src/

**Contributor:**
1. SECURITY.md
2. PRE_COMMIT_CHECKLIST.md
3. README_SCRIPTS.md

## 🆕 What's New

### Recent Additions
- ✅ **Web GUI** - Beautiful Flask-based interface
- ✅ **Auto-labeling** - Process 30 emails automatically
- ✅ **Security docs** - Comprehensive security guide
- ✅ **Stop script** - Clean shutdown script
- ✅ **Auto port detection** - Smart port selection
- ✅ **Example credentials** - Template files for users

### Changed Files
- `src/agent.py` - Fixed JSON parsing for Claude responses
- `.gitignore` - Enhanced security rules
- `web_gui.py` - Auto port detection added
- `README.md` - Updated with web GUI info

## 📁 File Structure

```
AgentSmith/
├── README.md                    ← Start here
├── SETUP.md                     ← Setup guide
├── QUICKSTART.md                ← Quick start
├── SECURITY.md                  ← Security (important!)
├── GUI_README.md                ← Web GUI docs
├── README_SCRIPTS.md            ← Scripts guide
├── PRE_COMMIT_CHECKLIST.md      ← Pre-commit checks
├── CLEANUP_SUMMARY.md           ← Cleanup log
├── DOCUMENTATION_INDEX.md       ← This file
│
├── docs/                        ← Technical docs
│   ├── GMAIL_SETUP.md          ← Gmail setup
│   ├── ARCHITECTURE.md         ← System design
│   ├── AGENT_CONCEPTS.md       ← Agent theory
│   └── NEXT_STEPS.md           ← Advanced topics
│
├── src/                         ← Source code
│   ├── agent.py                ← Main agent
│   ├── gmail_helper.py         ← Gmail API
│   └── prompts.py              ← AI prompts
│
├── examples/                    ← Example scripts
│   ├── basic_agent.py          ← Simple demo
│   ├── auto_label.py           ← Auto-label (10)
│   └── auto_label_30.py        ← Auto-label (30)
│
├── templates/                   ← Web GUI templates
│   └── index.html              ← Main interface
│
├── web_gui.py                   ← Web server
├── launch_web_gui.sh            ← Start GUI
├── stop_web_gui.sh              ← Stop GUI
├── verify_security.sh           ← Security check
│
├── .env.example                 ← API key template
├── credentials.json.example     ← OAuth template
└── requirements.txt             ← Dependencies
```

## 🎯 Learning Paths

### Path 1: Quick Start (15 minutes)
1. README.md (overview)
2. SETUP.md (setup)
3. Launch web GUI
4. Try it out!

### Path 2: Developer (1 hour)
1. README.md
2. docs/AGENT_CONCEPTS.md
3. docs/ARCHITECTURE.md
4. Read source code
5. Run examples
6. Customize prompts

### Path 3: Contributor (30 minutes)
1. SECURITY.md
2. PRE_COMMIT_CHECKLIST.md
3. CLEANUP_SUMMARY.md
4. README_SCRIPTS.md

## 🔍 Finding Information

### By Topic

**Setup & Installation:**
- SETUP.md
- docs/GMAIL_SETUP.md
- requirements.txt

**Usage:**
- GUI_README.md (web interface)
- README_SCRIPTS.md (command line)
- examples/ (code examples)

**Security:**
- SECURITY.md (best practices)
- PRE_COMMIT_CHECKLIST.md (checks)
- .gitignore (protected files)

**Development:**
- docs/ARCHITECTURE.md (design)
- docs/AGENT_CONCEPTS.md (theory)
- src/ (source code)

**Troubleshooting:**
- GUI_README.md (web GUI issues)
- README_SCRIPTS.md (script issues)
- SETUP.md (setup issues)

## 📞 Getting Help

1. Check relevant documentation above
2. Run `./verify_security.sh` for security issues
3. Check `python setup_check.py` for setup issues
4. Review error messages carefully
5. Search issues on GitHub
6. Create new issue with details

## ✏️ Contributing to Docs

When adding documentation:
1. Follow existing format
2. Update this index
3. Add to relevant section
4. Cross-reference related docs
5. Run security check
6. Update CLEANUP_SUMMARY.md

---

**Last Updated:** 2025-11-23

*All documentation is up to date with the latest changes.*
