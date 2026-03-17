# Plan.md

## Project Title
Marketplace API

## Project Idea
This project is a backend application for an online marketplace.  
Users can register, log in, browse products, search items, add products to cart, create orders, leave reviews, and manage their own data.  
Admins can manage categories and users. Sellers can create and manage products.

---

## Main Goal
Build a REST API with authentication, authorization, database support, and business logic for a marketplace system.

---

## Technologies
- FastAPI
- SQLModel
- PostgreSQL
- JWT Authentication

---

## Entities

### 1. User
Represents a system user.

Attributes:
- id: UUID
- username: string
- email: string
- password_hash: string
- role: string
- created_at: datetime

---

### 2. Category
Represents product category.

Attributes:
- id: UUID
- name: string
- description: string

---

### 3. Product
Represents a product in the marketplace.

Attributes:
- id: UUID
- title: string
- description: string
- price: decimal
- stock: integer
- seller_id: UUID
- category_id: UUID
- created_at: datetime

---

### 4. Cart
Represents a user shopping cart.

Attributes:
- id: UUID
- user_id: UUID
- created_at: datetime

---

### 5. CartItem
Represents an item inside a cart.

Attributes:
- id: UUID
- cart_id: UUID
- product_id: UUID
- quantity: integer

---

### 6. Order
Represents user order.

Attributes:
- id: UUID
- user_id: UUID
- total_price: decimal
- status: string
- created_at: datetime

---

### 7. OrderItem
Represents purchased items in an order.

Attributes:
- id: UUID
- order_id: UUID
- product_id: UUID
- quantity: integer 
- price_at_purchase: decimal

---

### 8. Review
Represents product review.

Attributes:
- id: UUID
- user_id: UUID
- product_id: UUID
- rating: integer
- comment: string
- created_at: datetime

---

### 9. RefreshToken
Represents stored refresh token for user session.

Attributes:
- id: UUID
- user_id: UUID
- token: string
- expires_at: datetime

---

## Relationships

- One User can create many Products
- One User has one Cart
- One Cart can contain many CartItems
- One Product can appear in many CartItems
- One User can create many Orders
- One Order can contain many OrderItems
- One Product can appear in many OrderItems
- One Category can have many Products
- One User can write many Reviews
- One Product can have many Reviews
- One User can have many RefreshTokens

---

## Functional Requirements

### Guest
- View all products
- View product details
- Search products
- Sort products by price or date
- Filter products by category

### Authenticated User
- Register account
- Log in
- Log out
- Refresh access token
- View own profile
- Update own profile
- Add product to cart
- Update cart item quantity
- Remove item from cart
- Create order from cart
- View own orders
- Leave review for product

### Seller
- Create product
- Update own product
- Delete own product
- View own products

### Admin
- Create category
- Update category
- Delete category
- View all users
- Manage user roles if needed

---

## Authentication Scenarios

Authentication is required for:
- viewing own profile
- updating own profile
- working with cart
- creating order
- viewing own orders
- leaving review
- creating products
- updating products
- deleting products
- category management

Authentication is not required for:
- browsing products
- viewing product details
- searching and sorting products
- viewing categories

---

## Authorization Rules

- Only authenticated users can access personal data
- Only seller can create products
- Only product owner or admin can update/delete a product
- Only admin can manage categories
- Only order owner can view own orders
- Only logged in user can manage own cart
- Only logged in user can leave review
- One user cannot modify another user’s cart, orders, or profile

---

## Search and Sorting

Search:
- by product title
- by product description
- by category name

Sorting:
- by price ascending
- by price descending
- by created date newest first
- by created date oldest first

---

## Edge Cases

### User
- user cannot register with existing email
- user cannot register with existing username
- user cannot login with wrong password
- user cannot access another user profile

### Category
- category name should be unique
- category cannot be deleted if products depend on it, unless handled safely
- only admin can create, update, delete category

### Product
- price cannot be negative
- stock cannot be negative
- seller cannot edit product of another seller
- product cannot be created without valid category
- deleted product should not stay active in cart/order flow

### Cart
- user cannot have multiple active carts if system uses one cart per user
- user cannot add non-existing product
- user cannot add out-of-stock product
- user cannot add quantity more than available stock

### CartItem
- quantity must be greater than 0
- if same product is added again, quantity should be updated instead of duplicate row
- user cannot edit cart item of another user

### Order
- user cannot create order from empty cart
- user cannot order more items than available stock
- total price must be calculated from cart items correctly
- stock must decrease after successful order
- user cannot access another user order

### OrderItem
- quantity must stay fixed after order creation
- price_at_purchase must be saved even if product price changes later

### Review
- rating must be in valid range, for example 1 to 5
- user should not leave review for non-existing product
- user should not spam many duplicate reviews if business rule allows only one review per product

### Refresh Token / Logout
- expired refresh token must not work
- deleted refresh token must not work
- logged out access token should be blocked with Redis blocklist
- invalid token must return unauthorized error

---

## Custom Exceptions
Application should handle custom exceptions such as:
- UserAlreadyExists
- InvalidCredentials
- ForbiddenAction
- ProductNotFound
- CategoryNotFound
- CartNotFound
- OrderNotFound
- ReviewNotFound
- TokenExpired
- TokenInvalid

---

## Database Requirements
- PostgreSQL is used as main database
- SQLModel is used for ORM
- Async database session is used
- Alembic is used for migrations

---

## API Testing
All endpoints should be tested in Postman or Insomnia.  
Collection should include:
- auth endpoints
- category endpoints
- product endpoints
- cart endpoints
- order endpoints
- review endpoints

---

## ERD
ERD includes:
- entities
- attributes
- data types
- primary keys
- foreign keys
- relationships between all tables

ERD will be attached as PNG and exported as JSON/TXT.

---

## Expected Result
At the end, the project should provide a complete marketplace backend with:
- REST API
- authentication and authorization
- search and sorting
- cart and order logic
- product reviews
- database integration
