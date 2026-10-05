import streamlit as st
import pandas as pd
from src.Database.data_requester import DatabaseRequester 
from typing import List
from src.Database.models import CarrotField


def get_field_data() -> List[CarrotField]:
    """
    Obtains all the fields from the database

    Returns:
        List[CarrotField]: A List containing CarrotField objects 
    """
    requester = DatabaseRequester()
    fields = requester.get_all_fields()
    return fields

def field_dropdown_button() -> CarrotField:
    """ 
    Builds a dropdown menu with all of the Fields inside the database, and returns the user selected field

    Returns:
        CarrotField: Data to be downloaded from CarrotField.data_points
    """
    requester = DatabaseRequester()
    fields = requester.get_all_fields()
    field_names = []

    for field in fields:
        field_names.append(field.name)

    option = st.selectbox("Select the field you wish to download data from:", field_names)
    st.write(f"You selected: {option}")

    selected_field = requester.get_field_by_name(option)
    return selected_field

def convert_for_download(models) -> pd.DataFrame:
    """Takes in either a List of CarrotFields or ImageMetadata, extracts the data, and formats in a Pandas Dataframe for download.

    Args:
        models (List[CarrotField] or List[ImageMetadata]): Data to be formatted as Dataframe 

    Returns:
        pd.DataFrame: Formatted data ready for download
    """
    if not models:
        return pd.DataFrame().to_csv().encode("utf-8")

    if isinstance(models, List):
        data = [m.model_dump() for m in models] # if the incoming data is a List of CarrotFields, then we need to separate those, otherwise it is just a Pandas DF 
    else:
        data = models
    return pd.DataFrame(data).to_csv().encode("utf-8")

if __name__ == "__main__":

    # ---------------------------- UI Interface ---------------------------------------
    st.set_page_config(page_title="Export", page_icon=":sparkles:", layout="centered")
    st.markdown("<h1 style='text-align: center; color: #f0f0f0;'>Export Data</h1>", unsafe_allow_html=True)

    st.logo('./src/Visualization_App/media/bolthouse_fresh_logo.png', size='large')

    st.write("Welcome to the Export Data page! Here you can download all of the fields inside the database, in the form of a CSV file, "
    "or you can download the metadata for a specific field using the dropdown menu!")
    # --------------------------------------------------------------------------------

    df = get_field_data() # Gets all fields 
    fields_df = convert_for_download(df) # Converts Carrot Field to Pandas Dataframe for download

    selected_field = field_dropdown_button() # Getting the selected field user wants 
    selected_field_df = convert_for_download(selected_field.data_points) # Converting field metadata to pandas dataframe

    # ---------------------- Download Buttons ----------------------------
    st.download_button(
        label="Download All Fields",
        data=fields_df,
        file_name="all_fields.csv",
        mime="text/csv",
        icon=":material/download:",
    )

    st.download_button(
        label="Download Selected Field",
        data=selected_field_df,
        file_name=selected_field.name,
        mime="text/csv",
        icon=":material/download:",
    )