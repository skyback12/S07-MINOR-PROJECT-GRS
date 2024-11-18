import React from 'react';
import axios from 'axios';

function SlideController() {
  const handleNextSlide = () => {
    axios.post('http://localhost:5000/next')
      .then(response => {
        console.log('Next slide triggered:', response.data);
      })
      .catch(error => {
        console.error('Error triggering next slide:', error);
      });
  };

  const handlePreviousSlide = () => {
    axios.post('http://localhost:5000/prev')
      .then(response => {
        console.log('Previous slide triggered:', response.data);
      })
      .catch(error => {
        console.error('Error triggering previous slide:', error);
      });
  };

  return (
    <div className="flex justify-center items-center space-x-4 mt-4">
      <button 
        onClick={handlePreviousSlide}
        className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition duration-200"
      >
        Previous Slide
      </button>
      <button 
        onClick={handleNextSlide}
        className="px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition duration-200"
      >
        Next Slide
      </button>
    </div>
  );
}

export default SlideController;


