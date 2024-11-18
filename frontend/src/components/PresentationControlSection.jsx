import React, { useState } from 'react';

function PresentationControlSection({ onTryPresentationControl, onStopPresentationControl, isPresentationRunning }) {
  const [isIframeVisible, setIframeVisible] = useState(false);

  const handleTryPresentationControl = () => {
    onTryPresentationControl();
    setIframeVisible(true); // Show the iframe when presentation control starts
  };

  const handleStopPresentationControl = () => {
    onStopPresentationControl();
    setIframeVisible(false); // Hide the iframe when stopping presentation control
  };

  return (
    <section className="container mx-auto py-16 px-4 text-center">
      <h2 className="text-3xl font-bold mb-4">Gesture-Controlled Presentation System</h2>
      <p className="text-lg text-gray-600 max-w-xxl mx-auto mb-6">
        Navigate through slides seamlessly using hand gestures. Control your presentations without touching your device.
      </p>
      <div className="flex justify-center">
        <button
          onClick={handleTryPresentationControl}
          className="mt-4 mb-8 bg-blue-600 text-white px-6 py-3 rounded-full shadow-lg hover:bg-blue-700"
        >
          Try Presentation Control
        </button>
        <button
          onClick={handleStopPresentationControl}
          className="mt-4 mb-8 bg-red-600 text-white px-6 py-3 rounded-full shadow-lg hover:bg-red-700 m-2 "
        >
          Stop Presentation Control
        </button>
      </div>

      {/* Conditionally render iframe when presentation control is active */}
      {isIframeVisible && (
        <iframe
          src="http://localhost:5000/slide_feed"
          width="1240"
          height="840"
          title="Slide Feed"
          frameBorder="0"
          className="mx-auto mt-8"
        ></iframe>
      )}
    </section>
  );
}

export default PresentationControlSection;
