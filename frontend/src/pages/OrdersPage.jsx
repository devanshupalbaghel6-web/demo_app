import React, { useEffect, useState } from 'react';
import { orderService } from '../services/order';
import { useAuth } from '../context/AuthContext';

const OrdersPage = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    const fetchOrders = async () => {
      if (user) {
        try {
          // Again, assuming we have user.id or using a fallback
          const userId = user.id || 2; 
          const data = await orderService.getUserOrders(userId);
          setOrders(data);
        } catch (error) {
          console.error("Failed to fetch orders", error);
        } finally {
          setLoading(false);
        }
      }
    };

    fetchOrders();
  }, [user]);

  if (loading) return <div className="text-center p-4">Loading orders...</div>;

  if (orders.length === 0) {
    return (
      <div className="text-center py-10">
        <h2 className="text-2xl font-bold mb-4">No Orders Yet</h2>
        <p className="text-gray-600">Start shopping to see your orders here.</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-6">Your Orders</h2>
      <div className="space-y-6">
        {orders.map((order) => (
          <div key={order.id} className="bg-white shadow-md rounded-lg overflow-hidden border border-gray-200">
            <div className="bg-gray-50 p-4 border-b border-gray-200 flex justify-between items-center">
              <div>
                <span className="font-bold text-gray-700">Order #{order.id}</span>
                <span className="ml-4 text-sm text-gray-500">{new Date(order.created_at || Date.now()).toLocaleDateString()}</span>
              </div>
              <div>
                <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                  order.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {order.status}
                </span>
              </div>
            </div>
            <div className="p-4">
              <ul className="divide-y divide-gray-100">
                {order.items && order.items.map((item) => (
                  <li key={item.id} className="py-3 flex justify-between">
                    <div className="flex items-center">
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
