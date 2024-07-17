import streamlit as st
import subprocess
import time
from datetime import datetime

def send_imessage(phone_number, message):
    apple_script = f'''
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{phone_number}" of targetService
        send "{message}" to targetBuddy
    end tell
    '''
    process = subprocess.Popen(['osascript', '-e', apple_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        st.error(f"Error: {stderr.decode('utf-8')}")
    else:
        st.success(f"Message sent to {phone_number} at {datetime.now()}")

def schedule_message(phone_number, message, send_time):
    schedule_time = datetime.strptime(send_time, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    delay = (schedule_time - now).total_seconds()

    if delay > 0:
        time.sleep(delay)
        send_imessage(phone_number, message)
    else:
        st.error("Scheduled time is in the past. Please enter a future time.")

st.title("iMessage Scheduler")

phone_number = st.text_input("Enter the recipient's phone number")
message = st.text_area("Enter your message")
send_time = st.text_input("Enter the scheduled time (YYYY-MM-DD HH:MM: SS )")

if st.button("Schedule Message"):
    schedule_message(phone_number, message, send_time)
