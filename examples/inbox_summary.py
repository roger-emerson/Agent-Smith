"""
BONUS: Inbox Summary Agent

Get a smart summary of your inbox.

Perfect for:
- Morning inbox review
- Quick overview when you're busy
- Understanding email backlog
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent import EmailAgent


def main():
    print("=" * 60)
    print("📊 INBOX SUMMARY AGENT")
    print("=" * 60)
    print()

    try:
        # Create agent
        agent = EmailAgent()

        # Ask for preferences
        num_emails = input("How many emails to summarize? (default: 20): ").strip()
        num_emails = int(num_emails) if num_emails else 20

        print(f"\n📬 Fetching {num_emails} most recent emails...")
        emails = agent.gmail.get_recent_emails(max_results=num_emails)

        if not emails:
            print("✅ Inbox is empty!\n")
            return

        print(f"✅ Got {len(emails)} emails")
        print("\n🤔 Generating summary with Claude...")

        # Get summary
        summary = agent.summarize_inbox(emails)

        # Display
        print("\n" + "=" * 60)
        print(summary)
        print("=" * 60)

        # Offer to save
        save = input("\nSave this summary? (y/n): ").lower()
        if save == 'y':
            filename = f"inbox_summary_{len(emails)}_emails.md"
            with open(filename, 'w') as f:
                f.write(summary)
            print(f"\n✅ Saved to {filename}\n")
        else:
            print()

    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")


if __name__ == '__main__':
    main()
