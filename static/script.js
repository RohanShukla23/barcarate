// barcarate frontend interactions

let selectedPlayer = null;
let searchTimeout = null;

// initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeSearch();
    initializeKeyboardShortcuts();
});

function initializeSearch() {
    const searchInput = document.getElementById('playerSearch');
    const searchResults = document.getElementById('searchResults');
    
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        
        // clear previous timeout
        if (searchTimeout) {
            clearTimeout(searchTimeout);
        }
        
        // hide results if query too short
        if (query.length < 2) {
            searchResults.style.display = 'none';
            return;
        }
        
        // debounced search
        searchTimeout = setTimeout(() => {
            searchPlayers(query);
        }, 300);
    });
    
    // hide results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
    
    // enter key to rate transfer
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            rateTransfer();
        }
    });
}

function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // ctrl/cmd + k to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            document.getElementById('playerSearch').focus();
        }
        
        // escape to clear search
        if (e.key === 'Escape') {
            clearSearch();
        }
    });
}

async function searchPlayers(query) {
    try {
        const response = await fetch(`/api/players/search?q=${encodeURIComponent(query)}`);
        const players = await response.json();
        
        displaySearchResults(players);
    } catch (error) {
        console.error('search failed:', error);
        showError('search failed. please try again.');
    }
}

function displaySearchResults(players) {
    const searchResults = document.getElementById('searchResults');
    
    if (players.length === 0) {
        searchResults.innerHTML = '<div class="search-result-item">no players found</div>';
        searchResults.style.display = 'block';
        return;
    }
    
    searchResults.innerHTML = players.map(player => 
        `<div class="search-result-item" onclick="selectPlayer('${player.name}')">
            <div><strong>${player.name}</strong></div>
            <div style="font-size: 0.9rem; color: var(--text-secondary);">
                ${player.team} • ${player.position} • Age ${player.age} • Rating ${player.rating.toFixed(1)}
            </div>
        </div>`
    ).join('');
    
    searchResults.style.display = 'block';
}

function selectPlayer(playerName) {
    selectedPlayer = playerName;
    document.getElementById('playerSearch').value = playerName;
    document.getElementById('searchResults').style.display = 'none';
}

async function rateTransfer() {
    const playerName = selectedPlayer || document.getElementById('playerSearch').value.trim();
    
    if (!playerName) {
        showError('please enter a player name');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/transfer/rate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ player_name: playerName })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'rating failed');
        }
        
        const result = await response.json();
        displayTransferRating(result);
        
    } catch (error) {
        console.error('rating failed:', error);
        showError(error.message || 'failed to rate transfer. please try again.');
    } finally {
        hideLoading();
    }
}

