/**
 * useProducts Hook
 * 
 * This custom hook fetches the list of products from the backend using React Query.
 * It handles caching, loading states, and error states automatically.
 */

import { useQuery } from '@tanstack/react-query';
// Import the product service to make the API call
import { productService } from '../services/product';

/**
 * Custom hook to fetch products.
 * 
 * @returns {Object} The query result object containing data, isLoading, error, etc.
 */
export const useProducts = () => {
  return useQuery({
    // Unique key for caching the product list
    queryKey: ['products'],
    // Function to fetch the data
    queryFn: () => productService.getProducts(),
  });
};
