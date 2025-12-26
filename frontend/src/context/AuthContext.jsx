import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../services/api';
import { userService } from '../services/user';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      if (token) {
        // Set the token in the default headers for all requests
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        try {
          const userData = await userService.getCurrentUser();
          setUser(userData);
        } catch (error) {
          console.error("Failed to fetch user", error);
          // If token is invalid, logout
          logout();
        }
      } else {
        delete api.defaults.headers.common['Authorization'];
        setUser(null);
      }
      setLoading(false);
    };

    fetchUser();
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
      // User will be fetched by the useEffect
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
