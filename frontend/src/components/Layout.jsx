/**
 * Layout Component
 * 
 * This component serves as the main wrapper for the application's pages.
 * It includes the header (navigation bar), the main content area, and the footer.
 * It handles responsive navigation and displays the cart item count.
 */

import React from 'react';
// Import Link for client-side navigation
import { Link } from 'react-router-dom';
// Import auth context to conditionally render links based on login status
import { useAuth } from '../context/AuthContext';
// Import cart context to display the number of items in the cart
import { useCart } from '../context/CartContext';

/**
 * Layout Component
 * 
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - The content to render inside the main area
 */
const Layout = ({ children }) => {
  // Get user authentication state and logout function
  const { user, logout } = useAuth();
  // Get cart state to calculate total items
  const { cart } = useCart();

  // Calculate the total number of items in the cart
  const cartItemCount = cart.reduce((acc, item) => acc + item.quantity, 0);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header Section */}
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          {/* Logo / Brand Name */}
          <Link to="/" className="text-2xl font-bold text-blue-600">E-Shop</Link>
          
          {/* Navigation Menu */}
          <nav>
            <ul className="flex space-x-6 items-center">
              <li><Link to="/" className="text-gray-600 hover:text-blue-600 font-medium">Home</Link></li>
              
              {/* Cart Link with Badge */}
              <li>
                <Link to="/cart" className="text-gray-600 hover:text-blue-600 font-medium relative">
                  Cart
                  {cartItemCount > 0 && (
                    <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                      {cartItemCount}
                    </span>
                  )}
                </Link>
              </li>
              
              {/* Conditional Rendering based on Auth Status */}
              {user ? (
                <>
                  <li><Link to="/orders" className="text-gray-600 hover:text-blue-600 font-medium">Orders</Link></li>
                  <li><Link to="/profile" className="text-gray-600 hover:text-blue-600 font-medium">Profile</Link></li>
                </>
              ) : (
                <>
                  <li><Link to="/login" className="text-gray-600 hover:text-blue-600 font-medium">Login</Link></li>
                  <li><Link to="/register" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition duration-200">Register</Link></li>
                </>
              )}
            </ul>
          </nav>
        </div>
      </header>
      
      {/* Main Content Area */}
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
      
      {/* Footer Section */}
      <footer className="bg-gray-800 text-white py-8 mt-auto">
        <div className="container mx-auto px-4 text-center">
          <p>&copy; 2025 E-Shop. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
