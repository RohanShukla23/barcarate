from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
from typing import Dict, List, Any, Tuple
import math
import random
from datetime import datetime
from players_database import CURRENT_SQUAD, LA_LIGA_PLAYERS, get_players_by_team
import unicodedata

app = Flask(__name__, static_folder='.')
CORS(app)

def normalize_string(text: str) -> str:
    """
    Normalize string by removing accents and converting to lowercase
    """
    if not text:
        return ""
    
    # Normalize unicode characters and remove accents
    normalized = unicodedata.normalize('NFD', text)
    # Filter out combining characters (accents)
    ascii_text = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    return ascii_text.lower()

class TransferAnalyzer:
    def __init__(self):
        # Updated analysis factors with more stringent weightings
        self.analysis_factors = {
            'age': {'weight': 0.25, 'optimal_range': (19, 26), 'peak_range': (21, 24)},
            'rating': {'weight': 0.20, 'threshold': 82},  # Raised threshold
            'value': {'weight': 0.20, 'efficiency_threshold': 800000},  # More stringent value requirement
            'position_need': {'weight': 0.25},  # Increased weight for position need
            'potential': {'weight': 0.10}
        }
        
        # Maximum possible rating is now 9.5 (no perfect 10s)
        self.max_rating = 9.5
        
        # Financial risk thresholds
        self.financial_risk_thresholds = {
            'high_risk': 80000000,    # 80M+ is high financial risk
            'medium_risk': 40000000,  # 40-80M is medium risk
            'low_risk': 20000000      # Under 20M is low risk
        }
    
    def check_existing_player(self, player_name: str) -> bool:
        """Check if player is already in Barcelona squad"""
        all_barca_players = []
        for position_group in CURRENT_SQUAD.values():
            all_barca_players.extend([p["name"].lower() for p in position_group])
        
        return player_name.lower() in all_barca_players
    
    def analyze_squad_weaknesses(self) -> List[str]:
        """Enhanced squad analysis with more detailed position tracking"""
        weaknesses = []
        
        # Goalkeeper analysis - stricter requirements
        goalkeepers = CURRENT_SQUAD["goalkeepers"]
        young_gks = [gk for gk in goalkeepers if gk["age"] < 30 and gk["rating"] >= 80]
        if len(young_gks) < 1:
            weaknesses.append("goalkeeper_quality")
        
        backup_gks = [gk for gk in goalkeepers if gk["age"] < 33 and gk["rating"] >= 75]
        if len(backup_gks) < 2:
            weaknesses.append("goalkeeper_depth")
        
        # Age distribution analysis - more stringent
        all_players = []
        for position_group in CURRENT_SQUAD.values():
            all_players.extend(position_group)
        
        aging_players = [p for p in all_players if p["age"] > 30]
        very_old_players = [p for p in all_players if p["age"] > 33]
        
        if len(aging_players) >= 6:
            weaknesses.append("aging_squad")
        if len(very_old_players) >= 3:
            weaknesses.append("critical_aging")
        
        # Position-specific depth analysis with higher standards
        forwards = CURRENT_SQUAD["forwards"]
        strikers = [p for p in forwards if p["position"] == "ST" and p["age"] < 35]
        wingers = [p for p in forwards if p["position"] in ["LW", "RW"] and p["age"] < 30]
        
        defenders = CURRENT_SQUAD["defenders"]
        center_backs = [p for p in defenders if p["position"] == "CB"]
        fullbacks = [p for p in defenders if p["position"] in ["LB", "RB"] and p["age"] < 29]
        
        midfielders = CURRENT_SQUAD["midfielders"]
        defensive_mids = [p for p in midfielders if p["position"] == "DM"]
        creative_mids = [p for p in midfielders if p["position"] == "AM" and p["age"] < 28]
        
        # Striker depth analysis
        if len(strikers) < 2:
            weaknesses.append("striker_depth")
        elif len(strikers) == 2 and any(s["age"] > 35 for s in strikers):
            weaknesses.append("striker_aging")
        
        # Center back depth - need quality and depth
        young_cbs = [cb for cb in center_backs if cb["age"] < 27 and cb["rating"] >= 78]
        if len(center_backs) < 4:
            weaknesses.append("cb_depth")
        if len(young_cbs) < 2:
            weaknesses.append("cb_future")
        
        # Defensive midfield - critical position
        if len(defensive_mids) < 2:
            weaknesses.append("dm_depth")
        
        quality_dms = [dm for dm in defensive_mids if dm["rating"] >= 80]
        if len(quality_dms) < 1:
            weaknesses.append("dm_quality")
        
        # Fullback depth
        if len(fullbacks) < 3:
            weaknesses.append("fullback_depth")
        
        # Quality thresholds by position group
        avg_ratings = {}
        for pos_name, players in CURRENT_SQUAD.items():
            if players:
                avg_ratings[pos_name] = sum(p["rating"] for p in players) / len(players)
        
        if avg_ratings.get("defenders", 0) < 78:
            weaknesses.append("defensive_quality")
        if avg_ratings.get("midfielders", 0) < 80:
            weaknesses.append("midfield_quality")
        
        return weaknesses
    
    def calculate_position_redundancy(self, player_position: str, player_age: int) -> Tuple[float, str]:
        """More balanced position redundancy calculation"""
        position_players = []
        for pos_group in CURRENT_SQUAD.values():
            position_players.extend([p for p in pos_group if p["position"] == player_position])
        
        # Count by age groups
        young_players = [p for p in position_players if p["age"] < 25]
        prime_players = [p for p in position_players if 25 <= p["age"] < 30]
        veteran_players = [p for p in position_players if p["age"] >= 30]
        
        total_at_position = len(position_players)
        redundancy_penalty = 0.0
        redundancy_desc = ""
        
        # Position-specific redundancy rules (less harsh)
        if player_position == "ST":
            if total_at_position >= 3:
                redundancy_penalty = -0.8  # Reduced from -1.5
                redundancy_desc = "striker position well-stocked"
            elif total_at_position == 2 and player_age > 30:
                redundancy_penalty = -0.4  # Reduced from -0.8
                redundancy_desc = "aging striker depth consideration"
        
        elif player_position in ["LW", "RW"]:
            if total_at_position >= 4:
                redundancy_penalty = -1.2  # Reduced from -2.0
                redundancy_desc = f"{player_position} position overcrowded"
            elif total_at_position >= 3:
                redundancy_penalty = -0.6  # Reduced from -1.0
                redundancy_desc = f"good {player_position} depth already"
        
        elif player_position == "AM":
            if total_at_position >= 3:
                redundancy_penalty = -0.8  # Reduced from -1.5
                redundancy_desc = "attacking midfield well-supplied"
            elif total_at_position >= 2 and player_age > 28:
                redundancy_penalty = -0.4  # Reduced from -0.8
                redundancy_desc = "sufficient attacking midfield options"
        
        elif player_position == "CM":
            if total_at_position >= 5:
                redundancy_penalty = -0.5  # Reduced from -1.0
                redundancy_desc = "central midfield well-stocked"
        
        elif player_position == "CB":
            if total_at_position >= 5:
                redundancy_penalty = -0.4  # Reduced from -0.8
                redundancy_desc = "center back depth adequate"
        
        elif player_position in ["LB", "RB"]:
            if total_at_position >= 3:
                redundancy_penalty = -0.6  # Reduced from -1.2
                redundancy_desc = f"sufficient {player_position} coverage"
        
        elif player_position == "DM":
            if total_at_position >= 3:
                redundancy_penalty = -0.3  # Reduced from -0.5
                redundancy_desc = "defensive midfield depth adequate"
        
        elif player_position == "GK":
            if total_at_position >= 3:
                redundancy_penalty = -1.5  # Reduced from -2.0
                redundancy_desc = "goalkeeper position full"
        
        return redundancy_penalty, redundancy_desc
    
    def calculate_position_need_score(self, player_position: str, player_age: int, weaknesses: List[str]) -> Tuple[float, str]:
        """Enhanced position need calculation"""
        # Base need scores
        position_needs = {
            "GK": {"base_score": 0.5, "urgent_weaknesses": ["goalkeeper_quality", "goalkeeper_depth"]},
            "CB": {"base_score": 1.0, "urgent_weaknesses": ["cb_depth", "cb_future", "defensive_quality"]},
            "LB": {"base_score": 0.8, "urgent_weaknesses": ["fullback_depth"]},
            "RB": {"base_score": 0.8, "urgent_weaknesses": ["fullback_depth"]},
            "DM": {"base_score": 1.5, "urgent_weaknesses": ["dm_depth", "dm_quality"]},
            "CM": {"base_score": 0.3, "urgent_weaknesses": ["midfield_quality"]},
            "AM": {"base_score": 0.0, "urgent_weaknesses": []},  # We have plenty
            "LW": {"base_score": -0.5, "urgent_weaknesses": []},  # Overcrowded
            "RW": {"base_score": -0.5, "urgent_weaknesses": []},  # Overcrowded
            "ST": {"base_score": 1.2, "urgent_weaknesses": ["striker_depth", "striker_aging"]}
        }
        
        need_info = position_needs.get(player_position, {"base_score": 0.0, "urgent_weaknesses": []})
        need_score = need_info["base_score"]
        
        # Check for urgent weaknesses
        urgent_need_bonus = 0.0
        for weakness in need_info["urgent_weaknesses"]:
            if weakness in weaknesses:
                urgent_need_bonus += 0.8
        
        # Age-based adjustments for need
        age_adjustment = 0.0
        if player_age < 22:
            age_adjustment = 0.3  # Young talent bonus
        elif player_age > 30:
            age_adjustment = -0.5  # Don't need aging players unless critical
        elif player_age > 33:
            age_adjustment = -1.2  # Strong penalty for very old players
        
        # Check for redundancy
        redundancy_penalty, redundancy_desc = self.calculate_position_redundancy(player_position, player_age)
        
        final_score = need_score + urgent_need_bonus + age_adjustment + redundancy_penalty
        
        # Generate description
        if final_score >= 1.5:
            desc = f"critical need at {player_position}"
        elif final_score >= 0.8:
            desc = f"beneficial addition at {player_position}"
        elif final_score >= 0.0:
            desc = f"moderate value at {player_position}"
        elif final_score >= -0.5:
            desc = f"limited need at {player_position}"
        else:
            if redundancy_desc:
                desc = redundancy_desc
            else:
                desc = f"surplus at {player_position}"
        
        return final_score, desc
    
    def analyze_player_age_impact(self, player: Dict) -> Tuple[float, str]:
        """Balanced age analysis - rewarding exceptional talents appropriately"""
        age = player["age"]
        rating = player["rating"]
        
        # Exceptional young talents (under 20 with high rating)
        if age <= 19:
            if rating >= 85:
                return 3.0, "generational talent - incredible potential"
            elif rating >= 80:
                return 2.5, "exceptional young prospect"
            elif rating >= 75:
                return 2.0, "promising youth with high potential"
            else:
                return 1.2, "developing talent for the future"
        
        # Prime development age (20-24)
        elif age <= 24:
            if rating >= 90:
                return 2.8, "world-class superstar in prime development"
            elif rating >= 87:
                return 2.4, "elite talent entering absolute peak"
            elif rating >= 84:
                return 2.0, "top-tier player in development phase"
            elif rating >= 81:
                return 1.6, "high-quality player approaching prime"
            elif rating >= 78:
                return 1.2, "solid prospect with room to grow"
            else:
                return 0.5, "average young player"
        
        # Peak years (25-28)
        elif age <= 28:
            if rating >= 90:
                return 2.2, "world-class player in absolute prime"
            elif rating >= 87:
                return 1.8, "elite performer at peak"
            elif rating >= 84:
                return 1.4, "quality player in prime years"
            elif rating >= 80:
                return 0.8, "decent player at peak"
            else:
                return 0.0, "below Barcelona standards even at peak"
        
        # Late peak/early decline (29-31)
        elif age <= 31:
            if rating >= 90:
                return 1.0, "world-class veteran, still excellent"
            elif rating >= 87:
                return 0.6, "elite player with good years remaining"
            elif rating >= 84:
                return 0.2, "quality player with some aging concerns"
            else:
                return -0.6, "aging player below required standard"
        
        # Clear decline phase (32-34)
        elif age <= 34:
            if rating >= 90:
                return 0.2, "legendary player but age concerns"
            elif rating >= 87:
                return -0.4, "elite veteran with decline risk"
            elif rating >= 84:
                return -1.0, "aging player, moderate risk investment"
            else:
                return -1.8, "too old and not elite enough"
        
        # Very old (35+)
        else:
            if rating >= 90:
                return -0.5, "world-class but short-term option"
            elif rating >= 87:
                return -1.2, "elite but risky due to age"
            else:
                return -2.5, "too old for Barcelona's standards"
    
    def calculate_financial_risk(self, player: Dict) -> Tuple[float, str]:
        """Balanced financial risk assessment"""
        value = player["value"]
        rating = player["rating"]
        age = player["age"]
        
        if value == 0:
            return 2.5, "free transfer - exceptional financial value"
        
        # Risk categories based on transfer fee - more balanced
        if value >= self.financial_risk_thresholds['high_risk']:
            base_penalty = -1.5
            risk_desc = "major financial investment"
            
            # World-class players justify high fees
            if rating >= 90 and age <= 28:
                base_penalty = 0.0  # No penalty for young superstars
                risk_desc = "premium investment in world-class talent"
            elif rating >= 87 and age <= 26:
                base_penalty = -0.3
                risk_desc = "substantial but justified investment in elite talent"
            elif rating >= 84 and age <= 24:
                base_penalty = -0.6
                risk_desc = "significant investment in high-potential player"
        
        elif value >= self.financial_risk_thresholds['medium_risk']:
            base_penalty = -0.6
            risk_desc = "moderate financial commitment"
            
            if rating >= 87 and age <= 30:
                base_penalty = 0.2
                risk_desc = "solid investment for elite quality"
            elif rating >= 84 and age <= 28:
                base_penalty = 0.0
                risk_desc = "reasonable investment for proven quality"
            elif rating >= 80 and age <= 25:
                base_penalty = -0.2
                risk_desc = "fair investment in developing talent"
        
        elif value >= self.financial_risk_thresholds['low_risk']:
            base_penalty = -0.1
            risk_desc = "reasonable financial commitment"
            
            if rating >= 82:
                base_penalty = 0.6
                risk_desc = "excellent value for proven quality"
            elif rating >= 78:
                base_penalty = 0.3
                risk_desc = "good value for solid quality"
        
        else:
            # Under 20M
            base_penalty = 1.0
            risk_desc = "low financial risk"
            
            if rating >= 82:
                base_penalty = 1.5
                risk_desc = "outstanding value for money"
            elif rating >= 78:
                base_penalty = 1.2
                risk_desc = "excellent budget signing"
        
        # Age-based financial risk adjustments (less harsh)
        if age > 33:
            base_penalty -= 0.6
            if "premium" not in risk_desc and "substantial" not in risk_desc:
                risk_desc += " with age concerns"
        elif age > 30:
            base_penalty -= 0.3
        
        # Rating vs value efficiency
        if value > 0:
            value_per_rating = value / max(rating, 1)
            if value_per_rating > 1200000:  # More than 1.2M per rating point
                base_penalty -= 0.3
                if "excellent" in risk_desc or "outstanding" in risk_desc:
                    risk_desc = "overpriced for quality level"
        
        return base_penalty, risk_desc
    
    def calculate_special_factors(self, player: Dict) -> Tuple[float, str]:
        """Enhanced special factors calculation"""
        special_score = 0.0
        special_factors = []
        
        # Rival bonus/penalty
        team = player.get("team", "")
        if "Real Madrid" in team:
            special_score += 1.2
            special_factors.append("significant blow to El Clasico rivals")
        elif "Atletico" in team:
            special_score += 0.8
            special_factors.append("weakens direct La Liga competitor")
        elif team in ["Sevilla FC", "Real Sociedad", "Athletic Bilbao", "Villarreal CF"]:
            special_score += 0.3
            special_factors.append("proven quality in competitive La Liga environment")
        
        # La Liga experience bonus
        if team != "FC Barcelona" and any(team in player.get("team", "") for team in ["Real Madrid", "Atletico", "Sevilla", "Villarreal", "Real Sociedad", "Athletic Bilbao"]):
            special_score += 0.4
            special_factors.append("valuable La Liga adaptation advantage")
        
        # Age and potential combination
        age = player["age"]
        rating = player["rating"]
        
        # Exceptional young talent bonus
        if age < 21 and rating >= 80:
            special_score += 0.8
            special_factors.append("rare combination of youth and proven ability")
        
        # Versatility bonus (players who can play multiple positions effectively)
        position = player["position"]
        if position in ["CB"] and rating >= 80:
            special_score += 0.2  # Center backs with leadership qualities
        
        # Market value considerations
        if player["value"] > 100000000:  # 100M+ signings
            special_score -= 0.5  # Penalty for galactico signings due to pressure
            special_factors.append("enormous expectation and pressure burden")
        
        return special_score, special_factors
    
    def generate_detailed_analysis(self, player: Dict, weaknesses: List[str]) -> Dict[str, Any]:
        """Enhanced analysis with stricter rating system"""
        
        # Check if player is already at Barcelona
        if self.check_existing_player(player["name"]):
            return {
                "error": True,
                "message": f"{player['name']} is already playing for FC Barcelona! Please search for a different player.",
                "rating": 0.0,
                "recommendation": "Invalid Transfer",
                "recommendation_desc": "Cannot transfer a player who is already in the squad"
            }
        
        # Base quality assessment with balanced standards
        quality_score = 0.0
        quality_notes = []
        
        rating = player["rating"]
        if rating >= 90:
            quality_score = 4.2  # Increased for superstars
            quality_notes.append("world-class elite talent")
        elif rating >= 87:
            quality_score = 3.5  # Increased for top-tier players
            quality_notes.append("exceptional top-tier performer")
        elif rating >= 84:
            quality_score = 2.8  # Increased
            quality_notes.append("high-quality proven player")
        elif rating >= 81:
            quality_score = 2.0  # Increased
            quality_notes.append("solid professional above average")
        elif rating >= 78:
            quality_score = 1.2  # Increased
            quality_notes.append("decent squad player")
        elif rating >= 75:
            quality_score = 0.4  # Less harsh
            quality_notes.append("borderline Barcelona quality")
        else:
            quality_score = -1.0  # Less harsh
            quality_notes.append("below Barcelona's required standards")
        
        # Age impact analysis
        age_score, age_desc = self.analyze_player_age_impact(player)
        
        # Financial risk assessment
        financial_score, financial_desc = self.calculate_financial_risk(player)
        
        # Position need analysis
        position_score, position_desc = self.calculate_position_need_score(
            player["position"], player["age"], weaknesses
        )
        
        # Special factors
        special_score, special_factors = self.calculate_special_factors(player)
        
        # Calculate raw total
        raw_total = quality_score + age_score + financial_score + position_score + special_score
        
        # Apply balanced rating cap and scaling - more generous for top players
        if raw_total >= 7.0:
            final_rating = min(9.5, 8.8 + (raw_total - 7.0) * 0.35)  # Easier to reach high ratings
        elif raw_total >= 5.0:
            final_rating = 7.5 + (raw_total - 5.0) * 0.65  # More generous scaling
        elif raw_total >= 3.0:
            final_rating = 6.0 + (raw_total - 3.0) * 0.75
        elif raw_total >= 1.0:
            final_rating = 4.5 + (raw_total - 1.0) * 0.75
        elif raw_total >= 0.0:
            final_rating = 3.5 + (raw_total * 1.0)
        else:
            final_rating = max(1.0, 3.5 + raw_total * 0.7)
        
        final_rating = round(final_rating, 1)
        
        # Generate comprehensive explanation
        explanation_parts = []
        explanation_parts.append(f"Quality assessment: {quality_notes[0]}")
        explanation_parts.append(f"Age factor: {age_desc}")
        explanation_parts.append(f"Financial aspect: {financial_desc}")
        explanation_parts.append(f"Positional need: {position_desc}")
        
        if special_factors:
            explanation_parts.extend(special_factors)
        
        # Enhanced risk assessment
        risk_factors = []
        
        # Age-related risks
        if player["age"] > 32:
            risk_factors.append("significant age-related decline risk")
        elif player["age"] > 29:
            risk_factors.append("approaching decline phase")
        
        # Financial risks
        if player["value"] > 80000000:
            risk_factors.append("massive financial commitment with pressure")
        elif player["value"] > 50000000:
            risk_factors.append("substantial financial investment required")
        
        # Performance risks
        if player.get("team") == "Real Madrid":
            risk_factors.append("complex and potentially hostile negotiation")
        
        # Position-specific risks
        redundancy_penalty, _ = self.calculate_position_redundancy(player["position"], player["age"])
        if redundancy_penalty < -0.5:
            risk_factors.append("position may become overcrowded")
        
        # Adaptation risks for non-La Liga players
        if player.get("team") and not any(la_liga_team in player["team"] for la_liga_team in ["Real Madrid", "Barcelona", "Atletico", "Sevilla", "Valencia", "Villarreal", "Real Sociedad", "Athletic Bilbao", "Real Betis", "Celta", "Getafe", "Osasuna", "Las Palmas", "Rayo", "Mallorca", "Girona", "Alaves", "Espanyol", "Leganes", "Valladolid"]):
            risk_factors.append("adaptation to La Liga style and pace required")
        
        # Final recommendation with balanced thresholds
        if final_rating >= 9.0:
            recommendation = "Dream Signing"
            recommendation_desc = "Exceptional talent that would transform the squad"
        elif final_rating >= 8.5:
            recommendation = "Excellent Target"
            recommendation_desc = "Outstanding signing addressing key needs perfectly"
        elif final_rating >= 8.0:
            recommendation = "Highly Recommended"
            recommendation_desc = "Top-quality addition with significant impact"
        elif final_rating >= 7.0:
            recommendation = "Recommended"
            recommendation_desc = "Good signing with clear benefits"
        elif final_rating >= 6.0:
            recommendation = "Consider Carefully"
            recommendation_desc = "Decent option with some limitations"
        elif final_rating >= 4.5:
            recommendation = "Questionable"
            recommendation_desc = "Limited improvement with notable concerns"
        else:
            recommendation = "Not Recommended"
            recommendation_desc = "Does not meet Barcelona's standards or needs"
        
        return {
            "rating": final_rating,
            "recommendation": recommendation,
            "recommendation_desc": recommendation_desc,
            "explanation": ". ".join(explanation_parts),
            "risk_factors": risk_factors,
            "breakdown": {
                "quality": round(quality_score, 1),
                "age_impact": round(age_score, 1),
                "financial_risk": round(financial_score, 1),
                "position_need": round(position_score, 1),
                "special_factors": round(special_score, 1),
                "raw_total": round(raw_total, 1)
            },
            "error": False
        }

