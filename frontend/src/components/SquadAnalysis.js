import React from 'react';
import { Star, AlertTriangle, Users, TrendingUp, DollarSign } from 'lucide-react';

function SquadAnalysis({ squadData, analysisData }) {
  if (!squadData || !analysisData) {
    return (
      <div className="text-center py-8">
        <div className="text-gray-500">no squad data available</div>
      </div>
    );
  }

  const getRatingColor = (rating) => {
    if (rating >= 85) return 'text-green-600 bg-green-100';
    if (rating >= 75) return 'text-blue-600 bg-blue-100';
    if (rating >= 65) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
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
      {/* team overview */}
      <div className="bg-gradient-to-r from-barca-blue to-barca-red rounded-lg p-6 text-white">
        <div className="flex items-center space-x-4 mb-4">
          {squadData.team.logo && (
            <img 
              src={squadData.team.logo} 
              alt={squadData.team.name}
              className="w-16 h-16 rounded-full bg-white p-2"
            />
          )}
          <div>
            <h2 className="text-2xl font-bold">{squadData.team.name}</h2>
            <p className="text-blue-100">current squad analysis</p>
          </div>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-white bg-opacity-20 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold">{analysisData.overallRating}</div>
            <div className="text-sm text-blue-100">overall rating</div>
          </div>
          <div className="bg-white bg-opacity-20 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold">{analysisData.totalPlayers}</div>
            <div className="text-sm text-blue-100">squad size</div>
          </div>
          <div className="bg-white bg-opacity-20 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold">{analysisData.averageAge}</div>
            <div className="text-sm text-blue-100">avg age</div>
          </div>
          <div className="bg-white bg-opacity-20 rounded-lg p-4 text-center">
            <div className="text-lg font-bold">{formatCurrency(analysisData.totalValue)}</div>
            <div className="text-sm text-blue-100">total value</div>
          </div>
        </div>
      </div>

      {/* improvement areas */}
      {analysisData.improvementAreas.length > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <div className="flex items-center space-x-2 mb-4">
            <AlertTriangle className="w-5 h-5 text-yellow-600" />
            <h3 className="text-lg font-semibold text-yellow-800">areas for improvement</h3>
          </div>
          <div className="space-y-3">
            {analysisData.improvementAreas.map((area, index) => (
              <div key={index} className="flex items-start space-x-3 p-3 bg-white rounded-lg">
                <div className={`px-2 py-1 rounded text-xs font-medium ${
                  area.priority === 'high' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'
                }`}>
                  {area.priority} priority
                </div>
                <div className="flex-1">
                  <div className="font-medium text-gray-900">{area.position}</div>
                  <div className="text-sm text-gray-600">{area.reason}</div>
                  <div className="text-sm text-gray-500 italic">{area.suggestion}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* position analysis */}
      <div className="bg-white rounded-lg border border-gray-200">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
            <Users className="w-5 h-5" />
            <span>squad by position</span>
          </h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 p-6">
          {analysisData.positionAnalysis.map((position, index) => (
            <div key={index} className="space-y-3">
              <div className="flex items-center justify-between">
                <h4 className="font-medium text-gray-900">{position.position}</h4>
                <div className={`px-2 py-1 rounded text-xs font-medium ${getRatingColor(position.averageRating)}`}>
                  {position.averageRating}
                </div>
              </div>
              <div className="text-sm text-gray-600">
                {position.count} player{position.count !== 1 ? 's' : ''}
              </div>
              <div className="space-y-2">
                {position.players.slice(0, 2).map((player, playerIndex) => (
                  <div key={playerIndex} className="flex items-center space-x-2 text-sm">
                    <div className="w-6 h-6 bg-gray-200 rounded-full flex-shrink-0 overflow-hidden">
                      {player.photo && (
                        <img src={player.photo} alt={player.name} className="w-full h-full object-cover" />
                      )}
                    </div>
                    <span className="text-gray-700 truncate">{player.name}</span>
                    <span className={`px-1 py-0.5 rounded text-xs ${getRatingColor(player.rating)}`}>
                      {Math.round(player.rating)}
                    </span>
                  </div>
                ))}
                {position.count > 2 && (
                  <div className="text-xs text-gray-500">
                    +{position.count - 2} more
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* top players */}
      <div className="bg-white rounded-lg border border-gray-200">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
            <Star className="w-5 h-5" />
            <span>top performers</span>
          </h3>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {squadData.players
              .sort((a, b) => b.rating - a.rating)
              .slice(0, 6)
              .map((player, index) => (
                <div key={player.id} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                  <div className="w-10 h-10 bg-gray-200 rounded-full flex-shrink-0 overflow-hidden">
                    {player.photo && (
                      <img src={player.photo} alt={player.name} className="w-full h-full object-cover" />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="font-medium text-gray-900 truncate">{player.name}</div>
                    <div className="text-sm text-gray-500">{player.position} • {player.age}y</div>
                  </div>
                  <div className="flex flex-col items-end">
                    <div className={`px-2 py-1 rounded text-xs font-medium ${getRatingColor(player.rating)}`}>
                      {Math.round(player.rating)}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">
                      {formatCurrency(player.marketValue)}
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default SquadAnalysis;