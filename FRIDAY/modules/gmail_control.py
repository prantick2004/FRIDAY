import os
import sys
import base64
import pickle
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
CREDS_FILE = os.path.expanduser("~") + "/FRIDAY/credentials.json"
TOKEN_FILE = os.path.expanduser("~") + "/FRIDAY/token_gmail.json"

def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def read_emails(max_results=3):
    try:
        service = get_gmail_service()
        results = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            maxResults=max_results,
            q='is:unread'
        ).execute()

        messages = results.get('messages', [])
        if not messages:
            return ["No unread emails found"]

        emails = []
        for msg in messages:
            txt = service.users().messages().get(
                userId='me',
                id=msg['id']
            ).execute()

            payload = txt['payload']
            headers = payload['headers']

            subject = "No subject"
            sender = "Unknown"

            for h in headers:
                if h['name'] == 'Subject':
                    subject = h['value']
                if h['name'] == 'From':
                    sender = h['value']

            emails.append(f"From {sender}. Subject: {subject}")

        return emails

    except Exception as e:
        return [f"Gmail error: {e}"]

def send_email(to, subject, body):
    try:
        service = get_gmail_service()
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(
            userId='me',
            body={'raw': raw}
        ).execute()
        return "Email sent successfully"
    except Exception as e:
        return f"Send error: {e}"

def search_emails(query, max_results=3):
    try:
        service = get_gmail_service()
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()

        messages = results.get('messages', [])
        if not messages:
            return [f"No emails found for {query}"]

        emails = []
        for msg in messages:
            txt = service.users().messages().get(
                userId='me',
                id=msg['id']
            ).execute()
            headers = txt['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            emails.append(f"From {sender}. Subject: {subject}")

        return emails

    except Exception as e:
        return [f"Search error: {e}"]