"""
Prompts for the AI Agent

This module contains all the prompts used to guide Claude's behavior.
Think of prompts as "instructions" you give to the AI.
"""


def get_email_analysis_prompt(email: dict) -> str:
    """
    Prompt for analyzing an email and deciding what to do with it.

    This is the core "thinking" prompt for the agent.
    """
    return f"""You are an intelligent email management assistant. Analyze this email and provide structured recommendations.

EMAIL DETAILS:
Subject: {email['subject']}
From: {email['from']}
Date: {email['date']}
Preview: {email['snippet']}

Body:
{email['body'][:1000]}

TASK: Analyze this email and respond with a JSON object containing:

1. "category": Choose ONE category that best fits:
   - "Work" - Professional emails, projects, meetings
   - "Personal" - Friends, family, personal matters
   - "Finance" - Bills, banking, transactions
   - "Shopping" - Orders, deliveries, receipts
   - "Newsletter" - Subscriptions, updates, marketing
   - "Social" - Social media notifications
   - "Urgent" - Time-sensitive or important matters
   - "Other" - Doesn't fit above categories

2. "priority": Rate the priority:
   - "high" - Requires immediate attention
   - "medium" - Should be addressed soon
   - "low" - Can be handled later

3. "sentiment": Overall tone:
   - "positive" - Good news, friendly
   - "neutral" - Informational
   - "negative" - Problems, complaints
   - "urgent" - Requires immediate action

4. "action_needed": Boolean - Does this require a response or action from the user?

5. "suggested_labels": Array of 1-3 suggested labels for organization

6. "summary": A one-sentence summary of the email (max 100 characters)

7. "reasoning": Brief explanation of your categorization

Respond ONLY with valid JSON, no other text:
"""


def get_reply_draft_prompt(email: dict, context: str = "") -> str:
    """
    Prompt for drafting a reply to an email.
    """
    return f"""You are helping draft a professional email reply.

ORIGINAL EMAIL:
Subject: {email['subject']}
From: {email['from']}
Body:
{email['body'][:1500]}

{context}

TASK: Draft a polite, professional reply to this email.

Guidelines:
- Keep it concise (2-4 paragraphs max)
- Match the tone of the original email
- Address all questions or points raised
- Be friendly but professional
- End with an appropriate closing

Provide ONLY the email body text, no subject line or signatures:
"""


def get_summary_prompt(emails: list) -> str:
    """
    Prompt for summarizing multiple emails.
    """
    email_list = "\n\n".join([
        f"From: {e['from']}\nSubject: {e['subject']}\nPreview: {e['snippet']}"
        for e in emails[:10]  # Limit to 10 for token efficiency
    ])

    return f"""You are an email assistant providing a daily inbox summary.

EMAILS:
{email_list}

TASK: Provide a brief, organized summary of these emails.

Format your response as:

## 📧 Inbox Summary ({len(emails)} emails)

### 🔴 Urgent/Important
- [List any emails that need immediate attention]

### 💼 Work/Professional
- [Brief points about work emails]

### 📬 Other
- [Brief points about other categories]

### 💡 Recommended Actions
- [2-3 suggested next steps]

Keep it concise and actionable!
"""


def get_smart_filter_prompt(email: dict, user_rules: dict = None) -> str:
    """
    Prompt for deciding whether to filter/auto-archive an email.
    """
    rules_text = ""
    if user_rules:
        rules_text = f"\n\nUSER PREFERENCES:\n{user_rules}\n"

    return f"""You are an email filtering assistant. Decide if this email should be auto-archived or needs attention.

EMAIL:
From: {email['from']}
Subject: {email['subject']}
Preview: {email['snippet']}
{rules_text}

TASK: Decide if this email can be safely archived or if the user should see it.

Common emails to AUTO-ARCHIVE:
- Marketing emails and promotions
- Automated notifications that don't need action
- Social media notifications
- Subscription newsletters (unless specifically requested)
- Automated receipts for regular purchases

Emails to KEEP IN INBOX:
- Personal correspondence
- Work-related emails
- Bills and important financial notifications
- Emails requiring action or response
- Confirmations for upcoming events/travel

Respond with JSON:
{{
    "action": "archive" or "keep",
    "confidence": "high", "medium", or "low",
    "reason": "Brief explanation"
}}
"""


def get_intent_extraction_prompt(email: dict) -> str:
    """
    Prompt for extracting actionable items from an email.
    """
    return f"""You are analyzing an email to extract actionable items.

EMAIL:
From: {email['from']}
Subject: {email['subject']}
Body:
{email['body'][:1000]}

TASK: Extract any actionable items, requests, or tasks from this email.

Respond with JSON:
{{
    "has_actions": true/false,
    "actions": [
        {{
            "action": "Brief description of the action",
            "due_date": "If mentioned, otherwise null",
            "priority": "high/medium/low"
        }}
    ],
    "questions_asked": ["List any questions the sender asked"],
    "requires_reply": true/false
}}
"""


# Template for custom prompts
def create_custom_prompt(system_message: str, email: dict, instructions: str) -> str:
    """
    Create a custom prompt for specific use cases.

    Args:
        system_message: Role/context for the AI
        email: Email dictionary
        instructions: Specific instructions for this task

    Returns:
        Formatted prompt string
    """
    return f"""{system_message}

EMAIL:
From: {email['from']}
Subject: {email['subject']}
Body:
{email['body'][:1500]}

{instructions}
"""
