import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import mysql.connector


st.set_page_config(layout = 'wide')

@st.cache_resource
def init_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="1203",
        database="global-GoalFlow"
    )

# Function to run queries
def run_query(query, params=None):
    conn = init_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


st.title(f"Welcome Political Strategist")
st.write('')
st.write('')
st.write('### What would you like to do today?')

try:
    emails = run_query("SELECT email FROM users")
    
    # Display as a clean list
    email_list = [email[0] for email in emails]  # Extract just the email strings
    st.write("Email List:")
    for email in email_list:
        st.write(f"• {email}")
        
except Exception as e:
    st.error(f"Error fetching emails: {e}")