import React, { useState, useEffect, useRef } from 'react';
import { Search, Star, DollarSign, AlertCircle, CheckCircle, XCircle, Users, TrendingUp } from 'lucide-react';
import { searchPlayers, evaluateTransfer } from '../services/api';
import LoadingSpinner from './LoadingSpinner';

function TransferSimulator() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [evaluating, setEvaluating] = useState(false);
  const [error, setError] = useState(null);
  const searchTimeout = useRef(null);

  // debounced search
  useEffect(() => {
    if (searchTimeout.current) {
      clearTimeout(searchTimeout.current);
    }

    if (searchQuery.length >= 2) {
      searchTimeout.current = setTimeout(() => {
        performSearch();
      }, 500);
    } else {
      setSearchResults([]);
    }

    return () => {
      if (searchTimeout.current) {
        clearTimeout(searchTimeout.current);
      }
    };
  }, [searchQuery]);

  const performSearch = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const results = await searchPlayers(searchQuery);
      setSearchResults(results);
    } catch (err) {
      console.error('search failed:', err);
      setError('failed to search players. please try again.');
      setSearchResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handlePlayerSelect = async (player) => {
    setSelectedPlayer(player);
    setEvaluation(null);
    
    try {
      setEvaluating(true);
      setError(null);
      
      const transferEvaluation = await evaluateTransfer({
        playerId: player.id,
        playerName: player.name,
        currentTeam: player.team.name,
        position: player.position,
        age: player.age,
        rating: player.rating,
        marketValue: player.marketValue
      });
      
      setEvaluation(transferEvaluation);
    } catch (err) {
      console.error('evaluation failed:', err);
      setError('failed to evaluate transfer. please try again.');
    } finally {
      setEvaluating(false);
    }
  };

  const getRatingColor = (rating) => {
    if (rating >= 8.5) return 'text-green-600 bg-green-100';
    if (rating >= 7.0) return 'text-blue-600 bg-blue-100';
    if (rating >= 5.5) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getRatingIcon = (rating) => {
    if (rating >= 8.5) return <CheckCircle className="w-5 h-5 text-green-600" />;
    if (rating >= 7.0) return <Star className="w-5 h-5 text-blue-600" />;
    if (rating >= 5.5) return <AlertCircle className="w-5 h-5 text-yellow-600" />;
    return <XCircle className="w-5 h-5 text-red-600" />;
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  return (
    <div className="space-y-6">
      {/* search header */}
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">transfer simulator</h2>
        <p className="text-gray-600">search for la liga players and evaluate potential transfers to barcelona</p>
      </div>

      {/* search input */}
      <div className="max-w-md mx-auto">
        <div className="relative">
          <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="search for players (e.g., vinicius, griezmann)"
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-barca-blue focus:border-transparent"
          />
        </div>
        {searchQuery.length > 0 && searchQuery.length < 2 && (
          <p className="text-sm text-gray-500 mt-2">type at least 2 characters to search</p>
        )}
      </div>

      {/* search results */}
      {loading && (
        <div className="flex justify-center py-8">
          <LoadingSpinner size="medium" message="searching players..." />
        </div>
      )}

      {searchResults.length > 0 && !loading && (
        <div className="bg-white rounded-lg border border-gray-200">
          <div className="p-4 border-b border-gray-200">
            <h3 className="font-semibold text-gray-900">search results ({searchResults.length})</h3>
          </div>
          <div className="max-h-96 overflow-y-auto">
            {searchResults.map((player) => (
              <div
                key={player.id}
                onClick={() => handlePlayerSelect(player)}
                className="flex items-center space-x-4 p-4 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0"
              >
                <div className="w-12 h-12 bg-gray-200 rounded-full flex-shrink-0 overflow-hidden">
                  {player.photo && (
                    <img src={player.photo} alt={player.name} className="w-full h-full object-cover" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="font-medium text-gray-900">{player.name}</div>
                  <div className="text-sm text-gray-500">
                    {player.position} • {player.age}y • {player.team.name}
                  </div>
                  {player.rivalry?.isRival && (
                    <div className="text-xs text-red-600 font-medium mt-1">⚠️ rival club</div>
                  )}
                </div>
                <div className="text-right">
                  <div className="font-medium text-gray-900">{player.rating}</div>
                  <div className="text-sm text-gray-500">{formatCurrency(player.marketValue)}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* no results */}
      {searchQuery.length >= 2 && searchResults.length === 0 && !loading && (
        <div className="text-center py-8">
          <Users className="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500">no players found matching "{searchQuery}"</p>
          <p className="text-sm text-gray-400 mt-2">try searching for different names or terms</p>
        </div>
      )}

      {/* selected player evaluation */}
      {selectedPlayer && (
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          <div className="bg-gradient-to-r from-barca-blue to-barca-red p-6 text-white">
            <div className="flex items-center space-x-4">
              <div className="w-16 h-16 bg-white bg-opacity-20 rounded-full flex-shrink-0 overflow-hidden">
                {selectedPlayer.photo && (
                  <img src={selectedPlayer.photo} alt={selectedPlayer.name} className="w-full h-full object-cover" />
                )}
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-bold">{selectedPlayer.name}</h3>
                <p className="text-blue-100">
                  {selectedPlayer.position} • {selectedPlayer.age} years • {selectedPlayer.team.name}
                </p>
                <div className="flex items-center space-x-4 mt-2">
                  <span className="bg-white bg-opacity-20 px-2 py-1 rounded text-sm">
                    rating: {selectedPlayer.rating}
                  </span>
                  <span className="bg-white bg-opacity-20 px-2 py-1 rounded text-sm">
                    value: {formatCurrency(selectedPlayer.marketValue)}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {evaluating && (
            <div className="p-8 text-center">
              <LoadingSpinner size="medium" message="evaluating transfer..." />
            </div>
          )}

          {evaluation && !evaluating && (
            <div className="p-6 space-y-6">
              {/* overall rating */}
              <div className="text-center">
                <div className="flex items-center justify-center space-x-3 mb-4">
                  {getRatingIcon(evaluation.transferRating)}
                  <div>
                    <div className={`text-3xl font-bold px-4 py-2 rounded-lg ${getRatingColor(evaluation.transferRating)}`}>
                      {evaluation.transferRating}/10
                    </div>
                    <div className="text-sm text-gray-600 mt-2">transfer rating</div>
                  </div>
                </div>
                <div className="max-w-lg mx-auto">
                  <p className="text-gray-700 font-medium">{evaluation.recommendation}</p>
                </div>
              </div>

              {/* factor breakdown */}
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                {Object.entries(evaluation.factors).map(([factor, score]) => (
                  <div key={factor} className="text-center">
                    <div className={`text-lg font-semibold px-3 py-2 rounded ${getRatingColor(score)}`}>
                      {score}/10
                    </div>
                    <div className="text-xs text-gray-600 mt-1 capitalize">
                      {factor.replace(/([A-Z])/g, ' $1').toLowerCase()}
                    </div>
                  </div>
                ))}
              </div>

              {/* pros and cons */}
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-green-50 rounded-lg p-4">
                  <h4 className="font-semibold text-green-800 mb-3 flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4" />
                    <span>pros</span>
                  </h4>
                  <ul className="space-y-2">
                    {evaluation.pros.map((pro, index) => (
                      <li key={index} className="text-sm text-green-700 flex items-start space-x-2">
                        <span className="w-1.5 h-1.5 bg-green-500 rounded-full mt-2 flex-shrink-0"></span>
                        <span>{pro}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="bg-red-50 rounded-lg p-4">
                  <h4 className="font-semibold text-red-800 mb-3 flex items-center space-x-2">
                    <XCircle className="w-4 h-4" />
                    <span>cons</span>
                  </h4>
                  <ul className="space-y-2">
                    {evaluation.cons.map((con, index) => (
                      <li key={index} className="text-sm text-red-700 flex items-start space-x-2">
                        <span className="w-1.5 h-1.5 bg-red-500 rounded-full mt-2 flex-shrink-0"></span>
                        <span>{con}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* cost and rivalry info */}
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="flex items-center space-x-3">
                    <DollarSign className="w-5 h-5 text-gray-500" />
                    <div>
                      <div className="font-medium text-gray-900">estimated cost</div>
                      <div className="text-sm text-gray-600">{formatCurrency(evaluation.estimatedCost)}</div>
                    </div>
                  </div>
                  
                  {evaluation.rivalry.isRival && (
                    <div className="flex items-center space-x-3">
                      <AlertCircle className="w-5 h-5 text-red-500" />
                      <div>
                        <div className="font-medium text-red-700">rivalry factor</div>
                        <div className="text-sm text-red-600">{evaluation.rivalry.description}</div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-5 h-5 text-red-500" />
            <span className="text-red-800 font-medium">error</span>
          </div>
          <p className="text-red-700 mt-2">{error}</p>
        </div>
      )}
    </div>
  );
}

export default TransferSimulator;