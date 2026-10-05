"""Visualization Page for the visualization app. This is the primary function of the app. 
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
# from streamlit_folium import st_folium
# from src.Database.data_requester import DatabaseRequester

def generate_example_dataframe() -> pd.DataFrame:
    # configuration parameters for the representative data records
    MAXIMUM_YIELD = 20
    MINIMUM_YIELD = 10
    NOISE_LEVEL = 0.00001
    
    LATITUDE_MIN = 37.3585
    LATITUDE_MAX = 37.3610
    LONGITUDE_MIN = -120.4201
    LONGITUDE_MAX = -120.4165

    POINTS = 15

    lats = np.linspace(LATITUDE_MIN, LATITUDE_MAX, POINTS)
    lons = np.linspace(LONGITUDE_MIN, LONGITUDE_MAX, POINTS)
    lat_grid, lon_grid = np.meshgrid(lats, lons)

    noise = np.random.normal(0, NOISE_LEVEL, (POINTS, POINTS, 2))
    noisy_lats = lat_grid + noise[:,:,0]
    noisy_lons = lon_grid + noise[:,:,1]

    yield_range = MAXIMUM_YIELD-MINIMUM_YIELD
    yield_values = np.random.normal(MINIMUM_YIELD + yield_range/2, yield_range/3, noisy_lats.shape)
    yield_values = np.clip(yield_values, MINIMUM_YIELD, MAXIMUM_YIELD)

    disease_values = np.random.normal(0.1, 0.15, noisy_lats.shape)
    disease_values = np.clip(disease_values, 0, 1)

    time_series = np.datetime64('2026-03-02T08:00') + np.arange(POINTS*POINTS) * np.timedelta64(1, 'm')

    df = pd.DataFrame({
        "Latitude":noisy_lats.flatten(),
        "Longitude":noisy_lons.flatten(),
        "Yield":yield_values.flatten(),
        "Disease":disease_values.flatten(),
        "Timestamp":time_series,
        "Field ID":["Field 1" for i in range(POINTS*POINTS)],
        "Record ID":[i for i in range(POINTS*POINTS)] # NOTE: the real records will have a different ID scheme
    })

    # For Debug: 
    # print(f"whole dataframe: {df}")
    # print(f"yield values ({yield_values.shape}):  {yield_values}")

    return df

@st.cache_data # This stores the requested dataframe in memory. TODO: We should look in more detail about what precisely is cached (between sessions) and how much memory is taken up. 
def load_and_format_data(field_name: str, date_start: datetime, date_end: datetime) -> pd.DataFrame:
    """This invokes the data requester utility to get the requested data from the database. It also collects the data into the proper shape and retains it in the webpage memory. 

    Args:
        field_ID (str): Name of the field for which the data is being gathered
        date (str): Date range to fetch data for

    Returns:o
        pd.DataFrame: Structured Dataframe consisting of Latitude, Longitude, Yield, Disease, Timestamp, Field ID, and Record ID columns. 
    """
    # field_data_packet = DatabaseRequester.request_df_from_db(field_name, date_start, date_end) # NOTE: unused for now. 
    
    df = generate_example_dataframe() # NOTE: for now, this uses representative data instead of the actual data from the pipeline

    return df

st.title("Visualization")

st.write("Example Dataset")
# df2 = load_and_format_data("North Sector A", np.datetime64('2026-03-21 05:21:47.075196'), np.datetime64('2026-03-21 05:21:47.075223') )
# st.dataframe(df2)

# st.write("Yield Distribution")
# counts, bin_edges = np.histogram(df2["Yield"], bins=20)
# hist_df = pd.DataFrame(counts, index=bin_edges[:-1], columns=["Count"])
# st.bar_chart(hist_df)