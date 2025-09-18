from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
from typing import Dict, List, Any
import math

app = Flask(__name__, static_folder='frontend/dist')
CORS(app)

# current barcelona squad based on the image
CURRENT_SQUAD = {
    "goalkeepers": [
        {"name": "Marc-André ter Stegen", "age": 33, "rating": 85, "value": 12000000, "position": "GK"},
        {"name": "Joan García", "age": 24, "rating": 75, "value": 25000000, "position": "GK"},
        {"name": "Wojciech Szczęsny", "age": 35, "rating": 78, "value": 0, "position": "GK"}
    ],
    "defenders": [
        {"name": "Alejandro Balde", "age": 21, "rating": 82, "value": 50000000, "position": "LB"},
        {"name": "Ronald Araújo", "age": 26, "rating": 85, "value": 70000000, "position": "CB"},
        {"name": "Pau Cubarsi", "age": 18, "rating": 78, "value": 40000000, "position": "CB"},
        {"name": "Andreas Christensen", "age": 29, "rating": 80, "value": 35000000, "position": "CB"},
        {"name": "Gerard Martín", "age": 23, "rating": 70, "value": 15000000, "position": "LB"},
        {"name": "Jules Koundé", "age": 26, "rating": 84, "value": 60000000, "position": "RB"},
        {"name": "Eric García", "age": 24, "rating": 75, "value": 20000000, "position": "CB"}
    ],
    "midfielders": [
        {"name": "Gavi", "age": 21, "rating": 85, "value": 80000000, "position": "CM"},
        {"name": "Pedri", "age": 22, "rating": 88, "value": 100000000, "position": "AM"},
        {"name": "Fermín López", "age": 22, "rating": 78, "value": 35000000, "position": "CM"},
        {"name": "Marc Casadó", "age": 22, "rating": 75, "value": 25000000, "position": "DM"},
        {"name": "Dani Olmo", "age": 27, "rating": 85, "value": 55000000, "position": "AM"},
        {"name": "Frenkie de Jong", "age": 28, "rating": 86, "value": 75000000, "position": "CM"},
        {"name": "Marc Bernal", "age": 18, "rating": 72, "value": 15000000, "position": "DM"}
    ],
    "forwards": [
        {"name": "Ferran Torres", "age": 25, "rating": 80, "value": 55000000, "position": "RW"},
        {"name": "Robert Lewandowski", "age": 37, "rating": 87, "value": 45000000, "position": "ST"},
        {"name": "Lamine Yamal", "age": 18, "rating": 85, "value": 120000000, "position": "RW"},
        {"name": "Raphinha", "age": 28, "rating": 84, "value": 58000000, "position": "LW"},
        {"name": "Marcus Rashford", "age": 27, "rating": 82, "value": 50000000, "position": "LW"}
    ]
}

