// Configuration and constants
const CONFIG = {
    API_BASE_URL: window.location.origin,
    DEBOUNCE_DELAY: 300,
    SEARCH_MIN_LENGTH: 2,
    MAX_SEARCH_RESULTS: 30
};

// Barcelona-themed loading messages
const LOADING_MESSAGES = [
    "Analyzing Barcelona DNA compatibility...",
    "Checking tiki-taka potential...",
    "Evaluating Camp Nou readiness...",
    "Assessing Culé worthiness...",
    "Scanning for Messi-like qualities...",
    "Reviewing La Liga adaptation potential..."
];

// Position icons mapping
const POSITION_ICONS = {
    'GK': '🥅',
    'CB': '🛡️',
    'LB': '⬅️',
    'RB': '➡️',
    'DM': '🛡️',
    'CM': '⚽',
    'AM': '🎯',
    'LW': '⬅️',
    'RW': '➡️',
    'ST': '⚽'
};

// Utility functions
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

function getRandomLoadingMessage() {
    return LOADING_MESSAGES[Math.floor(Math.random() * LOADING_MESSAGES.length)];
}

function fadeInElement(element) {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    setTimeout(() => {
        element.style.transition = 'all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
    }, 100);
}