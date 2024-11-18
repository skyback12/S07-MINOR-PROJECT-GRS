import React, { useRef, useState, useEffect } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import PresentationControlSection from './components/PresentationControlSection';
import InteractiveGestureWindow from './components/InteractiveGestureWindow';
import axios from 'axios';
import PptxUploader from './components/uploadpptx';
import Modal from './components/model';

function App() {
  const gestureSectionRef = useRef(null);
  const [isPresentationRunning, setIsPresentationRunning] = useState(false);
  const [isPresentation2Running, setIsPresentation2Running] = useState(false);
  const [isUploading, setIsUploading] = useState(false);  // State to control file upload window

  const handleGetStarted = () => {
    if (gestureSectionRef.current) {
      gestureSectionRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleTryPresentationControl = async () => {
    try {
      await startPresentation2();
      alert('Presentation control started!');
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const startPresentation = () => {
    return axios.get('http://localhost:5000/api/start1')
      .then(response => {
        console.log(response.data.status);
        setIsPresentationRunning(true);
      })
      .catch(error => {
        console.error('There was an error starting the presentation!', error);
      });
  };

  const stopPresentation = () => {
    axios.get('http://localhost:5000/api/stop1')
      .then(response => {
        console.log(response.data.status);
        setIsPresentationRunning(false);
      })
      .catch(error => {
        console.error('There was an error stopping the presentation!', error);
      });
  };

  const startPresentation2 = () => {
    return axios.get('http://localhost:5000/api/start2')
      .then(response => {
        console.log(response.data.status);
        setIsPresentation2Running(true);
      })
      .catch(error => {
        console.error('There was an error starting the presentation!', error);
      });
  };

  const stopPresentation2 = () => {
    axios.get('http://localhost:5000/api/stop2')
      .then(response => {
        console.log(response.data.status);
        setIsPresentation2Running(false);
      })
      .catch(error => {
        console.error('There was an error stopping the presentation!', error);
      });
  };

  // Handle the start button to open the PptxUploader
  const handleStartNow = () => {
    setIsUploading(true);  // Show the PptxUploader when Start Now is clicked
    startPresentation();    // Optionally start presentation functionality
  };

  return (
    <div className="bg-gray-100 min-h-screen">
      <Header onGetStarted={handleGetStarted} />
      <PresentationControlSection
        onTryPresentationControl={handleTryPresentationControl}
        onStopPresentationControl={stopPresentation2}
        isPresentationRunning={isPresentation2Running}
      />
      <InteractiveGestureWindow ref={gestureSectionRef} />

     

      <Footer 
        onStartNow={handleStartNow}  // Use the new handler here
        onStopNow={stopPresentation} 
        isPresentationRunning={isPresentationRunning} 
        onStartNow2={startPresentation2} 
        onStopNow2={stopPresentation2} 
        isPresentation2Running={isPresentation2Running} 
      />
      <Modal isOpen={isUploading} closeModal={() => setIsUploading(false)}>
        <PptxUploader setIsUploading={setIsUploading} />
      </Modal>
      

    </div>
  );
}

export default App;
