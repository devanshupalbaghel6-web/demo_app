import React from 'react';

const Layout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-blue-600">E-Shop</h1>
          <nav>
            <ul className="flex space-x-6">
              <li><a href="#" className="text-gray-600 hover:text-blue-600 font-medium">Home</a></li>
              <li><a href="#" className="text-gray-600 hover:text-blue-600 font-medium">Products</a></li>
              <li><a href="#" className="text-gray-600 hover:text-blue-600 font-medium">Cart</a></li>
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
