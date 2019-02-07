import {google} from 'googleapis';

const READONLY_CALENDAR_SCOPE = 'https://www.googleapis.com/auth/calendar.events.readonly';
const CALENDAR_VERSION = 'v3';
const MAX_RESULTS = 100;

export class GoogleCalendarConnection {

    constructor(calendar) {
        this.calendarId = calendar;
        this.credentials = null;
        this.calendar = null;
    }

    async start() {
        this.credentials = await google.auth.getClient({scopes: [READONLY_CALENDAR_SCOPE]});
        this.calendar = await google.calendar({version: CALENDAR_VERSION, auth: this.credentials});
    }

    async getEvents(start, end) {
        return await this.calendar.events.list({
            calendarId: this.calendarId,
            timeMin: start,
            timeMax: end,
            maxResults: MAX_RESULTS,
            singleEvents: true,
            orderBy: 'startTime'
        });
    }
}