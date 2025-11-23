"""
LEVEL 2: Auto-Labeling Agent

This agent automatically categorizes and labels your emails.

NEW FEATURES:
- Creates labels in Gmail
- Applies labels based on AI analysis
- Marks low-priority emails as read

⚠️ This MODIFIES your inbox (adds labels, marks as read)
   You'll be asked to confirm before any changes.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent import EmailAgent


def main():
    print("=" * 60)
    print("🏷️  AUTO-LABELING AGENT - LEVEL 2")
    print("=" * 60)
    print("\nThis agent will analyze your emails and apply labels.\n")

    # Safety confirmation
    print("⚠️  WARNING: This will make changes to your Gmail:")
    print("   - Create/apply labels")
    print("   - Mark low-priority emails as read")
    print()
    confirm = input("Continue? (yes/no): ").lower()

    if confirm != 'yes':
        print("\n❌ Cancelled. No changes made.")
        return

    try:
        # Create agent
        print("\n📡 Connecting...")
        agent = EmailAgent()
        print("✅ Connected!\n")

        # Get unread emails
        emails = agent.gmail.get_unread_emails(max_results=10)

        if not emails:
            print("✅ No unread emails!\n")
            return

        print(f"📬 Found {len(emails)} unread email(s)\n")

        # Process each email
        results = []
        for i, email in enumerate(emails, 1):
            print(f"\n[{i}/{len(emails)}] {email['subject'][:50]}...")

            # Analyze
            analysis = agent.analyze_email(email)

            if "error" in analysis:
                print(f"  ⚠️  Analysis failed: {analysis['error']}")
                continue

            print(f"  Category: {analysis.get('category')}")
            print(f"  Priority: {analysis.get('priority')}")

            # Show what we'll do
            actions = []

            # Add category label
            category = analysis.get('category')
            if category:
                actions.append(f"Add label: {category}")

            # Add priority label if high
            if analysis.get('priority') == 'high':
                actions.append("Add label: Urgent")

            # Mark as read if low priority
            if analysis.get('priority') == 'low':
                actions.append("Mark as read")

            if actions:
                print(f"  Actions: {', '.join(actions)}")

                # Ask for confirmation
                confirm_action = input("  Apply these actions? (y/n/all): ").lower()

                if confirm_action == 'all':
                    # Apply to this and all remaining without asking
                    auto_apply = True
                elif confirm_action != 'y':
                    print("  ⏭️  Skipped")
                    continue
                else:
                    auto_apply = False

                # Apply the actions
                for label in analysis.get('suggested_labels', []):
                    if agent.gmail.add_label(email['id'], label):
                        print(f"  ✓ Added label: {label}")

                if analysis.get('priority') == 'low':
                    if agent.gmail.mark_as_read(email['id']):
                        print(f"  ✓ Marked as read")

                results.append({
                    'email': email['subject'],
                    'actions': actions
                })

                # If user said "all", process remaining automatically
                if 'auto_apply' in locals() and auto_apply:
                    break

            else:
                print("  No actions needed")

        # Summary
        print("\n" + "=" * 60)
        print("✅ COMPLETE")
        print("=" * 60)
        print(f"\nProcessed: {len(results)} emails")

        if results:
            print("\nActions taken:")
            for r in results:
                print(f"  • {r['email'][:50]}")
                for action in r['actions']:
                    print(f"    - {action}")

        print("\n💡 TIP: Check your Gmail to see the labels!")
        print("    Labels appear in the left sidebar.\n")

    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")


if __name__ == '__main__':
    main()
