import { useEffect, useMemo, useState } from 'react';
import type { RouteName } from '../App';
import ProductCard from '../components/ProductCard';
import { marketService } from '../services/marketService';
import type { Category, Product } from '../types';

interface MainPageProps {
  navigate: (route: RouteName) => void;
  isAuthenticated: boolean;
}

function MainPage({ navigate, isAuthenticated }: MainPageProps) {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [search, setSearch] = useState('');
  const [selectedCategoryId, setSelectedCategoryId] = useState('all');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const [productsData, categoriesData] = await Promise.all([
        marketService.getProducts(search),
        marketService.getCategories(),
      ]);
      setProducts(productsData);
      setCategories(categoriesData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const visibleProducts = useMemo(() => {
    return products.filter((product) => {
      const matchesCategory = selectedCategoryId === 'all' || product.category_id === selectedCategoryId;
      const matchesSearch = product.name.toLowerCase().includes(search.toLowerCase());
      return matchesCategory && matchesSearch;
    });
  }, [products, selectedCategoryId, search]);

  const handleAddToCart = async (productId: string) => {
    if (!isAuthenticated) {
      navigate('login');
      return;
    }
    try {
      await marketService.addToCart(productId, 1);
      window.alert('Product added to cart');
    } catch (err) {
      window.alert(err instanceof Error ? err.message : 'Failed to add to cart');
    }
  };

  return (
    <section className="stack-large">
      <section className="hero-card card">
        <div>
          <p className="eyebrow">Portfolio-ready marketplace</p>
          <h1>Modern shopping experience for Assignment 4</h1>
          <p className="muted">
            Includes authentication, product browsing, cart, checkout, reviews and order history.
          </p>
        </div>
        <div className="hero-actions">
          <button className="primary-button" onClick={() => navigate('cart')}>Go to cart</button>
          <button className="ghost-button" onClick={() => navigate(isAuthenticated ? 'profile' : 'login')}>
            {isAuthenticated ? 'Open profile' : 'Login now'}
          </button>
        </div>
      </section>

      <section className="filters card">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search product name..."
        />
        <select value={selectedCategoryId} onChange={(e) => setSelectedCategoryId(e.target.value)}>
          <option value="all">All categories</option>
          {categories.map((category) => (
            <option key={category.id} value={category.id}>{category.name}</option>
          ))}
        </select>
        <button className="ghost-button" onClick={() => void load()}>Refresh</button>
      </section>

      {error ? <div className="alert error">{error}</div> : null}
      {loading ? <div className="card">Loading products...</div> : null}

      <section className="product-grid">
        {visibleProducts.map((product) => (
          <ProductCard key={product.id} product={product} onAddToCart={handleAddToCart} />
        ))}
      </section>

      {!loading && visibleProducts.length === 0 ? (
        <div className="card muted">No products found for the current search.</div>
      ) : null}
    </section>
  );
}

export default MainPage;
