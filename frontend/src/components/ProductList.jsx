/**
 * ProductList Component
 * 
 * This component renders a grid of ProductCard components.
 * It handles the case where no products are available.
 */

import React from 'react';
import ProductCard from './ProductCard';

/**
 * ProductList Component
 * 
 * @param {Object} props - Component props
 * @param {Array} props.products - List of product objects to display
 */
const ProductList = ({ products }) => {
  // Render a message if the product list is empty or undefined
  if (!products || products.length === 0) {
    return (
      <div className="text-center py-10">
        <p className="text-gray-500 text-lg">No products found.</p>
      </div>
    );
  }

  // Render the grid of product cards
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
};

export default ProductList;
