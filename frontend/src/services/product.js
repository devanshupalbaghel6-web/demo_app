/**
 * Product Service
 * 
 * This module provides methods for interacting with the product-related API endpoints.
 * It handles fetching product lists, getting product details, and creating new products.
 */

import api from './api';

export const productService = {
  /**
   * Retrieves a list of products with pagination.
   * 
   * @param {number} [skip=0] - Number of records to skip
   * @param {number} [limit=100] - Maximum number of records to return
   * @returns {Promise<Array>} List of products
   */
  getProducts: async (skip = 0, limit = 100) => {
    const response = await api.get(`/products/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  /**
   * Retrieves details of a specific product.
   * 
   * @param {string} id - The ID of the product
   * @returns {Promise<Object>} The product details
   */
  getProduct: async (id) => {
    const response = await api.get(`/products/${id}`);
    return response.data;
  },

  /**
   * Creates a new product.
   * 
   * @param {Object} productData - The data for the new product
   * @param {string} productData.name - Name of the product
   * @param {string} productData.description - Description of the product
   * @param {number} productData.price - Price of the product
   * @returns {Promise<Object>} The created product object
   */
  createProduct: async (productData) => {
    const response = await api.post('/products/', productData);
    return response.data;
  },
};
