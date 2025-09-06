#!/usr/bin/env python3
"""
barcarate - fc barcelona transfer rating tool
main flask application
"""

from flask import Flask, render_template_string, request, jsonify
from data.laliga_players import get_all_players, search_players, get_player_names
from data.barcelona_squad import squad_analysis
from utils.rating_engine import TransferRatingEngine
from utils.transfer_analyzer import TransferAnalyzer
import json

app = Flask(__name__)
app.secret_key = 'barcarate_secret_key_2025'

# initialize components
rating_engine = TransferRatingEngine()
analyzer = TransferAnalyzer()

# html template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BarcaRate - Barcelona Transfer Evaluator</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🔵🔴 BarcaRate</h1>
            <p class="subtitle">intelligent transfer evaluation for fc barcelona</p>
        </header>

        <nav class="nav-tabs">
            <button class="tab-btn active" onclick="showTab('analysis')">squad analysis</button>
            <button class="tab-btn" onclick="showTab('player-search')">player search</button>
            <button class="tab-btn" onclick="showTab('recommendations')">recommendations</button>
        </nav>

        <!-- squad analysis tab -->
        <div id="analysis" class="tab-content active">
            <section class="squad-overview">
                <h2>current squad analysis</h2>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>squad strength</h3>
                        <div class="strength-list">
                            {% for strength in analysis.strengths %}
                            <div class="strength-item">✓ {{ strength }}</div>
                            {% endfor %}
                        </div>
                    </div>
                    
                    <div class="stat-card">
                        <h3>areas for improvement</h3>
                        <div class="weakness-list">
                            {% for weakness in analysis.weaknesses %}
                            <div class="weakness-item">⚠ {{ weakness }}</div>
                            {% endfor %}
                        </div>
                    </div>
                </div>

                <div class="priority-positions">
                    <h3>transfer priorities</h3>
                    <div class="priority-grid">
                        {% for position in analysis.priority_positions %}
                        <div class="priority-card" data-urgency="{{ position.urgency }}">
                            <div class="position">{{ position.position }}</div>
                            <div class="urgency">urgency: {{ position.urgency }}/10</div>
                            <div class="reason">{{ position.reason }}</div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </section>
        </div>

        <!-- player search tab -->
        <div id="player-search" class="tab-content">
            <section class="search-section">
                <h2>evaluate la liga player</h2>
                
                <div class="search-container">
                    <input 
                        type="text" 
                        id="player-input" 
                        placeholder="enter la liga player name..."
                        autocomplete="off"
                    >
                    <div id="autocomplete-suggestions" class="suggestions"></div>
                    <button onclick="evaluatePlayer()">evaluate transfer</button>
                </div>

                <div id="player-result" class="result-container" style="display: none;">
                    <!-- player evaluation results will appear here -->
                </div>
            </section>
        </div>

        <!-- recommendations tab -->
        <div id="recommendations" class="tab-content">
            <section class="recommendations-section">
                <h2>transfer recommendations</h2>
                <p>top-rated players to address barcelona's needs</p>
                
                <div id="recommendations-list" class="recommendations-grid">
                    <div class="loading">analyzing la liga market...</div>
                </div>
            </section>
        </div>
    </div>

    <footer>
        <p>barcarate &copy; 2025 | for entertainment purposes only</p>
    </footer>

    <script src="/static/script.js"></script>
    <script>
        // pass data to javascript
        window.playerNames = {{ player_names|tojson }};
        window.allPlayers = {{ all_players|tojson }};
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """main page"""
    all_players = get_all_players()
    player_names = get_player_names()
    
    return render_template_string(
        HTML_TEMPLATE,
        analysis=squad_analysis,
        player_names=player_names,
        all_players=all_players
    )

@app.route('/static/<path:filename>')
def static_files(filename):
    """serve static files"""
    if filename == 'style.css':
        return get_css(), 200, {'Content-Type': 'text/css'}
    elif filename == 'script.js':
        return get_js(), 200, {'Content-Type': 'application/javascript'}
    return '', 404

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

