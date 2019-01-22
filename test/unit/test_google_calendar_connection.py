from datetime import datetime
from unittest.mock import patch, Mock

from src.google_calendar_connection import GoogleCalendarConnection


class TestGoogleCalendarConnection:

    @patch('src.google_calendar_connection.build')
    @patch('src.google_calendar_connection.json')
    @patch('src.google_calendar_connection.service_account')
    def test__init__gets_credentials_using_service_account_information(
            self,
            mock_service_account,
            mock_json,
            mock_build):
        service_account_information: str = 'Json information encoded as string'
        parsed_service_account_information: dict = {'key': 'value'}
        mock_json.loads.return_value = parsed_service_account_information
        mock_service_account.Credentials.from_service_account_info.return_value = 'Credentials object'

        credentials = GoogleCalendarConnection(service_account_information, Mock(), 'America/Guayaquil').credentials

        mock_json.loads.assert_called_with(service_account_information)
        mock_service_account.Credentials.from_service_account_info.assert_called_with(
            parsed_service_account_information)
        assert credentials == 'Credentials object'

    @patch('src.google_calendar_connection.build')
    @patch('src.google_calendar_connection.service_account')
    def test__init__creates_google_calendar_service(self, mock_service_account, mock_build):
        mock_service_account.Credentials.from_service_account_info.return_value = 'Credentials object'

        calendar_service = Mock()
        mock_build.return_value = calendar_service

        connection = GoogleCalendarConnection('{"foo": "bar"}', Mock(), 'America/Guayaquil')
        service = connection.calendar_service

        mock_build.assert_called_with('calendar', 'v3', credentials='Credentials object')
        assert service == calendar_service

    @patch('src.google_calendar_connection.build')
    @patch('src.google_calendar_connection.service_account')
    def test__get_latest_events__calls_list_method_of_events(self, service_account, build):
        service = Mock()
        build.return_value = service
        since = datetime(2018, 2, 1, 20, 30, 0)

        events_connection = Mock()
        list_request = Mock()
        list_request.execute.return_value = 'List of google events'
        events_connection.list.return_value = list_request
        service.events.return_value = events_connection

        connection = GoogleCalendarConnection('{"foo": "bar"}', 'calendar@domain', 'America/Guayaquil')
        events = connection.get_latest_events(since)

        connection.events.list.assert_called_with(
            calendarId='calendar@domain',
            timeMin='2018-02-02T01:30:00Z',
            maxResults=100,
            singleEvents=True,
            orderBy='startTime'
        )
        assert list_request.execute.called
        assert events == 'List of google events'

    @patch('src.google_calendar_connection.build')
    @patch('src.google_calendar_connection.service_account')
    def test__create_event__calls_insert_method_of_events(self, service_account, build):
        service = Mock()
        build.return_value = service

        events_connection = Mock()
        service.events.return_value = events_connection

        event = Mock()
        expected_event = Mock()
        events_connection.insert.return_value = event
        event.execute.return_value = expected_event

        start = datetime(2018, 2, 1, 20, 0, 0)
        end = datetime(2018, 2, 1, 21, 0, 0)

        connection = GoogleCalendarConnection('{"foo": "bar"}', 'calendar@domain', 'America/Guayaquil')
        created_event = connection.create_event(start, end, 'some subject', 'some description')

        event_body = {
            'summary': 'some subject',
            'start': {
                'dateTime': start.isoformat(),
                'timeZone': 'America/Guayaquil',
            },
            'end': {
                'dateTime': end.isoformat(),
                'timeZone': 'America/Guayaquil',
            },
            'description': 'some description'
        }
        events_connection.insert.assert_called_with(calendarId='calendar@domain', body=event_body)
        assert event.execute.called
        assert created_event == expected_event

    @patch('src.google_calendar_connection.build')
    @patch('src.google_calendar_connection.service_account')
    def test__cancel__calls_delete_and_execute(self, service_account, build):
        service = Mock()
        build.return_value = service

        events_connection = Mock()
        service.events.return_value = events_connection

        delete_request = Mock()
        events_connection.delete.return_value = delete_request

        connection = GoogleCalendarConnection('{"foo": "bar"}', 'calendar@domain', 'America/Guayaquil')

        connection.cancel('event_id')

        events_connection.delete.assert_called_with(calendarId='calendar@domain', eventId='event_id')
        assert delete_request.execute.called
