#Day1
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

def read_csv(file_path):
    return pd.read_csv(file_path)

def connect_google_sheets(sheet_name):
    # Define the necessary scopes
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Load credentials with scopes
    creds = Credentials.from_service_account_file('credentials/credentials.json', scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)

#Day2
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import streamlit as st

# Specify the scopes for Gmail API access
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    """
    Authenticates the user with Gmail API using OAuth2.
    Returns the credentials object that can be used for making API requests.
    """
    creds = None
    try:
        # Start the authentication flow using the credentials file
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials/gmail_credentials.json', SCOPES
        )
        creds = flow.run_local_server(port=8501)
        st.success("Authentication successful!")
    except Exception as e:
        st.error(f"Error during authentication: {e}")
    return creds

#email sending fn
from googleapiclient.discovery import build

def send_email(credentials, to_email, subject, message_body):
    service = build('gmail', 'v1', credentials=credentials)
    message = {
        'raw': base64.urlsafe_b64encode(
            f'To: {to_email}\nSubject: {subject}\n\n{message_body}'.encode('utf-8')
        ).decode('utf-8')
    }
    service.users().messages().send(userId='me', body=message).execute()
    st.success(f"Email sent to {to_email}")

def generate_custom_email(prompt, data_row):
    for placeholder, value in data_row.items():
        prompt = prompt.replace(f"{{{placeholder}}}", value)
    return prompt

# Example usage
row = {'Company Name': 'Tech Corp', 'Location': 'New York'}
custom_prompt = "Hello {Company Name}, we noticed your presence in {Location}."
print(generate_custom_email(custom_prompt, row))

#Day3
import schedule
import time
from datetime import datetime
import streamlit as st

def send_email_at_scheduled_time(email_data):
    # Your existing send_email function here
    print(f"Sending email to {email_data['recipient']} at {datetime.now()}")

# Schedule emails
def schedule_email(email_data, send_time):
    schedule.every().day.at(send_time).do(send_email_at_scheduled_time, email_data)
    st.write(f"Scheduled email to {email_data['recipient']} at {send_time}")

# Run the scheduler in a loop
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)  # Wait a bit between checks to reduce CPU usage

from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def send_email_task(email_data):
    # Call the send email logic here
    print(f"Sending email to {email_data['recipient']} at {datetime.now()}")
