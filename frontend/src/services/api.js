/**
 * API Service Configuration
 * 
 * This module configures the Axios instance used for making HTTP requests to the backend.
 * It sets the base URL and default headers.
 */

import axios from 'axios';

// Create an Axios instance with default configuration
const api = axios.create({
  // Base URL for the backend API
  baseURL: 'http://localhost:8000',
  // Default headers for all requests
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
