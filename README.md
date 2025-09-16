# BarcaRate 🔴🔵

A comprehensive transfer evaluation system for FC Barcelona that analyzes the current squad, identifies improvement areas, and rates potential La Liga player transfers.

## Features

- **Squad Analysis**: Real-time FC Barcelona lineup with performance metrics
- **Improvement Detection**: AI-powered analysis of squad weaknesses
- **Transfer Simulator**: Search and simulate transfers from La Liga teams
- **Smart Rating System**: Evaluates transfers based on performance, cost, and squad fit
- **Interactive UI**: Modern, responsive interface with Barcelona branding

## Tech Stack

- **Frontend**: React 18, Tailwind CSS, Lucide Icons
- **Backend**: Node.js, Express, Axios
- **Data**: Football API integration
- **Styling**: Custom Barcelona-themed design

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Football API key (see setup below)

## API Setup

### Required API Key

This project uses the **API-Football** service for real-time football data:

1. Visit [RapidAPI Football](https://rapidapi.com/api-sports/api/api-football)
2. Subscribe to the API-Football service (free tier available)
3. Copy your API key from the dashboard
4. Add it to your environment variables (see installation)

**Note**: The free tier includes 100 requests/day, which is sufficient for development and testing.

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/barcarate.git
   cd barcarate
   ```

2. **Install backend dependencies**
   ```bash
   cd backend
   npm install
   ```

3. **Install frontend dependencies**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Environment Setup**
   
   Create `.env` in the backend directory:
   ```env
   FOOTBALL_API_KEY=your_rapidapi_key_here
   PORT=5000
   ```

## Running the Application

1. **Start the backend server**
   ```bash
   cd backend
   npm run dev
   ```

2. **Start the frontend (in a new terminal)**
   ```bash
   cd frontend
   npm start
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## Project Structure

```
barcarate/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API services
│   │   └── utils/           # Helper functions
│   ├── public/
│   └── package.json
├── backend/                 # Node.js API server
│   ├── src/
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   └── utils/          # Helper functions
│   ├── server.js
│   └── package.json
├── README.md
└── .gitignore
```

## API Endpoints

- `GET /api/squad` - Get current Barcelona squad
- `GET /api/squad/analysis` - Get squad improvement analysis
- `GET /api/players/search` - Search La Liga players
- `POST /api/transfers/evaluate` - Evaluate transfer scenarios

## Usage

1. **View Squad**: See Barcelona's current lineup with ratings
2. **Analyze Weaknesses**: Review AI-generated improvement suggestions
3. **Search Players**: Use the transfer simulator to find La Liga players
4. **Evaluate Transfers**: Get detailed ratings and explanations for potential signings

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is for educational and entertainment purposes. Player ratings and transfer evaluations are simulated and should not be used for actual football management decisions.

---

**Visca Barça!** 🔴🔵