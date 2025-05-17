import React from 'react';
import ReactDOM from 'react-dom/client'; // Ensure this import is correct
import './index.css';
import App from './App';

// Get the root element
const container = document.getElementById('root');

// Create a root using the new API
const root = ReactDOM.createRoot(container);

// Render the app
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);