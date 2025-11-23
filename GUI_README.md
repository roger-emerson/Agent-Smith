# AgentSmith Web GUI - Email AI Agent

A beautiful, modern web interface for managing your Gmail inbox with AI.

## Features

### 📧 Email Summaries
- View all unread emails in a clean interface
- AI-powered analysis of email content
- Categorization (Work, Personal, Newsletter, etc.)
- Priority assessment (high, medium, low)
- Sentiment analysis
- Suggested actions

### ✏️ Prompt Viewer
- View AI analysis prompts
- Explore different prompt types
- See how the AI thinks
- Understand email analysis logic

### 📊 Statistics
- Email category breakdown
- Priority distribution
- Analysis insights
- Visual summaries

### 🤖 Agent Capabilities
- **Email Analysis**: Automatically categorize and prioritize emails
- **Auto-Labeling**: Apply Gmail labels based on AI analysis
- **Smart Filtering**: Identify emails to archive or keep
- **Inbox Summary**: Get daily inbox summaries
- **Action Extraction**: Extract tasks from emails

## Quick Start

### 1. Launch the Web GUI

**Option A: Using the launch script (Recommended)**
```bash
./launch_web_gui.sh
```

**Option B: Manual launch**
```bash
source venv/bin/activate
python web_gui.py
```

Browser opens automatically at http://127.0.0.1:5000

### 2. Connect to Services

1. Click **"Connect to Gmail & Claude"** button
2. First time: Browser opens to authorize Gmail
3. Grant permissions and return to the app
4. Connection status shows "Connected successfully!"

### 3. Fetch and Analyze Emails

1. Click **"Fetch Emails"** button
2. Adjust "Max emails" if needed (default: 30)
3. Wait for emails to load
4. Browse the email list
5. Click an email to view details
6. Click **"Analyze"** to get AI insights

## How to Use

### Emails Tab

**Fetching Emails:**
1. Go to the **📧 Emails** tab
2. Click "Fetch Emails"
3. Emails appear in the list below
4. Each shows: Subject, From, Date, Snippet

**Viewing Details:**
1. Click on any email in the list
2. Full email details appear in the right pane
3. Shows: Subject, From, To, Date, Full Body

**Analyzing Emails:**
- **Single Email**: Select email → Click "Analyze"
- **All Emails**: Click "Analyze All Emails" → Confirm
- Analysis shows:
  - Category (Work, Personal, Newsletter, etc.)
  - Priority (high, medium, low)
  - Sentiment (positive, neutral, negative)
  - Action needed (yes/no)
  - Suggested labels

### Prompts Tab

**Viewing Prompts:**
1. Go to the **✏️ Prompts** tab
2. Select a prompt type from dropdown:
   - Email Analysis
   - Reply Draft
   - Inbox Summary
   - Smart Filter
3. Click "Load Prompt"
4. See the AI prompt template
5. Understand how the AI thinks

**Prompt Types:**
- **Email Analysis**: How emails are categorized
- **Reply Draft**: How responses are generated
- **Summary**: How inbox summaries are created
- **Smart Filter**: How emails are filtered

### Stats Tab

**Viewing Statistics:**
1. Go to the **📊 Stats** tab
2. Click "Refresh Stats"
3. See:
   - Total emails fetched
   - Emails analyzed
   - Category breakdown
   - Priority distribution

## Web Interface Components

### Navigation Bar
- AgentSmith logo and title
- Navigation tabs: Emails | Prompts | Stats

### Email List
- Scrollable list of emails
- Click to select
- Shows key info at a glance

### Detail Pane
- Full email content
- AI analysis results
- Category badges
- Priority indicators

### Control Buttons
- Connect to Gmail & Claude
- Fetch Emails
- Analyze (single)
- Analyze All Emails
- Load Prompt
- Refresh Stats

### Status Area
- Connection status
- Operation feedback
- Error messages
- Success confirmations

## Tips & Tricks

### Performance
- Start with fewer emails (10-15) for faster analysis
- Increase to 30 for full inbox processing
- Web GUI is faster than command line for bulk operations

### Analysis
- Analyze all emails to get complete statistics
- Individual analysis is faster for single emails
- Analysis results are cached during session

### Prompts
- Review prompts to understand AI behavior
- See what information the AI considers
- Learn how categories are assigned

### Workflow
1. Connect once per session
2. Fetch emails
3. Review in list
4. Analyze interesting ones
5. Check stats for overview

## Troubleshooting

### Web GUI won't start
```bash
# Check if port 5000 is in use
lsof -i :5000

# Kill process if needed
./stop_web_gui.sh

# Launch again
./launch_web_gui.sh
```

### Port 5000 is busy
The web GUI automatically detects available ports (5000-5010).
If port 5000 is in use, it will use 5001, 5002, etc.

### Connection fails
- Check your `credentials.json` file exists
- Ensure you've authorized the desktop app
- Verify your `.env` file has `ANTHROPIC_API_KEY`
- Run `python examples/basic_agent.py` first to test

### Analysis fails
- Check your Anthropic API key in `.env`
- Ensure you have internet connection
- Verify API quota hasn't been exceeded
- Check browser console for errors (F12)

### Browser doesn't open
Manually open: http://127.0.0.1:5000

### Email list is empty
- Click "Fetch Emails" button
- Check you have unread emails in Gmail
- Try increasing "Max emails" number
- Verify Gmail connection succeeded

## Architecture

```
web_gui.py (Flask Server)
├── Routes
│   ├── / (Main page)
│   ├── /api/connect
│   ├── /api/fetch_emails
│   ├── /api/email/<id>
│   ├── /api/analyze/<id>
│   ├── /api/analyze_all
│   ├── /api/prompts
│   ├── /api/prompt/<type>
│   └── /api/stats
│
└── templates/index.html
    ├── Email Tab (Fetch, View, Analyze)
    ├── Prompts Tab (View AI prompts)
    └── Stats Tab (Analytics)
```

## Stopping the Web GUI

**Option A: In terminal**
Press `Ctrl+C`

**Option B: Using stop script**
```bash
./stop_web_gui.sh
```

The stop script will:
- Kill Flask processes
- Free port 5000 (and 5001, 8080)
- Clear Python cache
- Clear Flask cache
- Verify clean shutdown

## Security

⚠️ **Important**: The web GUI runs locally on http://127.0.0.1:5000
- Only accessible from your computer
- Not exposed to the internet
- Credentials stay on your machine
- No data sent to external servers (except Gmail/Anthropic APIs)

## Command Line Alternative

If you prefer command line:
```bash
# Basic analysis
python examples/basic_agent.py

# Auto-label 10 emails
python examples/auto_label.py

# Auto-label 30 emails
python examples/auto_label_30.py
```

See [README_SCRIPTS.md](README_SCRIPTS.md) for script documentation.

## Support

For issues or questions:
1. Check the main [README.md](README.md)
2. Review [SETUP.md](SETUP.md)
3. Read [docs/GMAIL_SETUP.md](docs/GMAIL_SETUP.md)
4. Check [SECURITY.md](SECURITY.md)
5. See [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)

---

**AgentSmith Web GUI v1.0**
*Powered by Flask & Claude AI*
