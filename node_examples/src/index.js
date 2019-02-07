import 'babel-polyfill';
import {GoogleCalendarConnection} from "./services/googleCalendarConnection";

//export GCLOUD_PROJECT=id of the project
//export GOOGLE_APPLICATION_CREDENTIALS=path to the service account json file

const main = async () => {
    const connection = new GoogleCalendarConnection('eguezgustavo@gmail.com');
    await connection.start();
    const events = await connection.getEvents('2019-02-01T00:00:00Z', '2019-02-06T19:00:00Z');
    // const auth = await google.auth.getClient({
    //     scopes: ['https://www.googleapis.com/auth/calendar.events.readonly']
    // });
    // const calendar = google.calendar({version: 'v3', auth});
    // const events = await calendar.events.list({
    //     calendarId: 'eguezgustavo@gmail.com',
    //     timeMin: (new Date()).toISOString(),
    //     maxResults: 10,
    //     singleEvents: true,
    //     orderBy: 'startTime'
    // });
    console.log(events.data.items);
};

main().catch(console.error);
