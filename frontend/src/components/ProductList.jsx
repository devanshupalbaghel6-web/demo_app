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

  if (isLoading) return <div>Loading products...</div>;
  if (error) return <div>Error loading products: {error.message}</div>;

  return (
    <div className="product-list">
      <h2>Our Products</h2>
      <div className="products-grid">
        {products.map((product) => (
          <div key={product.id} className="product-card">
            {/* Display product image if available */}
            {product.image_url && (
              <img src={product.image_url} alt={product.name} style={{ maxWidth: '100%' }} />
            )}
            <h3>{product.name}</h3>
            <p>{product.description}</p>
            <p className="price">${product.price}</p>
            <button>Add to Cart</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProductList;
