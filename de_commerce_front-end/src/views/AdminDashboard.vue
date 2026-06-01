<template>
  <div class="admin-dashboard-container">
    <div class="container py-5">
      <div class="admin-dashboard-top">
        <div class="row mb-4">
          <div class="col-12">
            <h1 class="display-5 fw-bold">Admin Control Center</h1>
            <p class="lead text-muted">Manage products, review orders, and invite admin users.</p>
          </div>
        </div>
      </div>

      <div class="row mb-4">
        <div class="col-12">
          <div class="nav nav-pills nav-fill admin-tabs" role="tablist">
            <button
              class="nav-link"
              :class="{ active: activeTab === 'upload' }"
              type="button"
              @click="activeTab = 'upload'"
            >Product Upload</button>
            <button
              class="nav-link"
              :class="{ active: activeTab === 'orders' }"
              type="button"
              @click="activeTab = 'orders'"
            >Order Analytics</button>
            <button
              class="nav-link"
              :class="{ active: activeTab === 'admins' }"
              type="button"
              @click="activeTab = 'admins'"
            >Admin Users</button>
          </div>
        </div>
      </div>

      <div v-show="activeTab === 'upload'" class="tab-pane fade show active">
        <div class="row gy-4">
          <div class="col-lg-6">
            <div class="card shadow-sm">
              <div class="card-header">
                <h5 class="mb-0">Bulk Product Import</h5>
              </div>
              <div class="card-body">
                <p class="text-muted">Upload a CSV or JSON file to import products in bulk.</p>
                <form @submit.prevent="handleBulkImport">
                  <div class="mb-3">
                    <label class="form-label fw-bold" for="admin-file">Select File</label>
                    <input
                      id="admin-file"
                      type="file"
                      class="form-control"
                      accept=".csv,.json"
                      @change="handleFileChange"
                      required
                    />
                  </div>

                  <div class="mb-3">
                    <label class="form-label fw-bold" for="admin-format">File Format</label>
                    <select id="admin-format" class="form-select" v-model="bulkForm.format" required>
                      <option value="csv">CSV</option>
                      <option value="json">JSON</option>
                    </select>
                  </div>

                  <div class="form-check mb-3">
                    <input class="form-check-input" type="checkbox" id="admin-update" v-model="bulkForm.update" />
                    <label class="form-check-label" for="admin-update">
                      Update existing products if they already exist
                    </label>
                  </div>

                  <button class="btn btn-primary" type="submit" :disabled="bulkLoading">
                    <span v-if="!bulkLoading"><i class="bi bi-upload"></i> Import Products</span>
                    <span v-else>
                      <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      Importing...
                    </span>
                  </button>
                </form>

                <div v-if="bulkResult" class="mt-4">
                  <div :class="['alert', bulkResult.success ? 'alert-success' : 'alert-danger']" role="alert">
                    <h5 class="alert-heading">{{ bulkResult.success ? 'Import Result' : 'Import Error' }}</h5>
                    <p class="mb-0">{{ bulkResult.error || bulkResult.message || 'Batch processing completed.' }}</p>
                  </div>
                  <div v-if="bulkResult.success" class="row g-3">
                    <div class="col-3">
                      <div class="stat-card">Processed<br /><strong>{{ bulkResult.total_processed }}</strong></div>
                    </div>
                    <div class="col-3">
                      <div class="stat-card stat-success">Created<br /><strong>{{ bulkResult.created }}</strong></div>
                    </div>
                    <div class="col-3">
                      <div class="stat-card stat-info">Updated<br /><strong>{{ bulkResult.updated }}</strong></div>
                    </div>
                    <div class="col-3">
                      <div class="stat-card stat-danger">Failed<br /><strong>{{ bulkResult.failed }}</strong></div>
                    </div>
                  </div>
                  <div v-if="bulkResult.errors && bulkResult.errors.length" class="mt-3">
                    <div class="alert alert-light border border-danger">
                      <h6 class="mb-2">Import Errors</h6>
                      <ul class="mb-0">
                        <li v-for="err in bulkResult.errors" :key="err.row">
                          <strong>Row {{ err.row }}:</strong> {{ err.message }}
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-lg-6">
            <div class="card shadow-sm">
              <div class="card-header">
                <h5 class="mb-0">Add Single Product</h5>
              </div>
              <div class="card-body">
                <form @submit.prevent="handleAddProduct">
                  <div class="mb-3">
                    <label class="form-label fw-bold" for="admin-name">Name *</label>
                    <input id="admin-name" type="text" class="form-control" v-model="singleForm.name" required />
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-bold" for="admin-price">Price *</label>
                    <input id="admin-price" type="number" class="form-control" step="0.01" min="0" v-model="singleForm.price" required />
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-bold" for="admin-category">Category *</label>
                    <input id="admin-category" type="text" class="form-control" v-model="singleForm.category" required />
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-bold" for="admin-stock">Stock Status</label>
                    <select id="admin-stock" class="form-select" v-model="singleForm.stock_status">
                      <option value="In Stock">In Stock</option>
                      <option value="Low Stock">Low Stock</option>
                      <option value="Out of Stock">Out of Stock</option>
                    </select>
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-bold" for="admin-description">Description</label>
                    <textarea id="admin-description" class="form-control" v-model="singleForm.description" rows="3"></textarea>
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-bold" for="admin-more-description">More Details</label>
                    <textarea id="admin-more-description" class="form-control" v-model="singleForm.more_description" rows="2"></textarea>
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-bold" for="admin-specifications">Specifications</label>
                    <textarea id="admin-specifications" class="form-control" v-model="singleForm.specifications" rows="2"></textarea>
                  </div>
                  <button class="btn btn-success" type="submit" :disabled="singleLoading">
                    <span v-if="!singleLoading"><i class="bi bi-plus-circle"></i> Add Product</span>
                    <span v-else>
                      <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      Adding...
                    </span>
                  </button>
                </form>

                <div v-if="singleResult" class="mt-4">
                  <div :class="['alert', singleResult.success ? 'alert-success' : 'alert-danger']" role="alert">
                    <h5 class="alert-heading">{{ singleResult.success ? 'Success' : 'Error' }}</h5>
                    <p class="mb-0">{{ singleResult.message || singleResult.error }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-show="activeTab === 'orders'" class="tab-pane fade show active">
        <div class="row g-4">
          <div class="col-12">
            <div class="card shadow-sm py-4 px-4">
                  <div class="d-flex justify-content-between align-items-start mb-4">
                    <div>
                      <h4>Order Analytics</h4>
                      <p class="admin-info-text mb-0">Review orders placed on the store and monitor status counts.</p>
                    </div>
                <button class="btn btn-outline-secondary" @click="reloadOrders">Refresh</button>
              </div>

              <div v-if="ordersLoading" class="text-center py-4">
                <div class="spinner-border" role="status"></div>
              </div>

              <div v-else>
                <div class="row g-3 mb-4">
                  <div class="col-sm-6 col-xl-3" v-for="(value, key) in orderStats" :key="key">
                    <div class="stat-card stat-summary">
                      <div class="small text-uppercase text-muted">{{ key }}</div>
                      <strong>{{ value }}</strong>
                    </div>
                  </div>
                </div>

                <div class="table-responsive">
                  <table class="table table-hover admin-orders-table align-middle">
                    <thead class="table-light">
                      <tr>
                        <th>Order</th>
                        <th>User</th>
                        <th>Status</th>
                        <th>Items</th>
                        <th>Total</th>
                        <th>Created</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="order in orders" :key="order.id">
                        <td>#{{ order.id }}</td>
                        <td>{{ order.user.username }}<br /><small>{{ order.user.email }}</small></td>
                        <td>{{ order.status }}</td>
                        <td>{{ order.total_items }}</td>
                        <td>${{ order.total_price.toFixed(2) }}</td>
                        <td>{{ formatDate(order.created_at) }}</td>
                      </tr>
                      <tr v-if="orders.length === 0">
                        <td colspan="6" class="text-muted text-center">No orders found.</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <div v-if="orderError" class="alert alert-danger mt-3">
                {{ orderError }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-show="activeTab === 'admins'" class="tab-pane fade show active">
        <div class="row">
          <div class="col-lg-6">
            <div class="card shadow-sm">
              <div class="card-header">
                <h5 class="mb-0">Create Admin User</h5>
              </div>
              <div class="card-body">
                <form @submit.prevent="handleCreateAdmin">
                  <div class="mb-3">
                    <label class="form-label fw-bold" for="admin-username">Username *</label>
                    <input id="admin-username" class="form-control" v-model="adminForm.username" required />
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-bold" for="admin-email">Email *</label>
                    <input id="admin-email" type="email" class="form-control" v-model="adminForm.email" required />
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-bold" for="admin-password">Password *</label>
                    <input id="admin-password" type="password" class="form-control" v-model="adminForm.password" required />
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-bold" for="admin-password2">Confirm Password *</label>
                    <input id="admin-password2" type="password" class="form-control" v-model="adminForm.password2" required />
                  </div>
                  <button class="btn btn-dark" type="submit" :disabled="adminLoading">
                    <span v-if="!adminLoading"><i class="bi bi-person-plus"></i> Create Admin</span>
                    <span v-else>
                      <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      Creating...
                    </span>
                  </button>
                </form>

                <div v-if="adminResult" class="mt-4">
                  <div :class="['alert', adminResult.success ? 'alert-success' : 'alert-danger']" role="alert">
                    <p class="mb-0">{{ adminResult.message || adminResult.error || 'Action completed.' }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-lg-6">
            <div class="card shadow-sm admin-info-card">
              <div class="card-body">
                <h5 class="card-title">Admin Privileges</h5>
                <p class="card-text text-muted">New admin accounts created here will have full administrative privileges, including product management and order analytics access.</p>
                <ul>
                  <li>Superuser access via Django `is_superuser` and `is_staff`.</li>
                  <li>Can upload products in bulk or individually.</li>
                  <li>Can review all customer orders and summary analytics.</li>
                  <li>Only existing admins may create new admins.</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/store/auth';
import { fetchAdminOrders, fetchAdminOrderSummary, createAdminUser } from '@/services/admin';
import api from '@/services/api';

export default {
  name: 'AdminDashboard',
  data() {
    return {
      activeTab: 'upload',
      bulkForm: {
        file: null,
        format: 'csv',
        update: false
      },
      bulkLoading: false,
      bulkResult: null,
      singleForm: {
        name: '',
        description: '',
        price: null,
        category: '',
        stock_status: 'In Stock',
        more_description: '',
        specifications: ''
      },
      singleLoading: false,
      singleResult: null,
      orders: [],
      orderStats: {
        'Total Orders': 0,
        Pending: 0,
        Shipped: 0,
        Delivered: 0,
        Cancelled: 0,
        'Total Revenue': '$0.00'
      },
      ordersLoading: false,
      orderError: null,
      adminForm: {
        username: '',
        email: '',
        password: '',
        password2: ''
      },
      adminLoading: false,
      adminResult: null
    };
  },
  mounted() {
    const auth = useAuthStore();
    if (!auth.isAuthenticated) {
      this.$router.push('/login');
      return;
    }
    if (!auth.isAdmin) {
      this.$router.push('/');
      return;
    }
    this.reloadOrders();
  },
  methods: {
    handleFileChange(event) {
      this.bulkForm.file = event.target.files[0];
    },
    async handleBulkImport() {
      if (!this.bulkForm.file) {
        this.bulkResult = { success: false, error: 'Please select a CSV or JSON file.' };
        return;
      }
      this.bulkLoading = true;
      const formData = new FormData();
      formData.append('file', this.bulkForm.file);
      formData.append('format', this.bulkForm.format);
      formData.append('update', this.bulkForm.update);

      try {
        const response = await api.post('admin/import_products/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        this.bulkResult = response.data;
      } catch (error) {
        this.bulkResult = {
          success: false,
          error: error.response?.data?.error || error.message || 'Import failed.'
        };
      } finally {
        this.bulkLoading = false;
      }
    },
    async handleAddProduct() {
      this.singleLoading = true;
      try {
        const response = await api.post('admin/add_single_product/', this.singleForm);
        this.singleResult = response.data;
      } catch (error) {
        this.singleResult = {
          success: false,
          error: error.response?.data?.error || error.message || 'Failed to add product.'
        };
      } finally {
        this.singleLoading = false;
      }
    },
    async handleCreateAdmin() {
      this.adminResult = null;
      if (this.adminForm.password !== this.adminForm.password2) {
        this.adminResult = { success: false, error: 'Passwords do not match.' };
        return;
      }
      this.adminLoading = true;
      try {
        const response = await createAdminUser({
          username: this.adminForm.username,
          email: this.adminForm.email,
          password: this.adminForm.password,
          password2: this.adminForm.password2
        });
        this.adminResult = response.data;
      } catch (error) {
        this.adminResult = {
          success: false,
          error: error.response?.data?.errors ? JSON.stringify(error.response.data.errors) : error.response?.data?.message || error.message || 'Failed to create admin.'
        };
      } finally {
        this.adminLoading = false;
      }
    },
    async reloadOrders() {
      this.ordersLoading = true;
      this.orderError = null;
      try {
        const [ordersResponse, summaryResponse] = await Promise.all([
          fetchAdminOrders(),
          fetchAdminOrderSummary()
        ]);
        this.orders = ordersResponse.data;
        const summary = summaryResponse.data;
        this.orderStats = {
          'Total Orders': summary.total_orders,
          Pending: summary.status_counts.pending,
          Shipped: summary.status_counts.shipped,
          Delivered: summary.status_counts.delivered,
          Cancelled: summary.status_counts.cancelled,
          'Total Revenue': `$${summary.total_revenue.toFixed(2)}`
        };
      } catch (error) {
        this.orderError = error.response?.data?.error || error.message || 'Unable to load admin orders.';
      } finally {
        this.ordersLoading = false;
      }
    },
    formatDate(value) {
      return new Date(value).toLocaleString();
    }
  }
};
</script>

<style scoped>
.admin-dashboard-container {
  min-height: 100vh;
  background: var(--background-color);
  color: var(--text-color);
}
.admin-dashboard-container .container {
  max-width: 1180px;
}
.admin-dashboard-top {
  background: var(--background-color);
  border-bottom: 2px solid var(--text-color);
  padding: 2.5rem 2rem;
  margin-bottom: 2rem;
}
.admin-dashboard-top h1,
.admin-dashboard-top .lead {
  color: var(--text-color);
}
.admin-tabs .nav-link {
  border-radius: 0;
  color: var(--text-color);
  font-weight: 700;
  padding: 0.95rem 1.7rem;
  margin-right: 0.5rem;
  border: 1px solid var(--text-color);
  background: var(--background-color);
}
.admin-tabs .nav-link:hover {
  background: var(--text-color);
  color: var(--background-color);
}
.admin-tabs .nav-link.active {
  background-color: var(--text-color);
  color: var(--background-color);
}
.card {
  border-radius: 0;
  border: 1px solid var(--text-color);
  background: var(--background-color);
  box-shadow: none;
}
.card-header {
  border-radius: 0;
  border-bottom: 1px solid var(--text-color);
  background: var(--background-color);
}
.card-body {
  color: var(--text-color);
}
.card .form-label {
  color: var(--text-color);
}
.btn-primary,
.btn-success,
.btn-dark,
.btn-outline-secondary {
  border-radius: 0;
  letter-spacing: 0.03em;
  font-weight: 700;
  background: var(--text-color);
  color: var(--background-color);
  border: 1px solid var(--text-color);
}
.btn-primary:hover,
.btn-success:hover,
.btn-dark:hover {
  background: var(--extra-color);
  border-color: var(--extra-color);
}
.btn-primary {
  background-color: var(--text-color);
  border-color: var(--text-color);
}
.btn-success {
  border-left: 4px solid var(--text-color);
  border-color: var(--text-color);
}
  border-left: 4px solid var(--text-color);
  background-color: var(--text-color);
  border-color: var(--text-color);
  border-left: 4px solid var(--text-color);
.stat-card {
  background: var(--background-color);
  border: 1px solid var(--text-color);
  border-radius: 0;
  padding: 1.3rem;
}
.stat-card strong,
.stat-card .small {
  color: var(--text-color);
}
.stat-summary {
  min-height: 120px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.45rem;
}
.admin-orders-table {
  background: var(--background-color);
  border: 1px solid var(--text-color);
  border-radius: 0;
}
.admin-orders-table th,
.admin-orders-table td {
  border-top: 1px solid rgba(25, 25, 25, 0.08);
}
.admin-orders-table thead {
  background: var(--background-color);
}
.admin-orders-table tbody tr:hover {
  background-color: rgba(241, 80, 37, 0.08);
}
.admin-orders-table tbody td {
  vertical-align: middle;
}
.alert-heading {
  font-weight: 700;
}
.card ul {
  list-style-type: disc;
  padding-left: 1.3rem;
}
.card ul li {
  margin-bottom: 0.75rem;
  color: var(--text-color);
}
.admin-info-text,
.text-muted {
  color: rgba(25, 25, 25, 0.75) !important;
}
.table-light {
  background: var(--background-color) !important;
}
.alert-success,
.alert-danger,
.alert-light {
  background: var(--background-color) !important;
  color: var(--text-color) !important;
  border: 1px solid var(--text-color) !important;
}
.border-danger {
  border-color: var(--text-color) !important;
}
.admin-info-card {
  border-left: 4px solid var(--text-color);
}
@media (max-width: 991px) {
  .admin-dashboard-top,
  .card {
    border-radius: 0;
  }
}
</style>
