const { fetchFromFootballAPI } = require('../utils/apiClient');

// barcelona team id in api-football
const BARCELONA_TEAM_ID = 529;
const CURRENT_SEASON = 2024;

async function getBarcelonaSquad() {
  try {
    // fetch squad from api
    const squadData = await fetchFromFootballAPI(`/players/squads?team=${BARCELONA_TEAM_ID}`);
    
    if (!squadData.response || squadData.response.length === 0) {
      throw new Error('no squad data found');
    }

    const squad = squadData.response[0];
    
    // format and enrich player data
    const formattedPlayers = squad.players.map(player => {
      const playerRating = calculatePlayerRating(player);
      return {
        id: player.id,
        name: player.name,
        age: player.age,
        position: player.position,
        nationality: player.nationality,
        photo: player.photo,
        rating: playerRating,
        marketValue: estimateMarketValue(player, playerRating),
        strengths: generatePlayerStrengths(player.position, playerRating),
        weaknesses: generatePlayerWeaknesses(player.position, playerRating)
      };
    });

    return {
      team: {
        id: squad.team.id,
        name: squad.team.name,
        logo: squad.team.logo
      },
      players: formattedPlayers,
      lastUpdated: new Date().toISOString()
    };
  } catch (error) {
    console.error('error in getBarcelonaSquad:', error);
    throw error;
  }
}

async function analyzeSquad() {
  try {
    const squadData = await getBarcelonaSquad();
    const players = squadData.players;
    
    // analyze by position
    const positionAnalysis = analyzeByPosition(players);
    
    // identify improvement areas
    const improvementAreas = identifyWeakAreas(positionAnalysis);
    
    // calculate overall team rating
    const overallRating = calculateTeamRating(players);
    
    return {
      overallRating,
      positionAnalysis,
      improvementAreas,
      totalPlayers: players.length,
      averageAge: calculateAverageAge(players),
      totalValue: calculateTotalValue(players)
    };
  } catch (error) {
    console.error('error in analyzeSquad:', error);
    throw error;
  }
}

function calculatePlayerRating(player) {
  // simplified rating based on age and position
  let baseRating = 75;
  
  // age factor
  if (player.age >= 18 && player.age <= 23) baseRating += 5; // young talent
  else if (player.age >= 24 && player.age <= 29) baseRating += 10; // prime years
  else if (player.age >= 30 && player.age <= 32) baseRating += 5; // experienced
  else if (player.age > 32) baseRating -= 5; // declining
  
  // position adjustments (simplified)
  if (['Goalkeeper'].includes(player.position)) baseRating += 0;
  else if (['Defender'].includes(player.position)) baseRating += 2;
  else if (['Midfielder'].includes(player.position)) baseRating += 5;
  else if (['Attacker'].includes(player.position)) baseRating += 8;
  
  return Math.min(95, Math.max(50, baseRating + Math.random() * 10));
}

function estimateMarketValue(player, rating) {
  // simplified market value calculation
  let baseValue = 1000000; // 1M base
  
  // rating multiplier
  baseValue *= (rating / 70);
  
  // age factor
  if (player.age <= 25) baseValue *= 1.5;
  else if (player.age <= 28) baseValue *= 1.2;
  else if (player.age > 30) baseValue *= 0.8;
  
  return Math.round(baseValue);
}

function generatePlayerStrengths(position, rating) {
  const strengthsByPosition = {
    'Goalkeeper': ['shot stopping', 'distribution', 'commanding area'],
    'Defender': ['tackling', 'aerial ability', 'positioning'],
    'Midfielder': ['passing', 'vision', 'work rate'],
    'Attacker': ['finishing', 'pace', 'dribbling']
  };
  
  const baseStrengths = strengthsByPosition[position] || ['technique', 'physicality'];
  
  // add extra strengths for high-rated players
  if (rating > 85) {
    baseStrengths.push('leadership', 'consistency');
  }
  
  return baseStrengths;
}

function generatePlayerWeaknesses(position, rating) {
  if (rating > 85) return ['minimal weaknesses'];
  
  const weaknessesByPosition = {
    'Goalkeeper': ['distribution under pressure'],
    'Defender': ['pace', 'attacking contribution'],
    'Midfielder': ['defensive work', 'physicality'],
    'Attacker': ['defensive contribution', 'consistency']
  };
  
  return weaknessesByPosition[position] || ['needs development'];
}

function analyzeByPosition(players) {
  const positions = ['Goalkeeper', 'Defender', 'Midfielder', 'Attacker'];
  
  return positions.map(position => {
    const positionPlayers = players.filter(p => p.position === position);
    const avgRating = positionPlayers.reduce((sum, p) => sum + p.rating, 0) / positionPlayers.length || 0;
    
    return {
      position,
      count: positionPlayers.length,
      averageRating: Math.round(avgRating * 10) / 10,
      players: positionPlayers.slice(0, 3), // top 3 players
      needsImprovement: avgRating < 78 || positionPlayers.length < 2
    };
  });
}

function identifyWeakAreas(positionAnalysis) {
  const weakAreas = [];
  
  positionAnalysis.forEach(pos => {
    if (pos.needsImprovement) {
      let reason = '';
      if (pos.averageRating < 75) reason = 'low average rating';
      else if (pos.count < 2) reason = 'insufficient squad depth';
      else reason = 'needs quality improvement';
      
      weakAreas.push({
        position: pos.position,
        priority: pos.averageRating < 70 ? 'high' : 'medium',
        reason,
        suggestion: generatePositionSuggestion(pos.position)
      });
    }
  });
  
  return weakAreas;
}

function generatePositionSuggestion(position) {
  const suggestions = {
    'Goalkeeper': 'consider a reliable backup or young prospect',
    'Defender': 'look for pace and leadership in the backline',
    'Midfielder': 'need creative playmakers or defensive stability',
    'Attacker': 'require clinical finishers and pace on the wings'
  };
  
  return suggestions[position] || 'assess current squad quality';
}

function calculateTeamRating(players) {
  const totalRating = players.reduce((sum, player) => sum + player.rating, 0);
  return Math.round((totalRating / players.length) * 10) / 10;
}

function calculateAverageAge(players) {
  const totalAge = players.reduce((sum, player) => sum + player.age, 0);
  return Math.round((totalAge / players.length) * 10) / 10;
}

function calculateTotalValue(players) {
  return players.reduce((sum, player) => sum + player.marketValue, 0);
}

module.exports = {
  getBarcelonaSquad,
  analyzeSquad
};