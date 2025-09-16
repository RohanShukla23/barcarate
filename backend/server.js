const express = require('express');
const cors = require('cors');
require('dotenv').config();

const squadRoutes = require('./src/routes/squad');
const playersRoutes = require('./src/routes/players');
const transfersRoutes = require('./src/routes/transfers');

const app = express();
const PORT = process.env.PORT || 5000;

// middleware
app.use(cors());
app.use(express.json());

// routes
app.use('/api/squad', squadRoutes);
app.use('/api/players', playersRoutes);
app.use('/api/transfers', transfersRoutes);

// health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'barcarate api is running' });
});

// error handling
app.use((err, req, res, next) => {
  console.error('server error:', err);
  res.status(500).json({ 
    error: 'internal server error', 
    message: err.message 
  });
});

// start server
app.listen(PORT, () => {
  console.log(`barcarate server running on port ${PORT}`);
});