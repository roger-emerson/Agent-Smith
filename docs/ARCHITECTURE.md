# Agent Architecture

Understanding how all the pieces fit together.

## System Overview

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR GMAIL ACCOUNT                   │
│                  (The Environment)                      │
└────────────┬────────────────────────────────────────────┘
             │
             │ Gmail API
             │
┌────────────▼────────────────────────────────────────────┐
│                   GmailHelper                           │
│              (src/gmail_helper.py)                      │
│                                                         │
│  • get_emails()      • add_label()                     │
│  • get_unread()      • mark_as_read()                  │
│  • get_email()       • create_draft()                  │
└────────────┬────────────────────────────────────────────┘
             │
             │ Python API
             │
┌────────────▼────────────────────────────────────────────┐
│                   EmailAgent                            │
│                 (src/agent.py)                          │
│                                                         │
│  ┌─────────────────────────────────────────────┐      │
│  │  PERCEIVE → THINK → ACT                     │      │
│  └─────────────────────────────────────────────┘      │
│                                                         │
│  • analyze_email()   ────┐                            │
│  • draft_reply()         │                            │
│  • summarize_inbox()     │                            │
└──────────────────────────┼──────────────────────────────┘
                           │
                           │ Anthropic API
                           │
┌──────────────────────────▼──────────────────────────────┐
│                   Claude (AI)                           │
│                                                         │
│  • Understands email content                           │
│  • Makes decisions                                     │
│  • Generates text                                      │
└─────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Gmail API Layer (`gmail_helper.py`)

**Purpose**: Abstracts away Gmail API complexity

**Key Methods**:
```python
# Reading
get_recent_emails(max_results, query)
get_unread_emails(max_results)
get_email(email_id)

# Actions
add_label(email_id, label_name)
mark_as_read(email_id)
archive_email(email_id)
star_email(email_id)
create_draft(to, subject, body)
```

**Why it exists**: Gmail API is complex. This wrapper makes it simple.

### 2. Prompts (`prompts.py`)

**Purpose**: Instructions that guide Claude's thinking

**Key Prompts**:
```python
get_email_analysis_prompt(email)
  → Returns JSON with category, priority, sentiment

get_reply_draft_prompt(email, context)
  → Returns draft email text

get_summary_prompt(emails)
  → Returns formatted summary
```

**Why it exists**: Prompts are the "programming language" for AI.

### 3. Agent Logic (`agent.py`)

**Purpose**: Orchestrates everything - the "brain" of the system

**Core Loop**:
```python
def process_email(email):
    # 1. PERCEIVE
    email = gmail.get_email(email_id)

    # 2. THINK
    analysis = claude.analyze(email)

    # 3. ACT
    for action in analysis.actions:
        execute(action)
```

**Why it exists**: Coordinates all components into an intelligent agent.

## Data Flow

### Example: Processing an Email

```
1. User runs: python examples/basic_agent.py
                     │
                     ▼
2. Agent: gmail.get_unread_emails()
                     │
                     ▼
3. GmailHelper: calls Gmail API
                     │
                     ▼
4. Returns: [email1, email2, ...]
                     │
                     ▼
5. Agent: For each email...
                     │
                     ▼
6. Agent: analysis = analyze_email(email)
                     │
                     ▼
7. Agent: Builds prompt from templates
                     │
                     ▼
8. Agent: claude.messages.create(prompt)
                     │
                     ▼
9. Claude: Analyzes email content
                     │
                     ▼
10. Returns: {category: "Work", priority: "high", ...}
                     │
                     ▼
11. Agent: Decides actions based on analysis
                     │
                     ▼
12. Agent: gmail.add_label(email_id, "Work")
                     │
                     ▼
13. GmailHelper: Calls Gmail API to apply label
                     │
                     ▼
14. Done! Email is categorized
```

## Prompt Engineering

Prompts are how you "program" the AI. Anatomy of a good prompt:

```python
def get_email_analysis_prompt(email):
    return f"""
    # 1. ROLE/CONTEXT
    You are an intelligent email management assistant.

    # 2. INPUT DATA
    Email Subject: {email['subject']}
    Email From: {email['from']}
    Body: {email['body']}

    # 3. TASK DESCRIPTION
    Analyze this email and categorize it.

    # 4. OUTPUT FORMAT
    Respond with JSON:
    {{
        "category": "Work/Personal/etc",
        "priority": "high/medium/low"
    }}

    # 5. CONSTRAINTS/RULES
    - Only use the categories listed
    - Be concise
    - Focus on actionability
    """
```

### Improving Prompts

You can make the agent "smarter" by editing prompts:

**Example: Adding custom categories**
```python
# In prompts.py, modify get_email_analysis_prompt()

# Before:
"category": Choose from: Work, Personal, Newsletter

# After:
"category": Choose from: Work, Personal, Newsletter, Family, Bills, Travel
```

