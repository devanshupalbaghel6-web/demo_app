/**
 * ProductCard Component
 * 
 * This component displays a single product's information in a card format.
 * It shows the product image, name, description, price, and an "Add to Cart" button.
 */

import React from 'react';
// Import cart context to handle adding products to the cart
import { useCart } from '../context/CartContext';

/**
 * ProductCard Component
 * 
 * @param {Object} props - Component props
 * @param {Object} props.product - The product object to display
 * @param {string} props.product.id - Product ID
 * @param {string} props.product.name - Product name
 * @param {string} props.product.description - Product description
 * @param {number} props.product.price - Product price
 * @param {string} [props.product.image_url] - URL of the product image
 */
const ProductCard = ({ product }) => {
  // Get the addToCart function from the cart context
  const { addToCart } = useCart();

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden flex flex-col h-full hover:shadow-lg transition-shadow duration-300">
      {/* Product Image */}
      {product.image_url && (
        <div className="h-48 overflow-hidden">
          <img 
            src={product.image_url} 
            alt={product.name} 
            className="w-full h-full object-cover hover:scale-105 transition-transform duration-300" 
          />
        </div>
      )}
      
      {/* Product Details */}
      <div className="p-4 flex-grow flex flex-col justify-between">
        <div>
          <h3 className="text-lg font-bold mb-2 text-gray-800">{product.name}</h3>
          <p className="text-gray-600 text-sm mb-4 line-clamp-3">{product.description}</p>
        </div>
        
        {/* Price and Action Button */}
        <div className="mt-auto">
          <div className="flex justify-between items-center mb-3">
            <span className="text-xl font-bold text-blue-600">${product.price.toFixed(2)}</span>
          </div>
          <button 
            onClick={() => addToCart(product)}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-200 flex items-center justify-center gap-2"
          >
            Add to Cart
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
