from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
from typing import Dict, List, Any, Tuple
import math
import random
from datetime import datetime
from players_database import CURRENT_SQUAD, LA_LIGA_PLAYERS, get_players_by_team

app = Flask(__name__, static_folder='frontend/dist')
CORS(app)

class TransferAnalyzer:
    def __init__(self):
        self.analysis_factors = {
            'age': {'weight': 0.20, 'optimal_range': (21, 28)},
            'rating': {'weight': 0.30, 'threshold': 80},
            'value': {'weight': 0.15, 'efficiency_threshold': 1500000},
            'position_need': {'weight': 0.20},
            'potential': {'weight': 0.15}
        }
    
    def analyze_squad_weaknesses(self) -> List[str]:
        """Advanced squad analysis to identify specific weaknesses"""
        weaknesses = []
        
        # Goalkeeper analysis
        goalkeepers = CURRENT_SQUAD["goalkeepers"]
        active_gks = [gk for gk in goalkeepers if gk["age"] < 35]
        if len(active_gks) < 2:
            weaknesses.append("goalkeeper_depth")
        
        # Age distribution analysis
        all_players = []
        for position_group in CURRENT_SQUAD.values():
            all_players.extend(position_group)
        
        aging_players = [p for p in all_players if p["age"] > 32]
        if len(aging_players) >= 4:
            weaknesses.append("aging_squad")
        
        # Position-specific depth analysis
        strikers = [p for p in CURRENT_SQUAD["forwards"] if p["position"] == "ST"]
        center_backs = [p for p in CURRENT_SQUAD["defenders"] if p["position"] == "CB"]
        defensive_mids = [p for p in CURRENT_SQUAD["midfielders"] if p["position"] == "DM"]
        
        if len(strikers) < 2:
            weaknesses.append("striker_depth")
        if len(center_backs) < 4:
            weaknesses.append("cb_depth")
        if len(defensive_mids) < 2:
            weaknesses.append("dm_depth")
        
        # Quality analysis
        avg_rating_by_position = {}
        for pos_name, players in CURRENT_SQUAD.items():
            if players:
                avg_rating_by_position[pos_name] = sum(p["rating"] for p in players) / len(players)
        
        if avg_rating_by_position.get("defenders", 0) < 80:
            weaknesses.append("defensive_quality")
        
        return weaknesses
    
    def calculate_position_need_score(self, player_position: str, weaknesses: List[str]) -> Tuple[float, str]:
        """Calculate how much the team needs this position"""
        position_needs = {
            "GK": {"weakness": "goalkeeper_depth", "score": 1.5, "desc": "critical goalkeeper shortage"},
            "CB": {"weakness": "cb_depth", "score": 1.2, "desc": "defensive depth required"},
            "DM": {"weakness": "dm_depth", "score": 1.0, "desc": "midfield protection needed"},
            "ST": {"weakness": "striker_depth", "score": 1.8, "desc": "urgent striker backup needed"}
        }
        
        need = position_needs.get(player_position, {"score": 0.0, "desc": "squad rotation option"})
        
        if need.get("weakness") in weaknesses:
            return need["score"], need["desc"]
        
        # General positional needs based on current squad
        current_players_at_position = []
        for pos_group in CURRENT_SQUAD.values():
            current_players_at_position.extend([p for p in pos_group if p["position"] == player_position])
        
        if len(current_players_at_position) < 2:
            return 0.8, f"additional {player_position} depth beneficial"
        elif len(current_players_at_position) >= 3:
            return -0.5, f"surplus at {player_position} position"
        
        return 0.2, "moderate positional value"
    
    def analyze_player_potential(self, player: Dict) -> Tuple[float, str]:
        """Analyze player's potential and development trajectory"""
        age = player["age"]
        rating = player["rating"]
        
        if age <= 20:
            if rating >= 75:
                return 2.0, "exceptional young talent with world-class potential"
            elif rating >= 70:
                return 1.5, "promising youngster with significant upside"
            else:
                return 1.0, "developing talent for the future"
        elif age <= 23:
            if rating >= 80:
                return 1.5, "entering peak years with elite ability"
            elif rating >= 75:
                return 1.0, "good prospect approaching prime"
            else:
                return 0.5, "decent young player with room to grow"
        elif age <= 28:
            if rating >= 85:
                return 0.8, "prime years performer"
            else:
                return 0.3, "established player at peak"
        elif age <= 32:
            if rating >= 87:
                return 0.0, "world-class veteran"
            else:
                return -0.3, "aging but experienced"
        else:
            return -1.0, "declining years, short-term solution only"
    
    def calculate_value_efficiency(self, player: Dict) -> Tuple[float, str]:
        """Calculate value for money score"""
        if player["value"] == 0:
            return 1.5, "free transfer - excellent value"
        
        value_per_rating = player["value"] / max(player["rating"], 1)
        
        if value_per_rating < 500000:
            return 2.0, "exceptional value for money"
        elif value_per_rating < 1000000:
            return 1.0, "good value proposition"
        elif value_per_rating < 1500000:
            return 0.0, "fair market price"
        elif value_per_rating < 2500000:
            return -1.0, "expensive for the quality"
        else:
            return -2.0, "overpriced significantly"
    
    def generate_detailed_analysis(self, player: Dict, weaknesses: List[str]) -> Dict[str, Any]:
        """Generate comprehensive transfer analysis"""
        # Base quality assessment
        quality_score = 0.0
        quality_notes = []
        
        if player["rating"] >= 90:
            quality_score = 4.0
            quality_notes.append("world-class talent")
        elif player["rating"] >= 85:
            quality_score = 3.0
            quality_notes.append("top-tier player")
        elif player["rating"] >= 80:
            quality_score = 2.0
            quality_notes.append("high-quality performer")
        elif player["rating"] >= 75:
            quality_score = 1.0
            quality_notes.append("solid professional")
        else:
            quality_score = -1.0
            quality_notes.append("below Barcelona standards")
        
        # Age factor analysis
        age_score, age_desc = self.analyze_player_potential(player)
        
        # Value efficiency
        value_score, value_desc = self.calculate_value_efficiency(player)
        
        # Position need
        position_score, position_desc = self.calculate_position_need_score(player["position"], weaknesses)
        
        # Special factors
        special_bonuses = []
        special_score = 0.0
        
        # Rival bonus
        if player.get("team") == "Real Madrid":
            special_score += 1.0
            special_bonuses.append("weakens El Clásico rivals")
        elif player.get("team") in ["Atlético Madrid", "Real Sociedad"]:
            special_score += 0.5
            special_bonuses.append("strengthens squad against direct competitors")
        
        # Spanish/La Liga adaptation bonus
        if player.get("team") != "FC Barcelona":  # Already in La Liga
            special_score += 0.3
            special_bonuses.append("proven in La Liga environment")
        
        # Calculate final rating
        total_score = quality_score + age_score + value_score + position_score + special_score
        final_rating = max(1.0, min(10.0, 5.0 + total_score))
        
        # Generate detailed explanation
        explanation_parts = []
        explanation_parts.append(f"Quality: {quality_notes[0]}")
        explanation_parts.append(f"Age factor: {age_desc}")
        explanation_parts.append(f"Value: {value_desc}")
        explanation_parts.append(f"Position need: {position_desc}")
        
        if special_bonuses:
            explanation_parts.extend(special_bonuses)
        
        # Risk assessment
        risk_factors = []
        if player["age"] > 30:
            risk_factors.append("age-related decline risk")
        if player["value"] > 80000000:
            risk_factors.append("high financial commitment")
        if player.get("team") == "Real Madrid":
            risk_factors.append("complex negotiation expected")
        
        # Final recommendation
        if final_rating >= 8.0:
            recommendation = "Highly Recommended"
            recommendation_desc = "Excellent signing that significantly improves the squad"
        elif final_rating >= 6.5:
            recommendation = "Recommended"
            recommendation_desc = "Good addition that addresses key needs"
        elif final_rating >= 5.0:
            recommendation = "Consider"
            recommendation_desc = "Decent option with some benefits"
        else:
            recommendation = "Not Recommended"
            recommendation_desc = "Doesn't meet Barcelona's standards or needs"
        
        return {
            "rating": round(final_rating, 1),
            "recommendation": recommendation,
            "recommendation_desc": recommendation_desc,
            "explanation": ". ".join(explanation_parts),
            "risk_factors": risk_factors,
            "breakdown": {
                "quality": round(quality_score, 1),
                "age_potential": round(age_score, 1),
                "value_efficiency": round(value_score, 1),
                "position_need": round(position_score, 1),
                "special_factors": round(special_score, 1)
            }
        }

