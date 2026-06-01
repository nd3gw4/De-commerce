import api from './api';

export function fetchAdminOrders() {
  return api.get('admin/orders/');
}

export function fetchAdminOrderSummary() {
  return api.get('admin/orders-summary/');
}

export function fetchAdminProducts() {
  return api.get('products/');
}

export function deleteAdminProduct(productId) {
  return api.post('admin/delete-product/', { id: productId });
}

export function createAdminUser(data) {
  return api.post('admin/create-admin/', data);
}
