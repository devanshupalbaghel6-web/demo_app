/**
 * App Component
 * 
 * This is the root component of the application.
 * It sets up the global providers (QueryClient, Auth, Cart) and the routing structure.
 */

import React from 'react';
// Import routing components
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// Import React Query provider and client
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
// Import context providers
import { AuthProvider } from './context/AuthContext';
import { CartProvider } from './context/CartContext';
// Import layout and page components
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import CartPage from './pages/CartPage';
import OrdersPage from './pages/OrdersPage';
import ProfilePage from './pages/ProfilePage';

// Create a client for React Query
const queryClient = new QueryClient();

/**
 * Main App Component
 * 
 * Wraps the application with necessary providers and defines the routes.
 */
function App() {
  return (
    // Provide React Query client to the app
    <QueryClientProvider client={queryClient}>
      {/* Provide Authentication state */}
      <AuthProvider>
        {/* Provide Cart state */}
        <CartProvider>
          {/* Set up Routing */}
          <Router>
            {/* Apply the main layout to all pages */}
            <Layout>
              <Routes>
                {/* Define application routes */}
                <Route path="/" element={<HomePage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/cart" element={<CartPage />} />
                <Route path="/orders" element={<OrdersPage />} />
                <Route path="/profile" element={<ProfilePage />} />
              </Routes>
            </Layout>
          </Router>
        </CartProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
