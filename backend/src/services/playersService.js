const { fetchFromFootballAPI } = require('../utils/apiClient');

// la liga league id
const LA_LIGA_ID = 140;
const CURRENT_SEASON = 2024;

// major la liga teams for filtering
const LA_LIGA_TEAMS = {
  529: 'Barcelona',
  541: 'Real Madrid', 
  530: 'Atlético Madrid',
  532: 'Valencia',
  533: 'Sevilla',
  536: 'Athletic Bilbao',
  531: 'Real Sociedad',
  538: 'Celta Vigo',
  540: 'Espanyol',
  542: 'Alavés',
  543: 'Real Betis',
  546: 'Getafe',
  547: 'Girona',
  715: 'Granada',
  724: 'Cádiz',
  797: 'Las Palmas',
  728: 'Rayo Vallecano',
  539: 'Levante',
  548: 'Real Valladolid',
  727: 'Osasuna'
};

async function searchLaLigaPlayers(query, position, team) {
  try {
    // search players by name
    const searchResults = await fetchFromFootballAPI(`/players?search=${encodeURIComponent(query)}&league=${LA_LIGA_ID}&season=${CURRENT_SEASON}`);
    
    if (!searchResults.response) {
      return [];
    }

    let players = searchResults.response.map(result => {
      const player = result.player;
      const stats = result.statistics[0] || {}; // first team stats
      
      return {
        id: player.id,
        name: player.name,
        age: player.age,
        nationality: player.nationality,
        photo: player.photo,
        position: stats.games?.position || 'Unknown',
        team: {
          id: stats.team?.id,
          name: stats.team?.name,
          logo: stats.team?.logo
        },
        rating: calculatePlayerRating(stats, player.age),
        marketValue: estimateMarketValue(stats, player.age),
        stats: extractKeyStats(stats),
        isBarcelona: stats.team?.id === 529
      };
    });

    // filter by position if specified
    if (position && position !== 'all') {
      players = players.filter(p => 
        p.position.toLowerCase().includes(position.toLowerCase())
      );
    }

    // filter by team if specified
    if (team && team !== 'all') {
      players = players.filter(p => 
        p.team.name?.toLowerCase().includes(team.toLowerCase())
      );
    }

    // exclude barcelona players from transfers
    players = players.filter(p => !p.isBarcelona);

    // sort by rating (best first)
    return players
      .sort((a, b) => b.rating - a.rating)
      .slice(0, 20); // limit results
      
  } catch (error) {
    console.error('error searching players:', error);
    throw error;
  }
}

function calculatePlayerRating(stats, age) {
  let rating = 65; // base rating
  
  // games played factor (more games = more proven)
  const gamesPlayed = stats.games?.appearences || 0;
  if (gamesPlayed > 20) rating += 10;
  else if (gamesPlayed > 10) rating += 5;
  
  // goals and assists
  const goals = stats.goals?.total || 0;
  const assists = stats.goals?.assists || 0;
  rating += Math.min(15, goals * 0.5 + assists * 0.3);
  
  // pass accuracy for midfielders
  const passAccuracy = stats.passes?.accuracy || 0;
  if (passAccuracy > 85) rating += 5;
  else if (passAccuracy > 75) rating += 2;
  
  // age factor
  if (age >= 22 && age <= 28) rating += 8; // prime years
  else if (age >= 18 && age <= 21) rating += 5; // young talent
  else if (age >= 29 && age <= 32) rating += 3; // experienced
  else if (age > 32) rating -= 3; // declining
  
  // position-specific bonuses
  const position = stats.games?.position?.toLowerCase() || '';
  if (position.includes('forward') || position.includes('attacker')) {
    rating += goals * 0.8; // strikers get more for goals
  } else if (position.includes('midfielder')) {
    rating += assists * 0.6; // midfielders for assists
  } else if (position.includes('defender')) {
    const cleanSheets = stats.goals?.conceded || 0;
    rating += Math.max(0, (gamesPlayed - cleanSheets) * 0.2); // clean sheets
  }
  
  return Math.min(95, Math.max(50, Math.round(rating)));
}

function estimateMarketValue(stats, age) {
  let baseValue = 2000000; // 2M base for la liga players
  
  const gamesPlayed = stats.games?.appearences || 0;
  const goals = stats.goals?.total || 0;
  const assists = stats.goals?.assists || 0;
  
  // performance multiplier
  baseValue *= (1 + (goals * 0.1) + (assists * 0.05) + (gamesPlayed * 0.01));
  
  // age factor
  if (age <= 23) baseValue *= 2.0; // young talent premium
  else if (age <= 26) baseValue *= 1.5;
  else if (age <= 29) baseValue *= 1.2;
  else if (age > 32) baseValue *= 0.6;
  
  // team factor (bigger teams = higher value)
  const teamId = stats.team?.id;
  if ([529, 541, 530].includes(teamId)) { // barca, real, atletico
    baseValue *= 2.0;
  } else if ([532, 533, 536].includes(teamId)) { // valencia, sevilla, athletic
    baseValue *= 1.3;
  }
  
  return Math.round(baseValue);
}

function extractKeyStats(stats) {
  return {
    appearances: stats.games?.appearences || 0,
    goals: stats.goals?.total || 0,
    assists: stats.goals?.assists || 0,
    yellowCards: stats.cards?.yellow || 0,
    redCards: stats.cards?.red || 0,
    passAccuracy: stats.passes?.accuracy || 0,
    rating: stats.games?.rating || '0.0'
  };
}

module.exports = {
  searchLaLigaPlayers
};