import api from './api';

export const userService = {
  createUser: async (userData) => {
    const response = await api.post('/users/', userData);
    return response.data;
  },

  getUsers: async (skip = 0, limit = 100) => {
    const response = await api.get(`/users/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  getUser: async (id) => {
    const response = await api.get(`/users/${id}`);
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get('/users/me');
    return response.data;
  },
};
