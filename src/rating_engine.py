import numpy as np
from src.database import get_barcelona_squad, get_cached_rating, cache_transfer_rating
from src.analyzer import SquadAnalyzer
from config import Config

class TransferRatingEngine:
    def __init__(self):
        self.weights = {
            'performance': Config.PERFORMANCE_WEIGHT,
            'value': Config.VALUE_WEIGHT,
            'tactical_fit': Config.TACTICAL_FIT_WEIGHT,
            'age_potential': Config.AGE_POTENTIAL_WEIGHT,
            'squad_role': Config.SQUAD_ROLE_WEIGHT
        }
        self.squad_analyzer = SquadAnalyzer()
        
    def rate_transfer(self, player):
        """main transfer rating function - returns rating out of 5 stars"""
        # check for cached rating
        cached = get_cached_rating(player['name'])
        if cached:
            return self._format_rating_response(cached)
        
        # calculate individual scores
        performance_score = self._calculate_performance_score(player)
        value_score = self._calculate_value_score(player)
        tactical_fit_score = self._calculate_tactical_fit_score(player)
        age_potential_score = self._calculate_age_potential_score(player)
        squad_role_score = self._calculate_squad_role_score(player)
        
        # weighted overall score
        overall_score = (
            performance_score * self.weights['performance'] +
            value_score * self.weights['value'] +
            tactical_fit_score * self.weights['tactical_fit'] +
            age_potential_score * self.weights['age_potential'] +
            squad_role_score * self.weights['squad_role']
        )
        
        # convert to 5-star rating
        star_rating = min(5.0, max(1.0, overall_score))
        
        # generate justification
        justification = self._generate_justification(
            player, star_rating, performance_score, value_score, 
            tactical_fit_score, age_potential_score, squad_role_score
        )
        
        # prepare result
        rating_data = {
            'player_name': player['name'],
            'rating': round(star_rating, 1),
            'performance_score': round(performance_score, 2),
            'value_score': round(value_score, 2),
            'tactical_fit_score': round(tactical_fit_score, 2),
            'age_potential_score': round(age_potential_score, 2),
            'squad_role_score': round(squad_role_score, 2),
            'justification': justification
        }
        
        # cache the result
        cache_transfer_rating(player['name'], rating_data)
        
        return self._format_rating_response(rating_data)
    
    def _calculate_performance_score(self, player):
        """rate player's current performance (0-5)"""
        # normalize stats based on position
        position = player.get('position', '').lower()
        
        base_score = 2.5  # average performance
        
        # goals and assists (scaled by position importance)
        goals = player.get('goals', 0)
        assists = player.get('assists', 0)
        
        if any(pos in position for pos in ['st', 'cf', 'lw', 'rw']):
            # attacking players - goals more important
            attack_contribution = goals * 0.15 + assists * 0.1
        elif any(pos in position for pos in ['am', 'cm']):
            # midfielders - balanced contribution  
            attack_contribution = goals * 0.1 + assists * 0.15
        else:
            # defenders/gk - assists slightly weighted
            attack_contribution = goals * 0.05 + assists * 0.08
        
        base_score += attack_contribution
        
        # minutes played (consistency factor)
        minutes = player.get('minutes_played', 0)
        if minutes > 2000:  # regular starter
            base_score += 0.5
        elif minutes > 1500:  # frequent player
            base_score += 0.3
        elif minutes > 1000:  # rotation player
            base_score += 0.1
        
        # technical stats bonus
        pass_completion = player.get('pass_completion', 80)
        if pass_completion > 90:
            base_score += 0.3
        elif pass_completion > 85:
            base_score += 0.2
        
        # position-specific bonuses
        if position == 'gk':
            # goalkeepers - different calculation
            base_score = 3.0  # assume decent if playing regularly
        
        return min(5.0, max(1.0, base_score))
    
    def _calculate_value_score(self, player):
        """rate transfer value proposition (0-5)"""
        market_value = player.get('market_value', 0)
        age = player.get('age', 25)
        
        # estimate transfer fee (typically 20-50% above market value)
        estimated_fee = market_value * 1.3
        
        # value brackets (in millions)
        if estimated_fee <= 10:
            fee_score = 5.0  # excellent value
        elif estimated_fee <= 25:
            fee_score = 4.0  # good value
        elif estimated_fee <= 50:
            fee_score = 3.0  # fair value
        elif estimated_fee <= 80:
            fee_score = 2.0  # expensive
        else:
            fee_score = 1.0  # very expensive
        
        # age factor - younger players better long-term value
        if age <= 23:
            age_factor = 1.2  # young talent bonus
        elif age <= 27:
            age_factor = 1.0  # prime years
        elif age <= 30:
            age_factor = 0.9  # experienced
        else:
            age_factor = 0.7  # aging
        
        value_score = fee_score * age_factor
        
        return min(5.0, max(1.0, value_score))
    
    def _calculate_tactical_fit_score(self, player):
        """rate tactical fit with barcelona's system (0-5)"""
        base_score = 3.0  # neutral fit
        
        # barcelona prefers technical players
        pass_completion = player.get('pass_completion', 80)
        dribbles = player.get('dribbles_completed', 1)
        key_passes = player.get('key_passes', 1)
        
        # technical ability bonus
        if pass_completion > 88:
            base_score += 0.5
        elif pass_completion > 85:
            base_score += 0.3
        
        if dribbles > 2.0:
            base_score += 0.3
        elif dribbles > 1.5:
            base_score += 0.2
        
        if key_passes > 2.0:
            base_score += 0.3
        elif key_passes > 1.5:
            base_score += 0.2
        
        # position-specific tactical fit
        position = player.get('position', '').lower()
        
        if any(pos in position for pos in ['cm', 'am']):
            # midfielders are crucial in barcelona's system
            base_score += 0.3
        elif position == 'cb':
            # ball-playing center backs preferred
            base_score += 0.2
        
        # la liga experience bonus (already adapted to spanish football)
        base_score += 0.4
        
        return min(5.0, max(1.0, base_score))
    
    def _calculate_age_potential_score(self, player):
        """rate age and potential (0-5)"""
        age = player.get('age', 25)
        
        # age curve for potential
        if age <= 21:
            return 5.0  # huge potential
        elif age <= 24:
            return 4.5  # high potential  
        elif age <= 27:
            return 4.0  # prime years
        elif age <= 29:
            return 3.5  # still good
        elif age <= 32:
            return 2.5  # declining
        else:
            return 1.5  # limited future
    
    def _calculate_squad_role_score(self, player):
        """rate potential squad role and playing time (0-5)"""
        position = player.get('position', '')
        
        # get current squad analysis
        squad_analysis = self.squad_analyzer.analyze_squad()
        priorities = squad_analysis['priorities']
        position_analysis = squad_analysis['position_analysis']
        
        base_score = 3.0
        
        # check if player's position is a priority
        player_group = self._get_position_group(position)
        
        for priority in priorities:
            if priority['position'] == player_group:
                if priority['urgency'] == 'high':
                    base_score += 1.5
                elif priority['urgency'] == 'medium':
                    base_score += 1.0
                break
        
        # check current depth in position
        if player_group in position_analysis:
            current_strength = position_analysis[player_group]['strength_rating']
            if current_strength < 5:
                base_score += 0.8  # high playing time likely
            elif current_strength < 7:
                base_score += 0.4  # decent playing time
            # else competition for places
        
        return min(5.0, max(1.0, base_score))
    
    def _get_position_group(self, position):
        """map specific position to position group"""
        position = position.lower()
        
        for group, positions in Config.POSITION_GROUPS.items():
            if any(pos in position for pos in positions):
                if group == 'gk':
                    return 'goalkeepers'
                elif group == 'def':
                    return 'defenders'
                elif group == 'mid':
                    return 'midfielders'
                elif group == 'att':
                    return 'forwards'
        
        return 'midfielders'  # default
    
    def _generate_justification(self, player, rating, perf_score, value_score, 
                               fit_score, age_score, role_score):
        """generate detailed justification for the rating"""
        
        # star rating description
        if rating >= 4.5:
            rating_desc = "excellent signing"
        elif rating >= 4.0:
            rating_desc = "very good signing"
        elif rating >= 3.5:
            rating_desc = "solid signing"
        elif rating >= 3.0:
            rating_desc = "decent option"
        elif rating >= 2.5:
            rating_desc = "questionable signing"
        else:
            rating_desc = "poor signing"
        
        justification_parts = [f"this would be a {rating_desc}"]
        
        # performance analysis
        if perf_score >= 4.0:
            justification_parts.append("excellent current form and statistics")
        elif perf_score >= 3.5:
            justification_parts.append("strong recent performances")
        elif perf_score >= 3.0:
            justification_parts.append("decent current performance levels")
        else:
            justification_parts.append("concerns about recent form")
        
        # value analysis
        market_value = player.get('market_value', 0)
        if value_score >= 4.0:
            justification_parts.append(f"excellent value at ~€{market_value}m market value")
        elif value_score >= 3.5:
            justification_parts.append(f"good value proposition at current market rate")
        elif value_score >= 3.0:
            justification_parts.append(f"fairly priced transfer")
        else:
            justification_parts.append(f"expensive option that may not justify the cost")
        
        # tactical fit
        if fit_score >= 4.0:
            justification_parts.append("perfect fit for barcelona's playing style")
        elif fit_score >= 3.5:
            justification_parts.append("good tactical compatibility with possession-based system")
        elif fit_score >= 3.0:
            justification_parts.append("should adapt well to barcelona's approach")
        else:
            justification_parts.append("may struggle to adapt to barcelona's tactical demands")
        
        # age and potential
        age = player.get('age', 25)
        if age_score >= 4.0:
            if age <= 23:
                justification_parts.append(f"at {age}, offers significant future potential")
            else:
                justification_parts.append(f"at {age}, in prime years with room to improve")
        elif age_score >= 3.0:
            justification_parts.append(f"good age profile at {age} years old")
        else:
            justification_parts.append(f"age ({age}) limits long-term value")
        
        # squad role
        if role_score >= 4.0:
            justification_parts.append("would likely be a regular starter")
        elif role_score >= 3.5:
            justification_parts.append("good chance of significant playing time")
        elif role_score >= 3.0:
            justification_parts.append("decent squad role with rotation opportunities")
        else:
            justification_parts.append("may struggle for playing time")
        
        return ". ".join(justification_parts) + "."
    
    def _format_rating_response(self, rating_data):
        """format rating response for api"""
        return {
            'player': rating_data['player_name'],
            'overall_rating': rating_data['rating'],
            'star_rating': "⭐" * int(rating_data['rating']) + ("½" if rating_data['rating'] % 1 >= 0.5 else ""),
            'breakdown': {
                'performance': rating_data['performance_score'],
                'value': rating_data['value_score'], 
                'tactical_fit': rating_data['tactical_fit_score'],
                'age_potential': rating_data['age_potential_score'],
                'squad_role': rating_data['squad_role_score']
            },
            'justification': rating_data['justification'],
            'recommendation': self._get_recommendation(rating_data['rating'])
        }
    
    def _get_recommendation(self, rating):
        """get transfer recommendation based on rating"""
        if rating >= 4.0:
            return "strongly recommend"
        elif rating >= 3.5:
            return "recommend"
        elif rating >= 3.0:
            return "consider"
        elif rating >= 2.5:
            return "proceed with caution"
        else:
            return "do not recommend"