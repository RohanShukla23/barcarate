const { getBarcelonaSquad } = require('./squadService');

async function evaluateTransfer(playerData) {
  try {
    const { playerId, playerName, currentTeam, position, age, rating, marketValue } = playerData;
    
    // get current barcelona squad for comparison
    const squadData = await getBarcelonaSquad();
    const currentPlayers = squadData.players;
    
    // analyze the transfer
    const evaluation = {
      player: {
        id: playerId,
        name: playerName,
        currentTeam: currentTeam || 'Unknown',
        position,
        age,
        rating: rating || 75
      },
      transferRating: 0,
      factors: {
        squadFit: 0,
        value: 0,
        age: 0,
        quality: 0,
        position: 0
      },
      pros: [],
      cons: [],
      recommendation: '',
      estimatedCost: marketValue || estimateTransferCost(age, rating, currentTeam),
      rivalry: checkRivalryFactor(currentTeam)
    };
    
    // evaluate different factors
    evaluation.factors.squadFit = evaluateSquadFit(currentPlayers, position, rating);
    evaluation.factors.value = evaluateValueForMoney(evaluation.estimatedCost, rating, age);
    evaluation.factors.age = evaluateAge(age);
    evaluation.factors.quality = evaluateQuality(rating);
    evaluation.factors.position = evaluatePositionalNeed(currentPlayers, position);
    
    // calculate overall transfer rating
    evaluation.transferRating = calculateOverallRating(evaluation.factors, evaluation.rivalry);
    
    // generate pros and cons
    evaluation.pros = generatePros(evaluation.factors, playerData, evaluation.rivalry);
    evaluation.cons = generateCons(evaluation.factors, playerData, evaluation.rivalry);
    
    // generate recommendation
    evaluation.recommendation = generateRecommendation(evaluation.transferRating, evaluation.factors);
    
    return evaluation;
    
  } catch (error) {
    console.error('error evaluating transfer:', error);
    throw error;
  }
}

function evaluateSquadFit(currentPlayers, position, rating) {
  const positionPlayers = currentPlayers.filter(p => p.position === position);
  const avgPositionRating = positionPlayers.reduce((sum, p) => sum + p.rating, 0) / positionPlayers.length || 70;
  
  // better than average = good fit
  if (rating > avgPositionRating + 10) return 9;
  else if (rating > avgPositionRating + 5) return 8;
  else if (rating > avgPositionRating) return 7;
  else if (rating > avgPositionRating - 5) return 6;
  else return 4;
}

function evaluateValueForMoney(cost, rating, age) {
  // value calculation based on cost vs performance
  const expectedValue = rating * 1000000; // rough baseline
  
  if (cost < expectedValue * 0.5) return 9; // bargain
  else if (cost < expectedValue * 0.7) return 8; // good value
  else if (cost < expectedValue * 1.0) return 7; // fair
  else if (cost < expectedValue * 1.3) return 6; // slightly overpriced
  else if (cost < expectedValue * 1.5) return 5; // overpriced
  else return 3; // very expensive
}

function evaluateAge(age) {
  if (age >= 22 && age <= 26) return 9; // perfect age
  else if (age >= 18 && age <= 29) return 8; // good age
  else if (age >= 30 && age <= 32) return 6; // getting older
  else if (age > 32) return 4; // old
  else return 5; // too young
}

function evaluateQuality(rating) {
  if (rating >= 90) return 10; // world class
  else if (rating >= 85) return 9; // excellent
  else if (rating >= 80) return 8; // very good
  else if (rating >= 75) return 7; // good
  else if (rating >= 70) return 6; // decent
  else return 4; // below standard
}

function evaluatePositionalNeed(currentPlayers, position) {
  const positionPlayers = currentPlayers.filter(p => p.position === position);
  const topRatedInPosition = Math.max(...positionPlayers.map(p => p.rating), 0);
  
  if (positionPlayers.length < 2) return 9; // high need
  else if (topRatedInPosition < 75) return 8; // quality needed
  else if (topRatedInPosition < 80) return 7; // could improve
  else if (positionPlayers.length < 3) return 6; // depth needed
  else return 5; // position well covered
}

