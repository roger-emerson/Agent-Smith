# Script Usage Guide

## Web GUI Scripts

### Launch Web GUI
```bash
./launch_web_gui.sh
```

**What it does:**
- Activates Python virtual environment
- Starts Flask web server
- Automatically finds available port (5000-5010)
- Opens browser to the web interface

**Access:**
- Default: http://127.0.0.1:5000
- If port 5000 is in use, automatically uses next available port

### Stop Web GUI
```bash
./stop_web_gui.sh
```

**What it does:**
- Kills all `web_gui.py` processes
- Frees up ports 5000, 5001, 8080
- Clears Python cache (`__pycache__/`, `*.pyc`)
- Clears Flask cache (`instance/`, `.webassets-cache/`)
- Verifies shutdown completed
- Smart detection of macOS Control Center on port 5000

**Safe to run multiple times:** Will not harm system if nothing is running.

### Verify Security
```bash
./verify_security.sh
```

**What it does:**
- Checks if sensitive files are ignored by git
- Verifies no credentials in git status
- Scans for secrets in staged files
- Checks for hardcoded secrets in code
- Validates example files exist
- Confirms .gitignore is configured

**Exit codes:**
- `0` - All checks passed, safe to commit
- `1` - Issues found, DO NOT commit

## Example Scripts

### Basic Email Agent
```bash
source venv/bin/activate
python examples/basic_agent.py
```

**What it does:**
- Connects to Gmail and Claude
- Fetches 5 unread emails
- Analyzes each with AI
- Shows categorization, priority, sentiment
- **READ-ONLY** - No changes to inbox

### Auto-Label (10 emails)
```bash
source venv/bin/activate
python examples/auto_label.py
```

**What it does:**
- Fetches 10 unread emails
- AI analyzes each email
- **Asks for confirmation** before each action
- Creates Gmail labels based on AI analysis
- Marks low-priority emails as read

**Interactive:** Prompts `y/n/all` for each email

### Auto-Label (30 emails)
```bash
source venv/bin/activate
python examples/auto_label_30.py
```

**What it does:**
- Fetches 30 unread emails
- AI analyzes each email automatically
- **No confirmation** - processes all
- Creates Gmail labels
- Marks low-priority emails as read
- Shows summary by category

**Automatic:** Processes all emails without prompting

## Setup Scripts

### Setup Check
```bash
python setup_check.py
```

**What it does:**
- Verifies Python version
- Checks if virtual environment exists
- Validates dependencies installed
- Confirms credentials.json exists
- Tests .env file has API key
- Validates Gmail OAuth setup

**Exit codes:**
- `0` - All checks passed
- `1` - Setup incomplete

## Port Information

### Default Ports
- **5000** - Flask web GUI (default)
- **5001-5010** - Alternative ports (auto-selected if 5000 busy)

### Port Conflicts
If port 5000 is in use:
1. **macOS Control Center** - Safe to ignore, web_gui will use port 5001
2. **Another Flask app** - Stop it first with `./stop_web_gui.sh`
3. **Other service** - Web GUI will auto-select next available port

### Check What's Using a Port
```bash
lsof -i:5000
```

### Manually Free a Port
```bash
# Find process
lsof -ti:5000

# Kill it
kill -9 $(lsof -ti:5000)
```

## Common Workflows

### Development Cycle
```bash
# Start web GUI
./launch_web_gui.sh

# ... use the application ...

# Stop when done
./stop_web_gui.sh
```

### Before Committing
```bash
# Run security check
./verify_security.sh

# If passed, safe to commit
git add <files>
git commit -m "message"
```

### Quick Email Analysis
```bash
source venv/bin/activate
python examples/basic_agent.py
```

### Bulk Email Labeling
```bash
source venv/bin/activate
python examples/auto_label_30.py
```

## Troubleshooting

### "Port already in use"
```bash
./stop_web_gui.sh
./launch_web_gui.sh
```

### "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "No credentials"
```bash
# Check file exists
ls credentials.json

# If missing, copy example and edit
cp credentials.json.example credentials.json
# Then add your OAuth credentials
```

### "No API key"
```bash
# Check .env exists
cat .env

# If missing, copy and edit
cp .env.example .env
# Then add your Anthropic API key
```

### Clear Everything and Restart
```bash
# Stop all processes
./stop_web_gui.sh

# Clear all cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Restart
./launch_web_gui.sh
```

## Script Permissions

All scripts should be executable:
```bash
chmod +x launch_web_gui.sh
chmod +x stop_web_gui.sh
chmod +x verify_security.sh
chmod +x setup_check.py
```

## Environment Variables

### Required
- `ANTHROPIC_API_KEY` - Your Anthropic API key (in `.env`)

### Optional
- `MODEL` - Claude model to use (default: claude-sonnet-4-5-20250929)
- `PORT` - Web GUI port (default: auto-detect)

## Safety Features

All scripts include:
- ✅ Error handling
- ✅ Verification steps
- ✅ Clear output messages
- ✅ Safe defaults
- ✅ Cleanup on exit

## Getting Help

### View script help
```bash
./script_name.sh --help  # (if implemented)
```

### Check logs
```bash
# Web GUI logs
# (Shown in terminal where you ran launch_web_gui.sh)

# Python errors
# (Shown in script output)
```

### Report issues
Include in your bug report:
1. Script name
2. Error message
3. Output of `./verify_security.sh`
4. Python version: `python3 --version`
5. OS: `uname -a`

---

**All scripts are designed to be safe and idempotent** - you can run them multiple times without harm.
