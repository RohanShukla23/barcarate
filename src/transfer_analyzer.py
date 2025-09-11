import json
import os
from collections import Counter
from database import PlayerDatabase

class TransferAnalyzer:
    def __init__(self):
        self.db = PlayerDatabase()
        
        # position priorities based on typical barcelona needs
        self.position_priorities = {
            'Defender': 0.8,
            'Centre-Back': 0.9,
            'Right-Back': 0.7,
            'Left-Back': 0.7,
            'Midfielder': 0.6,
            'Defensive Midfield': 0.7,
            'Central Midfield': 0.6,
            'Attacking Midfield': 0.5,
            'Winger': 0.4,
            'Right Winger': 0.4,
            'Left Winger': 0.4,
            'Forward': 0.6,
            'Centre-Forward': 0.8,
            'Goalkeeper': 0.3
        }
        
        # age preferences
        self.ideal_age_range = (22, 28)
        self.acceptable_age_range = (18, 32)
    
    def analyze_barcelona_squad(self):
        """analyze current barcelona squad to identify strengths/weaknesses"""
        if not os.path.exists('data/barcelona_squad.json'):
            return {'error': 'barcelona squad data not available'}
            
        with open('data/barcelona_squad.json', 'r') as f:
            squad = json.load(f)
        
        # analyze by position
        positions = Counter()
        position_quality = {}
        
        for player in squad:
            pos = player['position']
            rating = float(player['rating']) if player['rating'] else 6.0
            
            positions[pos] += 1
            if pos not in position_quality:
                position_quality[pos] = []
            position_quality[pos].append(rating)
        
        # identify weak areas
        weak_positions = []
        strong_positions = []
        
        for pos, count in positions.items():
            avg_rating = sum(position_quality[pos]) / len(position_quality[pos])
            
            analysis = {
                'position': pos,
                'player_count': count,
                'avg_rating': round(avg_rating, 2),
                'priority': self.position_priorities.get(pos, 0.5)
            }
            
            # determine if position needs strengthening
            if count < 2 or avg_rating < 7.0:
                weak_positions.append(analysis)
            else:
                strong_positions.append(analysis)
        
        # sort by priority
        weak_positions.sort(key=lambda x: x['priority'], reverse=True)
        strong_positions.sort(key=lambda x: x['avg_rating'], reverse=True)
        
        return {
            'total_players': len(squad),
            'weak_positions': weak_positions[:5],
            'strong_positions': strong_positions[:3],
            'recommendations': self._generate_recommendations(weak_positions)
        }
    
    def rate_transfer(self, player):
        """rate a potential transfer on 1-5 star scale"""
        if not player:
            return {'stars': 0, 'justification': 'player not found'}
        
        # scoring components
        performance_score = self._rate_performance(player)
        age_score = self._rate_age(player['age'])
        position_score = self._rate_position_need(player['position'])
        value_score = self._rate_value(player)
        
        # weighted final score
        final_score = (
            performance_score * 0.4 +
            position_score * 0.3 +
            age_score * 0.2 +
            value_score * 0.1
        )
        
        stars = max(1, min(5, round(final_score)))
        
        justification = self._generate_justification(
            player, performance_score, age_score, 
            position_score, value_score, stars
        )
        
        return {
            'stars': stars,
            'final_score': round(final_score, 2),
            'performance_score': round(performance_score, 2),
            'age_score': round(age_score, 2),
            'position_score': round(position_score, 2),
            'value_score': round(value_score, 2),
            'justification': justification
        }
    
    def _rate_performance(self, player):
        """rate player performance (1-5)"""
        rating = player['rating']
        games = player['games_played']
        goals = player['goals']
        assists = player['assists']
        
        # base score from player rating
        if rating >= 8.0:
            score = 5.0
        elif rating >= 7.5:
            score = 4.5
        elif rating >= 7.0:
            score = 4.0
        elif rating >= 6.5:
            score = 3.5
        elif rating >= 6.0:
            score = 3.0
        else:
            score = 2.0
            
        # adjust for playing time
        if games < 10:
            score -= 0.5
        elif games > 25:
            score += 0.2
            
        # adjust for attacking contribution
        total_contributions = goals + assists
        if total_contributions > 15:
            score += 0.3
        elif total_contributions > 8:
            score += 0.1
        
        return max(1, min(5, score))
    
    def _rate_age(self, age):
        """rate player age appropriateness (1-5)"""
        if self.ideal_age_range[0] <= age <= self.ideal_age_range[1]:
            return 5.0
        elif self.acceptable_age_range[0] <= age <= self.acceptable_age_range[1]:
            # gradual decline outside ideal range
            if age < self.ideal_age_range[0]:
                return 4.0  # young but promising
            else:
                years_over = age - self.ideal_age_range[1]
                return max(3.0, 5.0 - (years_over * 0.3))
        else:
            return 2.0  # too young or too old
    
    def _rate_position_need(self, position):
        """rate how much barcelona needs this position (1-5)"""
        priority = self.position_priorities.get(position, 0.5)
        return 1 + (priority * 4)  # convert 0-1 to 1-5 scale
    
    def _rate_value(self, player):
        """estimate value for money (1-5)"""
        # simplified value rating based on age and performance
        age = player['age']
        rating = player['rating']
        
        # younger high-performers are better value
        if age <= 25 and rating >= 7.0:
            return 5.0
        elif age <= 30 and rating >= 7.5:
            return 4.0
        elif rating >= 8.0:
            return 4.5
        elif rating >= 6.5:
            return 3.5
        else:
            return 3.0
    
    def _generate_justification(self, player, perf, age, pos, val, stars):
        """generate human-readable justification for rating"""
        name = player['name']
        position = player['position']
        player_age = player['age']
        rating = player['rating']
        
        reasons = []
        
        # performance assessment
        if perf >= 4.5:
            reasons.append(f"excellent performance (rating: {rating})")
        elif perf >= 3.5:
            reasons.append(f"solid performance (rating: {rating})")
        else:
            reasons.append(f"concerning performance stats (rating: {rating})")
        
        # age assessment  
        if age >= 4.5:
            reasons.append(f"ideal age at {player_age}")
        elif age >= 3.5:
            reasons.append(f"acceptable age at {player_age}")
        else:
            reasons.append(f"age concerns at {player_age}")
        
        # position need
        if pos >= 4.0:
            reasons.append(f"high priority position ({position})")
        elif pos >= 3.0:
            reasons.append(f"moderate need at {position}")
        else:
            reasons.append(f"low priority position ({position})")
        
        # overall verdict
        if stars >= 4:
            verdict = f"{name} would be an excellent addition to barcelona. "
        elif stars >= 3:
            verdict = f"{name} could strengthen barcelona's squad. "
        else:
            verdict = f"{name} may not be the ideal fit for barcelona. "
        
        return verdict + " ".join(reasons).capitalize() + "."
    
    def _generate_recommendations(self, weak_positions):
        """generate transfer recommendations based on weak positions"""
        recommendations = []
        
        for pos_info in weak_positions[:3]:  # top 3 priorities
            pos = pos_info['position']
            recommendations.append(
                f"consider strengthening {pos} - currently {pos_info['player_count']} "
                f"players with avg rating {pos_info['avg_rating']}"
            )
        
        return recommendations