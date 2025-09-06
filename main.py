#!/usr/bin/env python3
"""
barcarate - fc barcelona transfer rating tool
main flask application - clean version with proper templates
"""

from flask import Flask, render_template, request, jsonify
from data.laliga_players import get_all_players, search_players, get_player_names
from data.barcelona_squad import squad_analysis
from utils.rating_engine import TransferRatingEngine
from utils.transfer_analyzer import TransferAnalyzer

app = Flask(__name__)
app.secret_key = 'barcarate_secret_key_2025'

# initialize components
rating_engine = TransferRatingEngine()
analyzer = TransferAnalyzer()

@app.route('/')
def index():
    """main page"""
    all_players = get_all_players()
    player_names = get_player_names()
    
    return render_template(
        'index.html',
        analysis=squad_analysis,
        player_names=player_names,
        all_players=all_players
    )

@app.route('/api/search')
def api_search():
    """search players api endpoint"""
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify([])
    
    results = search_players(query)
    return jsonify(results[:10])  # limit to 10 results

@app.route('/api/evaluate')
def api_evaluate():
    """evaluate player transfer"""
    player_name = request.args.get('player', '').strip()
    
    if not player_name:
        return jsonify({'error': 'player name required'})
    
    # find player
    all_players = get_all_players()
    player = None
    
    for p in all_players:
        if p['name'].lower() == player_name.lower():
            player = p
            break
    
    if not player:
        return jsonify({'error': 'player not found'})
    
    # evaluate transfer
    rating_data = rating_engine.calculate_rating(player, detailed=True)
    
    return jsonify({
        'player': player,
        'rating': rating_data
    })

@app.route('/api/recommendations')
def api_recommendations():
    """get transfer recommendations"""
    all_players = get_all_players()
    recommendations = analyzer.generate_transfer_recommendations(all_players)
    
    # format for frontend
    formatted_recs = []
    for rec in recommendations:
        formatted_recs.append({
            'player': rec['player'],
            'rating': rec['rating'],
            'weakness_addressed': rec['weakness']['description'],
            'priority': rec['priority']
        })
    
    return jsonify(formatted_recs)

if __name__ == '__main__':
    print("starting barcarate server...")
    print("access the app at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)