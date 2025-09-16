# BarcaRate - FC Barcelona Transfer Evaluation System

A comprehensive web application for analyzing FC Barcelona's current squad and evaluating potential player transfers from La Liga. Built with React frontend and Node.js/Express backend, featuring real-time data from football APIs.

## Features

### Squad Analysis
- Current Barcelona squad overview with player ratings
- Position-by-position analysis and depth assessment
- Team statistics including overall rating, average age, and total market value
- Identification of improvement areas and transfer priorities
- Visual representation of squad strengths and weaknesses

### Transfer Simulator
- Search and evaluate La Liga players for potential transfers
- Comprehensive transfer rating system (0-10 scale)
- Multi-factor evaluation including:
  - Squad fit and positional need
  - Value for money assessment
  - Age profile and long-term potential
  - Player quality and current performance
  - Rivalry considerations (El Clasico factor)
- Detailed pros/cons analysis
- Transfer cost estimation
- Personalized recommendations

### Technical Features
- Real-time data from football APIs
- Responsive design optimized for all devices
- Barcelona-themed UI with official colors
- Mock data fallback for development
- Error handling and loading states
- Debounced search functionality

## Tech Stack

**Frontend:**
- React 18 with functional components and hooks
- Tailwind CSS for styling
- Axios for API communication
- Lucide React for icons
- Responsive design principles

**Backend:**
- Node.js with Express framework
- RESTful API architecture
- Football API integration
- Environment-based configuration
- Comprehensive error handling

## Prerequisites

Before running this project, make sure you have:

- Node.js (version 14 or higher)
- npm or yarn package manager
- Football API key from [API-Sports](https://rapidapi.com/api-sports/api/api-football/)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd barcarate
   ```

2. **Install backend dependencies:**
   ```bash
   cd backend
   npm install
   ```

3. **Install frontend dependencies:**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Set up environment variables:**
   
   Create a `.env` file in the `backend` directory:
   ```bash
   cd ../backend
   touch .env
   ```
   
   Add the following content to `.env`:
   ```
   PORT=3001
   FOOTBALL_API_KEY=your_api_key_here
   NODE_ENV=development
   ```
   
   Replace `your_api_key_here` with your actual API key from API-Sports.

## Running the Application

### Development Mode

1. **Start the backend server:**
   ```bash
   cd backend
   npm run dev
   ```
   The backend will run on `http://localhost:3001`

2. **Start the frontend development server:**
   ```bash
   cd frontend
   npm start
   ```
   The frontend will run on `http://localhost:3000`

3. **Access the application:**
   Open your browser and navigate to `http://localhost:3000`

### Production Mode

1. **Build the frontend:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Start the backend server:**
   ```bash
   cd backend
   npm start
   ```

## Project Structure

```
barcarate/
├── backend/
│   ├── src/
│   │   ├── routes/          # API route handlers
│   │   │   ├── players.js   # Player search endpoints
│   │   │   ├── squad.js     # Squad analysis endpoints
│   │   │   └── transfers.js # Transfer evaluation endpoints
│   │   ├── services/        # Business logic
│   │   │   ├── playersService.js
│   │   │   ├── squadService.js
│   │   │   └── transferService.js
│   │   └── utils/
│   │       └── apiClient.js # External API integration
│   ├── server.js            # Express server setup
│   ├── package.json
│   └── .env                 # Environment variables
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── Header.js
│   │   │   ├── LoadingSpinner.js
│   │   │   ├── SquadAnalysis.js
│   │   │   └── TransferSimulator.js
│   │   ├── services/
│   │   │   └── api.js       # Frontend API client
│   │   ├── App.js           # Main application component
│   │   ├── index.css        # Global styles
│   │   └── index.js         # Application entry point
│   ├── package.json
│   └── tailwind.config.js   # Tailwind CSS configuration
└── README.md
```

## API Endpoints

### Squad Endpoints
- `GET /api/squad` - Get current Barcelona squad
- `GET /api/squad/analysis` - Get detailed squad analysis

### Player Endpoints  
- `GET /api/players/search?query={name}&position={pos}&team={team}` - Search La Liga players

### Transfer Endpoints
- `POST /api/transfers/evaluate` - Evaluate a potential transfer

### Health Check
- `GET /api/health` - API health status

## Configuration

### Environment Variables

**Backend (.env file):**
```
PORT=3001                    # Server port (default: 3001)
FOOTBALL_API_KEY=your_key    # API-Sports API key
NODE_ENV=development         # Environment (development/production)
```

### API Configuration

The application uses the API-Sports football API. Key endpoints:
- Player search and statistics
- Team squad information
- League data for La Liga (ID: 140)
- Barcelona team data (ID: 529)

### Frontend Proxy

Add to `frontend/package.json` for API proxy:
```json
{
  "proxy": "http://localhost:3001"
}
```

## Troubleshooting

### Common Issues

1. **Port 3001 already in use:**
   ```bash
   # Find process using port
   lsof -i :3001
   # Kill process (replace PID)
   kill -9 PID
   # Or use different port
   PORT=3002 npm run dev
   ```

2. **API key issues:**
   - Verify your API key is valid
   - Check API usage limits
   - Ensure proper environment variable setup

3. **CORS errors:**
   - Backend includes CORS middleware
   - Verify frontend proxy configuration

4. **Mock data mode:**
   - App automatically uses mock data when API fails in development
   - Check console for API error messages

### Development Tips

- Use `NODE_ENV=development` for mock data fallbacks
- API requests are logged in console for debugging
- Player search requires minimum 2 characters
- Transfer evaluations consider El Clasico rivalry factors

## Features in Detail

### Squad Analysis Algorithm
- Player ratings calculated using age, position, and performance metrics
- Market values estimated based on rating, age, and team factors
- Position analysis identifies depth and quality issues
- Improvement suggestions generated automatically

### Transfer Evaluation System
- Multi-factor scoring system (0-10 scale)
- Considers squad fit, value, age, quality, and positional need
- Special handling for Real Madrid transfers (rivalry factor)
- Comprehensive pros/cons generation
- Cost estimation with team and age adjustments

### Barcelona Theming
- Official FC Barcelona color scheme
- Responsive design for mobile and desktop
- Smooth animations and transitions
- Barcelona-inspired visual elements

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is for educational and demonstration purposes. All FC Barcelona trademarks and logos are property of FC Barcelona.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Verify API key and environment setup
3. Check console logs for detailed error messages
4. Ensure all dependencies are installed correctly

---

**Visca Barça!** 🔵🔴