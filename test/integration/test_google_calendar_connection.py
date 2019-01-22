import os
from datetime import datetime, timedelta

from src.google_calendar_connection import GoogleCalendarConnection


class TestGoogleCalendarConnection:

    def setup_method(self, method):
        self.calendar_id = os.environ.get('CALENDAR_ID')
        self.service_account_information = os.environ.get('SERVICE_ACCOUNT')
        self.connection = GoogleCalendarConnection(
            self.service_account_information,
            self.calendar_id,
            'America/Guayaquil'
        )
        self.start = datetime.now().replace(microsecond=0)
        self.end = (self.start + timedelta(minutes=30)).replace(microsecond=0)
        self.event = self.connection.create_event(self.start, self.end, 'Test',
                                                  'description line 1<br />description line 2')

    def teardown_method(self, method):
        self.connection.cancel(self.event.get('id'))

    def test__crete_event(self):
        assert self.event.get('summary') == 'Test'
        assert self.event.get('description') == 'description line 1<br />description line 2'

        assert self.event.get('start').get('dateTime') == self.start.isoformat() + '-05:00'
        assert self.event.get('start').get('timeZone') == 'America/Guayaquil'

        assert self.event.get('end').get('dateTime') == self.end.isoformat() + '-05:00'
        assert self.event.get('end').get('timeZone') == 'America/Guayaquil'

    def test__get_latest_events(self):
        events = self.connection.get_latest_events(self.start - timedelta(days=1))

        assert 'Test' in set([event.get('summary') for event in events.get('items')])
