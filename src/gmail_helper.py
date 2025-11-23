"""
Gmail Helper - A simplified wrapper around Gmail API

This module makes it easy to interact with Gmail without dealing with
the complexity of the Google API directly.
"""

import os
import base64
from email.mime.text import MIMEText
from typing import List, Dict, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GmailHelper:
    """
    A friendly wrapper for Gmail API operations.

    Usage:
        gmail = GmailHelper()
        emails = gmail.get_unread_emails(max_results=10)
        for email in emails:
            print(email['subject'])
    """

    # Scopes define what your app can do
    # Start with readonly, add more as needed
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.labels',
        'https://www.googleapis.com/auth/gmail.modify'
    ]

    def __init__(self, credentials_file='credentials.json', token_file='token.json'):
        """
        Initialize Gmail connection.

        Args:
            credentials_file: Path to OAuth credentials from Google Cloud
            token_file: Path where the access token will be stored
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = self._authenticate()

    def _authenticate(self):
        """
        Handles OAuth authentication with Gmail.

        First time: Opens browser for authorization
        After: Uses saved token
        """
        creds = None

        # Load existing token if it exists
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)

        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Refresh expired token
                creds.refresh(Request())
            else:
                # First time: Open browser for authorization
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials for next time
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())

        # Build and return the Gmail service
        return build('gmail', 'v1', credentials=creds)

    def get_recent_emails(self, max_results=10, query='') -> List[Dict]:
        """
        Get recent emails from inbox.

        Args:
            max_results: Maximum number of emails to fetch
            query: Gmail search query (e.g., 'is:unread', 'from:boss@company.com')

        Returns:
            List of email dictionaries with 'id', 'subject', 'from', 'body', etc.
        """
        try:
            # Search for messages
            results = self.service.users().messages().list(
                userId='me',
                maxResults=max_results,
                q=query
            ).execute()

            messages = results.get('messages', [])

            # Get full details for each message
            emails = []
            for message in messages:
                email = self.get_email(message['id'])
                if email:
                    emails.append(email)

            return emails

        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []

    def get_unread_emails(self, max_results=10) -> List[Dict]:
        """Get unread emails."""
        return self.get_recent_emails(max_results=max_results, query='is:unread')

    def get_email(self, email_id: str) -> Optional[Dict]:
        """
        Get full details of a specific email.

        Args:
            email_id: Gmail message ID

        Returns:
            Dictionary with email details
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=email_id,
                format='full'
            ).execute()

            # Extract headers
            headers = message['payload']['headers']
            subject = self._get_header(headers, 'Subject')
            from_email = self._get_header(headers, 'From')
            date = self._get_header(headers, 'Date')
            to = self._get_header(headers, 'To')

            # Extract body
            body = self._get_body(message['payload'])

            # Get labels
            labels = message.get('labelIds', [])

            return {
                'id': email_id,
                'thread_id': message['threadId'],
                'subject': subject,
                'from': from_email,
                'to': to,
                'date': date,
                'body': body,
                'labels': labels,
                'snippet': message.get('snippet', '')
            }

        except Exception as e:
            print(f"Error fetching email {email_id}: {e}")
            return None

    def _get_header(self, headers: List[Dict], name: str) -> str:
        """Extract a specific header value."""
        for header in headers:
            if header['name'].lower() == name.lower():
                return header['value']
        return ''

    def _get_body(self, payload: Dict) -> str:
        """
        Extract email body from payload.
        Handles plain text and HTML.
        """
        body = ''

        if 'parts' in payload:
            # Multipart message
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(
                            part['body']['data']).decode('utf-8')
                        break
        else:
            # Simple message
            if 'data' in payload['body']:
                body = base64.urlsafe_b64decode(
                    payload['body']['data']).decode('utf-8')

        return body

    def add_label(self, email_id: str, label_name: str) -> bool:
        """
        Add a label to an email.
        Creates the label if it doesn't exist.

        Args:
            email_id: Gmail message ID
            label_name: Name of the label

        Returns:
            True if successful
        """
        try:
            # Get or create label
            label_id = self._get_or_create_label(label_name)

            # Add label to message
            self.service.users().messages().modify(
                userId='me',
                id=email_id,
                body={'addLabelIds': [label_id]}
            ).execute()

            return True

        except Exception as e:
            print(f"Error adding label: {e}")
            return False

    def remove_label(self, email_id: str, label_name: str) -> bool:
        """Remove a label from an email."""
        try:
            label_id = self._get_label_id(label_name)
            if not label_id:
                return False

            self.service.users().messages().modify(
                userId='me',
                id=email_id,
                body={'removeLabelIds': [label_id]}
            ).execute()

            return True

        except Exception as e:
            print(f"Error removing label: {e}")
            return False

    def _get_label_id(self, label_name: str) -> Optional[str]:
        """Get label ID by name."""
        try:
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])

            for label in labels:
                if label['name'] == label_name:
                    return label['id']

            return None

        except Exception as e:
            print(f"Error getting label: {e}")
            return None

    def _get_or_create_label(self, label_name: str) -> str:
        """Get existing label ID or create new label."""
        # Try to get existing label
        label_id = self._get_label_id(label_name)
        if label_id:
            return label_id

        # Create new label
        try:
            label = self.service.users().labels().create(
                userId='me',
                body={
                    'name': label_name,
                    'labelListVisibility': 'labelShow',
                    'messageListVisibility': 'show'
                }
            ).execute()

            return label['id']

        except Exception as e:
            print(f"Error creating label: {e}")
            return None

    def mark_as_read(self, email_id: str) -> bool:
        """Mark an email as read."""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=email_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return True
        except Exception as e:
            print(f"Error marking as read: {e}")
            return False

    def mark_as_unread(self, email_id: str) -> bool:
        """Mark an email as unread."""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=email_id,
                body={'addLabelIds': ['UNREAD']}
            ).execute()
            return True
        except Exception as e:
            print(f"Error marking as unread: {e}")
            return False

    def archive_email(self, email_id: str) -> bool:
        """Archive an email (remove from inbox)."""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=email_id,
                body={'removeLabelIds': ['INBOX']}
            ).execute()
            return True
        except Exception as e:
            print(f"Error archiving email: {e}")
            return False

    def star_email(self, email_id: str) -> bool:
        """Star an email."""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=email_id,
                body={'addLabelIds': ['STARRED']}
            ).execute()
            return True
        except Exception as e:
            print(f"Error starring email: {e}")
            return False

    def create_draft(self, to: str, subject: str, body: str) -> bool:
        """
        Create a draft email.

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (plain text)

        Returns:
            True if successful
        """
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject

            raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

            self.service.users().drafts().create(
                userId='me',
                body={'message': {'raw': raw}}
            ).execute()

            return True

        except Exception as e:
            print(f"Error creating draft: {e}")
            return False


# Quick test when run directly
if __name__ == '__main__':
    print("Testing Gmail connection...")
    gmail = GmailHelper()

    print("\nFetching 5 most recent emails...")
    emails = gmail.get_recent_emails(max_results=5)

    print(f"\n✅ Found {len(emails)} emails\n")

    for i, email in enumerate(emails, 1):
        print(f"{i}. {email['subject']}")
        print(f"   From: {email['from']}")
        print(f"   Preview: {email['snippet'][:60]}...")
        print()
