import { useQuery } from '@tanstack/react-query';
import { productService } from '../services/product';

export const useProducts = () => {
  return useQuery({
    queryKey: ['products'],
    queryFn: () => productService.getProducts(),
  });
};
