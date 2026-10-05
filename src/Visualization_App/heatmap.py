import streamlit as st
from scipy.spatial import Voronoi
from shapely.geometry import Polygon
import geopandas as gpd
import branca.colormap as cm
import folium
from streamlit_folium import st_folium
from src.Database.data_requester import DatabaseRequester
from src.Database.image_storage import ImageStorage
import numpy as np
import base64
from datetime import datetime

st.set_page_config(layout="wide")

@st.cache_data
def get_cached_img(_requester, img):
    image = _requester.get_image_from_metadata(img)
    # If storage returns raw bytes (tests / new API), convert to a data URL
    if isinstance(image, (bytes, bytearray)):
        try:
            b64 = base64.b64encode(image).decode('utf-8')
            return f"data:image/jpeg;base64,{b64}"
        except Exception:
            return None
    return image

def add_field_boundary(feature_group):
    """Adds a field boundary overlay on the map"""
    folium.Polygon( # Make a bounding box for the field
        locations=st.session_state.polygon_coords,
        color="blue",       # Outline color
        weight=3,          # Outline thickness
        fill=True,         # Fill the inside
        fill_color="red",   # Inside color
        fill_opacity=0.01,  # Transparency
    ).add_to(feature_group)
    map.fit_bounds(st.session_state.polygon_coords)

    

def add_image_data_markers(feature_group, requester=DatabaseRequester()):
    """Adds markers showing the yield at each data point in this field. """
    for img in st.session_state.data_points: # Make data points for each image
        # Adding yield markers (Point-based)
        image_object = get_cached_img(requester, img)
        date_list = img.time_recorded.strftime("%Y-%m-%d %H:%M:%S").split(" ")

        if image_object:
            popup_html = f'''
                <div style="font-family: Arial, sans-serif;">
                    <img src="{image_object}" width="400"><br>
                    <strong>Lat:</strong> {img.lat}
                    <strong> Lon:</strong> {img.lon}<br>
                    <strong>Timestamp:</strong> {date_list[0]} {date_list[1]}<br>
                    
                </div>
            '''
        else:
            popup_html = f'''
                <div style="font-family: Arial, sans-serif;">
                    <strong>Lat:</strong> {img.lat}
                    <strong> Lon:</strong> {img.lon}<br>
                    <strong>Timestamp:</strong> {date_list[0]} {date_list[1]}<br>
                    <em>Image not available</em>
                </div>
'''
        folium.CircleMarker(
            location=[img.lat, img.lon],
            radius=4,
            color="black",
            fill=True,
            tooltip=f"Yield: {round(img.carrot_density_per_meter,2)}",
            popup=folium.Popup(popup_html)
            #popup = folium.Popup(st.image(image_object) if image_object is not None else "Image not available")

        ).add_to(feature_group)

def add_heatmap(map, feature_group):
    """Adds an overlay showing the field's yield heatmap. """

    gps_coordinates = np.array([[img.lon, img.lat] for img in st.session_state.data_points])
    values = [img.carrot_density_per_meter for img in st.session_state.data_points]
    boundary = Polygon([[lon, lat] for lat, lon in st.session_state.polygon_coords]) # the order of the coordinates is switched

    #create anchor points very far outside field to 'bound' voronoi polygons to not extend infinitely
    min_lon, min_lat, max_lon, max_lat = boundary.bounds
    buffer = 1.0  # Degrees; large enough to surround the field
    anchors = np.array([
        [min_lon - buffer, min_lat - buffer],
        [min_lon - buffer, max_lat + buffer],
        [max_lon + buffer, min_lat - buffer],
        [max_lon + buffer, max_lat + buffer]
    ])

    points_with_anchors = np.append(gps_coordinates, anchors, axis=0)


    vor = Voronoi(points_with_anchors)
    polygons = []
    valid_values = []


    for i, region_index in enumerate(vor.point_region):
        region = vor.regions[region_index]
        if -1 not in region and len(region) > 0: #cull unbounded/empty regions
            poly = Polygon([vor.vertices[j] for j in region])
            if poly.intersects(boundary): #clip polygon to field boundary
                clipped_poly = poly.intersection(boundary)
                if not clipped_poly.is_empty:
                    polygons.append(clipped_poly)
                    valid_values.append(values[i])
    
    if not polygons:
        st.warning("No valid polygons could be generated within the boundary")
        return

    gdf = gpd.GeoDataFrame({'value': valid_values}, geometry=polygons)
    gdf.set_crs(epsg=4326, inplace=True)
    colormap = cm.LinearColormap(
        colors=['red', 'yellow', 'green'],
        vmin=gdf['value'].min(),
        vmax=gdf['value'].max()
    )
    
    colormap.add_to(map)

    folium.GeoJson(gdf, style_function=lambda x: {
        'fillColor': colormap(x['properties']['value']),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7
        }).add_to(feature_group)

# Page Initialization
st.title("Folium Heatmap")
st.logo('./src/Visualization_App/media/bolthouse_fresh_logo.png', size='large')

# Heatmap Setup
if "polygon_coords" not in st.session_state: 
    st.session_state.polygon_coords = None
if "data_points" not in st.session_state:
    st.session_state.data_points = None

field_names = []
requester = DatabaseRequester()
fields = requester.get_all_fields()
for field in fields:
    field_names.append(field.name)

option = st.selectbox("Select a field to view", field_names)
st.write(f"You selected: {option}")

selected_field = requester.get_field_by_name(option)

if selected_field:
    st.session_state.polygon_coords = [[selected_field.lat1, selected_field.lon1],
                      [selected_field.lat2, selected_field.lon2], 
                      [selected_field.lat3, selected_field.lon3], 
                      [selected_field.lat4, selected_field.lon4]]

    # Use two separate date inputs to avoid partial-range state issues
    # Default to today if no data is present
    default_start = datetime.now().date()
    default_end = datetime.now().date()

    start_date = st.date_input("Start date", value=default_start)
    end_date = st.date_input("End date", value=default_end)

    # Only attempt to fetch when both dates are present and valid
    try:
        if start_date and end_date:
            # normalize to datetimes inclusive
            date_start = datetime.combine(start_date, datetime.min.time())
            date_end = datetime.combine(end_date, datetime.max.time())
            if date_end < date_start:
                st.warning("End date is before start date. Showing all data for field.")
                st.session_state.data_points = selected_field.data_points
            else:
                st.session_state.data_points = requester.get_image_metadata_for_field(selected_field.id, date_start, date_end)
        else:
            st.session_state.data_points = selected_field.data_points
    except Exception:
        st.session_state.data_points = selected_field.data_points

# map initialization
map = folium.Map(location=[37.3595, -120.4200], zoom_start=15, tiles='OpenStreetMap')
fg_yield = folium.FeatureGroup(name="Yield", show=True)
fg_boundary = folium.FeatureGroup(name="Field Boundary", show=True)
fg_heatmap = folium.FeatureGroup(name="Yield Heatmap", show=True)

fg_boundary.add_to(map)
fg_heatmap.add_to(map)
fg_yield.add_to(map)
folium.LayerControl(collapsed=False).add_to(map)

if st.session_state.polygon_coords: # If there is a field loaded, 
    add_field_boundary(fg_boundary)
    add_image_data_markers(fg_yield, requester=requester)
    add_heatmap(map, fg_heatmap)
    
    st_folium(map, width=1400, height=1000, returned_objects=[], key = "viewer_heatmap") # Make the map on the page
