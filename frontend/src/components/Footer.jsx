import React from 'react';

function Footer({ onStartNow, onStopNow, isPresentationRunning }) {
  return (
    <footer className="bg-gray-800 text-white py-8">
      <div className="container mx-auto text-center">
        <h3 className="text-2xl font-bold mb-2">Ready to Control with Gestures?</h3>
          
        <button
          onClick={onStartNow}
          className={`bg-blue-600 text-white px-6 py-3 rounded-full shadow-lg hover:bg-blue-700 ${isPresentationRunning ? 'opacity-50 cursor-not-allowed' : ''}`}
          disabled={isPresentationRunning}
        >
          {isPresentationRunning ? "Running..." : "Start Now"}
        </button>
        
        <button
          onClick={onStopNow}
          className={`bg-red-600 text-white px-6 py-3 m-2 rounded-full shadow-lg hover:bg-red-700 ${!isPresentationRunning ? 'opacity-50 cursor-not-allowed' : ''}`}
          disabled={!isPresentationRunning}
        >
          {isPresentationRunning ? "Stop Now" : "Stopped"}
        </button>
      </div>
    </footer>
  );
}

export default Footer;
