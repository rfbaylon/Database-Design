import streamlit as st
import requests
import datetime

st.title("Add New Project")

with st.form("add_project_form"):
    user_id = st.number_input("User ID", min_value=1)
    tag_id = st.number_input("Tag ID", min_value=1)
    title = st.text_input("Project Title")
    notes = st.text_area("Notes")
    status = st.selectbox("Status", options=["onIce", "ACTIVE", "ARCHIVED"], index=0)
    priority = st.slider("Priority (1=Critical, 4=Low)", min_value=1, max_value=4, value=4)
    completed_at = st.date_input("Completed At (optional)", value=None)
    schedule = st.date_input("Deadline (Schedule) (optional)", value=None)

    submitted = st.form_submit_button("Add Project")

if submitted:
    # Format dates as string if provided
    completed_at_str = completed_at.strftime('%Y-%m-%d') if completed_at else None
    schedule_str = schedule.strftime('%Y-%m-%d') if schedule else None

    payload = {
        "userID": user_id,
        "tagID": tag_id,
        "title": title,
        "notes": notes,
        "status": status,
        "priority": priority,
        "completedAt": completed_at_str,
        "schedule": schedule_str
    }

    try:
        response = requests.post("http://localhost:5000/projects", json=payload)
        if response.status_code == 200:
            st.success("Project added successfully!")
        else:
            st.error(f"Failed to add project: {response.text}")
    except Exception as e:
        st.error(f"Error sending request: {e}")
