const express = require('express');
const { getBarcelonaSquad, analyzeSquad } = require('../services/squadService');

const router = express.Router();

// get current barcelona squad
router.get('/', async (req, res) => {
  try {
    const squad = await getBarcelonaSquad();
    res.json(squad);
  } catch (error) {
    console.error('error fetching squad:', error);
    res.status(500).json({ 
      error: 'failed to fetch squad', 
      message: error.message 
    });
  }
});

// get squad analysis with improvement areas
router.get('/analysis', async (req, res) => {
  try {
    const analysis = await analyzeSquad();
    res.json(analysis);
  } catch (error) {
    console.error('error analyzing squad:', error);
    res.status(500).json({ 
      error: 'failed to analyze squad', 
      message: error.message 
    });
  }
});

module.exports = router;