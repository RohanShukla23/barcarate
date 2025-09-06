// barcarate javascript functionality - clean separated js

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

// utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    setupAutocomplete();
    
    // add loading states for better ux
    const buttons = document.querySelectorAll('button');
    buttons.forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.textContent.includes('evaluate')) {
                this.disabled = true;
                this.textContent = 'evaluating...';
                setTimeout(() => {
                    this.disabled = false;
                    this.textContent = 'evaluate transfer';
                }, 3000);
            }
        });
    });
});