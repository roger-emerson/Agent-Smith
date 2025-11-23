"""
LEVEL 3: Smart Reply Agent

This agent generates draft replies to your emails.

NEW FEATURES:
- Analyzes email content
- Drafts appropriate replies
- Saves drafts to Gmail (doesn't send!)

💡 Perfect for:
   - Quick responses to common emails
   - Professional reply templates
   - Getting past writer's block
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent import EmailAgent


def main():
    print("=" * 60)
    print("✍️  SMART REPLY AGENT - LEVEL 3")
    print("=" * 60)
    print("\nThis agent drafts replies to your emails.\n")

    try:
        # Create agent
        print("📡 Connecting...")
        agent = EmailAgent()
        print("✅ Connected!\n")

        # Get unread emails
        emails = agent.gmail.get_unread_emails(max_results=5)

        if not emails:
            print("✅ No unread emails!\n")
            return

        print(f"📬 Found {len(emails)} unread email(s)\n")
        print("Which emails should I draft replies for?\n")

        # Show emails and let user choose
        for i, email in enumerate(emails, 1):
            print(f"{i}. {email['subject']}")
            print(f"   From: {email['from']}")
            print(f"   Preview: {email['snippet'][:60]}...")
            print()

        # Get user choice
        choice = input("Enter number (or 'all' for all, 'q' to quit): ").strip()

        if choice.lower() == 'q':
            print("\n👋 Goodbye!")
            return

        # Determine which emails to process
        if choice.lower() == 'all':
            selected_emails = emails
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(emails):
                    selected_emails = [emails[idx]]
                else:
                    print("\n❌ Invalid choice!")
                    return
            except ValueError:
                print("\n❌ Invalid input!")
                return

        # Process selected emails
        for email in selected_emails:
            print("\n" + "=" * 60)
            print(f"📧 {email['subject']}")
            print("=" * 60)

            # First, analyze to understand the email
            print("\n🤔 Analyzing email...")
            analysis = agent.analyze_email(email)

            if "error" in analysis:
                print(f"❌ Analysis failed: {analysis['error']}")
                continue

            print(f"Category: {analysis.get('category')}")
            print(f"Action needed: {'Yes' if analysis.get('action_needed') else 'No'}")

            if not analysis.get('action_needed'):
                print("\n💡 This email doesn't seem to need a reply.")
                proceed = input("Draft a reply anyway? (y/n): ").lower()
                if proceed != 'y':
                    continue

            # Get any additional context from user
            print("\n📝 Drafting reply...")
            context = input("Any specific points to include? (press Enter to skip): ").strip()

            # Draft the reply
            reply = agent.draft_reply(email, context)

            if reply:
                print("\n" + "-" * 60)
                print("DRAFT REPLY:")
                print("-" * 60)
                print(reply)
                print("-" * 60)

                # Ask what to do with it
                print("\nWhat would you like to do?")
                print("1. Save as draft in Gmail")
                print("2. Copy to clipboard (manual)")
                print("3. Discard")

                action = input("\nChoice (1/2/3): ").strip()

                if action == '1':
                    # Extract sender email
                    sender = email['from']
                    # Simple email extraction (you might want to improve this)
                    if '<' in sender:
                        sender_email = sender.split('<')[1].split('>')[0]
                    else:
                        sender_email = sender

                    # Create draft
                    subject = f"Re: {email['subject']}"
                    if agent.gmail.create_draft(sender_email, subject, reply):
                        print("\n✅ Draft saved to Gmail!")
                        print("   Check your Drafts folder.")
                    else:
                        print("\n❌ Failed to save draft")

                elif action == '2':
                    print("\n📋 Copy the text above and paste where needed.")

                else:
                    print("\n🗑️  Discarded")

        print("\n" + "=" * 60)
        print("✅ COMPLETE")
        print("=" * 60)
        print("\n💡 TIPS:")
        print("   - Always review drafts before sending!")
        print("   - Edit drafts in Gmail to add personal touches")
        print("   - Use the context parameter for specific instructions\n")

    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")


if __name__ == '__main__':
    main()
