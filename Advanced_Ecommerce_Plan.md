# Advanced E-commerce API: Project Specification

## Goal Description
Build a production-grade, high-performance E-commerce REST API. The primary goal is to master advanced backend concepts: **concurrency control**, **asynchronous database operations**, **caching implementation**, and **complex state management**.

This project steps up from a simple CRUD app by introducing "Real World" problems like race conditions (two people buying the last item), distributed session management, and background processing.

## Tech Stack & "Level Up" Tools

| Component | Standard Tool | "Level Up" Tool (We will use) | Why? |
| :--- | :--- | :--- | :--- |
| **Language** | Python | Python | |
| **Framework** | FastAPI | **FastAPI + Async** | Learn to handle high-concurrency non-blocking I/O. |
| **Database** | SQLite/Postgres | **PostgreSQL (Async)** | Industry standard for relational data. Using `asyncpg` driver. |
| **ORM** | SQLAlchemy (Sync) | **SQLAlchemy 2.0 (Async)** | Modern, type-safe, and async-first ORM usage. |
| **Caching** | None | **Redis** | Learn caching strategies, session storage, and rate limiting. |
| **Migrations** | None | **Alembic** | Professional database schema version control. |
| **Testing** | Unittest | **Pytest + AsyncIO** | Modern testing patterns for async code. |
| **Tasks** | None | **Celery or Arq** | Background job processing (e.g., sending emails, resizing images). |
| **Container** | None | **Docker & Docker Compose** | Reproducible dev environments (running DB/Redis locally). |

## Core Modules & Complexity Analysis

### 1. User Management & Authentication
*   **Standard:** Login/Register.
*   **Advanced:**
    *   **RBAC (Role-Based Access Control):** Admin vs User vs Manager permissions.
    *   **Refresh Tokens:** Secure long-lived sessions with short-lived access tokens.
    *   **Email Verification:** Background task to send welcome emails.

### 2. Product Catalog (The "High Read" System)
*   **Standard:** List products.
*   **Advanced:**
    *   **Complex Filtering:** Filter by price, category, attributes (Color/Size) using dynamic query building.
    *   **Redis Caching:** Cache product details and list results. Implement cache invalidation when admin updates a product.
    *   **Search:** Implement Full-Text Search (using Postgres `tsvector`).

### 3. Inventory & Orders (The "High Write/Critical" System)
*   **Standard:** User clicks buy, stock goes down.
*   **Advanced:**
    *   **Concurrency Control:** Prevent overselling. Use **Database Transactions** and **Row-Level Locking** (`SELECT ... FOR UPDATE`) to handle simultaneous purchases.
    *   **Order State Machine:** Manage states: `PENDING` -> `PAYMENT_CONFIRMED` -> `PROCESSING` -> `SHIPPED`.
    *   **Idempotency:** Ensure that retrying a payment request doesn't charge the user twice.

### 4. Shopping Cart
*   **Standard:** Database table `cart_items`.
*   **Advanced:**
    *   **Redis Cart:** Store anonymous user carts in Redis for speed and auto-expiration (TTL). Merge with database cart upon login.

## Proposed Database Schema (Key Entities)

*   `users`: uuid, email, password_hash, role, is_verified
*   `products`: uuid, name, description, price, stock_quantity, category_id
*   `categories`: uuid, name, parent_id (Adjacency List for hierarchical categories)
*   `orders`: uuid, user_id, total_amount, status, created_at
*   `order_items`: uuid, order_id, product_id, quantity, price_at_purchase
*   `payments`: uuid, order_id, transaction_id, provider, status

## Roadmap

1.  **Phase 1: Setup & Auth**
    *   Docker Compose for Postgres + Redis.
    *   User Auth with JWT & Refresh Tokens.
    *   Alembic setup.
2.  **Phase 2: Product & Catalog**
    *   CRUD for Products/Categories.
    *   Filtering logic.
    *   **Challenge:** Implementing Redis Cache for GET requests.
3.  **Phase 3: The Core (Order & Inventory)**
    *   Cart logic.
    *   Order placement logic (Transaction management).
    *   **Challenge:** Simulation script to fire multiple requests to test concurrency locks.
4.  **Phase 4: Optimization & Polish**
    *   Background tasks for emails.
    *   Dockerizing the app itself.
