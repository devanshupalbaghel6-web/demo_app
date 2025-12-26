/**
 * CartPage Component
 * 
 * This component displays the contents of the user's shopping cart.
 * It allows users to view items, update quantities, remove items, and proceed to checkout.
 */

import React from 'react';
// Import the cart context to access cart state and actions
import { useCart } from '../context/CartContext';
// Import the auth context to check if the user is logged in
import { useAuth } from '../context/AuthContext';
// Import useNavigate for programmatic navigation
import { useNavigate } from 'react-router-dom';
// Import the order service to submit the order
import { orderService } from '../services/order';

const CartPage = () => {
  // Destructure cart state and actions from the CartContext
  const { cart, removeFromCart, updateQuantity, clearCart, total } = useCart();
  // Get the current user from AuthContext
  const { user } = useAuth();
  // Initialize the navigation hook
  const navigate = useNavigate();

  /**
   * Handles the checkout process.
   * 
   * 1. Checks if the user is logged in. If not, redirects to login.
   * 2. Prepares the order payload from the cart items.
   * 3. Calls the backend API to create the order.
   * 4. Clears the cart upon success and redirects to the orders page.
   */
  const handleCheckout = async () => {
    // If user is not authenticated, redirect to login page
    if (!user) {
      navigate('/login');
      return;
    }

    try {
      // Prepare order data in the format expected by the backend
      // We map the cart items to an array of objects containing product_id and quantity
      const orderData = {
        items: cart.map(item => ({
          product_id: item.id,
          quantity: item.quantity
        }))
      };

      // Call the createOrder service method.
      // The backend now extracts the user ID from the authentication token,
      // so we don't need to pass it explicitly.
      await orderService.createOrder(orderData);
      
      // Clear the local cart state
      clearCart();
      
      // Notify the user of success
      alert('Order placed successfully!');
      
      // Redirect to the orders history page
      navigate('/orders');
    } catch (error) {
      // Log error and notify user if checkout fails
      console.error("Checkout failed", error);
      alert('Checkout failed. Please try again.');
    }
  };

  // Render empty cart state if there are no items
  if (cart.length === 0) {
    return (
      <div className="text-center py-10">
        <h2 className="text-2xl font-bold mb-4">Your Cart is Empty</h2>
        <p className="text-gray-600">Go add some products!</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-6">Shopping Cart</h2>
      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-4 text-left">Product</th>
              <th className="p-4 text-center">Price</th>
              <th className="p-4 text-center">Quantity</th>
              <th className="p-4 text-center">Total</th>
              <th className="p-4 text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            {cart.map((item) => (
              <tr key={item.id} className="border-b">
                <td className="p-4">
                  <div className="flex items-center">
                    {item.image_url && (
                      <img src={item.image_url} alt={item.name} className="w-16 h-16 object-cover rounded mr-4" />
                    )}
                    <span className="font-semibold">{item.name}</span>
                  </div>
                </td>
                <td className="p-4 text-center">${item.price.toFixed(2)}</td>
                <td className="p-4 text-center">
                  <input
                    type="number"
                    min="1"
                    value={item.quantity}
                    onChange={(e) => updateQuantity(item.id, parseInt(e.target.value))}
                    className="w-16 border rounded p-1 text-center"
                  />
                </td>
                <td className="p-4 text-center">${(item.price * item.quantity).toFixed(2)}</td>
                <td className="p-4 text-center">
                  <button
                    onClick={() => removeFromCart(item.id)}
                    className="text-red-500 hover:text-red-700"
                  >
                    Remove
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="p-6 bg-gray-50 flex justify-between items-center">
          <div className="text-xl font-bold">
            Total: ${total.toFixed(2)}
          </div>
          <button
            onClick={handleCheckout}
            className="bg-green-600 text-white py-2 px-6 rounded hover:bg-green-700 transition duration-200"
          >
            Checkout
          </button>
        </div>
      </div>
    </div>
  );
};

export default CartPage;
