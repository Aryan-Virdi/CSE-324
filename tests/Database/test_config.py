from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Add the missing fields so Pydantic knows to expect them
    database_url: str
    db_user: str
    db_password: str
    db_name: str
    
    # Use the modern ConfigDict (fixes your deprecation warning too)
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  
    )

def test_settings_load():
    settings = Settings()
    assert settings.database_url.startswith("postgresql://")
    # assert settings.db_user == "admin"

