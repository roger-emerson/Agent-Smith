# AgentSmith - Your Personal Gmail AI Agent 🤖

A beginner-friendly tutorial for building your first AI agent that manages your Gmail inbox.

## What You'll Learn

- What AI agents are and how they work
- How to connect to Gmail API
- How to use Claude (Anthropic's AI) to process emails
- Basic agent design patterns
- Real-world automation with AI

## What is an AI Agent?

An **AI agent** is a program that:
1. **Perceives** - Observes its environment (your Gmail inbox)
2. **Thinks** - Uses AI to understand and decide what to do
3. **Acts** - Takes actions based on those decisions (reply, label, archive, etc.)

Think of it as a smart assistant that can read your emails and help manage them automatically.

## Prerequisites

- Python 3.8 or higher
- A Gmail account
- Basic Python knowledge
- An Anthropic API key (for Claude)

## Quick Start

### Option 1: Web GUI (Recommended)

```bash
# 1. Set up (first time only)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure credentials (see SETUP.md)
cp .env.example .env
cp credentials.json.example credentials.json
# Edit both files with your credentials

# 3. Launch web interface
./launch_web_gui.sh
```

Browser opens automatically at http://127.0.0.1:5000

### Option 2: Command Line

```bash
# Basic email analysis (read-only)
source venv/bin/activate
python examples/basic_agent.py

# Auto-label 30 emails
python examples/auto_label_30.py
```

See [SETUP.md](SETUP.md) for detailed setup instructions.

### 4. Run Your First Agent

```bash
python examples/basic_agent.py
```

## Project Structure

```
AgentSmith/
├── README.md                 # You are here!
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment variables
├── docs/
│   ├── GMAIL_SETUP.md       # Step-by-step Gmail API setup
│   └── AGENT_CONCEPTS.md    # Understanding AI agents
├── src/
│   ├── gmail_helper.py      # Gmail API wrapper
│   ├── agent.py             # Main agent logic
│   └── prompts.py           # AI prompts for different tasks
└── examples/
    ├── basic_agent.py       # Simple email reader
    ├── auto_label.py        # Automatically label emails
    └── smart_reply.py       # Draft replies to emails
```

## Features You'll Build

### 1. Email Reading & Understanding
Your agent will read emails and understand their content, sentiment, and importance.

### 2. Smart Labeling
Automatically categorize emails (work, personal, newsletters, urgent, etc.)

### 3. Draft Replies
Generate helpful draft replies based on email content.

### 4. Email Summarization
Get daily summaries of your inbox.

## Tutorial Progression

1. **Level 1**: Read emails and have Claude summarize them
2. **Level 2**: Automatically label/categorize emails
3. **Level 3**: Generate draft replies
4. **Level 4**: Build custom workflows (your choice!)

## Safety & Best Practices

⚠️ **Important**: This agent will have access to your email. Start with:
- A test Gmail account (not your main one)
- Read-only permissions first
- Review all actions before enabling automation

## Getting Help

- Check `docs/` for detailed guides
- Review `examples/` for working code
- Each Python file has extensive comments

## Next Steps

1. Read `docs/AGENT_CONCEPTS.md` to understand agent architecture
2. Follow `docs/GMAIL_SETUP.md` to set up Gmail API
3. Start with `examples/basic_agent.py`

Let's build your first AI agent! 🚀
