import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      // In a real app, you'd validate the token with the backend here
      // For now, we'll just assume it's valid and decode the email if possible
      // or just set a dummy user state if we don't have a /me endpoint yet
      // Let's try to fetch user details if we had an endpoint, but we don't have /me yet.
      // So we will just persist the login state.
      setUser({ email: 'user@example.com' }); // Placeholder
    }
    setLoading(false);
  }, [token]);

  const login = async (email, password) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    try {
      const response = await api.post('/token', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      const { access_token } = response.data;
      setToken(access_token);
      localStorage.setItem('token', access_token);
      setUser({ email });
      return true;
    } catch (error) {
      console.error("Login failed", error);
      return false;
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
  };

  const register = async (email, password) => {
    try {
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

export const useAuth = () => useContext(AuthContext);