# la liga players database (sample - in real app would be much larger)
LA_LIGA_PLAYERS = [
    # real madrid
    {"name": "Kylian Mbappé", "age": 26, "rating": 91, "value": 180000000, "position": "ST", "team": "Real Madrid"},
    {"name": "Vinícius Jr.", "age": 24, "rating": 89, "value": 150000000, "position": "LW", "team": "Real Madrid"},
    {"name": "Jude Bellingham", "age": 21, "rating": 87, "value": 120000000, "position": "CM", "team": "Real Madrid"},
    {"name": "Rodrygo", "age": 24, "rating": 85, "value": 90000000, "position": "RW", "team": "Real Madrid"},
    {"name": "Federico Valverde", "age": 26, "rating": 86, "value": 100000000, "position": "CM", "team": "Real Madrid"},
    {"name": "Antonio Rüdiger", "age": 32, "rating": 84, "value": 35000000, "position": "CB", "team": "Real Madrid"},
    {"name": "Thibaut Courtois", "age": 32, "rating": 89, "value": 60000000, "position": "GK", "team": "Real Madrid"},
    
    # atletico madrid
    {"name": "Antoine Griezmann", "age": 34, "rating": 85, "value": 40000000, "position": "AM", "team": "Atlético Madrid"},
    {"name": "Álvaro Morata", "age": 32, "rating": 82, "value": 25000000, "position": "ST", "team": "Atlético Madrid"},
    {"name": "Koke", "age": 33, "rating": 83, "value": 20000000, "position": "CM", "team": "Atlético Madrid"},
    {"name": "José Giménez", "age": 30, "rating": 82, "value": 35000000, "position": "CB", "team": "Atlético Madrid"},
    
    # real sociedad
    {"name": "Mikel Oyarzabal", "age": 28, "rating": 83, "value": 50000000, "position": "LW", "team": "Real Sociedad"},
    {"name": "Alexander Sørloth", "age": 29, "rating": 80, "value": 35000000, "position": "ST", "team": "Real Sociedad"},
    {"name": "Martin Zubimendi", "age": 26, "rating": 84, "value": 60000000, "position": "DM", "team": "Real Sociedad"},
    
    # athletic bilbao
    {"name": "Nico Williams", "age": 22, "rating": 84, "value": 70000000, "position": "LW", "team": "Athletic Bilbao"},
    {"name": "Oihan Sancet", "age": 25, "rating": 81, "value": 45000000, "position": "AM", "team": "Athletic Bilbao"},
    
    # villarreal
    {"name": "Yeremy Pino", "age": 22, "rating": 80, "value": 40000000, "position": "RW", "team": "Villarreal"},
    {"name": "Gerard Moreno", "age": 32, "rating": 82, "value": 25000000, "position": "ST", "team": "Villarreal"},
    
    # valencia
    {"name": "José Gayà", "age": 30, "rating": 81, "value": 25000000, "position": "LB", "team": "Valencia"},
    {"name": "Carlos Soler", "age": 28, "rating": 80, "value": 30000000, "position": "CM", "team": "Valencia"},
    
    # sevilla
    {"name": "Youssef En-Nesyri", "age": 28, "rating": 79, "value": 20000000, "position": "ST", "team": "Sevilla"},
    {"name": "Jesús Navas", "age": 39, "rating": 78, "value": 5000000, "position": "RB", "team": "Sevilla"}
]

def analyze_squad_weaknesses():
    """analyze current squad to identify areas for improvement"""
    weaknesses = []
    
    # check goalkeeper depth
    gk_count = len(CURRENT_SQUAD["goalkeepers"])
    if gk_count < 2:
        weaknesses.append("goalkeeper_depth")
    
    # check for aging players
    aging_players = []
    for position_group in CURRENT_SQUAD.values():
        for player in position_group:
            if player["age"] > 32:
                aging_players.append(player)
    
    if aging_players:
        weaknesses.append("aging_squad")
    
    # check striker options
    strikers = [p for p in CURRENT_SQUAD["forwards"] if p["position"] == "ST"]
    if len(strikers) < 2:
        weaknesses.append("striker_depth")
    
    # check center back depth
    center_backs = [p for p in CURRENT_SQUAD["defenders"] if p["position"] == "CB"]
    if len(center_backs) < 3:
        weaknesses.append("cb_depth")
    
    return weaknesses