def get_css():
    """return css styles"""
    return """
/* barcarate styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'segoe ui', tahoma, geneva, verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #004d98 0%, #a50044 100%);
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background: white;
    margin-top: 20px;
    margin-bottom: 20px;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

header {
    text-align: center;
    margin-bottom: 30px;
    padding: 20px 0;
    border-bottom: 3px solid #004d98;
}

header h1 {
    font-size: 3em;
    color: #004d98;
    margin-bottom: 10px;
    font-weight: bold;
}

.subtitle {
    color: #a50044;
    font-size: 1.2em;
    font-weight: 500;
}

.nav-tabs {
    display: flex;
    border-bottom: 2px solid #eee;
    margin-bottom: 30px;
}

.tab-btn {
    padding: 12px 24px;
    border: none;
    background: none;
    cursor: pointer;
    font-size: 1em;
    color: #666;
    border-bottom: 3px solid transparent;
    transition: all 0.3s ease;
}

.tab-btn.active,
.tab-btn:hover {
    color: #004d98;
    border-bottom-color: #004d98;
}

.tab-content {
    display: none;
}

.tab-content.active {
    display: block;
}

.stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 30px;
}

.stat-card {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #004d98;
}

.stat-card h3 {
    color: #004d98;
    margin-bottom: 15px;
    font-size: 1.3em;
}

.strength-item {
    color: #28a745;
    padding: 5px 0;
    font-weight: 500;
}

.weakness-item {
    color: #dc3545;
    padding: 5px 0;
    font-weight: 500;
}

.priority-positions h3 {
    color: #004d98;
    margin-bottom: 20px;
    font-size: 1.4em;
}

.priority-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
}

.priority-card {
    background: white;
    border: 2px solid #eee;
    padding: 15px;
    border-radius: 8px;
    transition: transform 0.2s ease;
}

.priority-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.priority-card[data-urgency="9"],
.priority-card[data-urgency="10"] {
    border-color: #dc3545;
    background: #fff5f5;
}

.priority-card[data-urgency="7"],
.priority-card[data-urgency="8"] {
    border-color: #ffc107;
    background: #fffbf0;
}

.position {
    font-size: 1.4em;
    font-weight: bold;
    color: #004d98;
    margin-bottom: 5px;
}

.urgency {
    font-size: 0.9em;
    color: #666;
    margin-bottom: 8px;
}

.reason {
    font-size: 0.95em;
    color: #333;
}

.search-container {
    max-width: 500px;
    margin: 0 auto 30px;
    position: relative;
}

#player-input {
    width: 100%;
    padding: 15px;
    font-size: 1.1em;
    border: 2px solid #ddd;
    border-radius: 8px;
    outline: none;
    transition: border-color 0.3s ease;
}

#player-input:focus {
    border-color: #004d98;
}

.suggestions {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border: 2px solid #ddd;
    border-top: none;
    border-radius: 0 0 8px 8px;
    max-height: 200px;
    overflow-y: auto;
    z-index: 1000;
    display: none;
}

.suggestion-item {
    padding: 10px 15px;
    cursor: pointer;
    border-bottom: 1px solid #eee;
}

.suggestion-item:hover,
.suggestion-item.selected {
    background: #f0f7ff;
    color: #004d98;
}

button {
    background: #004d98;
    color: white;
    border: none;
    padding: 15px 30px;
    font-size: 1.1em;
    border-radius: 8px;
    cursor: pointer;
    margin-top: 15px;
    transition: background-color 0.3s ease;
}

button:hover {
    background: #003d7a;
}

.result-container {
    background: #f8f9fa;
    border-radius: 10px;
    padding: 25px;
    margin-top: 20px;
    border-left: 5px solid #004d98;
}

.player-info {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 20px;
}

.player-details h3 {
    color: #004d98;
    margin-bottom: 10px;
}

.detail-item {
    margin-bottom: 5px;
}

.rating-display {
    text-align: center;
    margin: 20px 0;
}

.rating-stars {
    font-size: 2.5em;
    color: #ffc107;
    margin-bottom: 10px;
}

.rating-score {
    font-size: 2em;
    color: #004d98;
    font-weight: bold;
}

.rating-breakdown {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin: 20px 0;
}

.breakdown-item {
    text-align: center;
    padding: 10px;
    background: white;
    border-radius: 8px;
    border: 1px solid #ddd;
}

.breakdown-label {
    font-size: 0.9em;
    color: #666;
    margin-bottom: 5px;
}

.breakdown-value {
    font-size: 1.2em;
    font-weight: bold;
    color: #004d98;
}

.justification {
    background: white;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #28a745;
    margin-top: 20px;
}

.justification h4 {
    color: #004d98;
    margin-bottom: 10px;
}

.recommendations-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}

.recommendation-card {
    background: white;
    border: 2px solid #eee;
    border-radius: 10px;
    padding: 20px;
    transition: all 0.3s ease;
}

.recommendation-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    border-color: #004d98;
}

.rec-player-name {
    font-size: 1.3em;
    font-weight: bold;
    color: #004d98;
    margin-bottom: 10px;
}

.rec-details {
    color: #666;
    margin-bottom: 15px;
}

.rec-rating {
    text-align: center;
    margin: 15px 0;
}

.rec-stars {
    font-size: 1.5em;
    color: #ffc107;
}

.rec-weakness {
    background: #fff3cd;
    padding: 10px;
    border-radius: 5px;
    border-left: 4px solid #ffc107;
    margin-top: 15px;
}

.loading {
    text-align: center;
    color: #666;
    padding: 40px;
    font-size: 1.1em;
}

footer {
    text-align: center;
    color: white;
    padding: 20px;
    margin-top: 20px;
}

@media (max-width: 768px) {
    .container {
        margin: 10px;
        padding: 15px;
    }
    
    header h1 {
        font-size: 2em;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
    }
    
    .nav-tabs {
        flex-direction: column;
    }
    
    .tab-btn {
        border-bottom: 1px solid #eee;
        border-left: 3px solid transparent;
    }
    
    .tab-btn.active,
    .tab-btn:hover {
        border-left-color: #004d98;
        border-bottom-color: #eee;
    }
}
"""

