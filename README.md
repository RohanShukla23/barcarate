# BarcaRate 🔵🔴

A comprehensive transfer evaluation tool for FC Barcelona that analyzes squad needs and rates potential La Liga signings on a five-star scale.

## Features

- **Current Squad Analysis**: Evaluates Barcelona's 2025-26 squad strengths and weaknesses
- **Transfer Needs Assessment**: Identifies priority positions for reinforcement
- **Player Database**: Complete La Liga player database with stats and market values
- **Smart Rating System**: Five-star rating system considering performance, value, fit, and more
- **Interactive Interface**: User-friendly web interface with autocomplete player search

## How It Works

1. **Squad Analysis**: BarcaRate analyzes Barcelona's current lineup to identify gaps and areas for improvement
2. **Player Search**: Enter any La Liga player name with intelligent autocomplete
3. **Transfer Evaluation**: Get a detailed 1-5 star rating with comprehensive justification
4. **Rating factors**:
   - Player performance and statistics
   - Market value and transfer feasibility
   - Position fit and squad needs
   - Age and potential
   - Playing style compatibility

## Installation

1. Clone the repository:
```bash
git clone https://github.com/RohanShukla23/barcarate.git
cd barcarate
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the scraper to update player data:
```bash
python scraper.py
```

5. Start the application:
```bash
python main.py
```

6. Open your browser and navigate to `http://localhost:5000`

## Usage

1. **View Squad Analysis**: See Barcelona's current strengths and areas needing reinforcement
2. **Search Players**: Use the autocomplete search to find any La Liga player
3. **Get Transfer Rating**: View detailed analysis and star rating for potential signings
4. **Compare Options**: Evaluate multiple players for the same position

## Technical Details

- **Backend**: Python Flask
- **Data Source**: Web scraping from Transfermarkt and La Liga official sources
- **Frontend**: HTML/CSS/JavaScript with autocomplete functionality
- **Data Storage**: JSON files for player database and squad information

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for entertainment and analysis purposes only. Transfer ratings are algorithmic evaluations and should not be considered professional scouting advice. Market values and player data are sourced from publicly available information.