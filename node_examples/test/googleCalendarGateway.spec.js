import {expect} from 'chai';
import {GoogleCalendarGateway} from "../src/services/googleCalendarGateway";


describe('google calendar gateway', () => {

    it('transforms google event into a parsed event', () => {

        const google_event = {
            id: 'SomeId1234',
            summary: 'Some Title',
            description: 'Some Description',
            start: {
                dateTime: '2019-02-06T04:30:00-05:00'
            },
            end: {
                dateTime: '2019-02-06T05:00:00-05:00'
            },
        };

        const event = new GoogleCalendarGateway().parseEvent(google_event);

        expect(event).to.deep.equal({
            id: 'SomeId1234',
            title: 'Some Title',
            start: '2019-02-06T09:30:00Z',
            end: '2019-02-06T10:00:00Z',
            details: 'Some Description'
        });
    });
});