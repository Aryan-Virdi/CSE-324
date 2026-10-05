import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np

st.set_page_config(page_title="Viewer 2025", page_icon=":sparkles:", layout="centered")


st.markdown("<h1 style='text-align: center; color: #f0f0f0;'>Viewer 2025</h1>", unsafe_allow_html=True)



st.logo('./src/Visualization_App/media/bolthouse-Fresh.jpg', size='large')

st.write("Welcome to the Viewer 2025 page! This is where you can find the 2025 data and analysis.")

image = Image.open('./src/Visualization_App/media/1000005199.jpg')
new_image = image.resize((400, 400))
st.image(new_image, caption="This is a sample image from one of the fields in the dataset.")

lat_start, lat_end = 37.3595, 37.3605   #
lon_start, lon_end = -120.4200, -120.4180 

num_rows = 10        
dots_per_row = 10    
total_points = num_rows * dots_per_row


lats_grid = np.linspace(lat_start, lat_end, num_rows)
lons_grid = np.linspace(lon_start, lon_end, dots_per_row)

all_lats, all_lons = np.meshgrid(lats_grid, lons_grid)


df = pd.DataFrame({
    "lat": all_lats.flatten(),
    "lon": all_lons.flatten(),
    "size": np.full(total_points, 0.5) 
})

st.map(df, size="size", color="#FC2E00", width=400, height=400)