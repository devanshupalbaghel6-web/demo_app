/**
 * OrdersPage Component
 * 
 * This component displays the list of orders placed by the authenticated user.
 * It fetches order data from the backend and renders it in a list format.
 */

import React, { useEffect, useState } from 'react';
// Import the order service to make API calls related to orders
import { orderService } from '../services/order';
// Import the auth context to get the current user's information
import { useAuth } from '../context/AuthContext';

const OrdersPage = () => {
  // State to store the list of orders
  const [orders, setOrders] = useState([]);
  // State to handle the loading status of the data fetch
  const [loading, setLoading] = useState(true);
  // Get the authenticated user object from the AuthContext
  const { user } = useAuth();

  /**
   * useEffect hook to fetch orders when the component mounts or when the user changes.
   */
  useEffect(() => {
    const fetchOrders = async () => {
      // Only attempt to fetch if a user is logged in and has an ID
      if (user && user.id) {
        try {
          // Call the service to get orders for the specific user ID
          const data = await orderService.getUserOrders(user.id);
          // Update the state with the fetched orders
          setOrders(data);
        } catch (error) {
          // Log any errors that occur during the fetch
          console.error("Failed to fetch orders", error);
        } finally {
          // Set loading to false regardless of success or failure
          setLoading(false);
        }
      }
    };

    fetchOrders();
  }, [user]); // Dependency array: re-run if 'user' changes

  // Render a loading message while data is being fetched
  if (loading) return <div className="text-center p-4">Loading orders...</div>;

  // Render a message if the user has no orders
  if (orders.length === 0) {
    return (
      <div className="text-center py-10">
        <h2 className="text-2xl font-bold mb-4">No Orders Yet</h2>
        <p className="text-gray-600">Start shopping to see your orders here.</p>
      </div>
    );
  }

  // Render the list of orders
  return (
    <div className="max-w-4xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-6">Your Orders</h2>
      <div className="space-y-6">
        {/* Map through the orders array and render a card for each order */}
        {orders.map((order) => (
          <div key={order.id} className="bg-white shadow-md rounded-lg overflow-hidden border border-gray-200">
            {/* Order Header: ID, Date, Status */}
            <div className="bg-gray-50 p-4 border-b border-gray-200 flex justify-between items-center">
              <div>
                <span className="font-bold text-gray-700">Order #{order.id}</span>
                <span className="ml-4 text-sm text-gray-500">
                  {/* Format the creation date */}
                  {new Date(order.created_at || Date.now()).toLocaleDateString()}
                </span>
              </div>
              <div>
                {/* Display status with conditional styling based on value */}
                <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                  order.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {order.status}
                </span>
              </div>
            </div>
            {/* Order Body: List of Items */}
            <div className="p-4">
              <ul className="divide-y divide-gray-100">
                {/* Map through the items in the order */}
                {order.items && order.items.map((item) => (
                  <li key={item.id} className="py-3 flex justify-between">
                    <div className="flex items-center">
                      {/* Display Product ID (In a real app, we'd fetch the product name) */}
                      <span className="font-medium text-gray-800">Product ID: {item.product_id}</span>
                      <span className="ml-4 text-gray-600">x {item.quantity}</span>
                    </div>
                    <span className="font-medium text-gray-800">${item.price_at_purchase}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default OrdersPage;
