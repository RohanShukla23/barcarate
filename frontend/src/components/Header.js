import React from 'react';
import { TrendingUp, Users, Search } from 'lucide-react';

function Header() {
  return (
    <header className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between py-6">
          {/* logo and title */}
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-gradient-to-r from-barca-blue to-barca-red rounded-full flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Barca<span className="text-barca-red">Rate</span>
              </h1>
              <p className="text-sm text-gray-600">transfer evaluation system</p>
            </div>
          </div>
          
          {/* features */}
          <div className="hidden md:flex items-center space-x-6">
            <div className="flex items-center space-x-2 text-gray-600">
              <Users className="w-4 h-4" />
              <span className="text-sm">squad analysis</span>
            </div>
            <div className="flex items-center space-x-2 text-gray-600">
              <Search className="w-4 h-4" />
              <span className="text-sm">player search</span>
            </div>
            <div className="flex items-center space-x-2 text-gray-600">
              <TrendingUp className="w-4 h-4" />
              <span className="text-sm">transfer rating</span>
            </div>
          </div>
          
          {/* barcelona colors accent */}
          <div className="flex space-x-1">
            <div className="w-3 h-8 bg-barca-blue rounded"></div>
            <div className="w-3 h-8 bg-barca-red rounded"></div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;