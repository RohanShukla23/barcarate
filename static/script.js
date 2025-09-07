// barcarate frontend javascript

document.addEventListener('DOMContentLoaded', function() {
    const playerInput = document.getElementById('player-input');
    const searchResults = document.getElementById('search-results');
    const ratingResult = document.getElementById('rating-result');
    const loadingOverlay = document.getElementById('loading-overlay');
    
    let searchTimeout;
    let currentPlayers = [];
    
    // player search with autocomplete
    playerInput.addEventListener('input', function() {
        const query = this.value.trim();
        
        // clear previous timeout
        clearTimeout(searchTimeout);
        
        if (query.length < 2) {
            hideSearchResults();
            return;
        }
        
        // debounce search requests
        searchTimeout = setTimeout(() => {
            searchPlayers(query);
        }, 300);
    });
    
    // hide search results when clicking outside
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.player-search')) {
            hideSearchResults();
        }
    });
    
    // search players via api
    async function searchPlayers(query) {
        try {
            const response = await fetch(`/api/players/search?q=${encodeURIComponent(query)}`);
            const players = await response.json();
            
            currentPlayers = players;
            displaySearchResults(players);
        } catch (error) {
            console.error('error searching players:', error);
            hideSearchResults();
        }
    }
    
    // display search results
    function displaySearchResults(players) {
        searchResults.innerHTML = '';
        
        if (players.length === 0) {
            searchResults.innerHTML = '<div class="search-result-item">no players found</div>';
            showSearchResults();
            return;
        }
        
        players.forEach(player => {
            const item = document.createElement('div');
            item.className = 'search-result-item';
            item.innerHTML = `
                <div class="player-info">
                    <div class="player-name">${player.name}</div>
                    <div class="player-details">${player.team} • ${formatPosition(player.position)} • ${player.age}y</div>
                </div>
            `;
            
            item.addEventListener('click', () => {
                playerInput.value = player.name;
                hideSearchResults();
                rateTransfer(player.name);
            });
            
            searchResults.appendChild(item);
        });
        
        showSearchResults();
    }
    
    function showSearchResults() {
        searchResults.style.display = 'block';
    }
    
    function hideSearchResults() {
        searchResults.style.display = 'none';
    }
    
    // rate transfer
    async function rateTransfer(playerName) {
        showLoading();
        
        try {
            const response = await fetch('/api/rate-transfer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    player_name: playerName
                })
            });
            
            if (!response.ok) {
                throw new Error(`http error! status: ${response.status}`);
            }
            
            const rating = await response.json();
            displayRatingResult(rating);
            
        } catch (error) {
            console.error('error rating transfer:', error);
            displayError('failed to rate transfer. please try again.');
        } finally {
            hideLoading();
        }
    }
    
    // display rating result
    function displayRatingResult(rating) {
        const recommendationClass = getRecommendationClass(rating.recommendation);
        
        ratingResult.innerHTML = `
            <div class="rating-header">
                <div class="player-card">
                    <h3>${rating.player}</h3>
                    <div class="overall-rating">${rating.overall_rating}</div>
                    <div class="star-rating">${rating.star_rating}</div>
                    <div class="recommendation ${recommendationClass}">
                        ${rating.recommendation}
                    </div>
                </div>
            </div>
            
            <div class="rating-breakdown">
                <div class="breakdown-item">
                    <div class="breakdown-label">performance</div>
                    <div class="breakdown-score">${rating.breakdown.performance}</div>
                </div>
                <div class="breakdown-item">
                    <div class="breakdown-label">value</div>
                    <div class="breakdown-score">${rating.breakdown.value}</div>
                </div>
                <div class="breakdown-item">
                    <div class="breakdown-label">tactical fit</div>
                    <div class="breakdown-score">${rating.breakdown.tactical_fit}</div>
                </div>
                <div class="breakdown-item">
                    <div class="breakdown-label">age/potential</div>
                    <div class="breakdown-score">${rating.breakdown.age_potential}</div>
                </div>
                <div class="breakdown-item">
                    <div class="breakdown-label">squad role</div>
                    <div class="breakdown-score">${rating.breakdown.squad_role}</div>
                </div>
            </div>
            
            <div class="justification">
                <h4>analysis:</h4>
                <p>${rating.justification}</p>
            </div>
        `;
        
        ratingResult.style.display = 'block';
        
        // scroll to results
        ratingResult.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
    }
    
    // display error message
    function displayError(message) {
        ratingResult.innerHTML = `
            <div class="error-message">
                <h3>error</h3>
                <p>${message}</p>
            </div>
        `;
        ratingResult.style.display = 'block';
    }
    
    // get recommendation css class
    function getRecommendationClass(recommendation) {
        const classes = {
            'strongly recommend': 'recommend-strongly',
            'recommend': 'recommend',
            'consider': 'consider',
            'proceed with caution': 'caution',
            'do not recommend': 'not-recommend'
        };
        
        return classes[recommendation] || 'consider';
    }
    
    // format position display
    function formatPosition(position) {
        const positionMap = {
            'gk': 'goalkeeper',
            'cb': 'centre-back',
            'lb': 'left-back',
            'rb': 'right-back',
            'dm': 'defensive midfielder',
            'cm': 'central midfielder',
            'am': 'attacking midfielder',
            'lw': 'left winger',
            'rw': 'right winger',
            'st': 'striker',
            'cf': 'centre-forward'
        };
        
        return positionMap[position.toLowerCase()] || position;
    }
    
    // loading functions
    function showLoading() {
        loadingOverlay.style.display = 'flex';
    }
    
    function hideLoading() {
        loadingOverlay.style.display = 'none';
    }
    
    // keyboard navigation for search results
    playerInput.addEventListener('keydown', function(event) {
        const items = searchResults.querySelectorAll('.search-result-item');
        const currentFocus = searchResults.querySelector('.search-result-item.focused');
        
        if (event.key === 'ArrowDown') {
            event.preventDefault();
            
            if (currentFocus) {
                currentFocus.classList.remove('focused');
                const next = currentFocus.nextElementSibling;
                if (next) {
                    next.classList.add('focused');
                } else {
                    items[0]?.classList.add('focused');
                }
            } else {
                items[0]?.classList.add('focused');
            }
        } else if (event.key === 'ArrowUp') {
            event.preventDefault();
            
            if (currentFocus) {
                currentFocus.classList.remove('focused');
                const prev = currentFocus.previousElementSibling;
                if (prev) {
                    prev.classList.add('focused');
                } else {
                    items[items.length - 1]?.classList.add('focused');
                }
            } else {
                items[items.length - 1]?.classList.add('focused');
            }
        } else if (event.key === 'Enter') {
            event.preventDefault();
            
            if (currentFocus) {
                currentFocus.click();
            } else if (items.length === 1) {
                items[0].click();
            }
        } else if (event.key === 'Escape') {
            hideSearchResults();
        }
    });
    
    // add focused styling
    const style = document.createElement('style');
    style.textContent = `
        .search-result-item.focused {
            background: #e3f2fd !important;
            border-left: 4px solid #004d98;
        }
    `;
    document.head.appendChild(style);
    
    // update data function (for manual refresh)
    window.updateData = async function() {
        showLoading();
        
        try {
            const response = await fetch('/api/update-data', {
                method: 'POST'
            });
            
            const result = await response.json();
            
            if (result.status === 'success') {
                alert('data updated successfully!');
                location.reload();
            } else {
                alert('error updating data: ' + result.message);
            }
        } catch (error) {
            console.error('error updating data:', error);
            alert('failed to update data');
        } finally {
            hideLoading();
        }
    };
});