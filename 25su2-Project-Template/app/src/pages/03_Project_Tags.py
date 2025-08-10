import streamlit as st
import requests

st.title("Project Tags")

try:
    # Call your Flask endpoint
    response = requests.get("http://localhost:3306/projects/projecttags")

    if response.status_code == 200:
        tags = response.json()

        if tags:
            for tag in tags:
                st.subheader(tag.get('name', 'Unnamed Tag'))
                st.write(f"Tag ID: {tag.get('tagID', 'N/A')}")
                st.write(f"Color: {tag.get('color', 'No color specified')}")
                st.write("---")
        else:
            st.info("No project tags found.")

    elif response.status_code == 404:
        st.info("No project tags found.")

    else:
        st.error(f"Error fetching tags: {response.status_code}")

except Exception as e:
    st.error(f"Failed to fetch tags: {e}")