function displayTransferRating(result) {
    const { player, rating, stars, justification } = result;
    
    const transferResult = document.getElementById('transferResult');
    
    // build star display
    const starDisplay = Array.from({length: 5}, (_, i) => 
        `<span class="star ${i < stars ? 'filled' : ''}">★</span>`
    ).join('');
    
    // build rating text
    const ratingText = getRatingText(stars);
    
    // estimated market value
    const estimatedValue = estimateMarketValue(player);
    
    transferResult.innerHTML = `
        <div class="player-header">
            <img src="${player.photo || '/static/default-player.png'}" 
                 alt="${player.name}" class="player-photo"
                 onerror="this.style.display='none'">
            <div class="player-info">
                <h3>${player.name}</h3>
                <div class="player-meta">
                    <span><i class="fas fa-shield-alt"></i> ${player.team}</span>
                    <span><i class="fas fa-running"></i> ${player.position}</span>
                    <span><i class="fas fa-birthday-cake"></i> ${player.age} years</span>
                    <span><i class="fas fa-flag"></i> ${player.nationality}</span>
                </div>
            </div>
        </div>
        
        <div class="rating-display">
            <div class="stars">${starDisplay}</div>
            <div class="rating-text">${ratingText}</div>
            <div style="color: var(--text-secondary);">${stars}/5 stars</div>
        </div>
        
        <div class="score-breakdown">
            <div class="score-item">
                <h4>performance</h4>
                <div class="score-value">${rating.performance_score.toFixed(1)}</div>
            </div>
            <div class="score-item">
                <h4>age factor</h4>
                <div class="score-value">${rating.age_score.toFixed(1)}</div>
            </div>
            <div class="score-item">
                <h4>position need</h4>
                <div class="score-value">${rating.position_score.toFixed(1)}</div>
            </div>
            <div class="score-item">
                <h4>value rating</h4>
                <div class="score-value">${rating.value_score.toFixed(1)}</div>
            </div>
        </div>
        
        <div class="player-stats">
            <h4 style="margin-bottom: 1rem; color: var(--gold);">
                <i class="fas fa-chart-line"></i> season stats
            </h4>
            <div class="stats-grid">
                <div class="stat-item">
                    <span class="stat-label">games played</span>
                    <span class="stat-value">${player.games_played}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">goals</span>
                    <span class="stat-value">${player.goals}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">assists</span>
                    <span class="stat-value">${player.assists}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">avg rating</span>
                    <span class="stat-value">${player.rating.toFixed(1)}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">minutes</span>
                    <span class="stat-value">${player.minutes_played.toLocaleString()}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">est. value</span>
                    <span class="stat-value">${estimatedValue}</span>
                </div>
            </div>
        </div>
        
        <div class="justification">
            <h4><i class="fas fa-comment-alt"></i> analysis</h4>
            <p>${justification}</p>
        </div>
    `;
    
    transferResult.style.display = 'block';
    transferResult.scrollIntoView({ behavior: 'smooth' });
}

function getRatingText(stars) {
    const ratings = {
        5: 'outstanding signing',
        4: 'excellent addition', 
        3: 'solid option',
        2: 'questionable fit',
        1: 'poor choice'
    };
    return ratings[stars] || 'unrated';
}

function estimateMarketValue(player) {
    const age = player.age;
    const rating = player.rating;
    const games = player.games_played;
    const goals = player.goals;
    const assists = player.assists;
    
    // base value from rating
    let baseValue = Math.max(0, (rating - 5.0) * 10);
    
    // age adjustment
    let ageMultiplier = 1.0;
    if (age <= 23) ageMultiplier = 1.3;
    else if (age <= 27) ageMultiplier = 1.0;
    else if (age <= 30) ageMultiplier = 0.8;
    else ageMultiplier = 0.5;
    
    // performance bonus
    let performanceBonus = 0;
    if (games > 20) {
        performanceBonus = Math.min(10, (goals + assists) * 0.5);
    }
    
    let estimatedValue = (baseValue * ageMultiplier) + performanceBonus;
    estimatedValue = Math.max(1, Math.min(100, estimatedValue));
    
    if (estimatedValue >= 50) return `€${estimatedValue.toFixed(0)}M`;
    else if (estimatedValue >= 10) return `€${estimatedValue.toFixed(1)}M`;
    else return `€${estimatedValue.toFixed(1)}M`;
}

async function updateData() {
    showLoading();
    
    try {
        const response = await fetch('/api/update_data');
        const result = await response.json();
        
        if (result.status === 'success') {
            showSuccess('data updated successfully!');
            // reload page after short delay
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            throw new Error(result.message);
        }
        
    } catch (error) {
        console.error('update failed:', error);
        showError(error.message || 'failed to update data');
    } finally {
        hideLoading();
    }
}

function clearSearch() {
    document.getElementById('playerSearch').value = '';
    document.getElementById('searchResults').style.display = 'none';
    selectedPlayer = null;
}

function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

function showError(message) {
    showNotification(message, 'error');
}

function showSuccess(message) {
    showNotification(message, 'success');
}

function showNotification(message, type = 'info') {
    // create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas ${type === 'error' ? 'fa-exclamation-triangle' : 
                      type === 'success' ? 'fa-check-circle' : 'fa-info-circle'}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="notification-close">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // add to page
    document.body.appendChild(notification);
    
    // auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// utility functions
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

function formatCurrency(amount) {
    if (amount >= 1000) {
        return `€${(amount/1000).toFixed(1)}M`;
    } else {
        return `€${amount.toFixed(1)}M`;
    }
}