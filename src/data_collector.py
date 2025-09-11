import requests
import json
import os
from database import PlayerDatabase
from utils import get_api_headers, safe_request
from dotenv import load_dotenv

load_dotenv()

class DataCollector:
    def __init__(self):
        self.db = PlayerDatabase()
        
    def update_barcelona_squad(self):
        """fetch current barcelona squad from api"""
        print("fetching barcelona squad...")
        
        # api endpoint for barcelona players (team id 529)
        url = "https://api-football-v1.p.rapidapi.com/v3/players"
        params = {
            'team': '529',  # fc barcelona
            'season': '2024',  # current season
            'page': '1'
        }
        
        response = safe_request(url, params)
        if not response:
            return False
            
        players_data = response.get('response', [])
        
        # process and save squad data
        squad = []
        for item in players_data:
            player = item['player']
            stats = item['statistics'][0] if item['statistics'] else {}
            
            squad_player = {
                'id': player['id'],
                'name': player['name'],
                'age': player['age'],
                'position': stats.get('games', {}).get('position', 'Unknown'),
                'nationality': player['nationality'],
                'height': player['height'],
                'weight': player['weight'],
                'games_played': stats.get('games', {}).get('appearences', 0),
                'goals': stats.get('goals', {}).get('total', 0),
                'assists': stats.get('goals', {}).get('assists', 0),
                'rating': stats.get('games', {}).get('rating', '0')
            }
            squad.append(squad_player)
        
        # save to file
        os.makedirs('data', exist_ok=True)
        with open('data/barcelona_squad.json', 'w') as f:
            json.dump(squad, f, indent=2)
            
        print(f"saved {len(squad)} barcelona players")
        return True
    
    def update_laliga_players(self):
        """fetch all la liga players and store in database"""
        print("fetching la liga players...")
        
        # get all la liga teams first
        teams = self._get_laliga_teams()
        if not teams:
            print("failed to fetch teams")
            return False
            
        total_players = 0
        
        # fetch players for each team
        for team in teams:
            team_id = team['team']['id']
            team_name = team['team']['name']
            
            print(f"fetching players for {team_name}...")
            
            players = self._get_team_players(team_id)
            if players:
                self.db.insert_players(players, team_name)
                total_players += len(players)
                
        print(f"saved {total_players} la liga players")
        return True
    
    def _get_laliga_teams(self):
        """get all teams in la liga"""
        url = "https://api-football-v1.p.rapidapi.com/v3/teams"
        params = {
            'league': '140',  # la liga
            'season': '2024'
        }
        
        response = safe_request(url, params)
        if response:
            return response.get('response', [])
        return []
    
    def _get_team_players(self, team_id):
        """get players for specific team"""
        url = "https://api-football-v1.p.rapidapi.com/v3/players"
        params = {
            'team': str(team_id),
            'season': '2024',
            'page': '1'
        }
        
        response = safe_request(url, params)
        if not response:
            return []
            
        players_data = response.get('response', [])
        players = []
        
        for item in players_data:
            player = item['player']
            stats = item['statistics'][0] if item['statistics'] else {}
            
            player_data = {
                'api_id': player['id'],
                'name': player['name'],
                'age': player['age'],
                'position': stats.get('games', {}).get('position', 'Unknown'),
                'nationality': player['nationality'],
                'height': player['height'] or '0cm',
                'weight': player['weight'] or '0kg',
                'games_played': stats.get('games', {}).get('appearences', 0),
                'goals': stats.get('goals', {}).get('total', 0) or 0,
                'assists': stats.get('goals', {}).get('assists', 0) or 0,
                'rating': float(stats.get('games', {}).get('rating', 0) or 0),
                'minutes_played': stats.get('games', {}).get('minutes', 0) or 0,
                'yellow_cards': stats.get('cards', {}).get('yellow', 0) or 0,
                'red_cards': stats.get('cards', {}).get('red', 0) or 0,
                'photo': player['photo']
            }
            players.append(player_data)
            
        return players