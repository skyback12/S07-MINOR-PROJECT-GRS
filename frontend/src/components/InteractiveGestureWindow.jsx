import React, { useState } from 'react';

function InteractiveGestureWindow(props, ref) {
  const [showIframe, setShowIframe] = useState(false);

  return (
    <section ref={ref} className="bg-white py-16">
      <div className="container mx-auto text-center">
        <h2 className="text-3xl font-bold mb-4">Interactive Gesture Window</h2>
        <p className="text-lg text-gray-600 mb-6">
          Test gestures and interact with the system in real-time. Try swiping or pointing to see how the system responds.
        </p>
        <div className="mx-auto border-2 border-gray-300 rounded-lg shadow-lg flex items-center justify-center">
          {showIframe && (
            <iframe
              src="http://localhost:5000/slide_feed1"
              width="1240"
              height="840"
              title="Slide Feed"
              frameBorder="0"
              className="mx-auto mt-8"
            ></iframe>
          )}
        </div>
        <button
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
          onClick={() => setShowIframe(true)}
        >
          Show
        </button>
      </div>
    </section>
  );
}

export default React.forwardRef(InteractiveGestureWindow);