import sqlite3
import os
from config import Config

def get_db_connection():
    """create database connection"""
    # ensure data directory exists
    os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)
    
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # enable dict-like access
    return conn

def init_db():
    """initialize database with required tables"""
    conn = get_db_connection()
    
    # barcelona squad table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS barcelona_squad (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT,
            age INTEGER,
            squad_number INTEGER,
            position_group TEXT,
            market_value REAL DEFAULT 0,
            goals INTEGER DEFAULT 0,
            assists INTEGER DEFAULT 0,
            minutes_played INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # la liga players table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS laliga_players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            team TEXT NOT NULL,
            position TEXT,
            age INTEGER,
            market_value REAL DEFAULT 0,
            goals INTEGER DEFAULT 0,
            assists INTEGER DEFAULT 0,
            minutes_played INTEGER DEFAULT 0,
            pass_completion REAL DEFAULT 0,
            dribbles_completed REAL DEFAULT 0,
            tackles_won REAL DEFAULT 0,
            aerial_duels_won REAL DEFAULT 0,
            shots_per_game REAL DEFAULT 0,
            key_passes REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # transfer ratings cache
    conn.execute('''
        CREATE TABLE IF NOT EXISTS transfer_ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            rating REAL NOT NULL,
            performance_score REAL,
            value_score REAL,
            tactical_fit_score REAL,
            age_potential_score REAL,
            squad_role_score REAL,
            justification TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # squad analysis cache
    conn.execute('''
        CREATE TABLE IF NOT EXISTS squad_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            position_group TEXT NOT NULL,
            strength_rating REAL,
            need_priority INTEGER,
            analysis TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("database initialized successfully")

def get_barcelona_squad():
    """get current barcelona squad from database"""
    conn = get_db_connection()
    players = conn.execute('''
        SELECT * FROM barcelona_squad 
        ORDER BY position_group, squad_number
    ''').fetchall()
    conn.close()
    
    return [dict(player) for player in players]

def get_laliga_players(limit=None):
    """get all la liga players from database"""
    conn = get_db_connection()
    query = 'SELECT * FROM laliga_players ORDER BY market_value DESC'
    
    if limit:
        query += f' LIMIT {limit}'
    
    players = conn.execute(query).fetchall()
    conn.close()
    
    return [dict(player) for player in players]

def get_player_by_name(name):
    """get specific player by name"""
    conn = get_db_connection()
    player = conn.execute('''
        SELECT * FROM laliga_players 
        WHERE name = ? COLLATE NOCASE
    ''', (name,)).fetchone()
    conn.close()
    
    return dict(player) if player else None

def cache_transfer_rating(player_name, rating_data):
    """cache transfer rating to avoid recalculation"""
    conn = get_db_connection()
    
    # remove old rating for same player
    conn.execute('DELETE FROM transfer_ratings WHERE player_name = ?', (player_name,))
    
    # insert new rating
    conn.execute('''
        INSERT INTO transfer_ratings 
        (player_name, rating, performance_score, value_score, tactical_fit_score,
         age_potential_score, squad_role_score, justification)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        player_name, rating_data['rating'], rating_data['performance_score'],
        rating_data['value_score'], rating_data['tactical_fit_score'],
        rating_data['age_potential_score'], rating_data['squad_role_score'],
        rating_data['justification']
    ))
    
    conn.commit()
    conn.close()

def get_cached_rating(player_name):
    """get cached transfer rating if available and recent"""
    conn = get_db_connection()
    
    rating = conn.execute('''
        SELECT * FROM transfer_ratings 
        WHERE player_name = ? 
        AND datetime(created_at) > datetime('now', '-1 hour')
    ''', (player_name,)).fetchone()
    
    conn.close()
    
    return dict(rating) if rating else None