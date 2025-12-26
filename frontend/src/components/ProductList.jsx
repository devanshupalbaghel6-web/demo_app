import React from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../api';

// Function to fetch products from the API
const fetchProducts = async () => {
  const response = await api.get('/products');
  return response.data;
};

const ProductList = () => {
  // useQuery hook to fetch data
  // 'products' is the query key, used for caching
  const { data: products, isLoading, error } = useQuery({
    queryKey: ['products'],
    queryFn: fetchProducts,
  });

  if (isLoading) return <div className="text-center p-4">Loading products...</div>;
  if (error) return <div className="text-center text-red-500 p-4">Error loading products: {error.message}</div>;

  return (
    <div className="p-4">
      <h2 className="text-xl font-semibold mb-4">Our Products</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {products.map((product) => (
          <div key={product.id} className="bg-white rounded-lg shadow-md overflow-hidden flex flex-col">
            {/* Display product image if available */}
            {product.image_url && (
              <img src={product.image_url} alt={product.name} className="w-full h-48 object-cover" />
            )}
            <div className="p-4 flex-grow flex flex-col justify-between">
              <div>
                <h3 className="text-lg font-bold mb-2">{product.name}</h3>
                <p className="text-gray-600 text-sm mb-4">{product.description}</p>
              </div>
              <div>
                <p className="text-xl font-bold text-gray-800 mb-2">${product.price}</p>
                <button className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition duration-200">
                  Add to Cart
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProductList;
