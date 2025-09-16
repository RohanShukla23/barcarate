const express = require('express');
const { searchLaLigaPlayers } = require('../services/playersService');

const router = express.Router();

// search for la liga players
router.get('/search', async (req, res) => {
  try {
    const { query, position, team } = req.query;
    
    if (!query || query.length < 2) {
      return res.status(400).json({ 
        error: 'query parameter required (min 2 characters)' 
      });
    }

    const players = await searchLaLigaPlayers(query, position, team);
    res.json(players);
  } catch (error) {
    console.error('error searching players:', error);
    res.status(500).json({ 
      error: 'failed to search players', 
      message: error.message 
    });
  }
});

module.exports = router;