**Example: Changing behavior**
```python
# Make agent more conservative
"priority": Only mark as "high" if truly urgent and time-sensitive

# Make agent more aggressive
"priority": Mark as "high" if it might need attention within 24 hours
```

## Extension Points

### Adding New Actions

1. **Add to GmailHelper**:
```python
def forward_email(self, email_id, to_address):
    # Implementation
    pass
```

2. **Add to Agent**:
```python
def auto_forward_receipts(self):
    receipts = self.gmail.get_recent_emails(query='subject:receipt')
    for receipt in receipts:
        self.gmail.forward_email(receipt['id'], 'accounting@company.com')
```

3. **Create example**:
```python
# examples/auto_forward.py
agent = EmailAgent()
agent.auto_forward_receipts()
```

### Adding New Analysis Types

1. **Create prompt** in `prompts.py`:
```python
def get_meeting_extraction_prompt(email):
    return """Extract meeting details from this email..."""
```

2. **Add method** to `agent.py`:
```python
def extract_meetings(self, email):
    prompt = prompts.get_meeting_extraction_prompt(email)
    response = self.client.messages.create(...)
    return parse_response(response)
```

3. **Use in workflow**:
```python
# examples/calendar_sync.py
meetings = agent.extract_meetings(email)
add_to_calendar(meetings)
```

## Security Considerations

### What Has Access to What?

```
credentials.json
  └─> Proves your app is authorized by Google
  └─> Contains: client_id, client_secret
  └─> NEVER commit to Git

token.json
  └─> Your personal access token
  └─> Contains: access_token, refresh_token
  └─> NEVER commit to Git
  └─> Expires/refreshes automatically

ANTHROPIC_API_KEY
  └─> Your Claude API key
  └─> Contains: API key
  └─> NEVER commit to Git
  └─> Set in .env file
```

### Scopes and Permissions

The agent only gets permissions you grant:

```python
SCOPES = [
    'gmail.readonly',     # Can read emails
    'gmail.labels',       # Can manage labels
    'gmail.modify'        # Can archive, star, etc.
    # 'gmail.send'        # NOT included - can't send emails
]
```

To add sending capability:
1. Add `'gmail.send'` to SCOPES
2. Delete `token.json`
3. Reauthorize

### Best Practices

1. **Start read-only**: Use `gmail.readonly` until confident
2. **Test account first**: Don't use your main Gmail
3. **Review actions**: Check what the agent does
4. **Limit scope**: Only add permissions you need
5. **Monitor usage**: Check agent behavior regularly

## Performance Considerations

### API Rate Limits

**Gmail API**:
- 250 quota units per user per second
- 1 billion quota units per day

Most operations = 5 units, so ~50 requests/second

**Anthropic API**:
- Depends on your plan
- Rate limits shown in API response headers

### Optimization Tips

```python
# ❌ Slow: Analyze emails one by one
for email in emails:
    analysis = agent.analyze_email(email)

# ✅ Better: Batch when possible
analyses = []
for email in emails[:10]:  # Process in chunks
    analyses.append(agent.analyze_email(email))

# ✅ Best: Use async for true parallelism
# (requires async/await implementation)
```

### Token Usage

Claude pricing is per token. Optimize by:

```python
# ❌ Wasteful: Send entire email body
body = email['body']  # Could be 10,000+ tokens

# ✅ Efficient: Truncate long emails
body = email['body'][:2000]  # First 2000 chars

# ✅ Smart: Use snippets for simple tasks
snippet = email['snippet']  # Gmail's built-in preview
```

## Debugging

### Common Issues

**"Analysis returns error"**
- Check: Is email['body'] empty?
- Check: Is the response valid JSON?
- Solution: Add error handling

**"Actions not applied"**
- Check: Do you have the right scopes?
- Check: Is the email_id correct?
- Solution: Test GmailHelper methods directly

**"Rate limit exceeded"**
- Check: How many API calls per second?
- Solution: Add delays between requests

### Debugging Tools

```python
# Print raw email data
print(json.dumps(email, indent=2))

# Print AI prompt
prompt = prompts.get_email_analysis_prompt(email)
print(prompt)

# Print AI response
print(response.content[0].text)

# Test individual components
gmail = GmailHelper()
print(gmail.get_recent_emails(1))
```

## What You've Built

You now have:

1. ✅ Gmail API integration
2. ✅ AI-powered email analysis
3. ✅ Automated labeling system
4. ✅ Reply drafting capability
5. ✅ Custom workflow framework

You understand:

1. ✅ Agent architecture (perceive-think-act)
2. ✅ Prompt engineering
3. ✅ API integration
4. ✅ Security best practices

## Next Steps

- Read about [Advanced Patterns](https://docs.anthropic.com/claude/docs)
- Explore [Gmail API Docs](https://developers.google.com/gmail/api)
- Join the [Anthropic Discord](https://discord.gg/anthropic)
- Build something amazing!

The foundation is solid. Now innovate! 🚀
