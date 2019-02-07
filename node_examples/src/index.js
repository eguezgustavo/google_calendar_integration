import 'babel-polyfill';
import {GoogleCalendarConnection} from "./services/googleCalendarConnection";

//export GCLOUD_PROJECT=id of the project
//export GOOGLE_APPLICATION_CREDENTIALS=path to the service account json file

const main = async () => {
    const connection = new GoogleCalendarConnection('eguezgustavo@gmail.com');
    await connection.start();
    const events = await connection.getEvents('2019-02-01T00:00:00Z', '2019-02-06T19:00:00Z');
    console.log(events.data.items);
};

main().catch(console.error);
