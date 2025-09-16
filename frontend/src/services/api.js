import axios from 'axios';

// create axios instance with default config
const api = axios.create({
  baseURL: '/api',
  timeout: 30000, // 30 seconds for api calls
});

// request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`making request to: ${config.url}`);
    return config;
  },
  (error) => {
    console.error('request error:', error);
    return Promise.reject(error);
  }
);

// response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('api error:', error.response?.data || error.message);
    
    // customize error messages
    if (error.code === 'ECONNABORTED') {
      throw new Error('request timed out. please try again.');
    }
    
    if (error.response?.status === 500) {
      throw new Error('server error. please try again later.');
    }
    
    if (error.response?.data?.message) {
      throw new Error(error.response.data.message);
    }
    
    throw new Error('something went wrong. please try again.');
  }
);

// squad related api calls
export const getSquad = async () => {
  try {
    const data = await api.get('/squad');
    return data;
  } catch (error) {
    console.error('failed to fetch squad:', error);
    throw error;
  }
};

export const getSquadAnalysis = async () => {
  try {
    const data = await api.get('/squad/analysis');
    return data;
  } catch (error) {
    console.error('failed to fetch squad analysis:', error);
    throw error;
  }
};

// player search api calls
export const searchPlayers = async (query, position = null, team = null) => {
  try {
    const params = { query };
    if (position) params.position = position;
    if (team) params.team = team;
    
    const data = await api.get('/players/search', { params });
    return data;
  } catch (error) {
    console.error('failed to search players:', error);
    throw error;
  }
};

// transfer evaluation api calls
export const evaluateTransfer = async (playerData) => {
  try {
    const data = await api.post('/transfers/evaluate', playerData);
    return data;
  } catch (error) {
    console.error('failed to evaluate transfer:', error);
    throw error;
  }
};

// health check
export const checkApiHealth = async () => {
  try {
    const data = await api.get('/health');
    return data;
  } catch (error) {
    console.error('api health check failed:', error);
    throw error;
  }
};

export default api;