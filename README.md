# BarcaRate ⚽

rate potential transfers for fc barcelona based on current squad analysis and player performance data.

## features
- analyzes current barcelona squad to identify weak positions
- scrapes la liga player database 
- provides 5-star rating system for transfer suggestions
- considers performance stats, market value, and squad fit
- autocomplete search for la liga players

## setup

1. clone the repository
```bash
git clone https://github.com/yourusername/barcarate.git
cd barcarate
```

2. install dependencies
```bash
pip install -r requirements.txt
```

3. get api key
- sign up at [api-football.com](https://www.api-football.com/)
- copy your api key

4. configure environment
```bash
cp .env.example .env
# edit .env with your api key
```

5. run the application
```bash
python src/main.py
```

6. open browser to `http://localhost:5000`

## how it works

1. **squad analysis**: fetches current barcelona roster and analyzes position depth
2. **player database**: builds searchable database of all la liga players
3. **transfer rating**: evaluates potential signings based on:
   - player performance stats
   - position need priority  
   - estimated transfer fee
   - age and contract situation
   - playing style fit

## rating algorithm

the transfer rating uses a weighted scoring system:
- **performance (40%)**: based on season stats, games played, goals/assists
- **position need (30%)**: how much barcelona needs that position
- **age factor (20%)**: ideal age range 22-28, acceptable 18-32
- **value rating (10%)**: estimated value for money based on age/performance

### rating scale
- ⭐⭐⭐⭐⭐ outstanding signing - perfect fit for barcelona
- ⭐⭐⭐⭐ excellent addition - would strengthen the squad significantly
- ⭐⭐⭐ solid option - decent signing with some benefits
- ⭐⭐ questionable fit - may not suit barcelona's style
- ⭐ poor choice - not recommended for barcelona

## api usage
the app uses api-football for real-time data. free tier includes 100 requests/day which is sufficient for regular usage.

## file structure
```
barcarate/
├── src/
│   ├── main.py              # flask application entry point
│   ├── data_collector.py    # fetches data from api-football
│   ├── transfer_analyzer.py # rating algorithm and squad analysis
│   ├── database.py          # sqlite database operations
│   └── utils.py             # helper functions
├── static/
│   ├── style.css            # barcelona-themed ui styling
│   └── script.js            # frontend interactions
├── templates/
│   └── index.html           # main web interface
├── data/                    # generated data storage
└── requirements.txt         # python dependencies
```

## contributing
pull requests welcome. please ensure your code follows the existing style:
- lowercase comments
- descriptive function names
- proper error handling
- responsive design considerations

## troubleshooting

### common issues
- **"api key not found"**: make sure you've created .env file with your api key
- **"rate limit hit"**: free api tier has 100 requests/day, wait or upgrade
- **"no players found"**: database might be empty, click "update data" button
- **slow initial startup**: first run downloads all la liga players (~2000 players)

### data updates
- barcelona squad updates automatically check for recent transfers
- la liga player data updates seasonally or manually via "update data" button
- database stores locally to minimize api calls

## license
mit license - see LICENSE file

## disclaimer
transfer ratings are algorithmic suggestions based on statistical analysis. actual transfer success depends on many factors not captured in basic stats like team chemistry, tactical fit, injury history, etc.