# Initialize analyzer
analyzer = TransferAnalyzer()

@app.route('/api/squad')
def get_squad():
    """Get current Barcelona squad"""
    return jsonify(CURRENT_SQUAD)

@app.route('/api/players/search')
def search_players():
    """Search La Liga players for transfers with advanced filtering and accent-insensitive search"""
    query = request.args.get('q', '').lower()
    position = request.args.get('position', '').upper()
    team = request.args.get('team', '')
    min_rating = int(request.args.get('min_rating', 0))
    max_age = int(request.args.get('max_age', 50))
    max_value = int(request.args.get('max_value', 999999999))
    
    filtered_players = LA_LIGA_PLAYERS.copy()
    
    # Apply filters with accent-insensitive search for names
    if query:
        normalized_query = normalize_string(query)
        filtered_players = [
            p for p in filtered_players 
            if normalized_query in normalize_string(p["name"])
        ]
    
    if position:
        filtered_players = [p for p in filtered_players if p["position"] == position]
    
    if team:
        filtered_players = [p for p in filtered_players if team.lower() in p["team"].lower()]
    
    if min_rating > 0:
        filtered_players = [p for p in filtered_players if p["rating"] >= min_rating]
    
    if max_age < 50:
        filtered_players = [p for p in filtered_players if p["age"] <= max_age]
    
    if max_value < 999999999:
        filtered_players = [p for p in filtered_players if p["value"] <= max_value]
    
    # Sort by rating descending
    filtered_players.sort(key=lambda x: x["rating"], reverse=True)
    
    # Limit results to prevent overwhelming the UI
    return jsonify(filtered_players[:30])

