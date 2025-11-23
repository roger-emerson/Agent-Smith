# Gmail API Setup Guide

This guide walks you through setting up Gmail API access for your AI agent.

## Overview

To access Gmail programmatically, you need to:
1. Create a Google Cloud Project
2. Enable Gmail API
3. Create OAuth credentials
4. Authorize your application

Don't worry - this sounds complicated but it's straightforward!

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a Project" → "New Project"
3. Name it "Gmail Agent" (or whatever you like)
4. Click "Create"

## Step 2: Enable Gmail API

1. In your new project, go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click on it and press "Enable"

## Step 3: Create OAuth Credentials

### Why OAuth?
OAuth lets your app access Gmail without storing your password. It's secure and recommended by Google.

### Create Credentials:

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"

3. If prompted to configure OAuth consent screen:
   - Choose "External" (unless you have a Google Workspace)
   - Click "Create"
   - Fill in:
     - App name: "Gmail Agent"
     - User support email: Your email
     - Developer contact: Your email
   - Click "Save and Continue"
   - Skip "Scopes" for now (click "Save and Continue")
   - Add your email as a test user
   - Click "Save and Continue"

4. Back to creating OAuth client ID:
   - Application type: "Desktop app"
   - Name: "Gmail Agent Desktop"
   - Click "Create"

5. **Download the credentials**:
   - Click "Download JSON"
   - Save it as `credentials.json` in your AgentSmith folder

## Step 4: Set Scopes (Permissions)

Your agent needs permission to access Gmail. We'll start with read-only:

```python
# These are defined in the code
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',  # Read emails
    'https://www.googleapis.com/auth/gmail.labels',    # Manage labels
    'https://www.googleapis.com/auth/gmail.modify'     # Modify emails (archive, star, etc.)
]
```

### Available Scopes:

| Scope | What it allows |
|-------|----------------|
| `gmail.readonly` | Read all emails (safest to start) |
| `gmail.labels` | Create and manage labels |
| `gmail.modify` | Modify emails (archive, star, label, etc.) |
| `gmail.compose` | Create and send drafts |
| `gmail.send` | Send emails |

**Recommendation**: Start with `readonly` and `labels` only until you're comfortable.

## Step 5: First Authorization

1. Make sure `credentials.json` is in your AgentSmith folder:
   ```
   AgentSmith/
   ├── credentials.json  ← Downloaded from Google
   ├── src/
   └── ...
   ```

2. Run the basic example:
   ```bash
   python examples/basic_agent.py
   ```

3. First time: Browser will open asking you to:
   - Choose your Google account
   - Review permissions
   - Click "Continue" (you may see a warning - click "Advanced" → "Go to Gmail Agent")
   - Authorize access

4. After authorization:
   - A `token.json` file is created automatically
   - Future runs won't need the browser
   - Your agent is now authorized!

## Troubleshooting

### "Access blocked: This app's request is invalid"
- Make sure you added yourself as a test user in OAuth consent screen
- Check that credentials.json is in the right folder

### "invalid_grant" error
- Delete `token.json` and authorize again
- Check your system clock is correct

### "insufficient permissions"
- You may need to update scopes in the code
- Delete `token.json` and reauthorize

### Still having issues?
- Check the [Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)
- Make sure Gmail API is enabled in Google Cloud Console

## Security Best Practices

### ✅ Do:
- Keep `credentials.json` and `token.json` private (they're in .gitignore)
- Use read-only scopes when possible
- Revoke access if you're not using the app: [Google Account Permissions](https://myaccount.google.com/permissions)

### ❌ Don't:
- Commit credentials to Git
- Share your credentials with anyone
- Use your main Gmail account for initial testing (create a test account)

## Testing Your Setup

After authorization, verify it works:

```bash
python -c "from src.gmail_helper import GmailHelper; gh = GmailHelper(); print('✅ Connected! Found', len(gh.get_recent_emails(5)), 'emails')"
```

If you see "Connected!", you're ready to build your agent! 🎉

## Next Steps

1. ✅ Gmail API is set up
2. Next: Configure your Anthropic API key in `.env`
3. Then: Run your first agent with `examples/basic_agent.py`

## Quick Reference

### File Locations
```
AgentSmith/
├── credentials.json     # Download from Google Cloud (NEVER commit)
├── token.json          # Auto-generated after first auth (NEVER commit)
└── .env                # Your API keys (NEVER commit)
```

### Important Links
- [Google Cloud Console](https://console.cloud.google.com/)
- [Gmail API Reference](https://developers.google.com/gmail/api/reference/rest)
- [Manage App Permissions](https://myaccount.google.com/permissions)
