---

# Gesture Control System - Frontend

The frontend of the Gesture Control System is the user interface that interacts with the backend and allows users to control presentations using gestures and voice commands. This project is built with **Vite** for a fast, optimized development experience.

## Features

- **Fast Development**: Instant Hot Module Replacement (HMR) with Vite for a smooth development experience.
- **Interactive UI**: A clean, user-friendly interface for controlling presentations.
- **Real-time Communication**: Seamless communication with the backend using RESTful APIs or WebSockets.
- **Slide Control**: Display and control PowerPoint slides through gestures and voice.
- **Speech Recognition**: Integration with the backend's speech recognition system to control slides.
- **Custom Gesture Handling**: Display options for users to define their gestures for interaction.

## Technologies Used

- **Frontend Framework**: React.js (or Vue.js, depending on your choice)
- **Build Tool**: Vite
- **Styling**: CSS, Material UI (or any CSS framework you prefer)
- **Communication**: Axios (for API requests) or WebSocket (for real-time communication)
- **Speech Recognition**: JavaScript Web Speech API (or any other browser-based speech library)
- **Others**: React Router for page navigation, State management with Redux (optional)

## Installation

### Prerequisites

1. **Node.js** (version 16.x or later)
2. **npm** (Node Package Manager)

### Clone the repository
```bash
git clone https://github.com/skyback12/S07-MINOR-PROJECT-GRS.git
```

### Install dependencies
Navigate to the frontend directory and install dependencies:
```bash
cd frontend
npm install
```

### Run the Development Server
Start the Vite development server:
```bash
npm run dev
```
This will open the application in your browser (usually at `http://localhost:5173`).

## Folder Structure

```
frontend/
├── public/                # Static files (index.html, etc.)
├── src/                   # Main application code
│   ├── assets/            # Images, icons, etc.
│   ├── components/        # Reusable React components
│   ├── pages/             # Different pages/views in the app
│   ├── services/          # API service for backend communication
│   ├── App.jsx            # Root application component
│   ├── main.js            # Entry point for the app
│   └── styles/            # Custom styles
├── vite.config.js         # Vite configuration
├── package.json           # Project dependencies and scripts
└── README.md              # This file
```

## Usage

- The frontend communicates with the backend to retrieve slides and interact with the gesture control system.
- Use hand gestures to navigate through slides or speak commands to control the presentation.
- The interface will provide visual feedback for gesture recognition and actions.

## Vite Configuration

Vite is used as the build tool, and it provides fast development builds with HMR and optimizations for production builds. The configuration file (`vite.config.js`) allows for customizations such as plugin usage, aliasing, and environment variables.

```js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
});
```

## Future Enhancements

- Implement more advanced UI features for better user interaction.
- Add support for additional gesture types and actions.
- Optimize performance for handling large presentations.
- Implement cross-browser compatibility.


## Acknowledgements

- Vite for the fast build tool and development experience.
- React.js for the frontend framework.
- Material UI for design components.
- The Python backend for machine learning and gesture recognition.

---

