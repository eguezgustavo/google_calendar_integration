# Google Calendar Integration for services
Most of the times you need to use the Google Calendar API you want to create a service that will handle events in a particular calendar.

## Setup
To Achieve this goal we need to follow these steps:
* Create a __service account__ which will give you an email address for your application
  
  First of all you need to create a project and a service account in the google developers console, follow [this](https://developers.google.com/android/management/service-account) link to read information on how to do it.
  
  Once done, you will have a JSON file with information related to the service account.
  
* Add the service account email address as editor of the calendar

  The service account has an id similar to an email address, you need to add it to the calendar you want to control. Follow [this](https://support.google.com/calendar/answer/37082?hl=en) link to lear how to do it.
* Authenticate your application using the service account information
* Use the credentials to call the google calendar API methods

## Code
The code in this repository read, deletes and creates events. To make it work you have to export 2 env variables:

```
export CALENDAR_ID=xxxxx@gmail.com
export SERVICE_ACCOUNT=[Information inside the JSON file downloaded for the service account]
```

And then run the test using:

`pytest`
