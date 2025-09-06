#!/usr/bin/env python3
"""
web scraper for la liga player data
scrapes transfermarkt and other sources for current player information
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re

class LaLigaScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.base_url = 'https://www.transfermarkt.us'
        self.laliga_teams = []
        self.all_players = []
        
    def setup_driver(self):
        """setup selenium webdriver with options"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=chrome_options
        )
        return driver
    
    def get_laliga_teams(self):
        """scrape all la liga team urls and basic info"""
        url = f'{self.base_url}/laliga/startseite/wettbewerb/ES1'
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # find team links
            team_rows = soup.find_all('tr', class_='odd') + soup.find_all('tr', class_='even')
            
            for row in team_rows:
                team_link = row.find('a', href=True)
                if team_link and '/verein/' in team_link['href']:
                    team_name = team_link.get('title', '').strip()
                    if team_name:
                        self.laliga_teams.append({
                            'name': team_name,
                            'url': self.base_url + team_link['href'],
                            'id': team_link['href'].split('/')[-1]
                        })
            
            print(f"found {len(self.laliga_teams)} la liga teams")
            return self.laliga_teams
            
        except Exception as e:
            print(f"error scraping teams: {e}")
            return []
    
    def scrape_team_squad(self, team):
        """scrape individual team squad data"""
        squad_url = f"{team['url']}/kader/verein/{team['id']}"
        players = []
        
        try:
            driver = self.setup_driver()
            driver.get(squad_url)
            
            # wait for squad table to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "items"))
            )
            
            # find player rows
            player_rows = driver.find_elements(By.CSS_SELECTOR, "tr.odd, tr.even")
            
            for row in player_rows:
                try:
                    # player name and link
                    name_cell = row.find_element(By.CSS_SELECTOR, "td.hauptlink a")
                    player_name = name_cell.text.strip()
                    player_url = name_cell.get_attribute('href')
                    
                    if not player_name or not player_url:
                        continue
                    
                    # position
                    position_cell = row.find_elements(By.CSS_SELECTOR, "td")[1]
                    position = position_cell.text.strip() if position_cell else 'unknown'
                    
                    # age
                    age_cell = row.find_elements(By.CSS_SELECTOR, "td")[2]
                    age_text = age_cell.text.strip() if age_cell else '0'
                    age = self.extract_number(age_text)
                    
                    # market value
                    value_cell = row.find_elements(By.CSS_SELECTOR, "td.rechts.hauptlink")
                    market_value = 0
                    if value_cell:
                        value_text = value_cell[-1].text.strip()
                        market_value = self.parse_market_value(value_text)
                    
                    # nationality
                    flag_img = row.find_elements(By.CSS_SELECTOR, "img.flaggenrahmen")
                    nationality = 'unknown'
                    if flag_img:
                        nationality = flag_img[0].get_attribute('title') or 'unknown'
                    
                    player_data = {
                        'name': player_name,
                        'team': team['name'],
                        'position': self.normalize_position(position),
                        'age': age,
                        'nationality': nationality,
                        'market_value': market_value,
                        'url': player_url
                    }
                    
                    players.append(player_data)
                    
                except Exception as e:
                    continue  # skip problematic rows
            
            driver.quit()
            print(f"scraped {len(players)} players from {team['name']}")
            return players
            
        except Exception as e:
            print(f"error scraping {team['name']}: {e}")
            if 'driver' in locals():
                driver.quit()
            return []
    
    def parse_market_value(self, value_text):
        """convert market value text to float (in millions)"""
        if not value_text or value_text == '-':
            return 0.0
        
        # remove currency symbols and clean text
        clean_text = re.sub(r'[€$£]', '', value_text).strip()
        
        try:
            if 'm' in clean_text.lower():
                return float(re.findall(r'[\d.]+', clean_text)[0])
            elif 'k' in clean_text.lower():
                return float(re.findall(r'[\d.]+', clean_text)[0]) / 1000.0
            else:
                return 0.0
        except:
            return 0.0
    
    def normalize_position(self, position):
        """normalize position names to standard abbreviations"""
        position_map = {
            'goalkeeper': 'GK',
            'goalie': 'GK',
            'centre-back': 'CB',
            'center-back': 'CB',
            'central defender': 'CB',
            'right-back': 'RB',
            'left-back': 'LB',
            'defensive midfield': 'DM',
            'central midfield': 'CM',
            'attacking midfield': 'AM',
            'right winger': 'RW',
            'left winger': 'LW',
            'centre-forward': 'ST',
            'striker': 'ST'
        }
        
        pos_lower = position.lower().strip()
        for key, value in position_map.items():
            if key in pos_lower:
                return value
        
        return position.upper() if len(position) <= 3 else 'MF'
    
    def extract_number(self, text):
        """extract first number from text"""
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else 0
    
    def scrape_all_laliga_players(self):
        """main method to scrape all la liga players"""
        print("starting la liga player scraping...")
        
        # get team list
        if not self.laliga_teams:
            self.get_laliga_teams()
        
        if not self.laliga_teams:
            print("failed to get team list")
            return []
        
        # scrape each team
        for i, team in enumerate(self.laliga_teams):
            print(f"scraping team {i+1}/{len(self.laliga_teams)}: {team['name']}")
            
            team_players = self.scrape_team_squad(team)
            self.all_players.extend(team_players)
            
            # rate limiting
            time.sleep(2)
            
            # optional: stop after a few teams for testing
            # if i >= 2:  # uncomment for testing
            #     break
        
        print(f"total players scraped: {len(self.all_players)}")
        return self.all_players
    
    def save_to_file(self, filename='data/laliga_players.py'):
        """save scraped data to python file"""
        if not self.all_players:
            print("no player data to save")
            return
        
        # create the python file content
        file_content = f'''# la liga players database - generated by scraper.py
# total players: {len(self.all_players)}

laliga_players = {json.dumps(self.all_players, indent=4, ensure_ascii=False)}

def get_all_players():
    """return all la liga players"""
    return laliga_players

def search_players(query):
    """search players by name"""
    query_lower = query.lower()
    return [p for p in laliga_players if query_lower in p['name'].lower()]

def get_players_by_position(position):
    """get players by position"""
    return [p for p in laliga_players if p['position'] == position.upper()]

def get_players_by_team(team_name):
    """get players by team"""
    return [p for p in laliga_players if team_name.lower() in p['team'].lower()]

def get_player_names():
    """get list of all player names for autocomplete"""
    return [p['name'] for p in laliga_players]
'''
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(file_content)
            print(f"player data saved to {filename}")
        except Exception as e:
            print(f"error saving file: {e}")

def main():
    """main execution function"""
    scraper = LaLigaScraper()
    
    # scrape all players
    players = scraper.scrape_all_laliga_players()
    
    if players:
        # save to file
        scraper.save_to_file()
        
        # print some stats
        positions = {}
        teams = {}
        
        for player in players:
            pos = player['position']
            team = player['team']
            
            positions[pos] = positions.get(pos, 0) + 1
            teams[team] = teams.get(team, 0) + 1
        
        print("\nposition distribution:")
        for pos, count in sorted(positions.items()):
            print(f"  {pos}: {count}")
        
        print(f"\nteams scraped: {len(teams)}")
        print("scraping completed successfully!")
    else:
        print("scraping failed - no player data collected")

if __name__ == "__main__":
    main()