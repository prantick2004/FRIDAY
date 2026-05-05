import os
import sys
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDS_FILE = os.path.expanduser("~") + "/FRIDAY/credentials.json"
TOKEN_FILE = os.path.expanduser("~") + "/FRIDAY/token_calendar.json"

def get_calendar_service():
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
    return build('calendar', 'v3', credentials=creds)

def get_todays_events():
    try:
        service = get_calendar_service()
        now = datetime.datetime.utcnow()
        start = now.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
        end = now.replace(hour=23, minute=59, second=59).isoformat() + 'Z'

        events_result = service.events().list(
            calendarId='primary',
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        if not events:
            return ["No events today"]

        result = []
        for e in events:
            start_time = e['start'].get('dateTime', e['start'].get('date'))
            summary = e.get('summary', 'No title')
            result.append(f"{summary} at {start_time}")

        return result

    except Exception as e:
        return [f"Calendar error: {e}"]

def add_event(title, date_str, time_str="10:00"):
    try:
        service = get_calendar_service()
        start_dt = f"{date_str}T{time_str}:00"
        end_dt = f"{date_str}T{time_str}:00"

        event = {
            'summary': title,
            'start': {
                'dateTime': start_dt,
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end_dt,
                'timeZone': 'Asia/Kolkata',
            },
        }

        service.events().insert(
            calendarId='primary',
            body=event
        ).execute()

        return f"Event {title} added to calendar"

    except Exception as e:
        return f"Add event error: {e}"

def get_upcoming_events(days=7):
    try:
        service = get_calendar_service()
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        end = (datetime.datetime.utcnow() +
               datetime.timedelta(days=days)).isoformat() + 'Z'

        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end,
            singleEvents=True,
            orderBy='startTime',
            maxResults=5
        ).execute()

        events = events_result.get('items', [])
        if not events:
            return ["No upcoming events"]

        result = []
        for e in events:
            start_time = e['start'].get('dateTime', e['start'].get('date'))
            summary = e.get('summary', 'No title')
            result.append(f"{summary} on {start_time}")

        return result

    except Exception as e:
        return [f"Calendar error: {e}"]