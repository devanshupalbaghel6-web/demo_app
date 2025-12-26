/**
 * Order Service
 * 
 * This module provides methods for interacting with the order-related API endpoints.
 * It handles creating orders and fetching order history.
 */

import api from './api';

export const orderService = {
  /**
   * Creates a new order.
   * 
   * @param {Object} orderData - The data for the new order
   * @param {Array} orderData.items - List of items in the order
   * @returns {Promise<Object>} The created order object
   */
  createOrder: async (orderData) => {
    const response = await api.post('/orders/', orderData);
    return response.data;
  },

  /**
   * Retrieves a list of orders with pagination.
   * 
   * @param {number} [skip=0] - Number of records to skip
   * @param {number} [limit=100] - Maximum number of records to return
   * @returns {Promise<Array>} List of orders
   */
  getOrders: async (skip = 0, limit = 100) => {
    const response = await api.get(`/orders/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  /**
   * Retrieves orders for a specific user.
   * 
   * @param {string} userId - The ID of the user
   * @returns {Promise<Array>} List of orders for the user
   */
  getUserOrders: async (userId) => {
    const response = await api.get(`/users/${userId}/orders`);
    return response.data;
  },
};
