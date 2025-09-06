"""
transfer analyzer for barcarate
analyzes barcelona squad and provides transfer recommendations
"""

from data.barcelona_squad import barcelona_squad, squad_analysis
from utils.rating_engine import TransferRatingEngine

class TransferAnalyzer:
    def __init__(self):
        self.rating_engine = TransferRatingEngine()
        self.squad = barcelona_squad
        self.analysis = squad_analysis
    
    def analyze_squad_depth(self):
        """analyze current squad depth by position"""
        depth_analysis = {}
        
        # count players by position
        position_counts = {}
        for category in ['goalkeepers', 'defenders', 'midfielders', 'forwards']:
            for player in self.squad[category]:
                if category == 'goalkeepers':
                    pos = 'GK'
                else:
                    pos = player.get('position', 'MF')
                
                position_counts[pos] = position_counts.get(pos, 0) + 1
        
        # evaluate depth quality
        for pos, count in position_counts.items():
            if count >= 3:
                depth = "strong"
            elif count == 2:
                depth = "adequate"
            else:
                depth = "weak"
            
            depth_analysis[pos] = {
                'count': count,
                'depth': depth,
                'priority': self._get_position_priority(pos)
            }
        
        return depth_analysis
    
    def _get_position_priority(self, position):
        """get transfer priority for position"""
        for priority in self.analysis['priority_positions']:
            if priority['position'] == position:
                return priority['urgency']
        return 3  # default medium priority
    
    def get_squad_weaknesses(self):
        """identify key squad weaknesses"""
        weaknesses = []
        depth_analysis = self.analyze_squad_depth()
        
        # check for positions with weak depth
        for pos, data in depth_analysis.items():
            if data['depth'] == 'weak' and data['priority'] >= 6:
                weaknesses.append({
                    'type': 'depth',
                    'position': pos,
                    'severity': 'high',
                    'description': f"Only {data['count']} player(s) at {pos} - immediate reinforcement needed"
                })
            elif data['depth'] == 'adequate' and data['priority'] >= 8:
                weaknesses.append({
                    'type': 'depth',
                    'position': pos,
                    'severity': 'medium',
                    'description': f"Limited depth at {pos} - backup option recommended"
                })
        
        # age-related weaknesses
        aging_players = self._find_aging_players()
        for player in aging_players:
            weaknesses.append({
                'type': 'age',
                'position': player['position'],
                'severity': 'medium',
                'description': f"{player['name']} ({player['age']}) needs long-term replacement planning"
            })
        
        return weaknesses
    
    def _find_aging_players(self):
        """find players who need succession planning"""
        aging_players = []
        age_thresholds = {
            'GK': 33,
            'CB': 32,
            'LB': 30,
            'RB': 30,
            'DM': 31,
            'CM': 30,
            'AM': 29,
            'LW': 29,
            'RW': 29,
            'ST': 32
        }
        
        for category in ['goalkeepers', 'defenders', 'midfielders', 'forwards']:
            for player in self.squad[category]:
                age = player.get('age', 25)
                if category == 'goalkeepers':
                    pos = 'GK'
                else:
                    pos = player.get('position', 'MF')
                
                threshold = age_thresholds.get(pos, 30)
                if age >= threshold:
                    aging_players.append({
                        'name': player['name'],
                        'age': age,
                        'position': pos,
                        'market_value': player.get('market_value', 0)
                    })
        
        return aging_players
    
    def generate_transfer_recommendations(self, laliga_players=None):
        """generate specific player recommendations"""
        if not laliga_players:
            return []
        
        recommendations = []
        weaknesses = self.get_squad_weaknesses()
        
        # for each weakness, find top candidates
        for weakness in weaknesses:
            if weakness['type'] == 'depth' or weakness['type'] == 'age':
                position = weakness['position']
                candidates = [p for p in laliga_players if p.get('position') == position]
                
                # rate each candidate
                rated_candidates = []
                for candidate in candidates[:20]:  # limit for performance
                    if not self._is_already_at_barca(candidate):
                        rating_data = self.rating_engine.calculate_rating(candidate)
                        if rating_data['rating'] >= 3.0:  # only decent+ options
                            rated_candidates.append({
                                'player': candidate,
                                'rating': rating_data
                            })
                
                # sort by rating
                rated_candidates.sort(key=lambda x: x['rating']['rating'], reverse=True)
                
                # add top 3 recommendations for this position
                for candidate in rated_candidates[:3]:
                    recommendations.append({
                        'weakness': weakness,
                        'player': candidate['player'],
                        'rating': candidate['rating'],
                        'priority': weakness['severity']
                    })
        
        return recommendations[:10]  # return top 10 overall
    
    def _is_already_at_barca(self, player):
        """check if player is already at barcelona"""
        player_name = player.get('name', '').lower()
        team = player.get('team', '').lower()
        
        if 'barcelona' in team or 'barça' in team:
            return True
        
        # check against current squad
        all_barca_players = []
        for category in self.squad.values():
            if isinstance(category, list):
                all_barca_players.extend([p['name'].lower() for p in category])
        
        return player_name in all_barca_players
    
    def compare_players(self, players_list):
        """compare multiple players and return ratings"""
        comparisons = []
        
        for player in players_list:
            rating_data = self.rating_engine.calculate_rating(player)
            comparisons.append({
                'player': player,
                'rating': rating_data
            })
        
        # sort by rating
        comparisons.sort(key=lambda x: x['rating']['rating'], reverse=True)
        return comparisons
    
    def get_position_analysis(self, position):
        """detailed analysis of specific position needs"""
        current_players = []
        
        # find current players in position
        for category in ['goalkeepers', 'defenders', 'midfielders', 'forwards']:
            for player in self.squad[category]:
                if category == 'goalkeepers' and position == 'GK':
                    current_players.append(player)
                elif player.get('position') == position:
                    current_players.append(player)
        
        # analyze current situation
        total_players = len(current_players)
        avg_age = sum(p.get('age', 25) for p in current_players) / max(total_players, 1)
        total_value = sum(p.get('market_value', 0) for p in current_players)
        avg_rating = sum(p.get('rating', 7.0) for p in current_players) / max(total_players, 1)
        
        # determine need level
        priority = self._get_position_priority(position)
        
        if total_players <= 1:
            need_level = "critical"
        elif total_players == 2 and priority >= 7:
            need_level = "high"
        elif avg_age >= 30:
            need_level = "medium-term"
        else:
            need_level = "low"
        
        return {
            'position': position,
            'current_players': current_players,
            'count': total_players,
            'average_age': round(avg_age, 1),
            'total_market_value': total_value,
            'average_rating': round(avg_rating, 1),
            'need_level': need_level,
            'priority_score': priority,
            'recommendation': self._get_position_recommendation(position, need_level, avg_age)
        }
    
    def _get_position_recommendation(self, position, need_level, avg_age):
        """get specific recommendation for position"""
        if need_level == "critical":
            return f"Immediate signing required for {position} - less than 2 players available"
        elif need_level == "high":
            return f"High priority to strengthen {position} depth this transfer window"
        elif need_level == "medium-term":
            return f"Plan for {position} renewal - average age {avg_age} requires succession planning"
        else:
            return f"{position} is adequately covered for now"