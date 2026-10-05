"""Visualization App for analysis after data is gathered in the field. 

This app uses streamlit as a backbone, pandas for the statistical analysis, and folium for the map visualization. 
"""

import streamlit as st
from src.Database.database import create_db_and_tables

@st.cache_resource
def setup_database():
    create_db_and_tables()
    return True

if __name__ == "__main__":
    setup_database()

home_page = st.Page(
    "home.py",
    title="Home",
    icon=":material/home:",
    default=True,
)

auth_page = st.Page(
    "authentication.py",
    title="Authentication",
    icon=":material/lock:",
)

dataUpload_page = st.Page(
    "dataUpload.py",
    title="Admin Data Upload",
    icon =":material/upload:",
)

heatmap_page = st.Page(
    "heatmap.py",
    title="Heatmap",
    icon =":material/heat_pump:",
)

exportData_page = st.Page(
    "exportData.py",
    title="Export Field Data",
    icon =":material/download:",
)

create_field = st.Page(
    "createField.py",
    title="Field Management",
    icon =":material/add_location:",
)

pg = st.navigation(
    {
        "Account": [auth_page],
        "App": [home_page, dataUpload_page, heatmap_page, create_field , exportData_page],
    }
)

if __name__ == "__main__":
    pg.run()