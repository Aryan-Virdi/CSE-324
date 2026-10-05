from sqlmodel import SQLModel, Field, Relationship
from typing import Optional ,List
from datetime import datetime, timezone


class CarrotField(SQLModel, table=True):
    __tablename__ = "carrot_field"
    #id optional because the DB generates PK after save
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True, index=True)

    # GPS Bounds
    # Corner 1
    lat1: float = Field(nullable=False)
    lon1: float = Field(nullable=False)

    # Corner 2
    lat2: float = Field(nullable=False)
    lon2: float = Field(nullable=False)

    # Corner 3
    lat3: float = Field(nullable=False)
    lon3: float = Field(nullable=False)

    # Corner 4
    lat4: float = Field(nullable=False)
    lon4: float = Field(nullable=False)

    data_points: List["ImageMetadata"] = Relationship(back_populates="field", cascade_delete=True)

    entry_created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    # Should be updated manually in the access class
    entry_updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

class ImageMetadata(SQLModel, table=True):
    __tablename__ = "image_metadata"
    #id optional because the DB generates PK after save
    id: Optional[int] = Field(default=None, primary_key=True)

    carrot_density_per_meter: float

    # GPS Bounds
    lon: float = Field(index=True)
    lat: float = Field(index=True)

    time_recorded: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    field_id: int = Field(nullable=False, foreign_key="carrot_field.id")
    field: CarrotField = Relationship(back_populates="data_points")

    image_key: str = Field(nullable=True)

    entry_created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    # Should be updated manually in the access class
    entry_updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )