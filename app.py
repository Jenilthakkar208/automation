import streamlit as st
import datetime
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def create_calendar_event(title, start_datetime, duration_minutes=30):
    service = get_calendar_service()
    end_datetime = start_datetime + datetime.timedelta(minutes=duration_minutes)

    event = {
        'summary': title,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }

    service.events().insert(calendarId='primary', body=event).execute()


# -------- Streamlit UI --------

st.title("Google Calendar Event Creator")

title = st.text_input("Event Title")
date = st.date_input("Event Date")
time = st.time_input("Event Time")
duration = st.number_input("Duration (minutes)", min_value=5, value=30)

if st.button("Create Event"):
    start_datetime = datetime.datetime.combine(date, time)
    create_calendar_event(title, start_datetime, duration)
    st.success("Event created successfully!")
