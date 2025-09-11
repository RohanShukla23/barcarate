import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

def get_api_headers():
    """get headers for api-football requests"""
    return {
        "X-RapidAPI-Key": os.getenv('API_FOOTBALL_KEY'),
        "X-RapidAPI-Host": os.getenv('API_FOOTBALL_HOST', 'api-football-v1.p.rapidapi.com')
    }

def safe_request(url, params=None, max_retries=3):
    """make api request with error handling and rate limiting"""
    headers = get_api_headers()
    
    if not headers["X-RapidAPI-Key"]:
        print("api key not found. check your .env file")
        return None
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                # rate limit hit
                print(f"rate limit hit, waiting 60 seconds... (attempt {attempt + 1})")
                time.sleep(60)
                continue
            else:
                print(f"api error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"request failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            return None
    
    print(f"failed after {max_retries} attempts")
    return None

def format_player_name(name):
    """standardize player name formatting"""
    if not name:
        return ""
    return name.strip().title()

def parse_height(height_str):
    """convert height string to cm integer"""
    if not height_str or height_str == '0cm':
        return 0
    try:
        # extract number from string like "180cm"
        return int(''.join(filter(str.isdigit, height_str)))
    except:
        return 0

def parse_weight(weight_str):
    """convert weight string to kg integer"""
    if not weight_str or weight_str == '0kg':
        return 0
    try:
        # extract number from string like "75kg"  
        return int(''.join(filter(str.isdigit, weight_str)))
    except:
        return 0

def calculate_age_category(age):
    """categorize player by age"""
    if age < 21:
        return "young"
    elif age <= 27:
        return "prime"
    elif age <= 32:
        return "experienced"
    else:
        return "veteran"

def normalize_position(position):
    """normalize position names to standard format"""
    position_mapping = {
        'GK': 'Goalkeeper',
        'CB': 'Centre-Back',
        'LB': 'Left-Back', 
        'RB': 'Right-Back',
        'LWB': 'Left Wing-Back',
        'RWB': 'Right Wing-Back',
        'DM': 'Defensive Midfield',
        'CM': 'Central Midfield',
        'AM': 'Attacking Midfield',
        'LM': 'Left Midfield',
        'RM': 'Right Midfield',
        'LW': 'Left Winger',
        'RW': 'Right Winger',
        'ST': 'Centre-Forward',
        'CF': 'Centre-Forward',
        'LF': 'Left Forward',
        'RF': 'Right Forward'
    }
    
    return position_mapping.get(position, position)

def get_player_market_value_estimate(player):
    """rough estimate of player market value based on stats"""
    age = player.get('age', 25)
    rating = player.get('rating', 6.0)
    games = player.get('games_played', 0)
    goals = player.get('goals', 0)
    assists = player.get('assists', 0)
    
    # base value from rating
    base_value = max(0, (rating - 5.0) * 10)  # 0-30M range
    
    # age adjustment
    if age <= 23:
        age_multiplier = 1.3
    elif age <= 27:
        age_multiplier = 1.0
    elif age <= 30:
        age_multiplier = 0.8
    else:
        age_multiplier = 0.5
    
    # performance bonus
    if games > 20:
        performance_bonus = min(10, (goals + assists) * 0.5)
    else:
        performance_bonus = 0
    
    estimated_value = (base_value * age_multiplier) + performance_bonus
    
    return max(1, min(100, estimated_value))  # cap between 1-100M

def format_currency(amount):
    """format currency amount"""
    if amount >= 1000:
        return f"€{amount/1000:.1f}M"
    else:
        return f"€{amount:.1f}M"