"""Landing page for the webapp. This is necessary to restrict access to the visualizaiton until after authentication. 
"""

import streamlit as st

st.set_page_config(page_title="Home", page_icon=":sparkles:", layout="centered")
st.markdown("<h1 style='text-align: center; color: #f0f0f0;'>Home</h1>", unsafe_allow_html=True)
st.logo('./src/Visualization_App/media/bolthouse_fresh_logo.png', size='large')

st.image("./src/Visualization_App/media/Logo.svg", width=800)

st.markdown("<h4 style='text-align: center; color: #f0f0f0;'>Welcome to the Homepage for the Bolthouse Fresh Foods Data Visualization App!</h3>", unsafe_allow_html=True)

st.write("You can use this app to view all the images upload from the fields and the heatmaps generated from the data." 
" Please navigate to the appropriate page using the sidebar on the left. For any issues that may arise, please contact the administrator.")