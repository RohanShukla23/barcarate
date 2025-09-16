import React from 'react';

function LoadingSpinner({ size = 'large', message = 'loading...' }) {
  const sizeClasses = {
    small: 'w-6 h-6',
    medium: 'w-8 h-8', 
    large: 'w-12 h-12'
  };

  return (
    <div className="flex flex-col items-center justify-center space-y-4">
      <div className="relative">
        <div className={`${sizeClasses[size]} border-4 border-white border-opacity-30 rounded-full animate-spin`}>
          <div className={`${sizeClasses[size]} border-4 border-barca-yellow border-t-transparent rounded-full animate-spin`}></div>
        </div>
      </div>
      <div className="text-white text-sm font-medium animate-pulse">
        {message}
      </div>
    </div>
  );
}

export default LoadingSpinner;