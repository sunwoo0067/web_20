import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost:3306/ownerclan_dashboard?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    OWNERCLAN_API_URL = "https://api.ownerclan.com/v1"
    OWNERCLAN_AUTH_URL = "https://auth.ownerclan.com/auth"
    OWNERCLAN_USERNAME = os.getenv('OWNERCLAN_USERNAME', 'b00679540')
    OWNERCLAN_PASSWORD = os.getenv('OWNERCLAN_PASSWORD', 'ehdgod1101*')