import sqlite3
import os

class PlayerDatabase:
    def __init__(self, db_path='data/laliga_players.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    def get_connection(self):
        """get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # enables dict-like access
        return conn
    
    def initialize(self):
        """create database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # create players table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_id INTEGER UNIQUE,
                name TEXT NOT NULL,
                team TEXT NOT NULL,
                position TEXT,
                age INTEGER,
                nationality TEXT,
                height TEXT,
                weight TEXT,
                games_played INTEGER DEFAULT 0,
                goals INTEGER DEFAULT 0,
                assists INTEGER DEFAULT 0,
                rating REAL DEFAULT 0.0,
                minutes_played INTEGER DEFAULT 0,
                yellow_cards INTEGER DEFAULT 0,
                red_cards INTEGER DEFAULT 0,
                photo TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # create index for faster searching
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_player_name ON players(name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_player_position ON players(position)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_player_team ON players(team)')
        
        conn.commit()
        conn.close()
        print("database initialized")
    
    def insert_players(self, players, team_name):
        """insert list of players for a team"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for player in players:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO players (
                        api_id, name, team, position, age, nationality, 
                        height, weight, games_played, goals, assists, 
                        rating, minutes_played, yellow_cards, red_cards, photo
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    player['api_id'],
                    player['name'],
                    team_name,
                    player['position'],
                    player['age'],
                    player['nationality'],
                    player['height'],
                    player['weight'],
                    player['games_played'],
                    player['goals'],
                    player['assists'],
                    player['rating'],
                    player['minutes_played'],
                    player['yellow_cards'],
                    player['red_cards'],
                    player['photo']
                ))
            except sqlite3.Error as e:
                print(f"error inserting player {player['name']}: {e}")
        
        conn.commit()
        conn.close()
    
    def search_players(self, query, limit=10):
        """search players by name for autocomplete"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT name, team, position, age, rating 
            FROM players 
            WHERE name LIKE ? 
            ORDER BY rating DESC, name 
            LIMIT ?
        ''', (f'%{query}%', limit))
        
        players = []
        for row in cursor.fetchall():
            players.append({
                'name': row['name'],
                'team': row['team'],
                'position': row['position'],
                'age': row['age'],
                'rating': row['rating'],
                'label': f"{row['name']} ({row['team']}) - {row['position']}"
            })
        
        conn.close()
        return players
    
    def get_player_by_name(self, name):
        """get full player data by name"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM players 
            WHERE name = ? 
            ORDER BY rating DESC 
            LIMIT 1
        ''', (name,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_players_by_position(self, position, limit=20):
        """get players by position"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM players 
            WHERE position = ? 
            ORDER BY rating DESC 
            LIMIT ?
        ''', (position, limit))
        
        players = []
        for row in cursor.fetchall():
            players.append(dict(row))
        
        conn.close()
        return players
    
    def get_top_players(self, limit=50):
        """get top rated players across all positions"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM players 
            WHERE rating > 0 AND games_played > 5
            ORDER BY rating DESC 
            LIMIT ?
        ''', (limit,))
        
        players = []
        for row in cursor.fetchall():
            players.append(dict(row))
        
        conn.close()
        return players
    
    def get_player_count(self):
        """get total number of players in database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM players')
        count = cursor.fetchone()['count']
        
        conn.close()
        return count
    
    def get_teams(self):
        """get list of all teams"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT DISTINCT team FROM players ORDER BY team')
        teams = [row['team'] for row in cursor.fetchall()]
        
        conn.close()
        return teams
    
    def clear_database(self):
        """clear all player data (useful for updates)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM players')
        conn.commit()
        conn.close()
        print("database cleared")