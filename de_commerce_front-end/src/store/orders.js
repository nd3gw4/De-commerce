/**
 * Orders Store Module (Pinia)
 *
 * This module manages the user's orders using Pinia stores.
 * Stores frontend-side order state persisted to localStorage.
 * 
 * Note: This appears to be a frontend-only implementation.
 * Backend has order management via /api/orders/ endpoints.
 * Frontend may use this local store as cache/mirror of backend orders.
 * 
 * When checkout occurs:
 * 1. Order created in backend via API
 * 2. Frontend may add order to local store
 * 3. User can view orders from local store or fresh from backend
 */

import { defineStore } from 'pinia';
import api from '../services/api';

/**
 * useOrderStore: User orders state store
 * 
 * State Properties:
 * - orders: Array of user orders
 *   - Initial value: Loaded from localStorage
 *   - Each order has: {id, product, status, created_at}
 * 
 * Store ID: 'orders'
 * - Used to create store instance: const orders = useOrderStore()
 */
export const useOrderStore = defineStore('orders', {
  state: () => ({
    /**
     * orders: Array of orders placed by current user
     * 
     * Data Structure:
     * [
     *   {
     *     id: 1234567890,  // Timestamp-based ID (Date.now())
     *     product: {id, name, description, price, category, image},
     *     status: 'pending',  // or 'shipped', 'delivered', 'cancelled'
     *     created_at: "2024-01-15T10:30:00.000Z"  // ISO timestamp
     *   },
     *   {
     *     id: 1234567891,
     *     product: {...},
     *     status: 'shipped',
     *     created_at: "2024-01-14T14:20:00.000Z"
     *   }
     * ]
     * 
     * Initialized from localStorage:
     * - On component mount, load() called to restore saved orders
     * - Empty array if nothing in localStorage
     * 
     * Persisted via:
     * - save(): Called after every addOrder/updateStatus operation
     * - Saves as JSON string in localStorage key 'orders'
     * 
     * Accessed by:
     * - Profile.vue: Displays user's orders under profile
     * - OrderHistory.vue: Could show list of orders (currently unused)
     * - OrderDetail.vue: Could show order details (currently unused)
     * 
     * Note on Implementation:
     * Frontend locally tracks orders with timestamp IDs.
     * Backend /api/orders/ API provides authoritative order data.
     * This store may be redundant with backend API orders.
     */
    orders: JSON.parse(localStorage.getItem('orders') || '[]'),
  }),
  
  actions: {
    /**
     * addOrder(): Create new order and add to orders list
     * 
     * @param {Object} product - Product being ordered {id, name, price, ...}
     * @param {string} [status='pending'] - Initial order status (default 'pending')
     * 
     * Logic:
     * 1. Creates order object with:
     *    - id: Current timestamp (Date.now())
     *    - product: Passed product object
     *    - status: Passed status or 'pending'
     *    - created_at: Current ISO timestamp
     * 2. Pushes order to this.orders array
     * 3. Calls save() to persist to localStorage
     * 
     * Called by:
     * - ProductDetail.vue toggleCart(): When product added to cart
     *   But implementation appears to add to orders instead of cart
     * - Checkout flow: After order placed successfully
     * - Could be called when order confirmed
     * 
     * ID Generation:
     * - Uses Date.now() for unique timestamp-based IDs
     * - Provides millisecond precision
     * - Not database-style sequential IDs
     * 
     * Example:
     * const product = {id: 3, name: "Laptop", price: 999.99};
     * orders.addOrder(product, 'pending');
     * // Order created with id = 1705334400000 (Date.now())
     * // Order added to orders array
     * // Persisted to localStorage
     */
    addOrder(product, status = 'pending') {
      this.orders.push({
        id: Date.now(),
        product,
        status,
        created_at: new Date().toISOString(),
      });
      this.save();
    },

    /**
     * updateStatus(): Change order status
     * 
     * @param {number} orderId - ID of order to update
     * @param {string} status - New status ('pending', 'shipped', 'delivered', 'cancelled')
     * 
     * Logic:
     * 1. Finds order by orderId
     * 2. If found, updates order.status to new status
     * 3. Calls save() to persist change
     * 4. Does nothing if orderId not found (silent failure)
     * 
     * Called by:
     * - Admin/management interface (not implemented in current app)
     * - Simulating status changes (for testing)
     * - Could be called when webhook indicates order shipped
     * 
     * Status Progression (typical flow):
     * 1. addOrder() creates with status='pending'
     * 2. updateStatus(orderId, 'shipped') when order ships
     * 3. updateStatus(orderId, 'delivered') when delivered
     * 
     * Example:
     * orders.updateStatus(1705334400000, 'shipped');
     * // Order status changed from 'pending' to 'shipped'
     * // Persisted to localStorage
     */
    updateStatus(orderId, status) {
      const order = this.orders.find(o => o.id === orderId);
      if (order) order.status = status;
      this.save();
    },

    /**
     * save(): Persist orders to localStorage
     * 
     * Logic:
     * 1. Converts this.orders array to JSON string
     * 2. Stores as localStorage['orders']
     * 3. Survives page reloads
     * 
     * Called automatically by:
     * - addOrder(): After creating order
     * - updateStatus(): After status change
     * 
     * Storage Format:
     * JSON string with complete order objects
     * Example: [{"id":1705334400000,"product":{...},"status":"pending",...}]
     */
    save() {
      localStorage.setItem('orders', JSON.stringify(this.orders));
    },

    /**
     * load(): Restore orders from localStorage
     * 
     * Logic:
     * 1. Reads localStorage['orders']
     * 2. Parses JSON string to array
     * 3. Assigns to this.orders
     * 4. Defaults to [] if localStorage key missing
     * 
     * Called by:
     * - Profile.vue onMounted: Load orders for display
     * - OrderHistory.vue onMounted: Load orders list
     * - Any component needing current orders
     * 
     * Use Case:
     * User has 5 orders, closes browser, reopens site
     * load() restores those 5 orders automatically
     * 
     * Example:
     * orders.load();
     * console.log(orders.orders);  // [order1, order2, ..., order5]
     */
    async load() {
      try {
        const response = await api.get('orders/');
      this.orders = response.data;
      } catch (error) {
        console.error('Error loading orders:', error);
      }
    }
  },
});
