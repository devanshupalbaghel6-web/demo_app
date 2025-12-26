/**
 * User Service
 * 
 * This module provides methods for interacting with the user-related API endpoints.
 * It handles user registration, fetching user lists, and retrieving user profiles.
 */

import api from './api';

export const userService = {
  /**
   * Creates a new user (Registration).
   * 
   * @param {Object} userData - The data for the new user
   * @param {string} userData.email - User's email
   * @param {string} userData.password - User's password
   * @returns {Promise<Object>} The created user object
   */
  createUser: async (userData) => {
    const response = await api.post('/users/', userData);
    return response.data;
  },

  /**
   * Retrieves a list of users with pagination.
   * 
   * @param {number} [skip=0] - Number of records to skip
   * @param {number} [limit=100] - Maximum number of records to return
   * @returns {Promise<Array>} List of users
   */
  getUsers: async (skip = 0, limit = 100) => {
    const response = await api.get(`/users/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  /**
   * Retrieves details of a specific user by ID.
   * 
   * @param {string} id - The ID of the user
   * @returns {Promise<Object>} The user details
   */
  getUser: async (id) => {
    const response = await api.get(`/users/${id}`);
    return response.data;
  },

  /**
   * Retrieves the profile of the currently authenticated user.
   * 
   * @returns {Promise<Object>} The current user's profile
   */
  getCurrentUser: async () => {
    const response = await api.get('/users/me');
    return response.data;
  },
};
