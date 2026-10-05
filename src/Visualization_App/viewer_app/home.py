import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np


st.set_page_config(page_title="Viewer Homepage", page_icon=":sparkles:", layout="centered")


st.markdown("<h1 style='text-align: center; color: #f0f0f0;'>Viewer Homepage</h1>", unsafe_allow_html=True)


st.logo('viewer_app/media/bolthouse-Fresh.jpg', size='large')

st.write("Welcome to the Viewer Homepage! This is where you can find the current years " \
"data and insights. Use the navigation menu to explore different year's data and visualizations.")

image = Image.open('viewer_app/media/1000005203.jpg')
new_image = image.resize((400, 400))
st.image(new_image, caption="This is a sample image from one of the fields in the dataset.")

st.write("Sample: Within this image there are 24 carrots that was deteced by the model.")

# 1. Define the boundaries of the field area
lat_start, lat_end = 37.3595, 37.3605   # Vertical span
lon_start, lon_end = -120.4200, -120.4180 # Horizontal span

num_rows = 10        # Horizontal lines of dots
dots_per_row = 10    # number of dotd
total_points = num_rows * dots_per_row

# 3. Generate the coordinates
# This creates a "ladder" of latitudes
lats_grid = np.linspace(lat_start, lat_end, num_rows)
# This creates the horizontal spread
lons_grid = np.linspace(lon_start, lon_end, dots_per_row)

# 4. Use meshgrid to combine them into a full coordinate list
all_lats, all_lons = np.meshgrid(lats_grid, lons_grid)

# 5. Build the DataFrame
df = pd.DataFrame({
    "lat": all_lats.flatten(),
    "lon": all_lons.flatten(),
    "size": np.full(total_points, 0.5) # Matches the total grid size
})

st.map(df, size="size", color="#FC2E00", width=400, height=400)