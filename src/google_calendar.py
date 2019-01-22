from __future__ import print_function

import datetime
import json

from google.oauth2 import service_account
from googleapiclient.discovery import build

from src.google_calendar_connection import GoogleCalendarConnection

SERVICE_ACCOUNT_INFORMATION_FILE_NAME = 'service_account.json'


def get_credentials_using_service_account():
    with open(SERVICE_ACCOUNT_INFORMATION_FILE_NAME) as source:
        info = json.load(source)
    return service_account.Credentials.from_service_account_info(info)


def get_credentials():
    return get_credentials_using_service_account()


def get_latest_10_events(calendar_service):
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = calendar_service.events().list(
        calendarId='eguezgustavo@gmail.com',
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])


def create_event(calendar_service):
    event = {
        'summary': 'Google I/O 2015',
        'location': '800 Howard St., San Francisco, CA 94103',
        'description': 'A chance to hear more about Google\'s developer products.',
        'start': {
            'dateTime': '2019-01-21T20:00:00-05:00',
            'timeZone': 'America/Guayaquil',
        },
        'end': {
            'dateTime': '2019-01-21T21:00:00-05:00',
            'timeZone': 'America/Guayaquil',
        }
    }

    event = calendar_service.events().insert(calendarId='eguezgustavo@gmail.com', body=event).execute()
    print('Event creted', event)


def main():
    credentials = get_credentials_using_service_account()
    service = build('calendar', 'v3', credentials=credentials)
    events = get_latest_10_events(service)

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    create_event(service)


if __name__ == '__main__':
    f = open(SERVICE_ACCOUNT_INFORMATION_FILE_NAME, 'r')
    info = f.read()
    f.close()

    connection = GoogleCalendarConnection(info, 'eguezgustavo@gmail.com', 'America/Guayaquil')
    events = connection.get_latest_events(datetime.datetime(2019, 1, 1))

    print(events)
