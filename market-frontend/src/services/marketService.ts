import { api } from './api';
import type { Cart, Category, Order, Product, Review, User } from '../types';

export const marketService = {
  getProducts: (search = '') => api.get<Product[]>(`/products/${search ? `?search=${encodeURIComponent(search)}` : ''}`),
  getProductById: (productId: string) => api.get<Product>(`/products/${productId}`),
  getCategories: () => api.get<Category[]>('/categories/'),
  getMyCart: () => api.get<Cart>('/cart/'),
  addToCart: (product_id: string, quantity: number) => api.post('/cart/items', { product_id, quantity }),
  updateCartItem: (itemId: string, quantity: number) => api.patch(`/cart/items/${itemId}`, { quantity }),
  deleteCartItem: (itemId: string) => api.delete(`/cart/items/${itemId}`),
  checkout: () => api.post<Order>('/orders/checkout'),
  getMyOrders: () => api.get<Order[]>('/orders/my'),
  getReviewsByProduct: (productId: string) => api.get<Review[]>(`/reviews/product/${productId}`),
  createReview: (product_id: string, rating: number, comment: string) => api.post<Review>('/reviews/', { product_id, rating, comment }),
  getProfile: () => api.get<User>('/users/me'),
};
