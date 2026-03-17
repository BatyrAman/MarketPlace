import { useEffect, useMemo, useState } from 'react';
import type { RouteName } from '../App';
import { marketService } from '../services/marketService';
import type { Cart, Product } from '../types';

interface CartPageProps {
  navigate: (route: RouteName) => void;
  isAuthenticated: boolean;
}

function CartPage({ navigate, isAuthenticated }: CartPageProps) {
  const [cart, setCart] = useState<Cart | null>(null);
  const [productsMap, setProductsMap] = useState<Record<string, Product>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [checkoutLoading, setCheckoutLoading] = useState(false);

  const loadCart = async () => {
    setLoading(true);
    setError('');
    try {
      const cartData = await marketService.getMyCart();
      setCart(cartData);
      const productEntries = await Promise.all(
        cartData.items.map(async (item) => [item.product_id, await marketService.getProductById(item.product_id)] as const),
      );
      setProductsMap(Object.fromEntries(productEntries));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load cart');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('login');
      return;
    }
    void loadCart();
  }, [isAuthenticated, navigate]);

  const total = useMemo(() => {
    if (!cart) return 0;
    return cart.items.reduce((sum, item) => {
      const product = productsMap[item.product_id];
      return sum + (product ? Number(product.price) * item.quantity : 0);
    }, 0);
  }, [cart, productsMap]);

  const updateQuantity = async (itemId: string, quantity: number) => {
    try {
      await marketService.updateCartItem(itemId, quantity);
      await loadCart();
    } catch (err) {
      window.alert(err instanceof Error ? err.message : 'Failed to update quantity');
    }
  };

  const removeItem = async (itemId: string) => {
    try {
      await marketService.deleteCartItem(itemId);
      await loadCart();
    } catch (err) {
      window.alert(err instanceof Error ? err.message : 'Failed to remove item');
    }
  };

  const checkout = async () => {
    setCheckoutLoading(true);
    try {
      await marketService.checkout();
      window.alert('Order created successfully');
      navigate('orders');
    } catch (err) {
      window.alert(err instanceof Error ? err.message : 'Checkout failed');
    } finally {
      setCheckoutLoading(false);
    }
  };

  if (loading) return <div className="card">Loading cart...</div>;
  if (error) return <div className="alert error">{error}</div>;

  return (
    <section className="stack-large">
      <div className="card row-between">
        <div>
          <p className="eyebrow">Shopping cart</p>
          <h1>Your selected items</h1>
        </div>
        <button className="ghost-button" onClick={() => navigate('main')}>Continue shopping</button>
      </div>

      {!cart || cart.items.length === 0 ? (
        <div className="card muted">Cart is empty.</div>
      ) : (
        <>
          <div className="table-card card">
            <div className="table-header table-grid cart-grid">
              <span>Product</span>
              <span>Price</span>
              <span>Quantity</span>
              <span>Subtotal</span>
              <span>Action</span>
            </div>
            {cart.items.map((item) => {
              const product = productsMap[item.product_id];
              const price = Number(product?.price || 0);
              return (
                <div key={item.id} className="table-row table-grid cart-grid">
                  <span>{product?.name || item.product_id}</span>
                  <span>${price.toFixed(2)}</span>
                  <div className="qty-controls">
                    <button onClick={() => updateQuantity(item.id, Math.max(1, item.quantity - 1))}>-</button>
                    <span>{item.quantity}</span>
                    <button onClick={() => updateQuantity(item.id, item.quantity + 1)}>+</button>
                  </div>
                  <span>${(price * item.quantity).toFixed(2)}</span>
                  <button className="danger-button" onClick={() => removeItem(item.id)}>Remove</button>
                </div>
              );
            })}
          </div>

          <div className="card checkout-box">
            <div>
              <h2>Order summary</h2>
              <p className="muted">Total items: {cart.items.length}</p>
            </div>
            <h3>${total.toFixed(2)}</h3>
            <button className="primary-button" onClick={checkout} disabled={checkoutLoading}>
              {checkoutLoading ? 'Processing...' : 'Checkout now'}
            </button>
          </div>
        </>
      )}
    </section>
  );
}

export default CartPage;
