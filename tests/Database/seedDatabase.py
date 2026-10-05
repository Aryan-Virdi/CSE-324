from sqlmodel import Session
from src.Database.database import engine, create_db_and_tables, drop_db_and_tables
from src.Database.models import CarrotField, ImageMetadata
from datetime import datetime, timezone, timedelta
import numpy as np

# WARNING!! This code resets the database and reseeds it with dummy data

def generate_gps_grid(latitude_min, latitude_max, longitude_min, longitude_max, points=15, noise_level=0.00001):
  """Generates a noisy 2D grid of GPS coordinates"""
  # 1. Create the "True" Grid
  lats = np.linspace(latitude_min, latitude_max, points)
  lons = np.linspace(longitude_min, longitude_max, points)
  lat_grid, lon_grid = np.meshgrid(lats, lons)

  # 2. Generate 2D Gaussian Noise
  # mean=[0,0], cov=[[noise, 0], [0, noise]]
  noise = np.random.normal(0, noise_level, (points, points, 2))

  noisy_lats = lat_grid + noise[:,:,0]
  noisy_lons = lon_grid + noise[:,:,1]

  return noisy_lats, noisy_lons

def generate_data_values(field_id, lats, lons, min_yield=0, max_yield=150): # TODO: annotate with return data types
  """Generates a list of representative data points to be stored in an example field"""
  images = []

  yield_values = np.random.normal(np.average([min_yield, max_yield]), (max_yield-min_yield)/3, lats.shape) # makes a grid normally distributed within the range
  yield_values = np.clip(yield_values, min_yield, max_yield)
  
  for latitude, longitude, yield_v in zip(lats.ravel(), lons.ravel(), yield_values.ravel()):
    image = ImageMetadata(
      carrot_density_per_meter=float(yield_v), # these are numpy floats, which are not recognized by sqlalchemy. we have to convert them
      lat=float(latitude),
      lon=float(longitude),
      time_recorded=datetime.now(timezone.utc),
      field_id=field_id
    )

    images.append(image)

  return images

def seed_data():
    print("Wiping and recreating database...")
    drop_db_and_tables()
    create_db_and_tables()

    with Session(engine) as session:
        # 1. Create a dummy Field
        field_1 = CarrotField(
            name="North Sector A",
            lat1=45.000, lon1=-93.000,
            lat2=45.000, lon2=-92.990,
            lat3=45.010, lon3=-92.990,
            lat4=45.010, lon4=-93.000
        )
        
        field_2 = CarrotField(
            name="South Sector B",
            lat1=44.990, lon1=-93.000,
            lat2=44.990, lon2=-92.990,
            lat3=45.000, lon3=-92.990,
            lat4=45.000, lon4=-93.000
        )

        field_3 = CarrotField(
            name="UC Merced Southeast",
            lat1=37.3580, lon1=-120.4205,
            lat2=37.3580, lon2=-120.4161,
            lat3=37.3615, lon3=-120.4161,
            lat4=37.3615, lon4=-120.4205
        )

        session.add(field_1)
        session.add(field_2)
        session.add(field_3)
        session.commit() # Commit so we have IDs for the next step
        session.refresh(field_1)

        # 2. Create dummy Image Data Points
        image_1 = ImageMetadata(
            carrot_density_per_meter=12.5,
            lat=45.005,
            lon=-92.995,
            time_recorded=datetime.now(timezone.utc),
            field_id=field_1.id
        )
        
        image_2 = ImageMetadata(
            carrot_density_per_meter=8.2,
            lat=45.003,
            lon=-92.997,
            time_recorded=datetime.now(timezone.utc) - timedelta(hours=1),
            field_id=field_1.id
        )

        image_3 = ImageMetadata(
            carrot_density_per_meter=5.5,
            lat=45.002,
            lon=-92.999,
            time_recorded=datetime.now(timezone.utc) - timedelta(hours=1),
            field_id=field_1.id
        )

        lats, lons = generate_gps_grid(37.3585, 37.3610, -120.4201, -120.4165)
        field_3_images = generate_data_values(field_3.id,lats,lons)

        session.add(image_1)
        session.add(image_2)
        session.add(image_3)
        for i in field_3_images:
           session.add(i)
        session.commit()
        
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()