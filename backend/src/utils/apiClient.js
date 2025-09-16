const axios = require('axios');

const API_BASE_URL = 'https://v3.football.api-sports.io';

// create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'X-RapidAPI-Key': process.env.FOOTBALL_API_KEY,
    'X-RapidAPI-Host': 'v3.football.api-sports.io'
  },
  timeout: 10000 // 10 second timeout
});

async function fetchFromFootballAPI(endpoint) {
  try {
    console.log(`fetching from api: ${endpoint}`);
    const response = await apiClient.get(endpoint);
    
    if (response.data.errors && response.data.errors.length > 0) {
      throw new Error(`api error: ${response.data.errors.join(', ')}`);
    }
    
    return response.data;
  } catch (error) {
    console.error('api request failed:', error.message);
    
    // return mock data if api fails (for development)
    if (process.env.NODE_ENV === 'development') {
      console.log('returning mock data for development');
      return getMockData(endpoint);
    }
    
    throw error;
  }
}

// mock data for development when api is unavailable
function getMockData(endpoint) {
  if (endpoint.includes('squads')) {
    return getMockSquadData();
  } else if (endpoint.includes('players')) {
    return getMockPlayersData();
  }
  
  return { response: [] };
}

function getMockSquadData() {
  return {
    response: [{
      team: {
        id: 529,
        name: 'Barcelona',
        logo: 'https://media.api-sports.io/football/teams/529.png'
      },
      players: [
        {
          id: 1,
          name: 'Robert Lewandowski',
          age: 35,
          position: 'Attacker',
          nationality: 'Poland',
          photo: 'https://media.api-sports.io/football/players/1.png'
        },
        {
          id: 2,
          name: 'Pedri González',
          age: 21,
          position: 'Midfielder',
          nationality: 'Spain',
          photo: 'https://media.api-sports.io/football/players/2.png'
        },
        {
          id: 3,
          name: 'Gavi',
          age: 20,
          position: 'Midfielder',
          nationality: 'Spain',
          photo: 'https://media.api-sports.io/football/players/3.png'
        },
        {
          id: 4,
          name: 'Ronald Araújo',
          age: 25,
          position: 'Defender',
          nationality: 'Uruguay',
          photo: 'https://media.api-sports.io/football/players/4.png'
        },
        {
          id: 5,
          name: 'Marc-André ter Stegen',
          age: 31,
          position: 'Goalkeeper',
          nationality: 'Germany',
          photo: 'https://media.api-sports.io/football/players/5.png'
        }
      ]
    }]
  };
}

function getMockPlayersData() {
  return {
    response: [
      {
        player: {
          id: 101,
          name: 'Vinícius Júnior',
          age: 24,
          nationality: 'Brazil',
          photo: 'https://media.api-sports.io/football/players/101.png'
        },
        statistics: [{
          team: {
            id: 541,
            name: 'Real Madrid',
            logo: 'https://media.api-sports.io/football/teams/541.png'
          },
          games: {
            appearences: 35,
            position: 'Attacker',
            rating: '7.8'
          },
          goals: {
            total: 15,
            assists: 8
          },
          passes: {
            accuracy: 82
          }
        }]
      },
      {
        player: {
          id: 102,
          name: 'Antoine Griezmann',
          age: 33,
          nationality: 'France',
          photo: 'https://media.api-sports.io/football/players/102.png'
        },
        statistics: [{
          team: {
            id: 530,
            name: 'Atlético Madrid',
            logo: 'https://media.api-sports.io/football/teams/530.png'
          },
          games: {
            appearences: 32,
            position: 'Attacker',
            rating: '7.5'
          },
          goals: {
            total: 12,
            assists: 6
          },
          passes: {
            accuracy: 85
          }
        }]
      }
    ]
  };
}

module.exports = {
  fetchFromFootballAPI
};