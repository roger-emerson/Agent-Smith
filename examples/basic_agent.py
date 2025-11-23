"""
LEVEL 1: Basic Email Agent

This is your first agent! It will:
1. Connect to Gmail
2. Read your unread emails
3. Use AI to analyze each one
4. Show you what it learned

This is a SAFE script - it only reads, never modifies anything.
"""

import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent import EmailAgent


def main():
    """
    Run the basic email analysis agent.
    """
    print("=" * 60)
    print("🤖 BASIC EMAIL AGENT - LEVEL 1")
    print("=" * 60)
    print("\nThis agent will analyze your unread emails.")
    print("It's READ-ONLY - no changes will be made to your inbox.\n")

    try:
        # Create the agent
        print("📡 Connecting to Gmail and Claude...")
        agent = EmailAgent()
        print("✅ Connected!\n")

        # Get unread emails
        print("📬 Fetching unread emails...\n")
        emails = agent.gmail.get_unread_emails(max_results=5)

        if not emails:
            print("✅ No unread emails! Your inbox is clean.\n")
            return

        print(f"Found {len(emails)} unread email(s)\n")
        print("=" * 60)

        # Analyze each email
        for i, email in enumerate(emails, 1):
            print(f"\n📧 EMAIL {i}/{len(emails)}")
            print("-" * 60)
            print(f"Subject: {email['subject']}")
            print(f"From: {email['from']}")
            print(f"Date: {email['date']}")
            print(f"\nPreview: {email['snippet'][:100]}...")

            # Ask Claude to analyze
            print("\n🤔 Asking Claude to analyze...")
            analysis = agent.analyze_email(email)

            if "error" in analysis:
                print(f"❌ Analysis failed: {analysis['error']}")
                continue

            # Display the analysis
            print("\n📊 ANALYSIS:")
            print(f"  Category: {analysis.get('category', 'Unknown')}")
            print(f"  Priority: {analysis.get('priority', 'Unknown')}")
            print(f"  Sentiment: {analysis.get('sentiment', 'Unknown')}")
            print(f"  Action Needed: {'Yes' if analysis.get('action_needed') else 'No'}")
            print(f"  Summary: {analysis.get('summary', 'N/A')}")

            if analysis.get('suggested_labels'):
                print(f"  Suggested Labels: {', '.join(analysis['suggested_labels'])}")

            print(f"\n  Why? {analysis.get('reasoning', 'N/A')}")

            print("\n" + "=" * 60)

        # Final summary
        print("\n✅ Analysis complete!")
        print(f"\nProcessed {len(emails)} email(s)")
        print("\nREMEMBER: This was read-only. No changes were made to your inbox.")

        # Show next steps
        print("\n" + "=" * 60)
        print("🎓 NEXT STEPS:")
        print("=" * 60)
        print("\n1. Try examples/auto_label.py to automatically label emails")
        print("2. Try examples/smart_reply.py to generate draft replies")
        print("3. Customize the prompts in src/prompts.py")
        print("4. Build your own agent!\n")

    except FileNotFoundError as e:
        print("\n❌ ERROR: Missing credentials file")
        print("\nPlease follow these steps:")
        print("1. Read docs/GMAIL_SETUP.md")
        print("2. Download credentials.json from Google Cloud Console")
        print("3. Place it in the AgentSmith folder")
        print("4. Run this script again\n")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nCheck that:")
        print("1. You have credentials.json in the project folder")
        print("2. Your .env file has ANTHROPIC_API_KEY set")
        print("3. You've run: pip install -r requirements.txt\n")


if __name__ == '__main__':
    main()
