import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

class Config:
    # flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'True').lower() in ['true', '1', 'yes']
    
    # api keys (optional - for enhanced data)
    FOOTBALL_API_KEY = os.environ.get('FOOTBALL_API_KEY')
    RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')
    
    # database config
    DATABASE_PATH = 'data/barcarate.db'
    
    # scraping config
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    REQUEST_DELAY = 1.0  # seconds between requests
    TIMEOUT = 10  # request timeout in seconds
    
    # barcelona config
    BARCELONA_SQUAD_URL = 'https://www.laliga.com/en-GB/clubs/fc-barcelona/squad'
    LALIGA_PLAYERS_URL = 'https://www.laliga.com/en-GB/players'
    FBREF_LALIGA_URL = 'https://fbref.com/en/comps/12/stats/La-Liga-Stats'
    
    # rating weights
    PERFORMANCE_WEIGHT = 0.30
    VALUE_WEIGHT = 0.25  
    TACTICAL_FIT_WEIGHT = 0.20
    AGE_POTENTIAL_WEIGHT = 0.15
    SQUAD_ROLE_WEIGHT = 0.10
    
    # position mappings
    POSITION_GROUPS = {
        'gk': ['goalkeeper', 'gk'],
        'def': ['centre-back', 'cb', 'left-back', 'lb', 'right-back', 'rb', 'defender', 'def'],
        'mid': ['defensive midfield', 'dm', 'central midfield', 'cm', 'attacking midfield', 'am', 'midfielder', 'mid'],
        'att': ['left winger', 'lw', 'right winger', 'rw', 'centre-forward', 'cf', 'striker', 'st', 'forward', 'att']
    }
    
    # barcelona tactical preferences (simplified)
    BARCA_STYLE = {
        'passing_importance': 0.9,
        'dribbling_importance': 0.8,
        'technical_skills': 0.9,
        'pace_importance': 0.6,
        'physicality_importance': 0.4
    }