// API interaction module
const API = {
    async loadSquadAnalysis() {
        try {
            const response = await axios.get('/api/squad/analysis');
            return response.data;
        } catch (error) {
            console.error('Error loading squad analysis:', error);
            throw error;
        }
    },

    async searchPlayers(params = {}) {
        try {
            const response = await axios.get('/api/players/search', { params });
            return response.data;
        } catch (error) {
            console.error('Error searching players:', error);
            throw error;
        }
    },

    async analyzeTransfer(playerData) {
        try {
            const response = await axios.post('/api/transfer/rate', playerData);
            return response.data;
        } catch (error) {
            console.error('Error analyzing transfer:', error);
            throw error;
        }
    },

    async getTeams() {
        try {
            const response = await axios.get('/api/teams');
            return response.data;
        } catch (error) {
            console.error('Error getting teams:', error);
            throw error;
        }
    },

    async getPlayersByTeam(teamName) {
        try {
            const response = await axios.get(`/api/players/by-team/${teamName}`);
            return response.data;
        } catch (error) {
            console.error('Error getting players by team:', error);
            throw error;
        }
    }
};