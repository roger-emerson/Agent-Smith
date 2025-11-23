#!/usr/bin/env python3
"""
Setup Checker - Verify your AgentSmith installation

Run this to check if everything is configured correctly.
"""

import os
import sys


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_python_version():
    """Check Python version."""
    print("🐍 Checking Python version...")
    version = sys.version_info

    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro}")
        print("   Need Python 3.8 or higher")
        return False


def check_dependencies():
    """Check if required packages are installed."""
    print("\n📦 Checking dependencies...")

    required = [
        'google.auth',
        'google_auth_oauthlib',
        'googleapiclient',
        'anthropic',
        'dotenv'
    ]

    all_good = True

    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - Not installed")
            all_good = False

    if not all_good:
        print("\n   Run: pip install -r requirements.txt")

    return all_good


def check_credentials():
    """Check for credentials files."""
    print("\n🔑 Checking credentials...")

    checks = {
        'credentials.json': 'Gmail API credentials',
        '.env': 'Environment variables file'
    }

    all_good = True

    for filename, description in checks.items():
        if os.path.exists(filename):
            print(f"   ✅ {filename} - {description}")
        else:
            print(f"   ❌ {filename} - {description} (missing)")
            all_good = False

    return all_good


def check_env_variables():
    """Check environment variables."""
    print("\n🔧 Checking environment variables...")

    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv('ANTHROPIC_API_KEY')

    if api_key:
        # Don't print the actual key, just confirm it exists
        masked = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print(f"   ✅ ANTHROPIC_API_KEY: {masked}")
        return True
    else:
        print(f"   ❌ ANTHROPIC_API_KEY not set in .env")
        return False


def check_gmail_connection():
    """Try to connect to Gmail."""
    print("\n📧 Testing Gmail connection...")

    try:
        sys.path.insert(0, 'src')
        from gmail_helper import GmailHelper

        gmail = GmailHelper()
        print("   ✅ Gmail connection successful!")

        # Try to fetch one email
        emails = gmail.get_recent_emails(max_results=1)
        print(f"   ✅ Can read emails (found {len(emails)})")

        return True

    except FileNotFoundError:
        print("   ❌ credentials.json not found")
        print("      See docs/GMAIL_SETUP.md for setup instructions")
        return False

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def check_anthropic_connection():
    """Try to connect to Anthropic API."""
    print("\n🤖 Testing Anthropic API connection...")

    try:
        from anthropic import Anthropic
        from dotenv import load_dotenv

        load_dotenv()

        client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

        # Simple test
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=50,
            messages=[{
                "role": "user",
                "content": "Reply with just 'OK'"
            }]
        )

        print("   ✅ Anthropic API connection successful!")
        return True

    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("      Check your ANTHROPIC_API_KEY in .env")
        return False


def show_next_steps(results):
    """Show next steps based on results."""
    print_header("RESULTS")

    all_passed = all(results.values())

    if all_passed:
        print("🎉 Everything is configured correctly!\n")
        print("Next steps:")
        print("  1. Run: python examples/basic_agent.py")
        print("  2. Read: docs/AGENT_CONCEPTS.md")
        print("  3. Explore: examples/\n")
    else:
        print("⚠️  Some checks failed. Fix these issues:\n")

        if not results['python']:
            print("  • Install Python 3.8 or higher")

        if not results['dependencies']:
            print("  • Run: pip install -r requirements.txt")

        if not results['credentials']:
            print("  • Download credentials.json from Google Cloud Console")
            print("    See: docs/GMAIL_SETUP.md")

        if not results['env']:
            print("  • Copy .env.example to .env")
            print("  • Add your ANTHROPIC_API_KEY to .env")

        if not results['gmail']:
            print("  • Complete Gmail API setup")
            print("    See: docs/GMAIL_SETUP.md")

        if not results['anthropic']:
            print("  • Check your Anthropic API key")
            print("    Get one at: https://console.anthropic.com/")

        print("\nRun this script again after fixing the issues.\n")


def main():
    """Run all checks."""
    print_header("AgentSmith Setup Checker")

    results = {
        'python': check_python_version(),
        'dependencies': check_dependencies(),
        'credentials': check_credentials(),
        'env': check_env_variables(),
    }

    # Only test connections if basics are in place
    if results['dependencies'] and results['credentials']:
        results['gmail'] = check_gmail_connection()
    else:
        results['gmail'] = False

    if results['dependencies'] and results['env']:
        results['anthropic'] = check_anthropic_connection()
    else:
        results['anthropic'] = False

    show_next_steps(results)


if __name__ == '__main__':
    main()
