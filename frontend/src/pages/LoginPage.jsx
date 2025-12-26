/**
 * LoginPage Component
 * 
 * This component provides a form for users to log in to the application.
 * It handles user input, form submission, and error display.
 * Upon successful login, it redirects the user to the home page.
 */

import React, { useState } from 'react';
// Import auth context to access the login function
import { useAuth } from '../context/AuthContext';
// Import navigation hooks
import { useNavigate, Link } from 'react-router-dom';

const LoginPage = () => {
  // State for form inputs and error messages
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  
  // Get login function from AuthContext
  const { login } = useAuth();
  // Initialize navigation hook
  const navigate = useNavigate();

  /**
   * Handles form submission.
   * 
   * Calls the login function with the provided email and password.
   * Redirects to the home page on success, or displays an error message on failure.
   * 
   * @param {Event} e - The form submission event
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // Clear previous errors
    
    // Attempt to log in
    const success = await login(email, password);
    
    if (success) {
      // Redirect to home page on success
      navigate('/');
    } else {
      // Show error message on failure
      setError('Invalid email or password');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 bg-white p-8 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>
      
      {/* Error Message Display */}
      {error && <div className="bg-red-100 text-red-700 p-3 rounded mb-4">{error}</div>}
      
      {/* Login Form */}
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700 mb-2">Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div className="mb-6">
          <label className="block text-gray-700 mb-2">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition duration-200"
        >
          Login
        </button>
      </form>
      
      {/* Registration Link */}
      <p className="mt-4 text-center text-gray-600">
        Don't have an account? <Link to="/register" className="text-blue-600 hover:underline">Register</Link>
      </p>
    </div>
  );
};

export default LoginPage;
