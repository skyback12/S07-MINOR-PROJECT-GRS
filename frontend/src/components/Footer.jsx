import React, { useState } from 'react';
import PptxUploader from './uploadpptx';

function Footer({ onStartNow, onStopNow, isPresentationRunning }) {
  const [isUploading, setIsUploading] = useState(false);

  const handleStartNow = () => {
    setIsUploading(true);
    onStartNow();
  };

  const handleStopNow = () => {
    setIsUploading(true);
    onStopNow();
  };

  return (
    <footer className="bg-gray-800 text-white py-8">
      <div className="container mx-auto text-center">
        <h3 className="text-2xl font-bold mb-2">Ready to Control with Gestures?</h3>
          
        <button
          onClick={handleStartNow}
          className={`bg-blue-600 text-white px-6 py-3 rounded-full shadow-lg hover:bg-blue-700 ${isPresentationRunning ? 'opacity-50 cursor-not-allowed' : ''}`}
          disabled={isPresentationRunning}
        >
          {isPresentationRunning ? "Running..." : "Start Now"}
        </button>
        
        <button
          onClick={handleStopNow}
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