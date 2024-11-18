#Day1
import streamlit as st
import pandas as pd
from utils import connect_google_sheets

st.title("Custom Email Sender Dashboard")
st.write("Welcome! Connect a Google Sheet to get started.")

try:
    # Fetch data from Google Sheets
    sheet_name = "Your Google Sheet Name Here"
    data_frame = connect_google_sheets(sheet_name)

    # Display DataFrame in Streamlit
    st.write("Data from Google Sheets:")
    st.dataframe(data_frame)
except Exception as e:
    st.error(f"An error occurred: {e}")


#Day2

import streamlit as st
from utils import authenticate_gmail

st.title("Custom Email Sender with Gmail OAuth2 Authentication")

credentials = None  # Initialize credentials

# Button to start the authentication process
if st.button("Authenticate with Gmail",):
    credentials = authenticate_gmail()  # Assign credentials after authentication

# Check if credentials have been obtained
if credentials:
    st.write("You are now authenticated and can send emails!")
else:
    if st.button("Check Authentication"):
        st.write("Please authenticate first.")

#dd
import streamlit as st

st.title("Email Customization")
prompt = st.text_area("Enter your prompt with placeholders like {Company Name}, {Location}")

if st.button("Generate and Send Emails"):
    for index, row in df.iterrows():
        email_body = generate_custom_email(prompt, row.to_dict())
        # Call send_email function
        st.write(f"Email to {row['Email']} generated.")

#Day3
if st.button("Schedule Email",key="schedule_email_1"):
    email_data = {
        'recipient': st.text_input("Recipient Email"),
        'subject': st.text_input("Subject"),
        'body': st.text_area("Message")
    }
    send_time = st.text_input("Enter time to send (HH:MM in 24-hour format)")
    if send_time:
        schedule_email(email_data, send_time)
        st.write(f"Email scheduled for {send_time}")

# app.py
import streamlit as st
from celery import Celery
from celery import current_app as celery_app
from datetime import datetime
from utils import send_email_task  # Import the task from celery.py

st.title("Email Scheduler")

# Collect email information from the user
recipient = st.text_input("Recipient Email")
subject = st.text_input("Email Subject")
body = st.text_area("Email Body")

if st.button("Schedule Email",key="schedule_email_2"):
    # Package email data
    email_data = {
        "recipient": recipient,
        "subject": subject,
        "body": body,
    }
    # Schedule email sending task with a 10-second delay
    send_email_task.apply_async((email_data,), countdown=10)
    st.success("Email scheduled to be sent in 10 seconds.")

# app.py
import time
import streamlit as st


# Sample function to fetch email status data from your database or task tracking system
def get_email_status():
    # Replace this with actual logic to retrieve email status
    email_status = {
        'total_sent': 50,
        'pending': 10,
        'failed': 5,
        'scheduled': 15
    }
    return email_status


# Display Dashboard
st.header("Email Sending Status Dashboard")


# Function to refresh data periodically
def display_dashboard():
    while True:
        email_status = get_email_status()  # Get the latest email status data

        # Display metrics
        st.metric("Total Emails Sent", email_status['total_sent'])
        st.metric("Emails Pending", email_status['pending'])
        st.metric("Emails Failed", email_status['failed'])
        st.metric("Emails Scheduled", email_status['scheduled'])

        time.sleep(10)  # Pause before refreshing
        st.experimental_rerun()  # Re-run the app to refresh data


# Run the dashboard display function
display_dashboard()
