import axios from 'axios';

// Create an Axios instance with the base URL of our backend
// This makes it easier to make requests without repeating the URL
const api = axios.create({
  baseURL: 'http://localhost:8000', // Default FastAPI port
});

export default api;
