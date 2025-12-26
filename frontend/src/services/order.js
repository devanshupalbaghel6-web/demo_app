import api from './api';

export const orderService = {
  createOrder: async (orderData, userId) => {
    const response = await api.post(`/orders/?user_id=${userId}`, orderData);
    return response.data;
  },

  getOrders: async (skip = 0, limit = 100) => {
    const response = await api.get(`/orders/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  getUserOrders: async (userId) => {
    const response = await api.get(`/users/${userId}/orders`);
    return response.data;
  },
};
