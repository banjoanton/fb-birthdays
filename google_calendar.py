from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main(birthdays={}):
    creds = None
    creds = get_credentials(creds)
    service = build('calendar', 'v3', credentials=creds)

    # TODO: Choose calendar name

    # returns ID if it exists, else it creates a calendar
    calendar_exists = see_if_calendar_exists(
        service)

    if calendar_exists is False:

        print("Creating calendar with name 'FB-Birthdays'...")
        # create calendar if it doesnt exists
        create_calendar(calendar_exists, service)

    # returns ID after the calendar is created
    calendar_id = see_if_calendar_exists(service)

    for key in birthdays:

        # get data
        name, birthday = birthdays[key]

        # print status
        print(f"Adding {name}...")

        # create event
        event = {
            'summary': f'{name} fyller år',  # change language
            'description': f'{name}',
            'start': {
                'dateTime': f'{birthday}',
                'timeZone': 'Europe/Stockholm',  # change time zone
            },
            'end': {
                'dateTime': f'{birthday}',
                'timeZone': 'Europe/Stockholm',  # change time zone
            },
            'recurrence': [
                'RRULE:FREQ=YEARLY'
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 24*60},
                    {'method': 'popup', 'minutes': 60*24*10}
                ],
            },
        }

        # Add to calendar
        event = service.events().insert(
            calendarId=calendar_id, body=event).execute()


def create_calendar(calendar_exists, service):
    # create calendar
    calendar = {
        'summary': 'FB-Birthdays'
    }

    # if the calendar doesnt exist, create it.
    if not calendar_exists:
        created_calendar = service.calendars().insert(body=calendar).execute()


def see_if_calendar_exists(service):
    """ returns False if no calendar with that name exists, else it returns the ID
    """
    page_token = None
    calendar_list = service.calendarList().list(pageToken=page_token).execute()

    for calendar_list_entry in calendar_list['items']:
        if "FB-Birthdays" in calendar_list_entry["summary"]:
            return calendar_list_entry["id"]

    return False


def get_credentials(creds):
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


if __name__ == '__main__':
    main()
