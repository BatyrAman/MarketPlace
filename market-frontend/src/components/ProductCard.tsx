import type { Product } from '../types';

interface ProductCardProps {
  product: Product;
  onAddToCart: (productId: string) => void;
}

function ProductCard({ product, onAddToCart }: ProductCardProps) {
  return (
    <article className="product-card">
      <div className="product-image-placeholder">{product.name.slice(0, 1).toUpperCase()}</div>
      <div className="product-body">
        <div className="product-meta-row">
          <span className="badge">Stock: {product.stock}</span>
          <span className="badge badge-accent">${Number(product.price).toFixed(2)}</span>
        </div>
        <h3>{product.name}</h3>
        <p>{product.description || 'No description provided yet.'}</p>
        <button className="primary-button" onClick={() => onAddToCart(product.id)} disabled={product.stock <= 0}>
          {product.stock > 0 ? 'Add to cart' : 'Out of stock'}
        </button>
      </div>
    </article>
  );
}

export default ProductCard;
