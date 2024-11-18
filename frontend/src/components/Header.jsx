import React from 'react';

function Header ({ onGetStarted }) {
  return (
    <header className="bg-blue-600 text-white py-12">
      <div className="container mx-auto text-center">
        <h1 className="text-5xl font-bold mb-4">Gesture Recognition System</h1>
        <p className="text-lg mb-6">
          Control your presentations and interact with the screen using hand gestures.
        </p>
        <button
          onClick={onGetStarted}
          className="bg-white text-blue-600 px-6 py-2 rounded-full shadow-lg hover:bg-gray-300 transition duration-300"
        >
          Get Started
        </button>
      </div>
    </header>
  );
};

export default Header;