function calculateOverallRating(factors, rivalry) {
  const weights = {
    squadFit: 0.25,
    value: 0.20,
    age: 0.15,
    quality: 0.25,
    position: 0.15
  };
  
  let rating = 0;
  Object.keys(weights).forEach(factor => {
    rating += factors[factor] * weights[factor];
  });
  
  // rivalry penalty for real madrid players
  if (rivalry.isRival) rating -= 1.5;
  
  return Math.round(rating * 10) / 10;
}

function generatePros(factors, playerData, rivalry) {
  const pros = [];
  
  if (factors.quality >= 8) pros.push('exceptional player quality');
  if (factors.squadFit >= 8) pros.push('would improve current squad significantly');
  if (factors.age >= 8) pros.push('excellent age profile for long-term investment');
  if (factors.value >= 8) pros.push('great value for money');
  if (factors.position >= 8) pros.push('addresses key squad weakness');
  
  // special cases
  if (playerData.age <= 23 && factors.quality >= 7) {
    pros.push('young talent with high potential');
  }
  
  if (rivalry.isRival && factors.quality >= 8) {
    pros.push('weakens direct rival while strengthening barcelona');
  }
  
  if (pros.length === 0) {
    pros.push('would add squad depth');
  }
  
  return pros;
}

function generateCons(factors, playerData, rivalry) {
  const cons = [];
  
  if (factors.quality <= 6) cons.push('questionable player quality for barcelona standard');
  if (factors.value <= 5) cons.push('overpriced for the quality offered');
  if (factors.age <= 5) cons.push('age concerns - limited long-term value');
  if (factors.position <= 5) cons.push('position already well covered in squad');
  
  // special cases
  if (playerData.age >= 32) cons.push('declining years ahead');
  if (rivalry.isRival) cons.push('potential fan backlash due to rivalry');
  if (factors.squadFit <= 6) cons.push('may struggle to break into first team');
  
  // financial concerns
  if (playerData.estimatedCost > 100000000) {
    cons.push('extremely high transfer fee could impact other signings');
  }
  
  if (cons.length === 0) {
    cons.push('minimal obvious drawbacks');
  }
  
  return cons;
}

function generateRecommendation(rating, factors) {
  if (rating >= 8.5) {
    return 'highly recommended - excellent signing that would significantly strengthen the squad';
  } else if (rating >= 7.5) {
    return 'recommended - good addition that addresses squad needs';
  } else if (rating >= 6.5) {
    return 'consider - decent option but explore alternatives first';
  } else if (rating >= 5.5) {
    return 'not recommended - significant concerns outweigh benefits';
  } else {
    return 'avoid - poor value and unlikely to improve the squad';
  }
}

function estimateTransferCost(age, rating, currentTeam) {
  let baseCost = rating * 1200000; // base calculation
  
  // age adjustments
  if (age <= 23) baseCost *= 1.8;
  else if (age <= 26) baseCost *= 1.4;
  else if (age <= 29) baseCost *= 1.1;
  else if (age >= 32) baseCost *= 0.7;
  
  // team adjustments
  if (currentTeam?.toLowerCase().includes('real madrid')) baseCost *= 2.5; // clasico tax
  else if (currentTeam?.toLowerCase().includes('atletico')) baseCost *= 1.8;
  else if (['sevilla', 'valencia', 'athletic'].some(team => 
    currentTeam?.toLowerCase().includes(team))) {
    baseCost *= 1.3;
  }
  
  return Math.round(baseCost);
}

function checkRivalryFactor(currentTeam) {
  const isRealMadrid = currentTeam?.toLowerCase().includes('real madrid');
  
  return {
    isRival: isRealMadrid,
    rivalryLevel: isRealMadrid ? 'maximum' : 'none',
    description: isRealMadrid ? 
      'el clasico rivalry - historically contentious transfer' : 
      'no significant rivalry concerns'
  };
}

module.exports = {
  evaluateTransfer
};