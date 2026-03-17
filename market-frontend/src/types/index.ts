export type User = {
  id: string;
  email: string;
  username: string;
  full_name?: string | null;
  role: 'customer' | 'seller' | 'admin';
  is_active: boolean;
  created_at: string;
};

export type Category = {
  id: string;
  name: string;
  description?: string | null;
};

export type Product = {
  id: string;
  name: string;
  description?: string | null;
  price: string;
  stock: number;
  is_active: boolean;
  seller_id: string;
  category_id: string;
  created_at: string;
};

export type CartItem = {
  id: string;
  product_id: string;
  quantity: number;
};

export type Cart = {
  id: string;
  user_id: string;
  items: CartItem[];
};

export type Review = {
  id: string;
  user_id: string;
  product_id: string;
  rating: number;
  comment?: string | null;
  created_at: string;
};

export type OrderItem = {
  id: string;
  product_id: string;
  quantity: number;
  price_at_purchase: string;
};

export type Order = {
  id: string;
  user_id: string;
  total_amount: string;
  status: 'pending' | 'paid' | 'shipped' | 'completed' | 'cancelled';
  created_at: string;
  items: OrderItem[];
};

export type TokenResponse = {
  access_token: string;
  refresh_token: string;
  token_type: string;
};
