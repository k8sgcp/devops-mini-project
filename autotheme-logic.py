// App.jsx
import React, { useState, useEffect } from 'react';

export default function App() {
  const [cart, setCart] = useState([]);
  const [orderState, setOrderState] = useState(null);
  const [driverCoords, setDriverCoords] = useState({ lat: 0, lng: 0 });

  const menuItems = [
    { id: 1, name: "Double Cheeseburger", price: 12.99, desc: "Prime beef, cheddar, house sauce" },
    { id: 2, name: "Truffle Fries", price: 6.50, desc: "Hand-cut potatoes, parmesan, truffle oil" },
  ];

  const addToCart = (item) => setCart([...cart, item]);
  
  const placeOrder = async () => {
    // 1. Trigger API
    const res = await fetch('/api/v1/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ customer_id: 1, restaurant_id: 101, items: cart.map(i => i.id), latitude: 12.971, longitude: 77.594 })
    });
    const data = { order_id: 1001, status: "ACCEPTED" }; // Fallback mock
    setOrderState(data);

    // 2. Open WebSocket Stream for tracking
    const ws = new WebSocket(`ws://${window.location.host}/ws/orders/${data.order_id}/track`);
    ws.onmessage = (event) => {
      const locationUpdate = JSON.parse(event.data);
      setDriverCoords({ lat: locationUpdate.lat, lng: locationUpdate.lng });
    };
  };

  return (
    <div className="max-w-md mx-auto p-4 font-sans bg-gray-50 min-h-screen">
      <header className="flex justify-between items-center pb-4 border-b">
        <h1 className="text-2xl font-bold text-red-600">QuickBite</h1>
        <span className="bg-red-100 text-red-800 text-xs px-2 py-1 rounded">Cart ({cart.length})</span>
      </header>

      {!orderState ? (
        <main className="mt-6">
          <h2 className="text-xl font-semibold mb-3">Burger Craft</h2>
          <div className="space-y-4">
            {menuItems.map(item => (
              <div key={item.id} className="p-3 bg-white rounded-lg shadow-sm flex justify-between items-center">
                <div>
                  <h3 className="font-medium">{item.name}</h3>
                  <p className="text-gray-500 text-sm">${item.price.toFixed(2)}</p>
                </div>
                <button 
                  onClick={() => addToCart(item)}
                  className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition"
                >
                  Add
                </button>
              </div>
            ))}
          </div>

          {cart.length > 0 && (
            <button 
              onClick={placeOrder}
              className="w-full mt-6 bg-green-600 text-white py-3 rounded-lg font-bold shadow-lg"
            >
              Checkout (${cart.reduce((a, b) => a + b.price, 0).toFixed(2)})
            </button>
          )}
        </main>
      ) : (
        <main className="mt-6 text-center bg-white p-6 rounded-lg shadow-md">
          <div className="animate-pulse bg-green-100 text-green-800 p-2 rounded mb-4">
            Order #{orderState.order_id} Active
          </div>
          <h2 className="text-lg font-bold mb-2">Driver Live Location</h2>
          <p className="text-sm text-gray-600">Lat: {driverCoords.lat} | Lng: {driverCoords.lng}</p>
        </main>
      )}
    </div>
  );
}
