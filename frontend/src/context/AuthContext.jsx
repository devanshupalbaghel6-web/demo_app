/**
 * AuthContext Module
 * 
 * This module provides authentication state management for the application.
 * It handles user login, registration, logout, and session persistence using JWT tokens.
 */

import React, { createContext, useState, useContext, useEffect } from 'react';
// Import the base API instance
import api from '../services/api';
// Import user service to fetch user details
import { userService } from '../services/user';

// Create the authentication context
const AuthContext = createContext();

/**
 * AuthProvider Component
 * 
 * Wraps the application (or part of it) to provide authentication state to children.
 * Manages the user object, authentication token, and loading state.
 * 
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Child components that need access to auth state
 */
export const AuthProvider = ({ children }) => {
  // State to hold the current authenticated user's information
  const [user, setUser] = useState(null);
  // State to hold the JWT access token, initialized from localStorage
  const [token, setToken] = useState(localStorage.getItem('token'));
  // State to track if the initial authentication check is in progress
  const [loading, setLoading] = useState(true);

  /**
   * Effect to handle token changes.
   * 
   * When the token changes:
   * 1. If a token exists, it sets the default Authorization header for API requests.
   * 2. Attempts to fetch the current user's profile.
   * 3. If the token is invalid or missing, it clears the user state and removes the header.
   */
  useEffect(() => {
    const fetchUser = async () => {
      if (token) {
        // Set the token in the default headers for all requests
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        try {
          // Fetch current user details from the backend
          const userData = await userService.getCurrentUser();
          setUser(userData);
        } catch (error) {
          console.error("Failed to fetch user", error);
          // If token is invalid or expired, logout the user
          logout();
        }
      } else {
        // Remove the Authorization header if no token is present
        delete api.defaults.headers.common['Authorization'];
        setUser(null);
      }
      // Mark loading as complete
      setLoading(false);
    };

    fetchUser();
  }, [token]);

  /**
   * Logs in a user with email and password.
   * 
   * @param {string} email - User's email address
   * @param {string} password - User's password
   * @returns {Promise<boolean>} - True if login was successful, false otherwise
   */
  const login = async (email, password) => {
    // Prepare form data for OAuth2 password flow
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    try {
      // Request a token from the backend
      const response = await api.post('/token', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      const { access_token } = response.data;
      
      // Update token state and persist to localStorage
      setToken(access_token);
      localStorage.setItem('token', access_token);
      
      // User details will be fetched automatically by the useEffect hook
      return true;
    } catch (error) {
      console.error("Login failed", error);
      return false;
    }
  };

  /**
   * Logs out the current user.
   * 
   * Clears the token and user state, and removes the token from localStorage.
   */
  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
  };

  /**
   * Registers a new user.
   * 
   * @param {string} email - User's email address
   * @param {string} password - User's password
   * @returns {Promise<boolean>} - True if registration was successful, false otherwise
   */
  const register = async (email, password) => {
    try {
      // Send registration request to the backend
      await api.post('/users/', { email, password });
      return true;
    } catch (error) {
      console.error("Registration failed", error);
      return false;
    }
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, register, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

/**
 * Custom hook to use the authentication context.
 * 
 * @returns {Object} The authentication context value (user, token, login, logout, register, loading)
 */
export const useAuth = () => useContext(AuthContext);
