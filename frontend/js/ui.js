// UI Components and rendering functions
const UI = {
    // Squad analysis display
    displaySquadAnalysis(analysis) {
        let html = `
            <div class="metrics-grid fade-in">
                <div class="metric-card">
                    <div class="metric-value">${analysis.metrics.total_players}</div>
                    <div class="metric-label">Squad Size</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${analysis.metrics.average_age}</div>
                    <div class="metric-label">Average Age</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${analysis.metrics.average_rating}</div>
                    <div class="metric-label">Average Rating</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">€${(analysis.metrics.total_value / 1000000).toFixed(0)}M</div>
                    <div class="metric-label">Total Value</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${analysis.metrics.young_players}</div>
                    <div class="metric-label">Young Talents (&lt;23)</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${analysis.metrics.veteran_players}</div>
                    <div class="metric-label">Experienced (30+)</div>
                </div>
            </div>
        `;

        if (analysis.priority_positions && analysis.priority_positions.length > 0) {
            html += `
                <div class="priority-positions">
                    <div class="priority-title">
                        <i class="fas fa-target"></i>
                        Transfer Priority Positions
                    </div>
                    <div class="priority-list">
                        ${analysis.priority_positions.map(pos => `<div class="priority-tag">${pos}</div>`).join('')}
                    </div>
                </div>
            `;
        }

        if (analysis.weaknesses.length > 0) {
            html += `
                <div class="section-header" style="margin-top: 2.5rem;">
                    <div class="section-icon">
                        <i class="fas fa-exclamation-triangle"></i>
                    </div>
                    <h3 class="section-title">Areas for Improvement</h3>
                </div>
                <div class="weaknesses-list fade-in">
            `;
            
            analysis.weaknesses.forEach(weakness => {
                const icons = {
                    'goalkeeper_quality': '🥅',
                    'goalkeeper_depth': '🥅',
                    'aging_squad': '👴',
                    'critical_aging': '⏰',
                    'striker_depth': '⚽',
                    'striker_aging': '⏳',
                    'cb_depth': '🛡️',
                    'cb_future': '🔮',
                    'dm_depth': '🛡️',
                    'dm_quality': '💎',
                    'fullback_depth': '↔️',
                    'defensive_quality': '⚠️',
                    'midfield_quality': '⚠️'
                };
                
                html += `
                    <div class="weakness-item">
                        <div class="weakness-icon">${icons[weakness] || '⚠'}</div>
                        <div class="weakness-text">${analysis.descriptions[weakness]}</div>
                    </div>
                `;
            });
            
            html += '</div>';
        } else {
            html += `
                <div class="section-header" style="margin-top: 2.5rem;">
                    <div class="section-icon" style="background: var(--success);">
                        <i class="fas fa-check"></i>
                    </div>
                    <h3 class="section-title">Squad Status</h3>
                </div>
                <div class="success-state">
                    ✅ Squad analysis shows Barcelona is in excellent shape with no major weaknesses identified!
                </div>
            `;
        }

        document.getElementById('squadAnalysis').innerHTML = html;
    },

    // Player list display
    displayPlayers(playerList) {
        const container = document.getElementById('playersList');
        
        if (playerList.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">😔</div>
                    <p>No players found matching your criteria. Try adjusting your search!</p>
                </div>
            `;
            return;
        }

        let html = '';
        playerList.forEach((player, index) => {
            // Color code player cards based on their rating
            let cardClass = 'player-card';
            if (player.rating >= 90) cardClass += ' world-class';
            else if (player.rating >= 85) cardClass += ' elite';
            else if (player.rating >= 80) cardClass += ' quality';

            html += `
                <div class="${cardClass} fade-in" onclick="analyzeTransfer(${index})">
                    <div class="player-header">
                        <div>
                            <div class="player-name">${player.name}</div>
                            <div style="font-size: 0.9rem; color: var(--text-secondary); margin-top: 0.4rem; font-weight: 500;">
                                ${player.team}
                            </div>
                        </div>
                        <div class="player-rating">${player.rating}</div>
                    </div>
                    <div class="player-details">
                        <div class="detail-item">
                            <span class="detail-icon">${POSITION_ICONS[player.position] || '⚽'}</span>
                            <span>${player.position}</span>
                        </div>
                        <div class="detail-item">
                            <i class="fas fa-birthday-cake detail-icon"></i>
                            <span>${player.age} years</span>
                        </div>
                        <div class="detail-item">
                            <i class="fas fa-euro-sign detail-icon"></i>
                            <span>€${(player.value / 1000000).toFixed(1)}M</span>
                        </div>
                        <div class="detail-item">
                            <i class="fas fa-flag detail-icon"></i>
                            <span>${player.nationality || 'International'}</span>
                        </div>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    },

    // Transfer analysis display
    displayAnalysis(player, analysis) {
        // Enhanced rating color system based on stringent Barcelona standards
        const ratingColor = analysis.rating >= 9.0 ? '#00ff88' : 
                          analysis.rating >= 8.5 ? '#00cc66' :
                          analysis.rating >= 7.5 ? 'var(--accent)' : 
                          analysis.rating >= 6.5 ? '#ffaa00' :
                          analysis.rating >= 5.5 ? 'var(--warning)' : 
                          analysis.rating >= 4.0 ? '#ff8c42' :
                          'var(--danger)';
        
        const recommendationClass = analysis.recommendation.toLowerCase().replace(/ /g, '-');
        
        let html = `
            <div class="analysis-container slide-in-right">
                <div class="rating-display">
                    <div class="rating-circle" style="--rating: ${analysis.rating}; background: conic-gradient(${ratingColor} 0deg, ${ratingColor} calc(${analysis.rating} * 38deg), var(--surface) calc(${analysis.rating} * 38deg), var(--surface) 360deg);">
                        <div class="rating-inner">
                            <div class="rating-score" style="color: ${ratingColor};">${analysis.rating}</div>
                            <div class="rating-label">Transfer Rating</div>
                            <div class="rating-max">Max: 9.5</div>
                        </div>
                    </div>
                </div>
                
                <div class="recommendation ${recommendationClass}">
                    <strong>${analysis.recommendation}</strong><br>
                    <small>${analysis.recommendation_desc}</small>
                </div>
                
                <div class="analysis-breakdown">
                    <div class="breakdown-item">
                        <div class="breakdown-label">Quality</div>
                        <div class="breakdown-value ${analysis.breakdown.quality >= 0 ? 'positive' : 'negative'}">${analysis.breakdown.quality >= 0 ? '+' : ''}${analysis.breakdown.quality}</div>
                    </div>
                    <div class="breakdown-item">
                        <div class="breakdown-label">Age Impact</div>
                        <div class="breakdown-value ${analysis.breakdown.age_impact >= 0 ? 'positive' : 'negative'}">${analysis.breakdown.age_impact >= 0 ? '+' : ''}${analysis.breakdown.age_impact}</div>
                    </div>
                    <div class="breakdown-item">
                        <div class="breakdown-label">Financial</div>
                        <div class="breakdown-value ${analysis.breakdown.financial_risk >= 0 ? 'positive' : 'negative'}">${analysis.breakdown.financial_risk >= 0 ? '+' : ''}${analysis.breakdown.financial_risk}</div>
                    </div>
                    <div class="breakdown-item">
                        <div class="breakdown-label">Position Need</div>
                        <div class="breakdown-value ${analysis.breakdown.position_need >= 0 ? 'positive' : 'negative'}">${analysis.breakdown.position_need >= 0 ? '+' : ''}${analysis.breakdown.position_need}</div>
                    </div>
                    <div class="breakdown-item">
                        <div class="breakdown-label">Special</div>
                        <div class="breakdown-value ${analysis.breakdown.special_factors >= 0 ? 'positive' : 'negative'}">${analysis.breakdown.special_factors >= 0 ? '+' : ''}${analysis.breakdown.special_factors}</div>
                    </div>
                </div>
                
                <div class="explanation-text">
                    <strong><i class="fas fa-microscope"></i> Barcelona DNA Analysis:</strong> ${analysis.explanation}
                </div>
        `;
        
        if (analysis.risk_factors && analysis.risk_factors.length > 0) {
            html += `
                <div class="risk-factors">
                    <div class="risk-title">
                        <i class="fas fa-exclamation-triangle"></i>
                        Risk Factors to Consider
                    </div>
                    <ul class="risk-list">
                        ${analysis.risk_factors.map(risk => `<li class="risk-item">${risk}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
        
        html += '</div>';
        
        document.getElementById('transferAnalysis').innerHTML = html;
    },

    // Error analysis display
    displayErrorAnalysis(errorData) {
        const html = `
            <div class="analysis-container slide-in-right">
                <div class="recommendation invalid-transfer">
                    <strong>${errorData.recommendation}</strong><br>
                    <small>${errorData.recommendation_desc}</small>
                </div>
                
                <div class="explanation-text">
                    <strong><i class="fas fa-exclamation-circle"></i> Notice:</strong> ${errorData.message}
                </div>
                
                <div style="text-align: center; padding: 2rem; background: var(--surface); border-radius: 20px; color: var(--text-secondary);">
                    <i class="fas fa-info-circle" style="color: var(--accent); margin-right: 0.8rem; font-size: 1.2rem;"></i>
                    Try searching for players from other teams to analyze potential transfer opportunities for FC Barcelona.
                </div>
            </div>
        `;
        
        document.getElementById('transferAnalysis').innerHTML = html;
    },

    // Loading state displays
    showLoading(containerId, message = null) {
        const container = document.getElementById(containerId);
        container.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>${message || getRandomLoadingMessage()}</p>
            </div>
        `;
    },

    showError(containerId, message = 'An error occurred') {
        const container = document.getElementById(containerId);
        container.innerHTML = `<div class="error"><i class="fas fa-exclamation-triangle"></i> ${message}</div>`;
    },

    showEmpty(containerId, message = 'No data available', icon = '📭') {
        const container = document.getElementById(containerId);
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">${icon}</div>
                <p>${message}</p>
            </div>
        `;
    }
};