@app.route('/api/players/by-team/<team_name>')
def get_players_by_team_route(team_name):
    """Get all players from a specific team"""
    players = get_players_by_team(team_name)
    return jsonify(players)

@app.route('/api/transfer/rate', methods=['POST'])
def rate_transfer():
    """Rate a potential transfer with detailed analysis"""
    player_data = request.get_json()
    
    if not player_data:
        return jsonify({"error": "Player data required"}), 400
    
    weaknesses = analyzer.analyze_squad_weaknesses()
    analysis = analyzer.generate_detailed_analysis(player_data, weaknesses)
    
    # If there's an error (like existing player), return it
    if analysis.get("error"):
        return jsonify(analysis), 400
    
    return jsonify({
        "player": player_data,
        "analysis": analysis,
        "squad_weaknesses": weaknesses,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/squad/analysis')
def squad_analysis():
    """Get comprehensive squad analysis"""
    weaknesses = analyzer.analyze_squad_weaknesses()
    
    # Enhanced weakness descriptions
    weakness_descriptions = {
        "goalkeeper_quality": "Lack of elite young goalkeeper for the future",
        "goalkeeper_depth": "Insufficient backup goalkeeper options",
        "aging_squad": "Too many players over 30 requiring succession planning",
        "critical_aging": "Multiple players in decline phase (33+)",
        "striker_depth": "Heavy reliance on aging Lewandowski with limited alternatives",
        "striker_aging": "Current striker options approaching end of prime years",
        "cb_depth": "Insufficient center-back depth for European competition",
        "cb_future": "Lack of young center-backs for long-term planning",
        "dm_depth": "Limited defensive midfield protection options",
        "dm_quality": "Need for elite defensive midfielder to control games",
        "fullback_depth": "Insufficient depth at fullback positions",
        "defensive_quality": "Below-standard average rating in defensive positions",
        "midfield_quality": "Midfield lacks consistent quality across all players"
    }
    
    # Calculate additional squad metrics
    all_players = []
    for pos_group in CURRENT_SQUAD.values():
        all_players.extend(pos_group)
    
    total_value = sum(p["value"] for p in all_players)
    avg_rating = sum(p["rating"] for p in all_players) / len(all_players)
    avg_age = sum(p["age"] for p in all_players) / len(all_players)
    
    # Age distribution
    young_players = [p for p in all_players if p["age"] < 23]
    prime_players = [p for p in all_players if 23 <= p["age"] < 30]
    veteran_players = [p for p in all_players if p["age"] >= 30]
    
    # Position distribution
    position_count = {}
    for player in all_players:
        pos = player["position"]
        position_count[pos] = position_count.get(pos, 0) + 1
    
    # Squad strength assessment with higher standards
    if avg_rating >= 85:
        squad_strength = "world-class"
    elif avg_rating >= 82:
        squad_strength = "excellent"
    elif avg_rating >= 79:
        squad_strength = "good"
    elif avg_rating >= 76:
        squad_strength = "average"
    else:
        squad_strength = "below standard"
    
    return jsonify({
        "weaknesses": weaknesses,
        "descriptions": {w: weakness_descriptions.get(w, w) for w in weaknesses},
        "metrics": {
            "total_players": len(all_players),
            "total_value": total_value,
            "average_rating": round(avg_rating, 1),
            "average_age": round(avg_age, 1),
            "young_players": len(young_players),
            "prime_players": len(prime_players),
            "veteran_players": len(veteran_players),
            "position_distribution": position_count
        },
        "squad_strength": squad_strength,
        "priority_positions": get_priority_transfer_positions(weaknesses)
    })

def get_priority_transfer_positions(weaknesses: List[str]) -> List[str]:
    """Get priority positions for transfers based on weaknesses"""
    priorities = []
    
    if "dm_quality" in weaknesses or "dm_depth" in weaknesses:
        priorities.append("DM - Defensive Midfielder")
    
    if "striker_depth" in weaknesses or "striker_aging" in weaknesses:
        priorities.append("ST - Striker")
    
    if "cb_depth" in weaknesses or "cb_future" in weaknesses:
        priorities.append("CB - Center Back")
    
    if "fullback_depth" in weaknesses:
        priorities.append("LB/RB - Fullbacks")
    
    if "goalkeeper_quality" in weaknesses:
        priorities.append("GK - Goalkeeper")
    
    return priorities

@app.route('/api/teams')
def get_teams():
    """Get list of all La Liga teams"""
    teams = list(set(player["team"] for player in LA_LIGA_PLAYERS))
    teams.sort()
    return jsonify(teams)

# Serve frontend from frontend directory
@app.route('/')
def serve_frontend():
    return send_from_directory('frontend', 'index.html')

@app.route('/styles/<path:path>')
def serve_styles(path):
    return send_from_directory('frontend/styles', path)

@app.route('/js/<path:path>')
def serve_js(path):
    return send_from_directory('frontend/js', path)

@app.route('/<path:path>')
def serve_static(path):
    # Try frontend directory first, fall back to root
    try:
        return send_from_directory('frontend', path)
    except:
        return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)