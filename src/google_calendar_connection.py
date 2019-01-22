import json
from datetime import datetime

import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build

MAX_RESULTS = 100

SERVICE_VERSION = 'v3'
CALENDAR_SERVICE = 'calendar'


class GoogleCalendarConnection(object):

    def __init__(self, service_account_information: str, calendar_id: str, time_zone: str):
        parsed_service_account = json.loads(service_account_information)

        self.credentials = service_account.Credentials.from_service_account_info(parsed_service_account)
        self.calendar_service = build(CALENDAR_SERVICE, SERVICE_VERSION, credentials=self.credentials)
        self.calendar_id = calendar_id
        self.local = pytz.timezone(time_zone)
        self.events = self.calendar_service.events()

    def __format_date(self, date):
        return self.local.localize(date).astimezone(pytz.utc).isoformat().replace('+00:00', 'Z')

    def get_latest_events(self, since: datetime):
        return self.events.list(
            calendarId=self.calendar_id,
            timeMin=self.__format_date(since),
            maxResults=MAX_RESULTS,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

    def create_event(self, start: datetime, end: datetime, subject: str, description=''):
        event = {
            'summary': subject,
            'start': {
                'dateTime': start.isoformat(),
                'timeZone': 'America/Guayaquil',
            },
            'end': {
                'dateTime': end.isoformat(),
                'timeZone': 'America/Guayaquil',
            },
            'description': description,
        }
        return self.events.insert(calendarId=self.calendar_id, body=event).execute()

    def cancel(self, event_id: str):
        self.events.delete(calendarId=self.calendar_id, eventId=event_id).execute()
