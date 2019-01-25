import json
import os
from datetime import datetime
from unittest.mock import patch, Mock, ANY

import pytest
from dateutil.tz import tzutc

from src.google_cloud_function import cloud_function, authorize, create_calendar, create_event


class TestAuthorize:

    @patch('src.google_cloud_function.service_account')
    def test__authorize__calls_from_service_account_info__with_information_from_env_variables(self, service_account):
        config_information = {'someServiceAccountConfig': 'some parameter'}
        os.environ['SERVICE_ACCOUNT'] = json.dumps(config_information)
        service_account.Credentials.from_service_account_info.return_value = 'Some Credentials Object'

        credentials = authorize()

        service_account.Credentials.from_service_account_info.assert_called_with(config_information)
        assert credentials == 'Some Credentials Object'


class TestCreateCalendar:

    @patch('src.google_cloud_function.authorize')
    @patch('src.google_cloud_function.build')
    def test__create_calendar_calls_build__with_credentials_information(self, build, authorize):
        credentials = Mock()
        authorize.return_value = credentials

        build.return_value = 'Some Calendar Object'

        calendar = create_calendar(credentials)

        build.assert_called_with('calendar', 'v3', credentials=credentials)
        assert 'Some Calendar Object' == calendar


class TestCreateEvent:

    @pytest.fixture
    def calendar(self):
        insert_request = Mock()

        events_service = Mock()
        events_service.return_value = insert_request

        calendar = Mock()
        calendar.events.return_value = events_service

        return calendar

    @pytest.fixture
    def start(self):
        return datetime(2019, 1, 21, 20, 0, 0)

    @pytest.fixture
    def end(self):
        return datetime(2019, 1, 21, 20, 30, 0)

    def test__create_event__calls_insert_method_of_events_object_in_calendar(self, calendar, start, end):
        create_event(calendar, start, end, None, None)

        assert calendar.events().insert.called

    def test__create_event__calls_execute_method_of_insert_request(self, calendar, start, end):
        create_event(calendar, start, end, None, None)

        assert calendar.events().insert().execute.called

    def test__create_event__gets_calendar_id_from_environment(self, calendar, start, end):
        os.environ['CALENDAR_ID'] = 'some@service'

        create_event(calendar, start, end, None, None)

        calendar.events().insert.assert_called_with(calendarId='some@service', body=ANY)

    def test__create_event__formats_event_body(self, calendar):
        expected_event_body = {
            'summary': 'Some Subject',
            'start': {
                'dateTime': '2019-01-21T20:00:00',
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': '2019-01-21T20:30:00',
                'timeZone': 'UTC',
            },
            'description': 'Some description',
        }

        create_event(
            calendar,
            datetime(2019, 1, 21, 20, 0, 0),
            datetime(2019, 1, 21, 20, 30, 0),
            'Some Subject',
            'Some description'
        )

        calendar.events().insert.assert_called_with(calendarId=ANY, body=expected_event_body)


@patch('src.google_cloud_function.create_event')
@patch('src.google_cloud_function.create_calendar')
@patch('src.google_cloud_function.authorize')
class TestGoogleCloudFunction:

    @pytest.fixture
    def request(self):
        request = Mock()
        request.get_json.return_value = {
            'start': '2019-01-21T20:00:00',
            'end': '2019-01-21T20:30:00',
            'subject': 'some subject',
            'description': 'some description'
        }
        return request

    def test__cloud_function__calls_authorize(self, authorize, create_calendar, create_event, request):
        event = {'id': 'some event id'}
        create_event.return_value = event

        cloud_function(request)

        assert authorize.called

    def test__cloud_function__calls_create_calendar_with_credentials(self, authorize, create_calendar, create_event, request):
        event = {'id': 'some event id'}
        create_event.return_value = event

        credentials = 'Credentials Object'
        authorize.return_value = credentials

        cloud_function(request)

        create_calendar.assert_called_with(credentials)

    def test__cloud_function__calls_create_event__with_calendar_with_start_and_end_date_and_with_subject_and_description(
            self,
            authorize,
            create_calendar,
            create_event,
            request):
        event = {'id': 'some event id'}
        create_event.return_value = event

        calendar = Mock()
        create_calendar.return_value = calendar

        expected_start_date = datetime(2019, 1, 21, 20, 0, 0)
        expected_end_date = datetime(2019, 1, 21, 20, 30, 0)

        response = cloud_function(request)

        create_event.assert_called_with(
            calendar,
            expected_start_date,
            expected_end_date,
            'some subject',
            'some description'
        )
        assert response == json.dumps({'eventId': 'some event id'})
