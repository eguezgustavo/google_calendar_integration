export class GoogleCalendarGateway {

    formatDate(dateAsString) {
        return new Date(dateAsString).toISOString().split('.')[0] + 'Z';
    }

    parseEvent(googleEvent) {
        return {
            id: googleEvent.id,
            title: googleEvent.summary,
            start: this.formatDate(googleEvent.start.dateTime),
            end: this.formatDate(googleEvent.end.dateTime),
            details: googleEvent.description
        }
    }
}