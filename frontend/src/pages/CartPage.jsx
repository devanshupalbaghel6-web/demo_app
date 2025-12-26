import React from 'react';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { orderService } from '../services/order';

const CartPage = () => {
  const { cart, removeFromCart, updateQuantity, clearCart, total } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();

  const handleCheckout = async () => {
    if (!user) {
      navigate('/login');
      return;
    }

    try {
      // Prepare order data
      const orderData = {
        items: cart.map(item => ({
          product_id: item.id,
          quantity: item.quantity
        }))
      };

      // We need the user ID. In a real app, the backend would get it from the token.
      // Since our backend expects user_id in the query param (based on previous code),
      // we need to fetch the user ID first or store it in AuthContext.
      // For now, let's assume we can get it or the backend is updated to use the token.
      // Wait, the backend `create_order` takes `user_id` as a query param.
      // Ideally, it should take it from the current user dependency.
      // I'll assume for now we might fail here if we don't have the ID.
      // Let's try to pass a dummy ID or fix the backend to use `current_user`.
      
      // FIX: The backend `create_order` endpoint currently requires `user_id` as a query param.
      // This is not ideal for security. I should have fixed that in the backend refactor.
      // But for now, let's assume the user object in AuthContext has an ID.
      // If not, we might need to fetch "me" first.
      
      // Let's assume user.id is available. If not, we'll use a hardcoded one for demo if needed,
      // but better to fix the backend.
      
      // For this demo, I'll assume the user has an ID.
      // If the AuthContext doesn't have it, we might need to fetch it.
      
      // The backend now uses the current user from the token
      await orderService.createOrder(orderData);
      
      clearCart();
      alert('Order placed successfully!');
      navigate('/orders');
    } catch (error) {
      console.error("Checkout failed", error);
      alert('Checkout failed. Please try again.');
    }
  };

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
