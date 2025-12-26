/**
 * CartContext Module
 * 
 * This module provides state management for the shopping cart.
 * It handles adding items, removing items, updating quantities, and calculating the total price.
 * The cart state is persisted to localStorage to survive page reloads.
 */

import React, { createContext, useState, useContext, useEffect } from 'react';

// Create the cart context
const CartContext = createContext();

/**
 * CartProvider Component
 * 
 * Wraps the application (or part of it) to provide cart state to children.
 * Manages the list of items in the cart and provides methods to manipulate them.
 * 
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Child components that need access to cart state
 */
export const CartProvider = ({ children }) => {
  // Initialize cart state from localStorage if available, otherwise default to an empty array
  const [cart, setCart] = useState(() => {
    const savedCart = localStorage.getItem('cart');
    return savedCart ? JSON.parse(savedCart) : [];
  });

  /**
   * Effect to persist cart state to localStorage whenever it changes.
   */
  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cart));
  }, [cart]);

  /**
   * Adds a product to the cart.
   * 
   * If the product is already in the cart, its quantity is incremented.
   * Otherwise, it is added as a new item with quantity 1.
   * 
   * @param {Object} product - The product to add
   * @param {string} product.id - Unique identifier of the product
   * @param {string} product.name - Name of the product
   * @param {number} product.price - Price of the product
   */
  const addToCart = (product) => {
    setCart((prevCart) => {
      // Check if the item already exists in the cart
      const existingItem = prevCart.find((item) => item.id === product.id);
      if (existingItem) {
        // If it exists, increment the quantity
        return prevCart.map((item) =>
          item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
        );
      }
      // If it doesn't exist, add it with quantity 1
      return [...prevCart, { ...product, quantity: 1 }];
    });
  };

  /**
   * Removes an item from the cart completely.
   * 
   * @param {string} productId - The ID of the product to remove
   */
  const removeFromCart = (productId) => {
    setCart((prevCart) => prevCart.filter((item) => item.id !== productId));
  };

  /**
   * Updates the quantity of a specific item in the cart.
   * 
   * @param {string} productId - The ID of the product to update
   * @param {number} quantity - The new quantity (must be at least 1)
   */
  const updateQuantity = (productId, quantity) => {
    // Prevent setting quantity to less than 1
    if (quantity < 1) return;
    
    setCart((prevCart) =>
      prevCart.map((item) =>
        item.id === productId ? { ...item, quantity } : item
      )
    );
  };

  /**
   * Clears all items from the cart.
   */
  const clearCart = () => {
    setCart([]);
  };

  // Calculate the total price of all items in the cart
  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  return (
    <CartContext.Provider value={{ cart, addToCart, removeFromCart, updateQuantity, clearCart, total }}>
      {children}
    </CartContext.Provider>
  );
};

/**
 * Custom hook to use the cart context.
 * 
 * @returns {Object} The cart context value (cart, addToCart, removeFromCart, updateQuantity, clearCart, total)
 */
export const useCart = () => useContext(CartContext);
