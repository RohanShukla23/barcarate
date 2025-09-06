"""
transfer rating engine for barcarate
calculates 5-star ratings for potential barcelona signings
"""

import math
from data.barcelona_squad import squad_analysis

class TransferRatingEngine:
    def __init__(self):
        self.max_rating = 5.0
        self.position_weights = {
            'ST': 1.2,  # high priority
            'CB': 1.1,
            'DM': 1.0,
            'RB': 0.9,
            'LB': 0.8,
            'CM': 0.8,
            'AM': 0.8,
            'RW': 0.7,
            'LW': 0.7,
            'GK': 0.6   # low priority
        }
        
        # ideal age ranges for positions
        self.ideal_ages = {
            'GK': (25, 32),
            'CB': (22, 30),
            'LB': (21, 28),
            'RB': (21, 28),
            'DM': (23, 30),
            'CM': (22, 28),
            'AM': (21, 27),
            'LW': (20, 27),
            'RW': (20, 27),
            'ST': (22, 29)
        }
    
    def calculate_rating(self, player, detailed=True):
        """
        calculate comprehensive transfer rating
        returns dict with rating and breakdown
        """
        
        # base components
        need_score = self._calculate_position_need(player)
        performance_score = self._calculate_performance_score(player)
        value_score = self._calculate_value_score(player)
        fit_score = self._calculate_barcelona_fit(player)
        age_score = self._calculate_age_factor(player)
        
        # weighted final score
        weights = {
            'need': 0.25,
            'performance': 0.25,
            'value': 0.20,
            'fit': 0.20,
            'age': 0.10
        }
        
        raw_score = (
            need_score * weights['need'] +
            performance_score * weights['performance'] +
            value_score * weights['value'] +
            fit_score * weights['fit'] +
            age_score * weights['age']
        )
        
        # normalize to 1-5 scale
        final_rating = max(1.0, min(5.0, raw_score))
        
        if detailed:
            return {
                'rating': round(final_rating, 1),
                'stars': self._rating_to_stars(final_rating),
                'breakdown': {
                    'position_need': round(need_score, 2),
                    'performance': round(performance_score, 2),
                    'value_for_money': round(value_score, 2),
                    'barcelona_fit': round(fit_score, 2),
                    'age_factor': round(age_score, 2)
                },
                'justification': self._generate_justification(player, final_rating, {
                    'need': need_score,
                    'performance': performance_score,
                    'value': value_score,
                    'fit': fit_score,
                    'age': age_score
                })
            }
        
        return round(final_rating, 1)
    
    def _calculate_position_need(self, player):
        """calculate how much barcelona needs this position"""
        position = player.get('position', 'MF')
        
        # get position priority from squad analysis
        priority_positions = {p['position']: p['urgency'] for p in squad_analysis['priority_positions']}
        
        urgency = priority_positions.get(position, 3)  # default medium need
        
        # convert urgency (1-10) to score (1-5)
        position_weight = self.position_weights.get(position, 0.8)
        base_score = (urgency / 10.0) * 5.0
        
        return base_score * position_weight
    
    def _calculate_performance_score(self, player):
        """estimate performance based on market value and age"""
        market_value = player.get('market_value', 0)
        age = player.get('age', 25)
        
        # market value indicates performance level
        if market_value >= 80:
            base_performance = 5.0
        elif market_value >= 50:
            base_performance = 4.5
        elif market_value >= 25:
            base_performance = 4.0
        elif market_value >= 10:
            base_performance = 3.5
        elif market_value >= 5:
            base_performance = 3.0
        else:
            base_performance = 2.5
        
        # age adjustment
        if 22 <= age <= 27:
            age_multiplier = 1.0  # prime age
        elif 28 <= age <= 30:
            age_multiplier = 0.95
        elif 21 <= age <= 21:
            age_multiplier = 0.9  # young but promising
        elif 31 <= age <= 33:
            age_multiplier = 0.8
        else:
            age_multiplier = 0.7  # too young or too old
        
        return base_performance * age_multiplier
    
    def _calculate_value_score(self, player):
        """calculate value for money rating"""
        market_value = player.get('market_value', 0)
        age = player.get('age', 25)
        position = player.get('position', 'MF')
        
        # barcelona's financial constraints consideration
        if market_value <= 20:
            affordability = 5.0
        elif market_value <= 40:
            affordability = 4.0
        elif market_value <= 60:
            affordability = 3.0
        elif market_value <= 80:
            affordability = 2.5
        else:
            affordability = 2.0
        
        # value relative to age
        if age <= 25 and market_value <= 30:
            age_value = 5.0  # young and affordable
        elif age <= 27 and market_value <= 50:
            age_value = 4.0
        elif age >= 30 and market_value <= 15:
            age_value = 4.5  # experienced and cheap
        else:
            age_value = 3.0
        
        return (affordability + age_value) / 2.0
    
    def _calculate_barcelona_fit(self, player):
        """calculate how well player fits barcelona's style"""
        position = player.get('position', 'MF')
        nationality = player.get('nationality', '').lower()
        age = player.get('age', 25)
        team = player.get('team', '').lower()
        
        fit_score = 3.0  # base fit
        
        # la liga experience bonus
        fit_score += 0.5
        
        # spanish/catalan players fit better
        if 'spain' in nationality:
            fit_score += 0.8
        elif nationality in ['brazil', 'netherlands', 'france', 'argentina']:
            fit_score += 0.3  # historically good fits
        
        # age preferences for different positions
        ideal_range = self.ideal_ages.get(position, (22, 28))
        if ideal_range[0] <= age <= ideal_range[1]:
            fit_score += 0.4
        elif abs(age - ((ideal_range[0] + ideal_range[1]) / 2)) <= 3:
            fit_score += 0.2
        
        # certain teams play similar style
        similar_style_teams = ['real sociedad', 'villarreal', 'real betis', 'athletic bilbao']
        if any(team_name in team for team_name in similar_style_teams):
            fit_score += 0.3
        
        return min(5.0, fit_score)
    
    def _calculate_age_factor(self, player):
        """calculate age-based rating factor"""
        age = player.get('age', 25)
        position = player.get('position', 'MF')
        
        # different positions have different age curves
        if position == 'GK':
            if 25 <= age <= 32:
                return 5.0
            elif 23 <= age <= 34:
                return 4.0
            else:
                return 3.0
        
        elif position in ['CB', 'DM']:
            if 24 <= age <= 29:
                return 5.0
            elif 22 <= age <= 31:
                return 4.0
            else:
                return 3.0
        
        else:  # attacking positions
            if 22 <= age <= 27:
                return 5.0
            elif 20 <= age <= 29:
                return 4.0
            elif age <= 31:
                return 3.0
            else:
                return 2.0
    
    def _rating_to_stars(self, rating):
        """convert numerical rating to star display"""
        full_stars = int(rating)
        half_star = 1 if rating - full_stars >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star
        
        return '★' * full_stars + ('☆' if half_star else '') + '☆' * empty_stars
    
    def _generate_justification(self, player, rating, scores):
        """generate detailed justification for the rating"""
        name = player.get('name', 'Player')
        position = player.get('position', 'MF')
        age = player.get('age', 25)
        market_value = player.get('market_value', 0)
        nationality = player.get('nationality', 'Unknown')
        team = player.get('team', 'Unknown')
        
        # determine rating category
        if rating >= 4.5:
            category = "Excellent signing"
        elif rating >= 4.0:
            category = "Very good signing"
        elif rating >= 3.5:
            category = "Good signing"
        elif rating >= 3.0:
            category = "Decent option"
        elif rating >= 2.5:
            category = "Risky signing"
        else:
            category = "Poor fit"
        
        justification = f"{category} - "
        
        # position need analysis
        priority_positions = {p['position']: p['urgency'] for p in squad_analysis['priority_positions']}
        if position in priority_positions and priority_positions[position] >= 7:
            justification += f"{name} addresses a crucial need at {position}. "
        elif position in priority_positions:
            justification += f"Barcelona could use depth at {position}. "
        else:
            justification += f"{position} is not a priority position currently. "
        
        # performance analysis
        if scores['performance'] >= 4.0:
            justification += f"At {age}, {name} is at an excellent level (€{market_value}M value reflects strong performances). "
        elif scores['performance'] >= 3.5:
            justification += f"Solid performer with good upside potential. "
        else:
            justification += f"Performance level may not meet Barcelona's standards. "
        
        # value analysis
        if scores['value'] >= 4.0:
            justification += f"Great value at €{market_value}M for a player of this caliber. "
        elif scores['value'] >= 3.0:
            justification += f"Reasonable price considering age and ability. "
        else:
            justification += f"High transfer fee (€{market_value}M) may strain Barcelona's finances. "
        
        # fit analysis
        if scores['fit'] >= 4.0:
            justification += f"Excellent fit for Barcelona's possession-based style, especially with La Liga experience. "
        elif scores['fit'] >= 3.5:
            justification += f"Good tactical fit with Barcelona's system. "
        else:
            justification += f"May need time to adapt to Barcelona's playing style. "
        
        # age factor
        if scores['age'] >= 4.0:
            justification += f"At {age}, offers ideal combination of experience and longevity."
        elif scores['age'] >= 3.0:
            justification += f"Age ({age}) is acceptable for the position."
        else:
            justification += f"Age ({age}) is a concern for long-term planning."
        
        return justification