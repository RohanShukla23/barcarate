import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.rating_engine import TransferRatingEngine

class TestTransferRatingEngine(unittest.TestCase):
    
    def setUp(self):
        self.mock_player = {
            'name': 'test player',
            'team': 'test team',
            'position': 'cm',
            'age': 25,
            'market_value': 30,
            'goals': 5,
            'assists': 8,
            'minutes_played': 2000,
            'pass_completion': 87.5,
            'dribbles_completed': 2.1,
            'tackles_won': 1.8,
            'aerial_duels_won': 65.0,
            'shots_per_game': 1.5,
            'key_passes': 2.3
        }
        
    @patch('src.rating_engine.get_cached_rating')
    @patch('src.rating_engine.get_barcelona_squad')
    def test_rating_engine_initialization(self, mock_get_squad, mock_cached):
        """test rating engine initializes correctly"""
        mock_get_squad.return_value = []
        mock_cached.return_value = None
        
        engine = TransferRatingEngine()
        
        # check weights sum to 1.0
        total_weight = sum(engine.weights.values())
        self.assertAlmostEqual(total_weight, 1.0, places=2)
        
        # check all required weights present
        required_weights = ['performance', 'value', 'tactical_fit', 'age_potential', 'squad_role']
        for weight in required_weights:
            self.assertIn(weight, engine.weights)
    
    @patch('src.rating_engine.cache_transfer_rating')
    @patch('src.rating_engine.get_cached_rating')
    @patch('src.rating_engine.get_barcelona_squad')
    def test_transfer_rating(self, mock_get_squad, mock_cached, mock_cache):
        """test main transfer rating functionality"""
        mock_get_squad.return_value = []
        mock_cached.return_value = None
        mock_cache.return_value = None
        
        engine = TransferRatingEngine()
        result = engine.rate_transfer(self.mock_player)
        
        # check result structure
        required_fields = ['player', 'overall_rating', 'star_rating', 'breakdown', 'justification', 'recommendation']
        for field in required_fields:
            self.assertIn(field, result)
        
        # check rating bounds
        self.assertGreaterEqual(result['overall_rating'], 1.0)
        self.assertLessEqual(result['overall_rating'], 5.0)
        
        # check breakdown scores
        breakdown = result['breakdown']
        for score in breakdown.values():
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 5.0)
    
    @patch('src.rating_engine.get_barcelona_squad')
    def test_performance_score_calculation(self, mock_get_squad):
        """test performance score calculation"""
        mock_get_squad.return_value = []
        
        engine = TransferRatingEngine()
        score = engine._calculate_performance_score(self.mock_player)
        
        self.assertGreaterEqual(score, 1.0)
        self.assertLessEqual(score, 5.0)
        self.assertIsInstance(score, float)
    
    @patch('src.rating_engine.get_barcelona_squad')
    def test_value_score_calculation(self, mock_get_squad):
        """test value score calculation"""
        mock_get_squad.return_value = []
        
        engine = TransferRatingEngine()
        score = engine._calculate_value_score(self.mock_player)
        
        self.assertGreaterEqual(score, 1.0)
        self.assertLessEqual(score, 5.0)
        self.assertIsInstance(score, float)
    
    @patch('src.rating_engine.get_barcelona_squad')
    def test_tactical_fit_score_calculation(self, mock_get_squad):
        """test tactical fit score calculation"""
        mock_get_squad.return_value = []
        
        engine = TransferRatingEngine()
        score = engine._calculate_tactical_fit_score(self.mock_player)
        
        self.assertGreaterEqual(score, 1.0)
        self.assertLessEqual(score, 5.0)
        self.assertIsInstance(score, float)
    
    @patch('src.rating_engine.get_barcelona_squad')
    def test_age_potential_score_calculation(self, mock_get_squad):
        """test age and potential score calculation"""
        mock_get_squad.return_value = []
        
        engine = TransferRatingEngine()
        
        # test different age ranges
        young_player = {**self.mock_player, 'age': 20}
        prime_player = {**self.mock_player, 'age': 26}
        older_player = {**self.mock_player, 'age': 33}
        
        young_score = engine._calculate_age_potential_score(young_player)
        prime_score = engine._calculate_age_potential_score(prime_player)
        older_score = engine._calculate_age_potential_score(older_player)
        
        # younger players should score higher
        self.assertGreaterEqual(young_score, prime_score)
        self.assertGreaterEqual(prime_score, older_score)
    
    @patch('src.rating_engine.get_barcelona_squad')
    def test_squad_role_score_calculation(self, mock_get_squad):
        """test squad role score calculation"""
        mock_get_squad.return_value = []
        
        engine = TransferRatingEngine()
        score = engine._calculate_squad_role_score(self.mock_player)
        
        self.assertGreaterEqual(score, 1.0)
        self.assertLessEqual(score, 5.0)
        self.assertIsInstance(score, float)
    
    @patch('src.rating_engine.get_barcelona_squad')
    def test_position_group_mapping(self, mock_get_squad):
        """test position group mapping functionality"""
        mock_get_squad.return_value = []
        
        engine = TransferRatingEngine()
        
        # test various position mappings
        test_cases = [
            ('gk', 'goalkeepers'),
            ('cb', 'defenders'),
            ('lb', 'defenders'),
            ('cm', 'midfielders'),
            ('am', 'midfielders'),
            ('st', 'forwards'),
            ('lw', 'forwards')
        ]
        
        for position, expected_group in test_cases:
            group = engine._get_position_group(position)
            self.assertEqual(group, expected_group)
    
    @patch('src.rating_engine.get_barcelona_squad')
    def test_justification_generation(self, mock_get_squad):
        """test rating justification generation"""
        mock_get_squad.return_value = []
        
        engine = TransferRatingEngine()
        
        # mock scores
        rating = 4.2
        perf_score = 4.0
        value_score = 3.8
        fit_score = 4.5
        age_score = 4.0
        role_score = 4.2
        
        justification = engine._generate_justification(
            self.mock_player, rating, perf_score, value_score, 
            fit_score, age_score, role_score
        )
        
        self.assertIsInstance(justification, str)
        self.assertGreater(len(justification), 50)  # should be substantial
        self.assertTrue(justification.endswith('.'))  # should be well formatted
    
    @patch('src.rating_engine.get_barcelona_squad')
    def test_recommendation_logic(self, mock_get_squad):
        """test recommendation generation logic"""
        mock_get_squad.return_value = []
        
        engine = TransferRatingEngine()
        
        test_ratings = [
            (4.8, 'strongly recommend'),
            (3.8, 'recommend'),
            (3.2, 'consider'),
            (2.7, 'proceed with caution'),
            (2.0, 'do not recommend')
        ]
        
        for rating, expected in test_ratings:
            recommendation = engine._get_recommendation(rating)
            self.assertEqual(recommendation, expected)
    
    @patch('src.rating_engine.get_cached_rating')
    @patch('src.rating_engine.get_barcelona_squad')
    def test_cached_rating_usage(self, mock_get_squad, mock_cached):
        """test cached rating retrieval"""
        mock_get_squad.return_value = []
        
        # mock cached rating
        cached_data = {
            'player_name': 'test player',
            'rating': 4.2,
            'performance_score': 4.0,
            'value_score': 3.8,
            'tactical_fit_score': 4.5,
            'age_potential_score': 4.0,
            'squad_role_score': 4.2,
            'justification': 'test justification'
        }
        mock_cached.return_value = cached_data
        
        engine = TransferRatingEngine()
        result = engine.rate_transfer(self.mock_player)
        
        # should use cached data
        self.assertEqual(result['overall_rating'], 4.2)
        self.assertEqual(result['justification'], 'test justification')

if __name__ == '__main__':
    unittest.main()