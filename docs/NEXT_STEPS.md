# Next Steps: Beyond the Basics

You've built a working Gmail agent! Here's how to take it further.

## Level Up Your Agent

### 1. Add Scheduling (Run Automatically)

Make your agent run every hour:

**Using cron (Mac/Linux)**:
```bash
# Edit crontab
crontab -e

# Add this line (runs every hour)
0 * * * * cd /path/to/AgentSmith && python examples/auto_label.py
```

**Using Python scheduler**:
```python
import schedule
import time

def run_agent():
    agent = EmailAgent()
    agent.process_inbox(auto_apply=True)

# Run every hour
schedule.every().hour.do(run_agent)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 2. Add Persistent Memory

Save what the agent learns:

```python
import json

class SmartAgent(EmailAgent):
    def __init__(self):
        super().__init__()
        self.memory = self.load_memory()

    def load_memory(self):
        try:
            with open('agent_memory.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'preferences': {}, 'patterns': {}}

    def save_memory(self):
        with open('agent_memory.json', 'w') as f:
            json.dump(self.memory, f)

    def learn_preference(self, sender, category):
        """Remember user's categorization preferences"""
        if sender not in self.memory['preferences']:
            self.memory['preferences'][sender] = category
            self.save_memory()
```

### 3. Add Multi-Agent Workflows

Chain multiple specialized agents:

```python
# Email Reader Agent
reader = EmailAgent()
emails = reader.process_inbox()

# Calendar Agent (extracts meetings)
calendar = CalendarAgent()
meetings = calendar.extract_meetings(emails)
calendar.add_to_google_calendar(meetings)

# Task Agent (extracts todos)
task = TaskAgent()
todos = task.extract_tasks(emails)
task.add_to_todoist(todos)
```

### 4. Add Better Error Handling

Production-ready error handling:

```python
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RobustAgent(EmailAgent):
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def analyze_email_with_retry(self, email):
        """Retry failed analyses with exponential backoff"""
        try:
            return self.analyze_email(email)
        except Exception as e:
            logger.error(f"Failed to analyze email {email['id']}: {e}")
            raise

    def safe_process(self, emails):
        """Process emails with comprehensive error handling"""
        results = {'success': [], 'failed': []}

        for email in emails:
            try:
                analysis = self.analyze_email_with_retry(email)
                results['success'].append(email['id'])
            except Exception as e:
                logger.error(f"Permanently failed: {email['id']}")
                results['failed'].append({
                    'id': email['id'],
                    'error': str(e)
                })

        return results
```

## Advanced Features

### 5. Context-Aware Responses

Use conversation history:

```python
def get_thread_context(self, email):
    """Get full email thread for context"""
    thread_id = email['thread_id']

    # Get all messages in thread
    thread = self.gmail.service.users().threads().get(
        userId='me',
        id=thread_id
    ).execute()

    messages = thread.get('messages', [])

    # Build context
    context = []
    for msg in messages[:-1]:  # All except current
        headers = msg['payload']['headers']
        context.append({
            'from': self._get_header(headers, 'From'),
            'subject': self._get_header(headers, 'Subject'),
            'body': self._get_body(msg['payload'])
        })

    return context

def draft_contextual_reply(self, email):
    """Draft reply considering full conversation"""
    context = self.get_thread_context(email)

    prompt = f"""
    Previous conversation:
    {context}

    Latest email:
    {email['body']}

    Draft a reply that acknowledges the conversation history.
    """

    return self.client.messages.create(...)
```

### 6. Smart Filters with Learning

Filter that improves over time:

```python
def train_filter(self, email, user_action):
    """Learn from user corrections"""
    # Store user's actual decision
    self.memory['training_data'].append({
        'email': {
            'from': email['from'],
            'subject': email['subject'],
            'snippet': email['snippet']
        },
        'user_action': user_action  # 'archive', 'keep', 'important'
    })

    # After 100+ examples, use for few-shot prompting
    if len(self.memory['training_data']) > 100:
        examples = self.memory['training_data'][-10:]  # Recent 10
        prompt = f"""
        Learn from these examples:
        {examples}

        Now categorize this new email:
        {email}
        """
```

### 7. Integration with Other Services

**Slack notifications**:
```python
from slack_sdk import WebClient

def notify_slack(self, important_emails):
    slack = WebClient(token=os.getenv('SLACK_TOKEN'))

    for email in important_emails:
        slack.chat_postMessage(
            channel='#inbox-alerts',
            text=f"Important email from {email['from']}: {email['subject']}"
        )
```

**Notion database**:
```python
from notion_client import Client

def save_to_notion(self, emails, database_id):
    notion = Client(auth=os.getenv('NOTION_TOKEN'))

    for email in emails:
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Subject": {"title": [{"text": {"content": email['subject']}}]},
                "From": {"rich_text": [{"text": {"content": email['from']}}]},
                "Category": {"select": {"name": email['category']}}
            }
        )
