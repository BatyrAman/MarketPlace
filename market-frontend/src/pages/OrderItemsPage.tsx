import { useEffect, useState } from 'react';
import type { RouteName } from '../App';
import { marketService } from '../services/marketService';
import type { Order, Product } from '../types';

interface OrderItemsPageProps {
  navigate: (route: RouteName) => void;
  isAuthenticated: boolean;
}

function OrderItemsPage({ navigate, isAuthenticated }: OrderItemsPageProps) {
  const [orders, setOrders] = useState<Order[]>([]);
  const [productsMap, setProductsMap] = useState<Record<string, Product>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('login');
      return;
    }

    const load = async () => {
      setLoading(true);
      setError('');
      try {
        const ordersData = await marketService.getMyOrders();
        setOrders(ordersData);
        const productIds = Array.from(new Set(ordersData.flatMap((order) => order.items.map((item) => item.product_id))));
        const productEntries = await Promise.all(productIds.map(async (id) => [id, await marketService.getProductById(id)] as const));
        setProductsMap(Object.fromEntries(productEntries));
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load orders');
      } finally {
        setLoading(false);
      }
    };

    void load();
  }, [isAuthenticated, navigate]);

  if (loading) return <div className="card">Loading orders...</div>;
  if (error) return <div className="alert error">{error}</div>;

  return (
    <section className="stack-large">
      <div className="card">
        <p className="eyebrow">Orders</p>
        <h1>Order history and order items</h1>
      </div>

      {orders.length === 0 ? (
        <div className="card muted">No orders yet.</div>
      ) : (
        <div className="stack-large">
          {orders.map((order) => (
            <div key={order.id} className="card stack-small">
              <div className="row-between wrap-gap">
                <div>
                  <h2>Order #{order.id.slice(0, 8)}</h2>
                  <p className="muted">{new Date(order.created_at).toLocaleString()}</p>
                </div>
                <div className="row-gap">
                  <span className="badge">{order.status}</span>
                  <span className="badge badge-accent">${Number(order.total_amount).toFixed(2)}</span>
                </div>
              </div>

              <div className="table-card">
                <div className="table-header table-grid order-grid">
                  <span>Product</span>
                  <span>Quantity</span>
                  <span>Price at purchase</span>
                  <span>Line total</span>
                </div>
                {order.items.map((item) => {
                  const product = productsMap[item.product_id];
                  const lineTotal = Number(item.price_at_purchase) * item.quantity;
                  return (
                    <div key={item.id} className="table-row table-grid order-grid">
                      <span>{product?.name || item.product_id}</span>
                      <span>{item.quantity}</span>
                      <span>${Number(item.price_at_purchase).toFixed(2)}</span>
                      <span>${lineTotal.toFixed(2)}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

export default OrderItemsPage;
