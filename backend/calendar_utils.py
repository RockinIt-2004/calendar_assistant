from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import os

# Absolute path that always works
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials', 'service_account.json')

SCOPES = ['https://www.googleapis.com/auth/calendar']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

calendar_id = "4e07bdcad0d1b34452647cafb353b9ecd24d5602d0af39035c12816737236ec6@group.calendar.google.com"

def get_calendar_service():
    return build('calendar', 'v3', credentials=credentials)

def get_free_slots():
    service = get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events = service.events().list(calendarId=calendar_id, timeMin=now,
                                   maxResults=10, singleEvents=True,
                                   orderBy='startTime').execute()
    return events.get('items', [])

def create_event(summary, start_time, end_time):
    service = get_calendar_service()
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'},
    }
    return service.events().insert(calendarId=calendar_id, body=event).execute()
