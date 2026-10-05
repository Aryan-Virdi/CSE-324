from sqlmodel import SQLModel, create_engine, Session
from pydantic_settings import BaseSettings, SettingsConfigDict

# 1. Configuration Logic
class Settings(BaseSettings):
    # Pydantic automatically maps DATABASE_URL env var to this field
    database_url: str
    db_user: str
    db_password: str
    db_name: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  
    )

# 2. Initialization
settings = Settings()

# FIX: Use the validated settings object instead of os.getenv
# This ensures that if DATABASE_URL is missing, the app crashes with a clear error
engine = create_engine(settings.database_url, echo=True) #echo=true prints sql statements in terminal.

# 3. Table Management
def create_db_and_tables():
    from src.Database.models import CarrotField, ImageMetadata  # noqa: F401
    SQLModel.metadata.create_all(engine)

def drop_db_and_tables():
    from src.Database.models import CarrotField, ImageMetadata  # noqa: F401
    SQLModel.metadata.drop_all(engine)

# 4. Session Generator
def get_session():
    with Session(engine) as session:
        yield session