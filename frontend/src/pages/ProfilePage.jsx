import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { orderService } from '../services/order';

const ProfilePage = () => {
  const { user, logout } = useAuth();
  const [orders, setOrders] = useState([]);
  const [loadingOrders, setLoadingOrders] = useState(true);

  useEffect(() => {
    const fetchOrders = async () => {
      if (user && user.id) {
        try {
          const data = await orderService.getUserOrders(user.id);
          setOrders(data);
        } catch (error) {
          console.error("Failed to fetch orders", error);
        } finally {
          setLoadingOrders(false);
        }
      }
    };

    fetchOrders();
  }, [user]);

  if (!user) {
    return <div className="text-center p-10">Please log in to view your profile.</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white shadow rounded-lg p-6 mb-8">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-3xl font-bold text-gray-800">My Profile</h1>
          <button 
            onClick={logout}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded transition duration-200"
          >
            Logout
          </button>
        </div>
        <div className="border-t border-gray-200 pt-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-500">Email</p>
              <p className="text-lg font-medium">{user.email}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">User ID</p>
              <p className="text-sm font-mono bg-gray-100 p-1 rounded">{user.id}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Account Status</p>
              <p className="text-lg font-medium">
                {user.is_active ? (
                  <span className="text-green-600">Active</span>
                ) : (
                  <span className="text-red-600">Inactive</span>
                )}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Role</p>
              <p className="text-lg font-medium">
                {user.is_admin ? 'Administrator' : 'Customer'}
              </p>
            </div>
          </div>
        </div>
      </div>

      <h2 className="text-2xl font-bold mb-4 text-gray-800">Order History</h2>
      {loadingOrders ? (
        <div className="text-center py-4">Loading orders...</div>
      ) : orders.length === 0 ? (
        <div className="bg-white shadow rounded-lg p-8 text-center">
          <p className="text-gray-500 mb-4">You haven't placed any orders yet.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {orders.map((order) => (
            <div key={order.id} className="bg-white shadow rounded-lg overflow-hidden border border-gray-200">
              <div className="bg-gray-50 px-6 py-4 border-b border-gray-200 flex flex-wrap justify-between items-center">
                <div>
                  <p className="text-sm text-gray-500">Order ID</p>
                  <p className="font-mono text-sm font-medium text-gray-700">{order.id}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Date</p>
                  <p className="font-medium text-gray-700">
                    {new Date(order.created_at).toLocaleDateString()}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Status</p>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    order.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                  </span>
                </div>
              </div>
              <div className="p-6">
                {/* We would list items here if the API returned them in the list view */}
                <p className="text-gray-600">Items details would appear here.</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ProfilePage;
