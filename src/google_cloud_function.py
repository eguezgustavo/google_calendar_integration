import json
import os

import dateutil.parser
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_VERSION = 'v3'
CALENDAR_SERVICE = 'calendar'


def authorize():
    service_account_information = os.environ.get('SERVICE_ACCOUNT')
    parsed_service_account = json.loads(service_account_information)

    return service_account.Credentials.from_service_account_info(parsed_service_account)


def create_calendar(credentials):
    return build(CALENDAR_SERVICE, SERVICE_VERSION, credentials=credentials)


def create_event(calendar, start, end, subject, description):
    event = {
        'summary': subject,
        'start': {
            'dateTime': start.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'description': description,
    }
    calendar_id = os.environ.get('CALENDAR_ID')
    return calendar.events().insert(calendarId=calendar_id, body=event).execute()


def cloud_function(request):
    credentials = authorize()
    calendar = create_calendar(credentials)

    args = request.get_json()

    start = dateutil.parser.parse(args.get('start'))
    end = dateutil.parser.parse(args.get('end'))
    subject = args.get('subject')
    description = args.get('description')

    event = create_event(calendar, start, end, subject, description)

    return json.dumps({
        'eventId': event.get('id')
    })
