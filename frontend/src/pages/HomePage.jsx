/**
 * HomePage Component
 * 
 * This is the landing page of the application.
 * It fetches and displays a list of featured products using the ProductList component.
 * It handles loading and error states during data fetching.
 */

import React from 'react';
// Import custom hook for fetching products
import { useProducts } from '../hooks/useProducts';
// Import component to display the list of products
import ProductList from '../components/ProductList';

const HomePage = () => {
  // Fetch products, loading state, and error state from the custom hook
  const { data: products, isLoading, error } = useProducts();

  // Display a loading spinner while data is being fetched
  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  // Display an error message if data fetching fails
  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong className="font-bold">Error!</strong>
        <span className="block sm:inline"> {error.message}</span>
      </div>
    );
  }

  // Render the main content
  return (
    <div>
      {/* Hero / Welcome Section */}
      <div className="mb-8 text-center">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">Featured Products</h2>
        <p className="text-gray-600">Check out our latest collection</p>
      </div>
      
      {/* Product Grid */}
      <ProductList products={products} />
    </div>
  );
};

export default HomePage;
