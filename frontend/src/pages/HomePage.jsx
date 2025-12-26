import React from 'react';
import { useProducts } from '../hooks/useProducts';
import ProductList from '../components/ProductList';

const HomePage = () => {
  const { data: products, isLoading, error } = useProducts();

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong className="font-bold">Error!</strong>
        <span className="block sm:inline"> {error.message}</span>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8 text-center">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">Featured Products</h2>
        <p className="text-gray-600">Check out our latest collection</p>
      </div>
      <ProductList products={products} />
    </div>
  );
};

export default HomePage;
