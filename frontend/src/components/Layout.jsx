import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';

const Layout = ({ children }) => {
  const { user, logout } = useAuth();
  const { cart } = useCart();

  const cartItemCount = cart.reduce((acc, item) => acc + item.quantity, 0);

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <Link to="/" className="text-2xl font-bold text-blue-600">E-Shop</Link>
          <nav>
            <ul className="flex space-x-6 items-center">
              <li><Link to="/" className="text-gray-600 hover:text-blue-600 font-medium">Home</Link></li>
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
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
      <footer className="bg-gray-800 text-white py-8 mt-auto">
        <div className="container mx-auto px-4 text-center">
          <p>&copy; 2025 E-Shop. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
