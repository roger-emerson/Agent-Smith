"""
LEVEL 4: Custom Workflow Agent

Build your own custom workflows!

This example shows how to combine multiple agent capabilities
into a custom workflow that matches YOUR needs.

Example workflow:
1. Find emails from specific senders
2. Analyze them
3. Apply custom rules
4. Generate weekly reports

💡 Use this as a template to build your own agent!
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent import EmailAgent


class CustomWorkflow:
    """
    Your custom agent workflow.

    Modify this class to create your own email automation!
    """

    def __init__(self):
        self.agent = EmailAgent()
        self.stats = {
            'processed': 0,
            'important': 0,
            'archived': 0,
            'replied': 0
        }

    def run(self):
        """
        Main workflow - customize this method!
        """
        print("=" * 60)
        print("🔧 CUSTOM WORKFLOW AGENT")
        print("=" * 60)
        print()

        # Example: Process newsletter emails
        self.process_newsletters()

        # Example: Handle important senders
        self.process_important_senders()

        # Show stats
        self.show_stats()

    def process_newsletters(self):
        """
        Custom rule: Auto-archive newsletters but save important ones.
        """
        print("📰 Processing newsletters...")

        # Search for common newsletter patterns
        query = 'from:newsletter OR from:noreply OR subject:unsubscribe'
        emails = self.agent.gmail.get_recent_emails(max_results=20, query=query)

        print(f"   Found {len(emails)} newsletter-like emails")

        for email in emails:
            # Use AI to determine if it's actually important
            analysis = self.agent.analyze_email(email)

            if analysis.get('priority') == 'high' or analysis.get('action_needed'):
                # Keep important newsletters
                self.agent.gmail.add_label(email['id'], 'Newsletter-Important')
                self.stats['important'] += 1
                print(f"   ⭐ Kept: {email['subject'][:50]}")
            else:
                # Archive routine newsletters
                self.agent.gmail.mark_as_read(email['id'])
                self.agent.gmail.add_label(email['id'], 'Newsletter')
                self.agent.gmail.archive_email(email['id'])
                self.stats['archived'] += 1

            self.stats['processed'] += 1

        print()

    def process_important_senders(self):
        """
        Custom rule: Priority handling for specific people.
        """
        print("👤 Processing VIP emails...")

        # Define your VIP senders
        vip_senders = [
            'boss@company.com',
            'client@important.com',
            # Add your important contacts here
        ]

        for sender in vip_senders:
            emails = self.agent.gmail.get_recent_emails(
                max_results=5,
                query=f'from:{sender} is:unread'
            )

            if not emails:
                continue

            print(f"   Found {len(emails)} from {sender}")

            for email in emails:
                # Auto-star emails from VIPs
                self.agent.gmail.star_email(email['id'])
                self.agent.gmail.add_label(email['id'], 'VIP')

                # Check if it needs a reply
                analysis = self.agent.analyze_email(email)

                if analysis.get('action_needed'):
                    print(f"   ✉️  Needs reply: {email['subject'][:40]}")

                    # Optionally auto-draft a reply
                    draft = self.agent.draft_reply(email)
                    if draft:
                        # You could auto-save this as a draft
                        # self.agent.gmail.create_draft(...)
                        self.stats['replied'] += 1

                self.stats['processed'] += 1

        print()

    def show_stats(self):
        """Display workflow statistics."""
        print("=" * 60)
        print("📊 WORKFLOW COMPLETE")
        print("=" * 60)
        print(f"\nProcessed: {self.stats['processed']} emails")
        print(f"Important: {self.stats['important']}")
        print(f"Archived: {self.stats['archived']}")
        print(f"Replied: {self.stats['replied']}")
        print()


def example_search_workflow():
    """
    Example: Find and process emails matching specific criteria.
    """
    print("\n🔍 SEARCH WORKFLOW EXAMPLE\n")

    agent = EmailAgent()

    # Example searches you can do:
    searches = {
        'Receipts': 'subject:receipt OR subject:invoice',
        'Social Media': 'from:facebook.com OR from:twitter.com OR from:linkedin.com',
        'This Week': 'newer_than:7d',
        'Unread Work': 'is:unread (to:work OR from:work)',
        'Large Emails': 'larger:5M',
    }

    print("Available search patterns:")
    for name, query in searches.items():
        print(f"\n{name}:")
        print(f"  Query: {query}")

        emails = agent.gmail.get_recent_emails(max_results=5, query=query)
        print(f"  Found: {len(emails)} emails")

        if emails:
            for email in emails[:3]:  # Show first 3
                print(f"    - {email['subject'][:50]}")


def example_batch_workflow():
    """
    Example: Process emails in batches with AI analysis.
    """
    print("\n📦 BATCH PROCESSING EXAMPLE\n")

    agent = EmailAgent()

    # Get all unread
    emails = agent.gmail.get_unread_emails(max_results=50)

    if not emails:
        print("No unread emails!")
        return

    # Categorize all emails first
    categorized = {
        'urgent': [],
        'work': [],
        'personal': [],
        'newsletters': [],
        'other': []
    }

    print(f"Analyzing {len(emails)} emails...\n")

    for email in emails:
        analysis = agent.analyze_email(email)

        # Categorize based on analysis
        if analysis.get('priority') == 'high' or analysis.get('sentiment') == 'urgent':
            categorized['urgent'].append(email)
        elif analysis.get('category') == 'Work':
            categorized['work'].append(email)
        elif analysis.get('category') == 'Personal':
            categorized['personal'].append(email)
        elif analysis.get('category') == 'Newsletter':
            categorized['newsletters'].append(email)
        else:
            categorized['other'].append(email)

    # Show results
    print("📊 Categorization Results:\n")
    for category, emails_list in categorized.items():
        if emails_list:
            print(f"{category.upper()}: {len(emails_list)} emails")
            for email in emails_list[:3]:
                print(f"  - {email['subject'][:50]}")
            if len(emails_list) > 3:
                print(f"  ... and {len(emails_list) - 3} more")
            print()


def main():
    """
    Main entry point - choose which workflow to run.
    """
    print("=" * 60)
    print("🔧 CUSTOM WORKFLOWS")
    print("=" * 60)
    print("\nChoose a workflow:\n")
    print("1. Full custom workflow (newsletters + VIPs)")
    print("2. Search examples")
    print("3. Batch processing example")
    print("4. Exit")

    choice = input("\nChoice (1-4): ").strip()

    if choice == '1':
        workflow = CustomWorkflow()
        workflow.run()

    elif choice == '2':
        example_search_workflow()

    elif choice == '3':
        example_batch_workflow()

    else:
        print("\n👋 Goodbye!")

    print("\n💡 TIP: Edit this file to create your own workflows!")
    print("   The code is heavily commented - customize it for your needs.\n")


if __name__ == '__main__':
    main()
