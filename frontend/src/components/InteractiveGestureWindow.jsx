import React, { forwardRef } from 'react';
//uses the forwardRef function from React to pass a ref to an element inside the component.

//This allows external components or elements to access and control the ref of the section, enabling features like scrolling, focus management, or tracking. 
function InteractiveGestureWindow(props, ref) {
  return (
    <section ref={ref} className="bg-white py-16">
      <div className="container mx-auto text-center">
        <h2 className="text-3xl font-bold mb-4">Interactive Gesture Window</h2>
        <p className="text-lg text-gray-600 mb-6">
          Test gestures and interact with the system in real-time. Try swiping or pointing to see how the system responds.
        </p>
        <div className="mx-auto w-96 h-96 border-2 border-gray-300 rounded-lg shadow-lg flex items-center justify-center">
          <span className="text-xl text-gray-500">Gesture Window (Demo)</span>   
        </div>
      </div>
    </section>
  );
}

export default forwardRef(InteractiveGestureWindow);


