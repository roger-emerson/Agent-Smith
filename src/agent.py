"""
AI Agent - The core logic that brings everything together

This is where the "agent" behavior lives - the perception-thought-action loop.
"""

import json
import os
from typing import List, Dict, Optional
from anthropic import Anthropic
from dotenv import load_dotenv

from gmail_helper import GmailHelper
import prompts


class EmailAgent:
    """
    An AI agent that can analyze and manage your Gmail inbox.

    The agent follows this loop:
    1. PERCEIVE - Check Gmail for emails
    2. THINK - Use Claude to analyze emails
    3. ACT - Take actions based on analysis
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the agent.

        Args:
            api_key: Anthropic API key (or set ANTHROPIC_API_KEY in .env)
        """
        # Load environment variables
        load_dotenv()

        # Initialize AI client
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError(
                "No Anthropic API key found. Set ANTHROPIC_API_KEY in .env file "
                "or pass it to EmailAgent(api_key='...')"
            )

        self.client = Anthropic(api_key=self.api_key)

        # Initialize Gmail helper
        self.gmail = GmailHelper()

        # Agent configuration
        self.model = "claude-sonnet-4-5-20250929"  # Latest Claude model
        self.max_tokens = 4096

    def analyze_email(self, email: Dict) -> Dict:
        """
        Analyze a single email using Claude.

        This is the "THINK" step - we ask Claude to understand the email
        and make recommendations.

        Args:
            email: Email dictionary from GmailHelper

        Returns:
            Analysis results as a dictionary
        """
        try:
            # Get the prompt
            prompt = prompts.get_email_analysis_prompt(email)

            # Ask Claude to analyze
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Get the response text
            response_text = response.content[0].text

            # Strip markdown code blocks if present
            if response_text.strip().startswith('```'):
                # Remove ```json or ``` from start
                response_text = response_text.strip()
                if response_text.startswith('```json'):
                    response_text = response_text[7:]
                elif response_text.startswith('```'):
                    response_text = response_text[3:]
                # Remove ``` from end
                if response_text.endswith('```'):
                    response_text = response_text[:-3]
                response_text = response_text.strip()

            # Parse the JSON response
            analysis = json.loads(response_text)

            return analysis

        except json.JSONDecodeError as e:
            print(f"⚠️ Could not parse AI response as JSON: {e}")
            # Return raw response if JSON parsing fails
            return {"error": "JSON parsing failed", "raw": response.content[0].text}

        except Exception as e:
            print(f"❌ Error analyzing email: {e}")
            return {"error": str(e)}

    def draft_reply(self, email: Dict, context: str = "") -> str:
        """
        Draft a reply to an email using Claude.

        Args:
            email: Email to reply to
            context: Additional context or instructions

        Returns:
            Draft reply text
        """
        try:
            prompt = prompts.get_reply_draft_prompt(email, context)

            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            return response.content[0].text

        except Exception as e:
            print(f"❌ Error drafting reply: {e}")
            return ""

    def summarize_inbox(self, emails: List[Dict]) -> str:
        """
        Generate a summary of multiple emails.

        Args:
            emails: List of email dictionaries

        Returns:
            Summary text
        """
        try:
            prompt = prompts.get_summary_prompt(emails)

            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            return response.content[0].text

        except Exception as e:
            print(f"❌ Error generating summary: {e}")
            return ""

    def process_email(self, email: Dict, auto_apply: bool = False) -> Dict:
        """
        Full processing pipeline for a single email.

        This combines THINK and ACT:
        1. Analyze the email
        2. Optionally apply the recommended actions

        Args:
            email: Email to process
            auto_apply: If True, automatically apply recommendations

        Returns:
            Dictionary with analysis and actions taken
        """
        print(f"\n📧 Processing: {email['subject']}")
        print(f"   From: {email['from']}")

        # THINK: Analyze the email
        analysis = self.analyze_email(email)

        if "error" in analysis:
            print(f"   ⚠️ Analysis failed: {analysis['error']}")
            return {"email": email, "analysis": analysis, "actions": []}

        # Display analysis
        print(f"   Category: {analysis.get('category', 'Unknown')}")
        print(f"   Priority: {analysis.get('priority', 'Unknown')}")
        print(f"   Summary: {analysis.get('summary', 'N/A')}")

        actions_taken = []

        # ACT: Apply recommendations (if enabled)
        if auto_apply:
            # Apply suggested labels
            for label in analysis.get('suggested_labels', []):
                if self.gmail.add_label(email['id'], label):
                    actions_taken.append(f"Added label: {label}")
                    print(f"   ✓ Added label: {label}")

            # Mark as read if low priority
            if analysis.get('priority') == 'low':
                if self.gmail.mark_as_read(email['id']):
                    actions_taken.append("Marked as read")
                    print(f"   ✓ Marked as read")

        return {
            "email": email,
            "analysis": analysis,
            "actions": actions_taken
        }

    def process_inbox(self, max_emails: int = 10, auto_apply: bool = False) -> List[Dict]:
        """
        Process multiple emails from the inbox.

        Args:
            max_emails: Maximum number of emails to process
            auto_apply: If True, automatically apply recommendations

        Returns:
            List of processing results
        """
        print(f"\n🤖 Agent starting - processing up to {max_emails} emails...")

        # PERCEIVE: Get emails from Gmail
        emails = self.gmail.get_unread_emails(max_results=max_emails)

        if not emails:
            print("✅ No unread emails found!")
            return []

        print(f"📬 Found {len(emails)} unread emails\n")

        # Process each email
        results = []
        for email in emails:
            result = self.process_email(email, auto_apply=auto_apply)
            results.append(result)

        print(f"\n✅ Processed {len(results)} emails")
        return results

    def run_custom_analysis(self, email: Dict, custom_prompt: str) -> str:
        """
        Run a custom analysis using your own prompt.

        This is useful for experimenting with different instructions.

        Args:
            email: Email to analyze
            custom_prompt: Your custom instructions

        Returns:
            AI response
        """
        try:
            full_prompt = f"""Email Subject: {email['subject']}
From: {email['from']}
Body:
{email['body'][:1500]}

{custom_prompt}
"""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{
                    "role": "user",
                    "content": full_prompt
                }]
            )

            return response.content[0].text

        except Exception as e:
            print(f"❌ Error in custom analysis: {e}")
            return ""


# Example usage and testing
if __name__ == '__main__':
    print("🤖 Email Agent Test\n")

    # Create agent
    agent = EmailAgent()

    # Get one email
    emails = agent.gmail.get_recent_emails(max_results=1)

    if emails:
        email = emails[0]
        print(f"Testing with email: {email['subject']}\n")

        # Test analysis
        print("=" * 50)
        print("ANALYSIS TEST")
        print("=" * 50)
        analysis = agent.analyze_email(email)
        print(json.dumps(analysis, indent=2))

        # Test reply draft
        print("\n" + "=" * 50)
        print("REPLY DRAFT TEST")
        print("=" * 50)
        reply = agent.draft_reply(email)
        print(reply)

    else:
        print("No emails found to test with!")