# Initialize analyzer
analyzer = TransferAnalyzer()

@app.route('/api/squad')
def get_squad():
    """Get current Barcelona squad"""
    return jsonify(CURRENT_SQUAD)

@app.route('/api/players/search')
def search_players():
    """Search La Liga players for transfers with advanced filtering"""
    query = request.args.get('q', '').lower()
    position = request.args.get('position', '').upper()
    team = request.args.get('team', '')
    min_rating = int(request.args.get('min_rating', 0))
    max_age = int(request.args.get('max_age', 50))
    max_value = int(request.args.get('max_value', 999999999))
    
    filtered_players = LA_LIGA_PLAYERS.copy()
    
    # Apply filters
    if query:
        filtered_players = [p for p in filtered_players if query in p["name"].lower()]
    
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
def get_players_by_team(team_name):
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
    
    weakness_descriptions = {
        "goalkeeper_depth": "Critical lack of reliable backup goalkeeper options",
        "aging_squad": "Multiple key players over 32 requiring eventual succession planning",
        "striker_depth": "Heavy reliance on Lewandowski with limited backup options",
        "cb_depth": "Insufficient center-back depth for European competition rotation",
        "dm_depth": "Lack of specialized defensive midfield protection",
        "defensive_quality": "Below-par average rating in defensive positions"
    }
    
    # Calculate additional squad metrics
    all_players = []
    for pos_group in CURRENT_SQUAD.values():
        all_players.extend(pos_group)
    
    total_value = sum(p["value"] for p in all_players)
    avg_rating = sum(p["rating"] for p in all_players) / len(all_players)
    avg_age = sum(p["age"] for p in all_players) / len(all_players)
    
    # Position distribution
    position_count = {}
    for player in all_players:
        pos = player["position"]
        position_count[pos] = position_count.get(pos, 0) + 1
    
    return jsonify({
        "weaknesses": weaknesses,
        "descriptions": {w: weakness_descriptions.get(w, w) for w in weaknesses},
        "metrics": {
            "total_players": len(all_players),
            "total_value": total_value,
            "average_rating": round(avg_rating, 1),
            "average_age": round(avg_age, 1),
            "position_distribution": position_count
        },
        "squad_strength": "excellent" if avg_rating >= 82 else "good" if avg_rating >= 78 else "average"
    })

@app.route('/api/teams')
def get_teams():
    """Get list of all La Liga teams"""
    teams = list(set(player["team"] for player in LA_LIGA_PLAYERS))
    teams.sort()
    return jsonify(teams)

# Serve frontend
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)