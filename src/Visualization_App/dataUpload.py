import streamlit as st
from src.Database.data_requester import DatabaseRequester
import numpy as np
from PIL import Image
from src.Models.resnet_liveprocessing import ImageToModelToDatabase
from datetime import datetime


@st.cache_resource
def get_requester() -> DatabaseRequester:
    return DatabaseRequester()


@st.cache_resource
def get_model_handler() -> ImageToModelToDatabase:
    return ImageToModelToDatabase()


if __name__ == "__main__":
    st.set_page_config(page_title="Admin Upload", page_icon=":sparkles:", layout="centered")
    st.markdown("<h1 style='text-align: center; color: #f0f0f0;'>Admin Data Upload</h1>", unsafe_allow_html=True)

    st.logo('./src/Visualization_App/media/bolthouse_fresh_logo.png', size='large')

    st.write("Welcome to the Admin Data Upload page! This is where you can upload and manage the data for the Admin application.")

    field_names = []
    requester = get_requester()
    model_handler = get_model_handler()

    fields = requester.get_all_fields()
    for field in fields:
        field_names.append(field.name)

    option = st.selectbox("Select the field you are updloading data to", field_names)
    st.write(f"You selected: {option}")

    selected_field = requester.get_field_by_name(option)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        lat = st.text_input("Image Latitude", placeholder="Latitude")
    with col2:
        lon = st.text_input("Image Longitude", placeholder="Longitude")
    with col3:
        img_date = st.date_input("Image Date", value=datetime.now().date())
    with col4:
        img_time = st.text_input("Image Time", value="00:00", placeholder="HH:MM")


    uploaded_file = st.file_uploader(
        "Upload image file, Drag and Drop files, File types: .jpg, .png", accept_multiple_files=False, type=["jpg", "png"]
    )

    if uploaded_file is not None:
        st.image(uploaded_file)
        uploaded_file.seek(0)  # Reset file pointer to start
        img = Image.open(uploaded_file)
        img_array = np.array(img)

        st.write("Image imported successfully! Ready to upload to database.")

        if st.button("Upload to Database"):
            if not option:
                st.error("Please select a field before uploading.")
                st.stop()
            if not lat or not lon:
                st.error("Please enter valid latitude and longitude")
                st.stop()
            try:
                time_text = img_time.strip()
                try:
                    parsed_time = datetime.strptime(time_text, "%H:%M").time()
                except ValueError:
                    parsed_time = datetime.strptime(time_text, "%H:%M:%S").time()

                # combine date and time using the current local timezone
                local_timezone = datetime.now().astimezone().tzinfo
                timestamp = datetime.combine(img_date, parsed_time, tzinfo=local_timezone)
                detections = model_handler.process_uploaded_image(uploaded_file=img_array, field_name=option, lat=float(lat), lon=float(lon), timestamp=timestamp)
                st.success(f"Data uploaded to database successfully! Detected {int(detections)} carrots in image.")
            except Exception as e:
                st.error(f"Failed to upload data to database: {str(e)}")



    uploaded_videos = st.file_uploader(
        "Upload video files, Drag and Drop files, File types: .mp4", accept_multiple_files=True, type=["mp4"]
    )

    for uploaded_file in uploaded_videos:
        st.video(uploaded_file)

    #if uploaded_videos is not None:
    #    st.success("Uploaded")