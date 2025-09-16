const express = require('express');
const { evaluateTransfer } = require('../services/transferService');

const router = express.Router();

// evaluate a potential transfer
router.post('/evaluate', async (req, res) => {
  try {
    const { playerId, playerName, currentTeam, position, age, rating } = req.body;
    
    if (!playerId || !playerName) {
      return res.status(400).json({ 
        error: 'playerId and playerName are required' 
      });
    }

    const evaluation = await evaluateTransfer({
      playerId,
      playerName,
      currentTeam,
      position,
      age,
      rating
    });
    
    res.json(evaluation);
  } catch (error) {
    console.error('error evaluating transfer:', error);
    res.status(500).json({ 
      error: 'failed to evaluate transfer', 
      message: error.message 
    });
  }
});

module.exports = router;