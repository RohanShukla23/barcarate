from fuzzywuzzy import fuzz
from src.database import get_laliga_players

def fuzzy_search_players(query, limit=10):
    """fuzzy search for la liga players with autocomplete"""
    players = get_laliga_players()
    
    # calculate similarity scores
    scored_players = []
    for player in players:
        # check name similarity
        name_score = fuzz.partial_ratio(query.lower(), player['name'].lower())
        
        # boost score if query matches start of name
        if player['name'].lower().startswith(query.lower()):
            name_score += 20
        
        # only include players with decent similarity
        if name_score >= 50:
            player['similarity'] = name_score
            scored_players.append(player)
    
    # sort by similarity score
    scored_players.sort(key=lambda x: x['similarity'], reverse=True)
    
    return scored_players[:limit]

def format_currency(amount):
    """format currency values"""
    if amount >= 1000:
        return f"€{amount/1000:.1f}M"
    else:
        return f"€{amount}M"

def format_position(position):
    """standardize position display"""
    position_map = {
        'gk': 'Goalkeeper',
        'cb': 'Centre-Back', 
        'lb': 'Left-Back',
        'rb': 'Right-Back',
        'dm': 'Defensive Midfielder',
        'cm': 'Central Midfielder',
        'am': 'Attacking Midfielder',
        'lw': 'Left Winger',
        'rw': 'Right Winger',
        'st': 'Striker',
        'cf': 'Centre-Forward'
    }
    
    return position_map.get(position.lower(), position.title())

def calculate_age_from_birth_date(birth_date):
    """calculate current age from birth date"""
    from datetime import datetime
    
    if not birth_date:
        return None
    
    try:
        birth = datetime.strptime(birth_date, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return age
    except:
        return None

def clean_player_name(name):
    """clean and standardize player names"""
    if not name:
        return ""
    
    # remove extra whitespace
    name = " ".join(name.split())
    
    # standardize common name variations
    replacements = {
        'Jr.': 'Jr',
        'Sr.': 'Sr',
    }
    
    for old, new in replacements.items():
        name = name.replace(old, new)
    
    return name.strip()

def get_team_color(team_name):
    """get team colors for ui styling"""
    colors = {
        'FC Barcelona': '#004D98',
        'Real Madrid': '#FEBE10',
        'Atlético Madrid': '#CE1126',
        'Athletic Bilbao': '#EE2523',
        'Real Sociedad': '#0066CC',
        'Valencia': '#FF7F00',
        'Villarreal': '#FFFF00',
        'Sevilla': '#D90B0B',
        'Real Betis': '#00A652',
        'Celta Vigo': '#87CEEB'
    }
    
    return colors.get(team_name, '#333333')

def validate_player_data(player_data):
    """validate player data structure"""
    required_fields = ['name', 'team', 'position']
    
    for field in required_fields:
        if field not in player_data or not player_data[field]:
            return False, f"missing required field: {field}"
    
    # validate age
    age = player_data.get('age')
    if age and (not isinstance(age, int) or age < 16 or age > 45):
        return False, "invalid age value"
    
    # validate market value
    market_value = player_data.get('market_value')
    if market_value and (not isinstance(market_value, (int, float)) or market_value < 0):
        return False, "invalid market value"
    
    return True, "valid"

def calculate_rating_stars(rating):
    """convert numeric rating to star display"""
    full_stars = int(rating)
    half_star = 1 if rating % 1 >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    return "★" * full_stars + ("☆" if half_star else "") + "☆" * empty_stars

def safe_divide(numerator, denominator, default=0):
    """safe division with default value"""
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ZeroDivisionError):
        return default

def normalize_stat(value, min_val, max_val):
    """normalize a stat to 0-1 range"""
    if max_val == min_val:
        return 0.5
    
    return max(0, min(1, (value - min_val) / (max_val - min_val)))