```

## AI Agent Patterns

### Pattern: Tool Use

Let Claude decide which tools to use:

```python
def analyze_with_tools(self, email):
    tools = [
        {
            "name": "apply_label",
            "description": "Apply a label to categorize the email",
            "input_schema": {
                "type": "object",
                "properties": {
                    "label": {"type": "string"}
                }
            }
        },
        {
            "name": "draft_reply",
            "description": "Create a draft reply",
            "input_schema": {
                "type": "object",
                "properties": {
                    "tone": {"type": "string"}
                }
            }
        }
    ]

    response = self.client.messages.create(
        model=self.model,
        max_tokens=4096,
        tools=tools,
        messages=[{
            "role": "user",
            "content": f"Process this email: {email}"
        }]
    )

    # Claude will decide which tools to use
    for tool_use in response.content:
        if tool_use.type == "tool_use":
            if tool_use.name == "apply_label":
                self.gmail.add_label(email['id'], tool_use.input['label'])
            elif tool_use.name == "draft_reply":
                self.draft_reply(email, tone=tool_use.input['tone'])
```

### Pattern: Multi-Step Reasoning

Break complex tasks into steps:

```python
def complex_analysis(self, email):
    # Step 1: Basic classification
    basic = self.analyze_email(email)

    # Step 2: Deep analysis if needed
    if basic['priority'] == 'high':
        deep = self.deep_analyze(email)
        basic.update(deep)

    # Step 3: Cross-reference with calendar
    if self.mentions_meeting(email):
        calendar_info = self.check_calendar(email)
        basic['calendar_conflict'] = calendar_info

    return basic
```

### Pattern: Reflection

Agent reviews its own decisions:

```python
def reflect_on_decision(self, email, initial_decision):
    reflection_prompt = f"""
    You initially decided to: {initial_decision}

    For this email: {email['subject']}

    Review your decision:
    1. Does it make sense?
    2. Any overlooked factors?
    3. Should you change it?

    Respond with: {{ "keep": true/false, "new_decision": "...", "reasoning": "..." }}
    """

    reflection = self.client.messages.create(...)

    if not reflection['keep']:
        return reflection['new_decision']
    return initial_decision
```

## Performance Optimization

### Caching

Cache AI responses for similar emails:

```python
import hashlib
import pickle

class CachedAgent(EmailAgent):
    def __init__(self):
        super().__init__()
        self.cache = {}

    def get_cache_key(self, email):
        # Hash email content
        content = f"{email['from']}:{email['subject']}"
        return hashlib.md5(content.encode()).hexdigest()

    def analyze_email(self, email):
        cache_key = self.get_cache_key(email)

        if cache_key in self.cache:
            return self.cache[cache_key]

        # Cache miss - do actual analysis
        analysis = super().analyze_email(email)
        self.cache[cache_key] = analysis

        return analysis
```

### Batch Processing

Process multiple emails in one API call:

```python
def batch_analyze(self, emails):
    # Create one prompt with multiple emails
    batch_prompt = f"""
    Analyze these {len(emails)} emails and return an array of analyses:

    {json.dumps([{
        'id': e['id'],
        'from': e['from'],
        'subject': e['subject'],
        'snippet': e['snippet']
    } for e in emails])}

    Return: [{{id, category, priority, summary}}, ...]
    """

    response = self.client.messages.create(...)
    return json.loads(response.content[0].text)
```

## Testing Your Agent

```python
import unittest

class TestEmailAgent(unittest.TestCase):
    def setUp(self):
        self.agent = EmailAgent()

    def test_analysis(self):
        mock_email = {
            'subject': 'Urgent: Server Down',
            'from': 'alerts@system.com',
            'body': 'Production server is down!',
            'snippet': 'Production server is down!'
        }

        analysis = self.agent.analyze_email(mock_email)

        self.assertEqual(analysis['priority'], 'high')
        self.assertEqual(analysis['sentiment'], 'urgent')

    def test_label_application(self):
        # Test with a real email
        emails = self.agent.gmail.get_recent_emails(1)
        if emails:
            result = self.agent.gmail.add_label(emails[0]['id'], 'Test')
            self.assertTrue(result)
```

## Resources

### Learn More About AI Agents
- [Anthropic's Claude Documentation](https://docs.anthropic.com/)
- [LangChain](https://python.langchain.com/) - Agent framework
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) - Advanced agent example

### Improve Your Prompts
- [Anthropic's Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Learn Prompting](https://learnprompting.org/)

### Gmail API Deep Dive
- [Gmail API Reference](https://developers.google.com/gmail/api/reference/rest)
- [Python Client Library](https://github.com/googleapis/google-api-python-client)

## Share Your Creation

Built something cool? Share it!

- Tag @AnthropicAI on Twitter
- Share in the Anthropic Discord
- Open source it on GitHub
- Write a blog post about what you learned

## Final Thoughts

You've learned:
- ✅ How AI agents work
- ✅ How to integrate multiple APIs
- ✅ Prompt engineering basics
- ✅ Real-world automation

The skills you've gained apply to ANY agent project:
- Calendar management agents
- Research agents
- Customer support agents
- Data analysis agents
- And much more!

Keep building. Keep experimenting. The future is autonomous! 🚀
