import { useEffect, useState } from 'react';
import type { RouteName } from '../App';
import { marketService } from '../services/marketService';
import type { Order, Product, Review } from '../types';

interface ReviewPageProps {
  navigate: (route: RouteName) => void;
  isAuthenticated: boolean;
}

function ReviewPage({ navigate, isAuthenticated }: ReviewPageProps) {
  const [orders, setOrders] = useState<Order[]>([]);
  const [reviews, setReviews] = useState<Record<string, Review[]>>({});
  const [products, setProducts] = useState<Record<string, Product>>({});
  const [selectedProductId, setSelectedProductId] = useState('');
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('login');
      return;
    }

    const load = async () => {
      const ordersData = await marketService.getMyOrders();
      setOrders(ordersData);
      const productIds = Array.from(new Set(ordersData.flatMap((order) => order.items.map((item) => item.product_id))));
      const entries = await Promise.all(productIds.map(async (id) => [id, await marketService.getProductById(id)] as const));
      setProducts(Object.fromEntries(entries));
      if (productIds[0]) {
        setSelectedProductId(productIds[0]);
      }
      const reviewEntries = await Promise.all(productIds.map(async (id) => [id, await marketService.getReviewsByProduct(id)] as const));
      setReviews(Object.fromEntries(reviewEntries));
    };

    void load();
  }, [isAuthenticated, navigate]);

  const submitReview = async (event: React.FormEvent) => {
    event.preventDefault();
    setMessage('');
    try {
      await marketService.createReview(selectedProductId, rating, comment);
      const updated = await marketService.getReviewsByProduct(selectedProductId);
      setReviews((prev) => ({ ...prev, [selectedProductId]: updated }));
      setComment('');
      setRating(5);
      setMessage('Review published successfully.');
    } catch (err) {
      setMessage(err instanceof Error ? err.message : 'Failed to create review');
    }
  };

  const productIds = Array.from(new Set(orders.flatMap((order) => order.items.map((item) => item.product_id))));

  return (
    <section className="stack-large">
      <div className="card">
        <p className="eyebrow">Reviews</p>
        <h1>Review purchased products</h1>
        <p className="muted">Backend allows reviews only for items that were purchased before.</p>
      </div>

      {productIds.length === 0 ? (
        <div className="card muted">You need at least one order before leaving a review.</div>
      ) : (
        <>
          <form className="card stack-small" onSubmit={submitReview}>
            <label>
              <span>Purchased product</span>
              <select value={selectedProductId} onChange={(e) => setSelectedProductId(e.target.value)} required>
                {productIds.map((productId) => (
                  <option key={productId} value={productId}>{products[productId]?.name || productId}</option>
                ))}
              </select>
            </label>
            <label>
              <span>Rating</span>
              <select value={rating} onChange={(e) => setRating(Number(e.target.value))}>
                {[5, 4, 3, 2, 1].map((item) => <option key={item} value={item}>{item} / 5</option>)}
              </select>
            </label>
            <label>
              <span>Comment</span>
              <textarea value={comment} onChange={(e) => setComment(e.target.value)} placeholder="Write your honest feedback" rows={4} />
            </label>
            {message ? <div className="alert success">{message}</div> : null}
            <button className="primary-button" type="submit">Submit review</button>
          </form>

          <div className="card stack-small">
            <h2>Recent reviews for selected product</h2>
            {(reviews[selectedProductId] || []).length === 0 ? (
              <p className="muted">No reviews yet.</p>
            ) : (
              <div className="stack-small">
                {(reviews[selectedProductId] || []).map((review) => (
                  <div key={review.id} className="review-card">
                    <div className="row-between">
                      <strong>{'★'.repeat(review.rating)}</strong>
                      <span className="muted">{new Date(review.created_at).toLocaleDateString()}</span>
                    </div>
                    <p>{review.comment || 'No text comment'}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </section>
  );
}

export default ReviewPage;
