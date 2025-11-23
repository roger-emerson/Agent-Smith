"""
Auto-label first 30 emails based on AI analysis
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent import EmailAgent


def main():
    print("=" * 60)
    print("🏷️  AUTO-LABELING AGENT - 30 EMAILS")
    print("=" * 60)
    print("\nThis agent will analyze 30 emails and apply labels.\n")

    # Safety confirmation
    print("⚠️  This will make changes to your Gmail:")
    print("   - Create/apply labels based on AI analysis")
    print("   - Mark low-priority emails as read")
    print("\n✅ Auto-confirmed - proceeding with analysis...")

    try:
        # Create agent
        print("\n📡 Connecting...")
        agent = EmailAgent()
        print("✅ Connected!\n")

        # Get 30 unread emails
        print("📬 Fetching up to 30 unread emails...")
        emails = agent.gmail.get_unread_emails(max_results=30)

        if not emails:
            print("✅ No unread emails!\n")
            return

        print(f"Found {len(emails)} unread email(s)\n")
        print("=" * 60)

        # Process each email
        results = []
        for i, email in enumerate(emails, 1):
            print(f"\n[{i}/{len(emails)}] Processing...")
            print(f"Subject: {email['subject'][:60]}...")
            print(f"From: {email['from'][:50]}")

            # Analyze
            analysis = agent.analyze_email(email)

            if "error" in analysis:
                print(f"  ⚠️  Analysis failed: {analysis['error']}")
                continue

            print(f"  📊 Category: {analysis.get('category')}")
            print(f"  📊 Priority: {analysis.get('priority')}")
            print(f"  📊 Summary: {analysis.get('summary', 'N/A')[:70]}...")

            # Apply labels
            actions_taken = []

            # Add suggested labels
            for label in analysis.get('suggested_labels', []):
                if agent.gmail.add_label(email['id'], label):
                    print(f"  ✅ Added label: {label}")
                    actions_taken.append(f"Label: {label}")

            # Mark as read if low priority
            if analysis.get('priority') == 'low':
                if agent.gmail.mark_as_read(email['id']):
                    print(f"  ✅ Marked as read")
                    actions_taken.append("Marked as read")

            if actions_taken:
                results.append({
                    'email': email['subject'],
                    'from': email['from'],
                    'actions': actions_taken,
                    'category': analysis.get('category'),
                    'priority': analysis.get('priority')
                })
            else:
                print("  ℹ️  No actions needed")

            print("-" * 60)

        # Summary
        print("\n" + "=" * 60)
        print("✅ COMPLETE")
        print("=" * 60)
        print(f"\nProcessed: {len(emails)} emails")
        print(f"Modified: {len(results)} emails")

        if results:
            print("\n📊 SUMMARY BY CATEGORY:")
            categories = {}
            for r in results:
                cat = r.get('category', 'Unknown')
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(r)

            for category, items in categories.items():
                print(f"\n{category} ({len(items)} emails):")
                for item in items[:3]:  # Show first 3 of each category
                    print(f"  • {item['email'][:60]}")
                if len(items) > 3:
                    print(f"  ... and {len(items) - 3} more")

        print("\n💡 TIP: Check your Gmail to see the labels!")
        print("    Labels appear in the left sidebar.\n")

    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
