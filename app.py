import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import uuid
import json

# Access credentials from secrets
credentials_info = st.secrets["GOOGLE_CREDENTIALS"]

# Google Sheets Authentication
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(json.loads(credentials_info), scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("Events").sheet1

# Admin Login
def admin_login():
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin@2025":
            st.session_state["logged_in"] = True
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

# Add New Event
def add_event():
    st.title("Add New Event")
    title = st.text_input("Title")
    description = st.text_area("Description")
    venue = st.text_input("Venue")
    date = st.date_input("Date")
    time = st.time_input("Time")
    reg_link = st.text_input("Registration Link (Optional)")
    event_type = st.selectbox("Event Type", ["Academic", "Cultural", "Technical"])

    if st.button("Add Event"):
        event_id = str(uuid.uuid4())
        sheet.append_row([event_id, title, description, venue, str(date), str(time), reg_link, event_type.lower()])
        st.success("Event added successfully!")

# Display Events (Public)
def display_events():
    st.title("Upcoming Events")
    events = sheet.get_all_records()
    if not events:
        st.write("No events found.")
        return

    for event in events:
        st.subheader(event["Title"])
        st.write(f"**Description:** {event['Description']}")
        st.write(f"📍 **Venue:** {event['Venue']}")
        st.write(f"📅 **Date:** {event['Date']}")
        st.write(f"⏰ **Time:** {event['Time']}")
        st.write(f"📝 **Type:** {event['Type'].capitalize()}")

# Main App Logic
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Navigation
page = st.sidebar.selectbox("Navigation", ["View Events", "Admin Panel"])

if page == "Admin Panel":
    if not st.session_state["logged_in"]:
        admin_login()
    else:
        add_event()
else:
    display_events()
