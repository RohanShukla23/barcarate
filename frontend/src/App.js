import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import SquadAnalysis from './components/SquadAnalysis';
import TransferSimulator from './components/TransferSimulator';
import LoadingSpinner from './components/LoadingSpinner';
import { getSquad, getSquadAnalysis } from './services/api';
import './index.css';

function App() {
  const [activeTab, setActiveTab] = useState('squad');
  const [squadData, setSquadData] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadSquadData();
  }, []);

  const loadSquadData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // fetch squad and analysis data
      const [squad, analysis] = await Promise.all([
        getSquad(),
        getSquadAnalysis()
      ]);
      
      setSquadData(squad);
      setAnalysisData(analysis);
    } catch (err) {
      console.error('failed to load data:', err);
      setError('failed to load barcelona data. please check your connection.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-barca-blue to-barca-red flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-barca-blue to-barca-red flex items-center justify-center">
        <div className="bg-white rounded-lg p-8 max-w-md mx-4 text-center">
          <div className="text-red-500 text-2xl mb-4">⚠️</div>
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Error Loading Data</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button 
            onClick={loadSquadData}
            className="bg-barca-blue text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-barca-blue to-barca-red">
      <Header />
      
      {/* navigation tabs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="flex border-b border-gray-200">
            <button
              onClick={() => setActiveTab('squad')}
              className={`px-6 py-4 text-sm font-medium transition-colors ${
                activeTab === 'squad' 
                  ? 'bg-barca-blue text-white border-b-2 border-barca-red' 
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              Squad Analysis
            </button>
            <button
              onClick={() => setActiveTab('transfers')}
              className={`px-6 py-4 text-sm font-medium transition-colors ${
                activeTab === 'transfers' 
                  ? 'bg-barca-blue text-white border-b-2 border-barca-red' 
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              Transfer Simulator
            </button>
          </div>
          
          <div className="p-6">
            {activeTab === 'squad' && (
              <SquadAnalysis 
                squadData={squadData} 
                analysisData={analysisData} 
              />
            )}
            {activeTab === 'transfers' && (
              <TransferSimulator />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;