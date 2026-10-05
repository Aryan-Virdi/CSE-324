"""Authentication page for the visualization app. 
"""

import streamlit as st

def authenticate_user(username: str, password: str): 
    """Sends the authentication request to the data requester module, then updates the user permissions pending the result.

    Args:
        username (str): Username that identifies the user. Possibly an email or something similar
        password (str): Password associated with user credential
    """
    pass


st.title("Authentication")
st.logo('./src/Visualization_App/media/bolthouse_fresh_logo.png', size='large')

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Log In"):
    st.success(f"Logged in as {email}")