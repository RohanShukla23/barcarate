// Main application logic
class BarcaRateApp {
    constructor() {
        this.players = [];
        this.currentAnalysis = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadSquadAnalysis();
    }

    setupEventListeners() {
        // Search event listeners with debouncing
        document.getElementById('playerSearch').addEventListener('input', 
            debounce(() => this.searchPlayers(), CONFIG.DEBOUNCE_DELAY)
        );
        document.getElementById('positionFilter').addEventListener('change', () => this.searchPlayers());
        document.getElementById('maxAge').addEventListener('input', 
            debounce(() => this.searchPlayers(), 500)
        );
        document.getElementById('minRating').addEventListener('input', 
            debounce(() => this.searchPlayers(), 500)
        );

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === '/' && !e.target.matches('input, textarea')) {
                e.preventDefault();
                document.getElementById('playerSearch').focus();
            }
        });
    }

    async loadSquadAnalysis() {
        try {
            UI.showLoading('squadAnalysis', 'Analyzing squad composition for FC Barcelona...');
            const analysis = await API.loadSquadAnalysis();
            UI.displaySquadAnalysis(analysis);
        } catch (error) {
            console.error('Error loading squad analysis:', error);
            UI.showError('squadAnalysis', 'Error loading squad analysis');
        }
    }

    async searchPlayers() {
        const query = document.getElementById('playerSearch').value;
        const position = document.getElementById('positionFilter').value;
        const maxAge = document.getElementById('maxAge').value;
        const minRating = document.getElementById('minRating').value;
        
        // Show empty state if no search criteria
        if (query.length < CONFIG.SEARCH_MIN_LENGTH && !position && !maxAge && !minRating) {
            UI.showEmpty('playersList', 'Enter search criteria to find potential Culés', '🔍');
            return;
        }

        try {
            UI.showLoading('playersList', 'Scouting players worldwide...');
            
            const params = {};
            if (query) params.q = query;
            if (position) params.position = position;
            if (maxAge) params.max_age = maxAge;
            if (minRating) params.min_rating = minRating;
            
            this.players = await API.searchPlayers(params);
            UI.displayPlayers(this.players);
        } catch (error) {
            console.error('Error searching players:', error);
            UI.showError('playersList', 'Error searching players');
        }
    }

    async analyzeTransfer(playerIndex) {
        const player = this.players[playerIndex];
        
        if (!player) {
            console.error('Player not found at index:', playerIndex);
            return;
        }

        try {
            UI.showLoading('transferAnalysis', 'Analyzing Barcelona DNA compatibility...');
            
            const result = await API.analyzeTransfer(player);
            this.currentAnalysis = result;
            
            UI.displayAnalysis(player, result.analysis);
        } catch (error) {
            console.error('Error analyzing transfer:', error);
            
            // Handle the case where player is already at Barcelona
            if (error.response && error.response.status === 400) {
                const errorData = error.response.data;
                if (errorData.error) {
                    UI.displayErrorAnalysis(errorData);
                    return;
                }
            }
            UI.showError('transferAnalysis', 'Error analyzing transfer potential');
        }
    }

    // Initialize tooltips for better UX
    initializeTooltips() {
        const elements = document.querySelectorAll('[title]');
        elements.forEach(el => {
            el.addEventListener('mouseenter', function() {
                // Custom tooltip implementation could go here
            });
        });
    }
}

// Global app instance
let app;

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    app = new BarcaRateApp();
    
    // Initialize tooltips after a delay
    setTimeout(() => {
        app.initializeTooltips();
    }, 1000);
});

// Global functions for onclick handlers (maintaining compatibility)
function searchPlayers() {
    if (app) {
        app.searchPlayers();
    }
}

function analyzeTransfer(playerIndex) {
    if (app) {
        app.analyzeTransfer(playerIndex);
    }
}

// Enhanced error handling with Barcelona flair
window.addEventListener('error', function(e) {
    console.error('BarcaRate Error:', e.error);
    // Optionally show user-friendly error messages
});

// Add smooth transitions for dynamic content
function fadeInElement(element) {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    setTimeout(() => {
        element.style.transition = 'all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
    }, 100);
}