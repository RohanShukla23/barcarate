from flask import Flask, render_template, request, jsonify
from data_collector import DataCollector
from transfer_analyzer import TransferAnalyzer
from database import PlayerDatabase
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# initialize components
collector = DataCollector()
analyzer = TransferAnalyzer()
db = PlayerDatabase()

@app.route('/')
def index():
    """main page with squad analysis and transfer form"""
    squad_analysis = analyzer.analyze_barcelona_squad()
    return render_template('index.html', analysis=squad_analysis)

@app.route('/api/players/search')
def search_players():
    """autocomplete endpoint for player search"""
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify([])
    
    players = db.search_players(query, limit=10)
    return jsonify(players)

@app.route('/api/transfer/rate', methods=['POST'])
def rate_transfer():
    """rate a potential transfer"""
    data = request.json
    player_name = data.get('player_name')
    
    if not player_name:
        return jsonify({'error': 'player name required'}), 400
    
    # get player data
    player = db.get_player_by_name(player_name)
    if not player:
        return jsonify({'error': 'player not found'}), 404
    
    # analyze transfer
    rating = analyzer.rate_transfer(player)
    
    return jsonify({
        'player': player,
        'rating': rating,
        'stars': rating['stars'],
        'justification': rating['justification']
    })

@app.route('/api/update_data')
def update_data():
    """manually trigger data update"""
    try:
        # update barcelona squad
        collector.update_barcelona_squad()
        
        # update la liga players (limited by api quota)
        collector.update_laliga_players()
        
        return jsonify({'status': 'success', 'message': 'data updated'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def setup_database():
    """initialize database and fetch initial data"""
    print("setting up barcarate...")
    
    # create database tables
    db.initialize()
    
    # fetch barcelona squad if not exists
    if not os.path.exists('data/barcelona_squad.json'):
        print("fetching barcelona squad...")
        collector.update_barcelona_squad()
    
    # fetch la liga players if database empty
    if db.get_player_count() == 0:
        print("fetching la liga players... (this may take a few minutes)")
        collector.update_laliga_players()
    
    print("setup complete!")

if __name__ == '__main__':
    setup_database()
    app.run(debug=True, host='0.0.0.0', port=5000)