def get_js():
    """return javascript code"""
    return """
// barcarate javascript functionality

let selectedSuggestionIndex = -1;
let currentSuggestions = [];

// tab switching
function showTab(tabName) {
    // hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // remove active from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // show selected tab
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
    
    // load recommendations when tab is opened
    if (tabName === 'recommendations') {
        loadRecommendations();
    }
}

// autocomplete functionality
function setupAutocomplete() {
    const input = document.getElementById('player-input');
    const suggestions = document.getElementById('autocomplete-suggestions');
    
    input.addEventListener('input', function() {
        const query = this.value.trim();
        
        if (query.length < 2) {
            hideSuggestions();
            return;
        }
        
        // filter player names
        currentSuggestions = window.playerNames.filter(name => 
            name.toLowerCase().includes(query.toLowerCase())
        ).slice(0, 8);
        
        showSuggestions(currentSuggestions);
    });
    
    // keyboard navigation
    input.addEventListener('keydown', function(e) {
        if (!currentSuggestions.length) return;
        
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            selectedSuggestionIndex = Math.min(
                selectedSuggestionIndex + 1, 
                currentSuggestions.length - 1
            );
            updateSuggestionSelection();
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            selectedSuggestionIndex = Math.max(selectedSuggestionIndex - 1, -1);
            updateSuggestionSelection();
        } else if (e.key === 'Enter') {
            e.preventDefault();
            if (selectedSuggestionIndex >= 0) {
                selectSuggestion(currentSuggestions[selectedSuggestionIndex]);
            } else {
                evaluatePlayer();
            }
        } else if (e.key === 'Escape') {
            hideSuggestions();
        }
    });
    
    // click outside to hide
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-container')) {
            hideSuggestions();
        }
    });
}

function showSuggestions(suggestions) {
    const container = document.getElementById('autocomplete-suggestions');
    
    if (suggestions.length === 0) {
        hideSuggestions();
        return;
    }
    
    container.innerHTML = suggestions.map((name, index) => 
        `<div class="suggestion-item" onclick="selectSuggestion('${name}')" 
              data-index="${index}">${name}</div>`
    ).join('');
    
    container.style.display = 'block';
    selectedSuggestionIndex = -1;
}

function hideSuggestions() {
    document.getElementById('autocomplete-suggestions').style.display = 'none';
    selectedSuggestionIndex = -1;
}

function updateSuggestionSelection() {
    const items = document.querySelectorAll('.suggestion-item');
    
    items.forEach((item, index) => {
        item.classList.toggle('selected', index === selectedSuggestionIndex);
    });
}

function selectSuggestion(playerName) {
    document.getElementById('player-input').value = playerName;
    hideSuggestions();
    evaluatePlayer();
}

// player evaluation
async function evaluatePlayer() {
    const playerName = document.getElementById('player-input').value.trim();
    const resultContainer = document.getElementById('player-result');
    
    if (!playerName) {
        alert('please enter a player name');
        return;
    }
    
    // show loading
    resultContainer.style.display = 'block';
    resultContainer.innerHTML = '<div class="loading">evaluating transfer...</div>';
    
    try {
        const response = await fetch(`/api/evaluate?player=${encodeURIComponent(playerName)}`);
        const data = await response.json();
        
        if (data.error) {
            resultContainer.innerHTML = `<div class="error">error: ${data.error}</div>`;
            return;
        }
        
        displayPlayerEvaluation(data);
        
    } catch (error) {
        resultContainer.innerHTML = '<div class="error">failed to evaluate player</div>';
        console.error('evaluation error:', error);
    }
}

function displayPlayerEvaluation(data) {
    const { player, rating } = data;
    const container = document.getElementById('player-result');
    
    const html = `
        <div class="player-info">
            <div class="player-details">
                <h3>${player.name}</h3>
                <div class="detail-item"><strong>team:</strong> ${player.team}</div>
                <div class="detail-item"><strong>position:</strong> ${player.position}</div>
                <div class="detail-item"><strong>age:</strong> ${player.age}</div>
                <div class="detail-item"><strong>nationality:</strong> ${player.nationality}</div>
                <div class="detail-item"><strong>market value:</strong> €${player.market_value}M</div>
            </div>
            
            <div class="rating-display">
                <div class="rating-stars">${rating.stars}</div>
                <div class="rating-score">${rating.rating}/5.0</div>
            </div>
        </div>
        
        <div class="rating-breakdown">
            <div class="breakdown-item">
                <div class="breakdown-label">position need</div>
                <div class="breakdown-value">${rating.breakdown.position_need}</div>
            </div>
            <div class="breakdown-item">
                <div class="breakdown-label">performance</div>
                <div class="breakdown-value">${rating.breakdown.performance}</div>
            </div>
            <div class="breakdown-item">
                <div class="breakdown-label">value for money</div>
                <div class="breakdown-value">${rating.breakdown.value_for_money}</div>
            </div>
            <div class="breakdown-item">
                <div class="breakdown-label">barcelona fit</div>
                <div class="breakdown-value">${rating.breakdown.barcelona_fit}</div>
            </div>
            <div class="breakdown-item">
                <div class="breakdown-label">age factor</div>
                <div class="breakdown-value">${rating.breakdown.age_factor}</div>
            </div>
        </div>
        
        <div class="justification">
            <h4>transfer analysis</h4>
            <p>${rating.justification}</p>
        </div>
    `;
    
    container.innerHTML = html;
}

// recommendations
async function loadRecommendations() {
    const container = document.getElementById('recommendations-list');
    
    try {
        const response = await fetch('/api/recommendations');
        const recommendations = await response.json();
        
        if (recommendations.length === 0) {
            container.innerHTML = '<div class="loading">no recommendations available</div>';
            return;
        }
        
        const html = recommendations.map(rec => `
            <div class="recommendation-card">
                <div class="rec-player-name">${rec.player.name}</div>
                <div class="rec-details">
                    ${rec.player.position} | ${rec.player.age} years | €${rec.player.market_value}M<br>
                    <strong>${rec.player.team}</strong> | ${rec.player.nationality}
                </div>
                <div class="rec-rating">
                    <div class="rec-stars">${rec.rating.stars}</div>
                    <div>${rec.rating.rating}/5.0</div>
                </div>
                <div class="rec-weakness">
                    <strong>addresses:</strong> ${rec.weakness_addressed}
                </div>
            </div>
        `).join('');
        
        container.innerHTML = html;
        
    } catch (error) {
        container.innerHTML = '<div class="error">failed to load recommendations</div>';
        console.error('recommendations error:', error);
    }
}

// initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    setupAutocomplete();
});
"""

if __name__ == '__main__':
    print("starting barcarate server...")
    print("access the app at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)