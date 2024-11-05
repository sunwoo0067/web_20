from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ownerclan Manager"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Ownerclan API 설정
    OWNERCLAN_API_URL: str = os.getenv("OWNERCLAN_API_URL", "https://api-sandbox.ownerclan.com/v1/graphql")
    OWNERCLAN_USERNAME: str = os.getenv("OWNERCLAN_USERNAME", "b00679540")
    OWNERCLAN_PASSWORD: str = os.getenv("OWNERCLAN_PASSWORD", "ehdgod1101*")
    
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    class Config:
        case_sensitive = True

settings = Settings()