# Understanding AI Agents

## What is an AI Agent?

An AI agent is different from a simple chatbot or AI tool. Here's the key difference:

### Regular AI (like ChatGPT web interface):
- You ask a question → AI responds
- One-shot interaction
- No ability to take actions

### AI Agent:
- Observes environment → Thinks → Takes action → Observes again
- Continuous loop
- Can interact with tools and systems

## The Agent Loop

```
┌─────────────────────────────────────┐
│  1. PERCEIVE (Observe Environment)  │
│     - Check Gmail inbox             │
│     - Read new emails               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  2. THINK (Use AI to Decide)        │
│     - Understand email content      │
│     - Determine appropriate action  │
│     - Consider context & rules      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  3. ACT (Take Action)               │
│     - Apply labels                  │
│     - Draft reply                   │
│     - Archive email                 │
└──────────────┬──────────────────────┘
               │
               ▼
           (Repeat)
```

## Components of Our Gmail Agent

### 1. Environment Interface (Gmail API)
This is how the agent "sees" and "acts" in the world.

```python
# Perception: Reading emails
emails = gmail.get_unread_emails()

# Action: Labeling an email
gmail.add_label(email_id, "Important")
```

### 2. AI Brain (Claude)
This is where the "thinking" happens.

```python
# The agent sends email content to Claude
response = claude.analyze_email(email_content)

# Claude returns structured decisions
# e.g., {"label": "Work", "priority": "High", "action": "draft_reply"}
```

### 3. Agent Logic (Your Python Code)
This orchestrates everything.

```python
while True:
    # 1. Perceive
    emails = get_new_emails()

    # 2. Think (using AI)
    for email in emails:
        decision = ai.decide_action(email)

        # 3. Act
        execute_action(decision)

    # Wait before next cycle
    time.sleep(60)
```

## Key Concepts

### Prompts: Teaching the Agent

You guide the AI's thinking through **prompts**:

```python
prompt = f"""
You are an email management assistant.

Email Subject: {subject}
Email From: {sender}
Email Content: {content}

Analyze this email and decide:
1. What label should it have? (Work, Personal, Newsletter, Urgent)
2. What priority? (High, Medium, Low)
3. Should we draft a reply? (Yes/No)

Respond in JSON format.
"""
```

### Tools: What the Agent Can Do

Tools are functions the agent can call:

```python
tools = {
    "apply_label": gmail.add_label,
    "draft_reply": gmail.create_draft,
    "archive": gmail.archive_email,
    "mark_important": gmail.star_email
}
```

### Memory: Context & State

Agents can remember things:

```python
# Short-term: Current session
recent_emails = []

# Long-term: Saved to file/database
user_preferences = {
    "auto_archive_newsletters": True,
    "important_senders": ["boss@company.com"]
}
```

## Design Patterns

### Pattern 1: Rule-Based + AI

Combine simple rules with AI intelligence:

```python
# Rule: Always mark emails from boss as important
if sender == "boss@company.com":
    mark_important(email)
else:
    # AI: Decide for everything else
    decision = ai.analyze(email)
    apply_decision(decision)
```

### Pattern 2: AI-First with Human Approval

Let AI decide, but require approval:

```python
decision = ai.analyze(email)
print(f"AI suggests: {decision}")
if input("Approve? (y/n)") == "y":
    execute(decision)
```

### Pattern 3: Fully Autonomous

Agent runs automatically (be careful!):

```python
# Only do this after thorough testing!
decisions = ai.batch_analyze(emails)
for decision in decisions:
    execute(decision)
```

## Safety Considerations

### Start Small
1. Read-only access first
2. Test with one email at a time
3. Always review before enabling automation

### Use Guardrails

```python
# Don't let AI delete anything permanently
ALLOWED_ACTIONS = ["label", "archive", "draft_reply"]

if decision.action not in ALLOWED_ACTIONS:
    print(f"⚠️ Blocked unsafe action: {decision.action}")
    continue
```

### Monitor Behavior

```python
# Log all agent actions
log_action(timestamp, email_id, decision, result)

# Review logs regularly to catch issues
```

## Advanced Concepts (For Later)

### Multi-Step Reasoning
Agent breaks down complex tasks:
1. Read email
2. Search for related emails
3. Check calendar for context
4. Draft reply considering all factors

### Learning from Feedback
```python
# When you correct the agent
if user_corrected_label:
    save_preference(sender, corrected_label)
    # Next time, use learned preference
```

### Chaining Multiple Agents
- Email agent finds action items
- Calendar agent schedules them
- Task agent tracks completion

## Next Steps

Now that you understand the concepts:
1. Follow `GMAIL_SETUP.md` to connect to Gmail
2. Look at `examples/basic_agent.py` to see these concepts in code
3. Start experimenting!

Remember: Start simple, test thoroughly, and gradually add complexity.
