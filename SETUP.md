# Quick Setup Guide

## Prerequisites

- Python 3.14+
- Gmail account
- Anthropic API key

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/AgentSmith.git
cd AgentSmith
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up credentials

#### Anthropic API Key

1. Get your API key from https://console.anthropic.com/
2. Copy the example env file:
```bash
cp .env.example .env
```
3. Edit `.env` and add your API key:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE
```

#### Gmail OAuth Credentials

1. Follow the detailed guide in `docs/GMAIL_SETUP.md`
2. Download your `credentials.json` from Google Cloud Console
3. Choose **Desktop App** as the application type
4. Place `credentials.json` in the project root

### 5. Run the application

#### Web GUI (Recommended)

```bash
./launch_web_gui.sh
```

Or manually:
```bash
source venv/bin/activate
python web_gui.py
```

Then open http://127.0.0.1:5000 in your browser.

#### Command Line Examples

```bash
# Basic email analysis
python examples/basic_agent.py

# Auto-label 30 emails
python examples/auto_label_30.py

# Auto-label (original)
python examples/auto_label.py
```

## First Run

On first run, you'll be prompted to authorize the app:

1. A browser window will open
2. Sign in with your Gmail account
3. Grant the requested permissions
4. Return to the application

A `token.json` file will be created to save your authorization.

## Troubleshooting

### "No module named '_tkinter'"

Use the web GUI instead:
```bash
python web_gui.py
```

### "No Anthropic API key found"

Make sure:
1. `.env` file exists in project root
2. Contains `ANTHROPIC_API_KEY=your_key_here`
3. No extra spaces around the `=`

### "Missing credentials file"

1. Check `credentials.json` exists in project root
2. Verify it's a valid JSON file
3. Should have `"installed"` key for desktop app

### OAuth redirect errors

Make sure you created a **Desktop app** OAuth client, not Web app.

## Security

⚠️ **NEVER commit these files:**
- `.env`
- `credentials.json`
- `token.json`
- `desktop.credentials.json`
- `web.credentials.json`

See [SECURITY.md](SECURITY.md) for more details.

## Next Steps

1. Read the full documentation in `README.md`
2. Check out example scripts in `examples/`
3. Customize prompts in `src/prompts.py`
4. Build your own workflows!

## Support

- Issues: https://github.com/yourusername/AgentSmith/issues
- Gmail Setup: `docs/GMAIL_SETUP.md`
- Security: `SECURITY.md`