def calculate_transfer_rating(player: Dict, weaknesses: List[str]) -> Dict[str, Any]:
    """calculate how good a transfer would be"""
    base_rating = 5.0  # out of 10
    explanation_parts = []
    
    # player quality factor
    if player["rating"] >= 90:
        base_rating += 3.0
        explanation_parts.append("world-class player quality")
    elif player["rating"] >= 85:
        base_rating += 2.0
        explanation_parts.append("excellent player quality")
    elif player["rating"] >= 80:
        base_rating += 1.0
        explanation_parts.append("good player quality")
    elif player["rating"] < 75:
        base_rating -= 1.0
        explanation_parts.append("below average quality")
    
    # age factor
    if player["age"] <= 23:
        base_rating += 1.0
        explanation_parts.append("young with potential")
    elif player["age"] >= 32:
        base_rating -= 1.5
        explanation_parts.append("aging player")
    elif player["age"] >= 28:
        base_rating -= 0.5
        explanation_parts.append("entering peak years")
    
    # value for money
    value_per_rating = player["value"] / max(player["rating"], 1)
    if value_per_rating > 2000000:  # expensive per rating point
        base_rating -= 2.0
        explanation_parts.append("very expensive relative to ability")
    elif value_per_rating > 1500000:
        base_rating -= 1.0
        explanation_parts.append("expensive for the quality")
    elif value_per_rating < 800000:
        base_rating += 1.0
        explanation_parts.append("good value for money")
    
    # addresses weaknesses
    position_need_bonus = 0
    if "striker_depth" in weaknesses and player["position"] == "ST":
        position_need_bonus = 1.5
        explanation_parts.append("addresses striker depth issue")
    elif "cb_depth" in weaknesses and player["position"] == "CB":
        position_need_bonus = 1.0
        explanation_parts.append("strengthens center back options")
    elif "aging_squad" in weaknesses and player["age"] <= 25:
        position_need_bonus = 0.5
        explanation_parts.append("helps lower squad age")
    
    base_rating += position_need_bonus
    
    # rival factor (signing from real madrid)
    if player.get("team") == "Real Madrid":
        base_rating += 0.5
        explanation_parts.append("weakens main rival")
    
    # ensure rating is between 1-10
    final_rating = max(1.0, min(10.0, base_rating))
    
    return {
        "rating": round(final_rating, 1),
        "explanation": ", ".join(explanation_parts) if explanation_parts else "standard transfer"
    }

@app.route('/api/squad')
def get_squad():
    """get current barcelona squad"""
    return jsonify(CURRENT_SQUAD)

@app.route('/api/players/search')
def search_players():
    """search la liga players for transfers"""
    query = request.args.get('q', '').lower()
    position = request.args.get('position', '').upper()
    
    filtered_players = LA_LIGA_PLAYERS
    
    if query:
        filtered_players = [p for p in filtered_players if query in p["name"].lower()]
    
    if position:
        filtered_players = [p for p in filtered_players if p["position"] == position]
    
    # limit results
    return jsonify(filtered_players[:20])

@app.route('/api/transfer/rate', methods=['POST'])
def rate_transfer():
    """rate a potential transfer"""
    player_data = request.get_json()
    
    if not player_data:
        return jsonify({"error": "player data required"}), 400
    
    weaknesses = analyze_squad_weaknesses()
    rating_data = calculate_transfer_rating(player_data, weaknesses)
    
    return jsonify({
        "player": player_data,
        "rating": rating_data["rating"],
        "explanation": rating_data["explanation"],
        "squad_weaknesses": weaknesses
    })

@app.route('/api/squad/analysis')
def squad_analysis():
    """get squad analysis and weaknesses"""
    weaknesses = analyze_squad_weaknesses()
    
    weakness_descriptions = {
        "goalkeeper_depth": "lack of backup goalkeeper options",
        "aging_squad": "several players over 32 need eventual replacement",
        "striker_depth": "limited striker options beyond lewandowski",
        "cb_depth": "need more center back depth for rotation"
    }
    
    return jsonify({
        "weaknesses": weaknesses,
        "descriptions": {w: weakness_descriptions.get(w, w) for w in weaknesses},
        "total_players": sum(len(pos) for pos in CURRENT_SQUAD.values()),
        "average_age": round(sum(p["age"] for pos in CURRENT_SQUAD.values() for p in pos) / 
                           sum(len(pos) for pos in CURRENT_SQUAD.values()), 1)
    })

# serve frontend
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)