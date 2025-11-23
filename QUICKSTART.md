# Quick Start Guide

Get your Gmail agent running in 10 minutes!

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Get Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Go to "API Keys"
4. Create a new key
5. Copy it

## Step 3: Set Up Environment

```bash
cp .env.example .env
```

Edit `.env` and paste your API key:
```
ANTHROPIC_API_KEY=your_key_here
```

## Step 4: Set Up Gmail API

This is the longest step but only done once!

### Quick Version:
1. Go to https://console.cloud.google.com/
2. Create new project
3. Enable Gmail API
4. Create OAuth credentials (Desktop app)
5. Download as `credentials.json`
6. Place in this folder

### Detailed Version:
See `docs/GMAIL_SETUP.md` for step-by-step instructions with screenshots.

## Step 5: Run Your First Agent!

```bash
python examples/basic_agent.py
```

First time:
- Browser opens
- Sign in to Google
- Grant permissions
- `token.json` is created

After that, it runs automatically!

## What to Do Next

1. **Read the concepts**: `docs/AGENT_CONCEPTS.md`
2. **Try the examples**:
   - `examples/basic_agent.py` - Read and analyze emails
   - `examples/auto_label.py` - Auto-categorize emails
   - `examples/smart_reply.py` - Draft replies
   - `examples/inbox_summary.py` - Get inbox overview

3. **Customize**:
   - Edit prompts in `src/prompts.py`
   - Modify agent behavior in `src/agent.py`
   - Build your own examples!

## Common Issues

### "No module named google"
```bash
pip install -r requirements.txt
```

### "credentials.json not found"
You need to download it from Google Cloud Console.
See `docs/GMAIL_SETUP.md`

### "ANTHROPIC_API_KEY not set"
Edit your `.env` file and add your API key.

### "invalid_grant"
Delete `token.json` and run again to re-authorize.

## File Structure

```
AgentSmith/
├── credentials.json     ← Download from Google (don't commit!)
├── token.json          ← Auto-generated (don't commit!)
├── .env                ← Your API keys (don't commit!)
├── src/
│   ├── gmail_helper.py ← Gmail API wrapper
│   ├── agent.py        ← AI agent logic
│   └── prompts.py      ← AI prompts
└── examples/           ← Start here!
```

## Safety Tips

1. **Start with a test Gmail account** (not your main one)
2. **Review all actions** before enabling auto-apply
3. **Never commit** credentials.json, token.json, or .env
4. All example scripts are safe - they ask for confirmation

## Need Help?

- Check `docs/` for detailed guides
- Read code comments in `src/` and `examples/`
- Start simple and build up gradually

## Next Steps

After trying the examples, you can:

1. **Customize prompts** - Change how the AI thinks
2. **Add new actions** - Archive, forward, etc.
3. **Build workflows** - Chain multiple agents
4. **Add scheduling** - Run automatically every hour
5. **Create your own agent** - The code is yours to modify!

Happy agent building! 🤖
