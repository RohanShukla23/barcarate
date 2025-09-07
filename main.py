from flask import Flask, render_template, request, jsonify
import json
import os
from config import Config
from src.database import init_db, get_db_connection
from src.scraper import update_all_data
from src.analyzer import SquadAnalyzer
from src.rating_engine import TransferRatingEngine
from src.utils import fuzzy_search_players

app = Flask(__name__)
app.config.from_object(Config)

# initialize database on startup
if not os.path.exists(Config.DATABASE_PATH):
    print("initializing database...")
    init_db()
    print("updating player data...")
    update_all_data()

@app.route('/')
def index():
    """main page with squad analysis and transfer rating interface"""
    analyzer = SquadAnalyzer()
    
    # get barcelona squad analysis
    squad_analysis = analyzer.analyze_squad()
    
    return render_template('index.html', 
                         squad_analysis=squad_analysis)

@app.route('/api/players/search')
def search_players():
    """autocomplete endpoint for player search"""
    query = request.args.get('q', '')
    
    if len(query) < 2:
        return jsonify([])
    
    # search la liga players
    players = fuzzy_search_players(query, limit=10)
    
    return jsonify([{
        'name': player['name'],
        'team': player['team'],
        'position': player['position'],
        'age': player.get('age', 'N/A')
    } for player in players])

@app.route('/api/rate-transfer', methods=['POST'])
def rate_transfer():
    """rate a potential transfer"""
    data = request.json
    player_name = data.get('player_name')
    
    if not player_name:
        return jsonify({'error': 'player name required'}), 400
    
    # get player data
    conn = get_db_connection()
    player = conn.execute(
        'SELECT * FROM laliga_players WHERE name = ?', 
        (player_name,)
    ).fetchone()
    conn.close()
    
    if not player:
        return jsonify({'error': 'player not found'}), 404
    
    # create rating engine and analyze transfer
    rating_engine = TransferRatingEngine()
    rating_result = rating_engine.rate_transfer(dict(player))
    
    return jsonify(rating_result)

@app.route('/api/squad-analysis')
def squad_analysis():
    """get detailed squad analysis"""
    analyzer = SquadAnalyzer()
    analysis = analyzer.analyze_squad()
    return jsonify(analysis)

@app.route('/api/update-data', methods=['POST'])
def update_data():
    """manually trigger data update"""
    try:
        update_all_data()
        return jsonify({'status': 'success', 'message': 'data updated successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)