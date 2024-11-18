import React from 'react';

function Modal({ isOpen, closeModal, children }) {
  if (!isOpen) return null;  // Do not render the modal if isOpen is false

  return (
    <div className="fixed inset-0 bg-gray-500 bg-opacity-50 flex justify-center items-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <button
          className="absolute top-2 right-2 text-gray-500"
          onClick={closeModal}
        >
          X
        </button>
        <div>
          {children}
        </div>
      </div>
    </div>
  );
}

export default Modal;
