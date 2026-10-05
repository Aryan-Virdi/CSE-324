"""This is the page that allows users to manage which fields are to be visualized. This involes creating, deleting, and loading fields. """
import streamlit as st
import folium
from streamlit_folium import st_folium
from src.Database.data_requester import DatabaseRequester 
from tests.Database.seedDatabase import seed_data # NOTE: This is temporary for now, we will find a better way to do this

# Page Preliminaries
requester = DatabaseRequester()

field_names = [] # field names and data
fields = requester.get_all_fields()
for field in fields:
    field_names.append(field.name)
    
polygon_coords = [] # bounding boxes corresponding to fields. TODO: There is likely a more proper way to implement this functionality
if "polygon_coords" not in st.session_state: 
    st.session_state.polygon_coords = None # TODO: see if we can use something other than the polygon coordinates to track this
st.logo('./src/Visualization_App/media/bolthouse_fresh_logo.png', size='large')

# Field Loading Section
# TODO: For now, we are loading dummy data. Ideally, this data should live in the database and be fetched on command. 
st.title("Load Field")
if st.button("Load All Pre-Existing Fields"):
    try:
        seed_data()
        st.success("Successfully loaded existing fields!")
    except ValueError:
        st.error("Failed to re-seed the databse.") # this shouldn't fail, but who knows...
option = st.selectbox("Select a field to view", field_names)
st.write(f"You selected: {option}")

# Field Deletion Section
st.title ("Delete Field")
if st.button("Delete Field"):
    field_to_delete = requester.get_field_by_name(option)
    if field_to_delete:
        requester.delete_field_by_id(field_to_delete.id)
        st.success(f"Field '{option}' deleted successfully!")
    else:
        st.error(f"Field '{option}' not found.")

# Field Creation Section
st.title("Create Field")
field_name = st.text_input(label = "Field Name", placeholder="Enter a name for the field")
col1, col2, col3, col4 = st.columns(4)

with col1:
    corner1_lat = st.text_input("Corner 1 Coordinates", placeholder="latitude")
    corner2_lat = st.text_input("Corner 2 Coordinates", placeholder="latitude")
    corner3_lat = st.text_input("Corner 3 Coordinates", placeholder="latitude")
    corner4_lat = st.text_input("Corner 4 Coordinates", placeholder="latitude")
    
with col2:
    corner1_lon = st.text_input(label = "Corner 1 Longitude", placeholder="longitude", key="corner1_lon", label_visibility="hidden")
    corner2_lon = st.text_input(label = "Corner 2 Longitude", placeholder="longitude", key="corner2_lon", label_visibility="hidden")
    corner3_lon = st.text_input(label = "Corner 3 Longitude", placeholder="longitude", key="corner3_lon", label_visibility="hidden")
    corner4_lon = st.text_input(label = "Corner 4 Longitude", placeholder="longitude", key="corner4_lon", label_visibility="hidden")

with col1:
    if st.button("Preview Field"):
        coords_exist = all([corner1_lat, corner2_lat, corner3_lat, corner4_lat, corner1_lon, corner2_lon, corner3_lon, corner4_lon])
        if coords_exist:
            try:
                st.session_state.polygon_coords = [
                    [float(corner1_lat), float(corner1_lon)],
                    [float(corner2_lat), float(corner2_lon)],
                    [float(corner3_lat), float(corner3_lon)],
                    [float(corner4_lat), float(corner4_lon)]
                ]
            except ValueError:
                st.error("Please enter valid coordinates.")
        else:
            st.error("Please enter coordinates for all four corners before previewing.")

with col4:
    if st.button("Save Field"):
        if field_name and st.session_state.polygon_coords:
            try:
                requester.add_field( name=field_name, lat1=float(corner1_lat), lon1=float(corner1_lon),
                    lat2=float(corner2_lat), lon2=float(corner2_lon),
                    lat3=float(corner3_lat), lon3=float(corner3_lon),
                    lat4=float(corner4_lat), lon4=float(corner4_lon)
                )
                st.success(f"Field '{field_name}' saved successfully!")
            except ValueError:
                st.error("Please enter valid coordinates and a field name.")
        else:
            st.error("Please enter a field name and valid coordinates before saving.")

# Visualize the map if it has been created
if st.session_state.polygon_coords:
    map = folium.Map(location=[37.3595, -120.4200], zoom_start=5, tiles='OpenStreetMap') # This default coordinate needs to depend on the polygon's coordinates, not a hardcoded value

    folium.Polygon(
                locations=st.session_state.polygon_coords,
                color="black",       # Outline color
                weight=2,          # Outline thickness
                fill=True,         # Fill the inside
                fill_color="green",   # Inside color
                fill_opacity=0.2,  # Transparency
            ).add_to(map)

    folium.Marker(
        location=st.session_state.polygon_coords[0],
        tooltip="Corner 1",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(map)
    folium.Marker(
        location=st.session_state.polygon_coords[1],
        tooltip="Corner 2",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(map)
    folium.Marker(
        location=st.session_state.polygon_coords[2],
        tooltip="Corner 3",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(map)
    folium.Marker(
        location=st.session_state.polygon_coords[3],
        tooltip="Corner 4",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(map)
    map.fit_bounds(st.session_state.polygon_coords)

    st_folium(map, width=700, height=500)
else:
    st.info("Enter the coordinates of the field corners and click 'Preview Field' to view the field.")