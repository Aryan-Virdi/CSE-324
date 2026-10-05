"""Configuration page of the visualization app. This is used for configuring how data are displayed + processing debug logs. 
"""

import streamlit as st

def modify_window_layout(layout: dict):
    """Modifies the visualization window and/or overall theme of the webapp

    Args:
        layout (dict): Dictionary containing all page elements that can be adjusted
    """
    pass

def save_configuration_parameters_to_file(layout: dict):
    """Saves the current configuration to a file, to be loaded later

    Args:
        layout (dict): Dictionary containing all page elements that can be adjusted
    """
    pass

def load_configuration_parameters_from_file() -> dict:
    """Opens the file explorer, parses configuration file, then applies changes to the webapp

    Returns:
        dict: Dictionary containing all page elements that can be adjusted
    """
    pass

st.title("Configuration and Debug")
st.subheader("Config Settings")
data_source = st.selectbox("Select Data Source", ["A", "B", "C"])
threshold = st.slider("Slider", 0, 100, 50)

st.info(f"Choice {data_source} and slider {threshold}.")