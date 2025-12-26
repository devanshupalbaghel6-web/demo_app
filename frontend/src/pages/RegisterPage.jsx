/**
 * RegisterPage Component
 * 
 * This component provides a form for new users to register an account.
 * It handles user input, password validation, and form submission.
 * Upon successful registration, it redirects the user to the login page.
 */

import React, { useState } from 'react';
// Import auth context to access the register function
import { useAuth } from '../context/AuthContext';
// Import navigation hooks
import { useNavigate, Link } from 'react-router-dom';

const RegisterPage = () => {
  // State for form inputs and error messages
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  
  // Get register function from AuthContext
  const { register } = useAuth();
  // Initialize navigation hook
  const navigate = useNavigate();

  /**
   * Handles form submission.
   * 
   * Validates that passwords match.
   * Calls the register function with the provided email and password.
   * Redirects to the login page on success, or displays an error message on failure.
   * 
   * @param {Event} e - The form submission event
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // Clear previous errors

    // Validate password confirmation
    if (password !== confirmPassword) {
      setError("Passwords don't match");
      return;
    }

    // Attempt to register
    const success = await register(email, password);
    
    if (success) {
      // Redirect to login page on success
      navigate('/login');
    } else {
      // Show error message on failure
      setError('Registration failed. Email might be taken.');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 bg-white p-8 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-center">Register</h2>
      
      {/* Error Message Display */}
      {error && <div className="bg-red-100 text-red-700 p-3 rounded mb-4">{error}</div>}
      
      {/* Registration Form */}
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
        <div className="mb-4">
          <label className="block text-gray-700 mb-2">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div className="mb-6">
          <label className="block text-gray-700 mb-2">Confirm Password</label>
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition duration-200"
        >
          Register
        </button>
      </form>
      
      {/* Login Link */}
      <p className="mt-4 text-center text-gray-600">
        Already have an account? <Link to="/login" className="text-blue-600 hover:underline">Login</Link>
      </p>
    </div>
  );
};

export default RegisterPage;
