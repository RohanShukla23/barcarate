
# BarcaRate ⭐

An intelligent transfer rating system for FC Barcelona that analyzes the current squad, identifies improvement areas, and rates potential La Liga signings on a five-star scale.

## Features

- **Squad Analysis**: Automatically analyzes FC Barcelona's current 2025-26 lineup
- **Position Gap Detection**: Identifies areas where the team could benefit from new signings
- **Player Database**: Comprehensive database of all current La Liga players with stats
- **Transfer Rating**: AI-powered rating system considering performance, value, fit, and feasibility  
- **Interactive Interface**: Web-based UI with player name autocomplete
- **Real-time Data**: Uses web scraping to gather the latest player statistics

## How It Works

1. **Data Collection**: Scrapes current Barcelona squad and La Liga player data
2. **Squad Analysis**: Evaluates team strengths and weaknesses by position
3. **Player Search**: Type any La Liga player name with autocomplete suggestions
4. **Transfer Rating**: Get a detailed 1-5 star rating with justification covering:
   - Player performance and statistics
   - Estimated transfer fee and financial feasibility
   - Tactical fit with Barcelona's system
   - Age profile and long-term value
   - Squad role and playing time potential

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/BarcaRate.git
cd BarcaRate
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API keys (optional):
```bash
cp config.py.example config.py
# Edit config.py with your API keys for enhanced data
```

5. Initialize the database:
```bash
python -c "from src.database import init_db; init_db()"
```

6. Run the application:
```bash
python main.py
```

Visit `http://localhost:5000` to start rating transfers!

## Usage

1. **View Squad Analysis**: See Barcelona's current lineup and identified needs
2. **Search Players**: Start typing a La Liga player's name for autocomplete suggestions
3. **Get Ratings**: Select a player to see their transfer rating and detailed analysis
4. **Compare Options**: Rate multiple players for the same position to find the best fit

## Rating Criteria

Our algorithm considers:
- **Performance** (30%): Goals, assists, key stats, form
- **Value** (25%): Market value vs. transfer fee estimation  
- **Tactical Fit** (20%): Playing style compatibility with Barcelona
- **Age/Potential** (15%): Current age and future development potential
- **Squad Role** (10%): Likely playing time and squad integration

## Data Sources

- FC Barcelona official sources
- La Liga player statistics  
- Transfer market valuations
- Performance metrics from multiple providers

## Development

Run tests:
```bash
python -m pytest tests/
```

Update player database:
```bash
python -c "from src.scraper import update_all_data; update_all_data()"
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for entertainment and analysis purposes only. Transfer ratings are algorithmic estimates and should not be considered professional scouting advice.