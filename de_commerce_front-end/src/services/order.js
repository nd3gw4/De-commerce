/**
 * Orders Service Module
 *
 * This module provides functions to fetch and manage user orders.
 * All order operations REQUIRE LOGIN - unauthenticated users get 401 errors.
 * 
 * Users can only view and manage their own orders.
 * Backend filters all orders to the authenticated user via get_queryset().
 */

import api from './api';

/**
 * Fetch All User Orders
 * 
 * API: GET /api/orders/
 * Access: REQUIRES LOGIN (IsAuthenticated)
 * 
 * Returns all orders placed by the authenticated user.
 * Backend automatically filters to show only current user's orders.
 * 
 * @returns {Promise} Axios promise
 * @resolves {Object} {data: [{id, user, created_at, status, items, ...}, ...]}
 * @rejects {AxiosError} 401 Unauthorized if not logged in
 * 
 * Response Data Structure:
 * {
 *   data: [
 *     {
 *       id: 1,
 *       user: 2,
 *       created_at: "2024-01-15T10:30:00Z",
 *       updated_at: "2024-01-15T10:30:00Z",
 *       shipping_address: "123 Main St, City, State 12345",
 *       phone_number: "555-0123",
 *       payment_method: "Credit Card",
 *       status: "pending",
 *       items: [
 *         {
 *           id: 45,
 *           product: {id: 3, name: "Product", price: 19.99, ...},
 *           quantity: 2,
 *           price: 19.99
 *         },
 *         ...
 *       ]
 *     },
 *     ...
 *   ]
 * }
 * 
 * Order Status Values:
 * - 'pending': Order created, awaiting shipment
 * - 'shipped': Order sent to customer
 * - 'delivered': Order arrived at customer
 * - 'cancelled': Order was cancelled
 * 
 * Usage:
 * try {
 *   const response = await fetchOrders();
 *   const orders = response.data;
 *   orders.forEach(order => {
 *     console.log(`Order #${order.id}: ${order.status}`);
 *   });
 * } catch (error) {
 *   if (error.response?.status === 401) {
 *     console.error('Must login to view orders');
 *   }
 * }
 * 
 * Frontend Integration:
 * - OrderHistory.vue: Fetches orders on component mount
 * - Displays list of all user's orders with date and status
 * - Shows total items in each order
 * - User can click order to view details
 * 
 * Security:
 * - User can ONLY view their own orders
 * - Backend query filter: Order.objects.filter(user=self.request.user)
 * - If user tries to access another user's order ID, filtered out
 */
export function fetchOrders() {
  return api.get('orders/');
}

/**
 * Fetch Single Order Details
 * 
 * API: GET /api/orders/{orderId}/
 * Access: REQUIRES LOGIN (IsAuthenticated)
 * 
 * Returns detailed information for a specific order by ID.
 * Includes all order items with product details and prices paid.
 * 
 * @param {number} orderId - ID of order to retrieve
 * @returns {Promise} Axios promise
 * @resolves {Object} {data: {id, user, created_at, status, items, ...}}
 * @rejects {AxiosError} 401 if not logged in, 404 if order not found
 * 
 * Response Data Structure:
 * {
 *   data: {
 *     id: 1,
 *     user: 2,
 *     created_at: "2024-01-15T10:30:00Z",
 *     updated_at: "2024-01-20T14:45:00Z",
 *     shipping_address: "123 Main St, City, State 12345",
 *     phone_number: "555-0123",
 *     payment_method: "Credit Card",
 *     status: "shipped",
 *     items: [
 *       {
 *         id: 45,
 *         product: {
 *           id: 3,
 *           name: "Laptop",
 *           description: "...",
 *           price: 999.99,
 *           category: {...},
 *           image: "..."
 *         },
 *         quantity: 1,
 *         price: 999.99
 *       },
 *       {
 *         id: 46,
 *         product: {
 *           id: 7,
 *           name: "Mouse",
 *           description: "...",
 *           price: 29.99,
 *           category: {...},
 *           image: "..."
 *         },
 *         quantity: 2,
 *         price: 29.99
 *       }
 *     ]
 *   }
 * }
 * 
 * Important Features:
 * - Stores price paid at time of order (price field in OrderItem)
 * - If product price changed since order, order still shows original price
 * - Ensures historical accuracy of what customer paid
 * 
 * Usage:
 * try {
 *   const response = await fetchOrder(orderId);
 *   const order = response.data;
 *   console.log(`Order total items: ${order.items.length}`);
 *   console.log(`Order status: ${order.status}`);
 *   // Calculate order total from items
 *   const total = order.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
 *   console.log(`Order total: $${total.toFixed(2)}`);
 * } catch (error) {
 *   if (error.response?.status === 404) {
 *     console.error('Order not found');
 *   } else if (error.response?.status === 401) {
 *     console.error('Must login to view order');
 *   }
 * }
 * 
 * Frontend Integration:
 * - OrderDetail.vue: Fetches order details from route parameter orderId
 * - Displays full order breakdown: items, quantities, prices, status
 * - Shows shipping and payment information
 * - User can navigate back to OrderHistory
 * - Also used in orderDetail.js service (similar functionality)
 * 
 * Security:
 * - User can ONLY view their own orders
 * - Backend verifies ownership before returning order
 * - Prevents cross-user order data leakage
 */
export function fetchOrder(orderId) {
  return api.get(`orders/${orderId}/`);
}

/**
 * Create a new order on the backend.
 *
 * API: POST /api/create-order/
 * Access: REQUIRES LOGIN (IsAuthenticated)
 *
 * @param {Object} data - Order payload
 * @returns {Promise} Axios promise
 */
export function createOrder(data) {
  return api.post('create-order/', data);
}
