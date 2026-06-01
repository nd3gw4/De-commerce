import api from './api';

export function fetchAdminOrders() {
  return api.get('admin/orders/');
}

export function fetchAdminOrderSummary() {
  return api.get('admin/orders-summary/');
}

export function createAdminUser(data) {
  return api.post('admin/create-admin/', data);
}
