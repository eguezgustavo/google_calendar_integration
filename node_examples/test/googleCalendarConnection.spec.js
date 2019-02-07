import {expect} from 'chai';
import sinon from "sinon";
import {GoogleCalendarConnection} from "../src/services/googleCalendarConnection";
import {google} from 'googleapis';

describe('google calendar connection', () => {

    let getClientStub;
    let createCalendarStub;

    beforeEach(() => {
        getClientStub = sinon.stub(google.auth, 'getClient');
        createCalendarStub = sinon.stub(google, 'calendar');
    });

    afterEach(() => {
        getClientStub.restore();
        createCalendarStub.restore();
    });

    describe('getting credentials', () => {

        it('gets credentials using service account information', async () => {

            const getClientPromise = new Promise((resolve) => {
                resolve('Some Credentials');
            });
            getClientStub.returns(getClientPromise);

            const connection = new GoogleCalendarConnection('someone@server');
            await connection.start();

            sinon.assert.calledWith(getClientStub, {
                scopes: ['https://www.googleapis.com/auth/calendar.events.readonly']
            });
            expect(connection.credentials).to.equal('Some Credentials');

        });

        it('does not set credentials when getClient failed', async () => {

            const getClientPromise = new Promise((_, reject) => {
                reject('Some Error');
            });
            getClientStub.returns(getClientPromise);

            const connection = new GoogleCalendarConnection('someone@server');
            try {
                await connection.start();
            } catch (e) {
            }

            expect(connection.credentials).to.equal(null);
        });

    });
end:
    describe('creating calendar service', () => {
        const getClientPromise = new Promise((resolve) => {
            resolve('Some Credentials');
        });

        beforeEach(() => {
            getClientStub.returns(getClientPromise);
        });

        it('creates calendar service', async () => {
            createCalendarStub.returns(new Promise((resolve) => {
                resolve('Some Calendar Instance');
            }));

            const connection = new GoogleCalendarConnection('someone@server');
            await connection.start();

            sinon.assert.calledWith(createCalendarStub, {version: 'v3', auth: 'Some Credentials'});
            expect(connection.calendar).to.equal('Some Calendar Instance');
        });

        it('does not set calendar when calendar creation failed', async () => {

            createCalendarStub.returns(new Promise((_, reject) => {
                reject('Some Calendar Instance');
            }));


            const connection = new GoogleCalendarConnection('someone@server');
            try {
                await connection.start();
            } catch (e) {
            }

            expect(connection.calendar).to.equal(null);
        });
    });

    describe('get events', () => {

        it('calls list method to get events with desired attributes', async () => {
            const connection = new GoogleCalendarConnection('someone@server');

            connection.calendar = sinon.stub();
            connection.calendar.events = sinon.stub();
            connection.calendar.events.list = sinon.stub().returns(
                new Promise((resolve) => resolve('A List of Google Calendar Events'))
            );

            const events = await connection.getEvents('2019-02-06T22:00:00Z', '2019-02-07T22:00:00Z');

            sinon.assert.calledWith(connection.calendar.events.list, {
                calendarId: 'someone@server',
                timeMin: '2019-02-06T22:00:00Z',
                timeMax: '2019-02-07T22:00:00Z',
                maxResults: 100,
                singleEvents: true,
                orderBy: 'startTime'
            });
            expect(events).to.equal('A List of Google Calendar Events');
        });
    });
});