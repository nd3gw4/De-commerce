<template>
  <div class="admin-container">
    <div class="container mt-5 mb-5">
      <!-- Page Header -->
      <div class="row mb-5">
        <div class="col-12">
          <h1 class="display-5 fw-bold">Admin Dashboard</h1>
          <p class="lead text-muted">Product Management & Bulk Import</p>
        </div>
      </div>

      <!-- Tabs for different import methods -->
      <ul class="nav nav-tabs mb-4" role="tablist">
        <li class="nav-item" role="presentation">
          <button
            class="nav-link active"
            id="bulk-tab"
            data-bs-toggle="tab"
            data-bs-target="#bulk-import"
            type="button"
            role="tab"
            aria-controls="bulk-import"
            aria-selected="true"
          >
            <i class="bi bi-upload"></i> Bulk Import
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button
            class="nav-link"
            id="single-tab"
            data-bs-toggle="tab"
            data-bs-target="#single-product"
            type="button"
            role="tab"
            aria-controls="single-product"
            aria-selected="false"
          >
            <i class="bi bi-plus-square"></i> Add Single Product
          </button>
        </li>
      </ul>

      <!-- Tab Content -->
      <div class="tab-content">
        <!-- Bulk Import Tab -->
        <div class="tab-pane fade show active" id="bulk-import" role="tabpanel" aria-labelledby="bulk-tab">
          <div class="card shadow-sm">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0">Bulk Product Import</h5>
            </div>
            <div class="card-body">
              <div class="alert alert-info" role="alert">
                <strong>Supported Formats:</strong> CSV or JSON<br>
                <strong>Max File Size:</strong> 5MB<br>
                <strong>Required Fields:</strong> name, price, category
              </div>

              <form @submit.prevent="handleBulkImport" class="needs-validation">
                <!-- File Upload -->
                <div class="mb-3">
                  <label for="file" class="form-label fw-bold">Select File</label>
                  <input
                    type="file"
                    class="form-control"
                    id="file"
                    @change="handleFileChange"
                    accept=".csv,.json"
                    required
                  />
                  <small class="text-muted d-block mt-2">
                    Upload CSV or JSON file with product data
                  </small>
                </div>

                <!-- Format Selection -->
                <div class="mb-3">
                  <label for="format" class="form-label fw-bold">File Format</label>
                  <select class="form-select" id="format" v-model="bulkForm.format" required>
                    <option value="csv">CSV (Comma Separated Values)</option>
                    <option value="json">JSON (JavaScript Object Notation)</option>
                  </select>
                </div>

                <!-- Update Existing -->
                <div class="mb-3 form-check">
                  <input
                    type="checkbox"
                    class="form-check-input"
                    id="update"
                    v-model="bulkForm.update"
                  />
                  <label class="form-check-label" for="update">
                    Update existing products (if unchecked, duplicates will be skipped)
                  </label>
                </div>

                <!-- Submit Button -->
                <button
                  type="submit"
                  class="btn btn-primary btn-lg"
                  :disabled="!bulkForm.file || bulkLoading"
                >
                  <span v-if="!bulkLoading">
                    <i class="bi bi-upload"></i> Import Products
                  </span>
                  <span v-else>
                    <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    Importing...
                  </span>
                </button>
              </form>

              <!-- Result Section for Bulk Import -->
              <div v-if="bulkResult" class="mt-4">
                <div :class="['alert', bulkResult.success ? 'alert-success' : 'alert-danger']" role="alert">
                  <h5 class="alert-heading">
                    <i :class="bulkResult.success ? 'bi bi-check-circle' : 'bi bi-exclamation-circle'"></i>
                    {{ bulkResult.success ? 'Import Complete' : 'Import Error' }}
                  </h5>

                  <hr />

                  <div class="row g-3">
                    <div class="col-md-3">
                      <div class="bg-light p-3 rounded">
                        <div class="text-muted small">Total Processed</div>
                        <div class="h4 mb-0">{{ bulkResult.total_processed }}</div>
                      </div>
                    </div>
                    <div class="col-md-3">
                      <div class="bg-success bg-opacity-10 p-3 rounded">
                        <div class="text-muted small">Created</div>
                        <div class="h4 mb-0 text-success">{{ bulkResult.created }}</div>
                      </div>
                    </div>
                    <div class="col-md-3">
                      <div class="bg-info bg-opacity-10 p-3 rounded">
                        <div class="text-muted small">Updated</div>
                        <div class="h4 mb-0 text-info">{{ bulkResult.updated }}</div>
                      </div>
                    </div>
                    <div class="col-md-3">
                      <div class="bg-danger bg-opacity-10 p-3 rounded">
                        <div class="text-muted small">Failed</div>
                        <div class="h4 mb-0 text-danger">{{ bulkResult.failed }}</div>
                      </div>
                    </div>
                  </div>

                  <!-- Errors Section -->
                  <div v-if="bulkResult.errors && bulkResult.errors.length > 0" class="mt-3">
                    <h6 class="text-danger fw-bold">Errors:</h6>
                    <div class="alert alert-light border border-danger">
                      <ul class="mb-0">
                        <li v-for="err in bulkResult.errors" :key="err.row" class="text-danger">
                          <strong>Row {{ err.row }}:</strong> {{ err.message }}
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>

                <button @click="resetBulkForm" class="btn btn-secondary mt-2">
                  Import Another File
                </button>
              </div>

              <!-- CSV Template Section -->
              <div class="mt-5 pt-4 border-top">
                <h6 class="fw-bold mb-3">CSV Template Example:</h6>
                <div class="card bg-light">
                  <div class="card-body">
                    <pre class="mb-0"><code>name,description,price,category,stock_status,more_description,specifications
"Blue Shirt","A comfortable shirt",19.99,"Clothing","In Stock","100% cotton","Size: S, M, L, XL"
"Red Shirt","A stylish shirt",24.99,"Clothing","In Stock","Premium cotton","Size: S, M, L, XL"
"Laptop Stand","Aluminum stand",49.99,"Accessories","In Stock","Adjustable height","Color: Silver"</code></pre>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Single Product Tab -->
        <div class="tab-pane fade" id="single-product" role="tabpanel" aria-labelledby="single-tab">
          <div class="card shadow-sm">
            <div class="card-header bg-success text-white">
              <h5 class="mb-0">Add Single Product</h5>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleAddProduct" class="needs-validation">
                <div class="row">
                  <!-- Product Name -->
                  <div class="col-md-6 mb-3">
                    <label for="name" class="form-label fw-bold">Product Name *</label>
                    <input
                      type="text"
                      class="form-control"
                      id="name"
                      v-model="singleForm.name"
                      required
                    />
                  </div>

                  <!-- Price -->
                  <div class="col-md-6 mb-3">
                    <label for="price" class="form-label fw-bold">Price *</label>
                    <div class="input-group">
                      <span class="input-group-text">$</span>
                      <input
                        type="number"
                        class="form-control"
                        id="price"
                        v-model="singleForm.price"
                        step="0.01"
                        min="0"
                        required
                      />
                    </div>
                  </div>

                  <!-- Category -->
                  <div class="col-md-6 mb-3">
                    <label for="category" class="form-label fw-bold">Category *</label>
                    <input
                      type="text"
                      class="form-control"
                      id="category"
                      v-model="singleForm.category"
                      placeholder="e.g., Clothing, Electronics"
                      required
                    />
                  </div>

                  <!-- Stock Status -->
                  <div class="col-md-6 mb-3">
                    <label for="stock_status" class="form-label fw-bold">Stock Status</label>
                    <select class="form-select" id="stock_status" v-model="singleForm.stock_status">
                      <option value="In Stock">In Stock</option>
                      <option value="Low Stock">Low Stock</option>
                      <option value="Out of Stock">Out of Stock</option>
                    </select>
                  </div>

                  <!-- Description -->
                  <div class="col-12 mb-3">
                    <label for="description" class="form-label fw-bold">Description</label>
                    <textarea
                      class="form-control"
                      id="description"
                      v-model="singleForm.description"
                      rows="3"
                      placeholder="Brief product description"
                    ></textarea>
                  </div>

                  <!-- More Description -->
                  <div class="col-12 mb-3">
                    <label for="more_description" class="form-label fw-bold">More Details</label>
                    <textarea
                      class="form-control"
                      id="more_description"
                      v-model="singleForm.more_description"
                      rows="2"
                      placeholder="Additional product details (materials, care instructions, etc.)"
                    ></textarea>
                  </div>

                  <!-- Specifications -->
                  <div class="col-12 mb-3">
                    <label for="specifications" class="form-label fw-bold">Specifications</label>
                    <textarea
                      class="form-control"
                      id="specifications"
                      v-model="singleForm.specifications"
                      rows="2"
                      placeholder="Technical specifications (size, color, dimensions, etc.)"
                    ></textarea>
                  </div>
                </div>

                <!-- Submit Button -->
                <button
                  type="submit"
                  class="btn btn-success btn-lg"
                  :disabled="singleLoading"
                >
                  <span v-if="!singleLoading">
                    <i class="bi bi-plus-circle"></i> Add Product
                  </span>
                  <span v-else>
                    <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    Adding...
                  </span>
                </button>
                <button type="reset" class="btn btn-outline-secondary btn-lg ms-2">Clear</button>
              </form>

              <!-- Result Section for Single Product -->
              <div v-if="singleResult" class="mt-4">
                <div :class="['alert', singleResult.success ? 'alert-success' : 'alert-danger']" role="alert">
                  <h5 class="alert-heading">
                    <i :class="singleResult.success ? 'bi bi-check-circle' : 'bi bi-exclamation-circle'"></i>
                    {{ singleResult.success ? 'Product Added' : 'Error' }}
                  </h5>
                  <p class="mb-0">{{ singleResult.message || singleResult.error }}</p>
                </div>

                <button @click="resetSingleForm" class="btn btn-secondary mt-2">
                  Add Another Product
                </button>
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
import api from '@/services/api';

export default {
  name: 'AdminImport',
  data() {
    return {
      // Bulk import form
      bulkForm: {
        file: null,
        format: 'csv',
        update: false
      },
      bulkLoading: false,
      bulkResult: null,

      // Single product form
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
      singleResult: null
    };
  },
  mounted() {
    // Check if user is authenticated AND is admin
    const auth = useAuthStore();
    if (!auth.isAuthenticated) {
      this.$router.push('/login');
      return;
    }

    // Check if user is superuser (admin)
    if (!auth.isAdmin) {
      // Non-admin users are redirected to home page
      this.$router.push('/');
      return;
    }
  },
  methods: {
    handleFileChange(e) {
      this.bulkForm.file = e.target.files[0];
    },

    async handleBulkImport() {
      if (!this.bulkForm.file) {
        this.bulkResult = { success: false, error: 'Please select a file' };
        return;
      }

      this.bulkLoading = true;
      const formData = new FormData();
      formData.append('file', this.bulkForm.file);
      formData.append('format', this.bulkForm.format);
      formData.append('update', this.bulkForm.update);

      try {
        const response = await api.post('api/admin/import_products/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        this.bulkResult = response.data;
      } catch (error) {
        this.bulkResult = {
          success: false,
          error: error.response?.data?.error || error.message || 'Import failed'
        };
      } finally {
        this.bulkLoading = false;
      }
    },

    async handleAddProduct() {
      this.singleLoading = true;

      try {
        const response = await api.post('api/admin/add_single_product/', this.singleForm);
        this.singleResult = response.data;
      } catch (error) {
        this.singleResult = {
          success: false,
          error: error.response?.data?.error || error.message || 'Failed to add product'
        };
      } finally {
        this.singleLoading = false;
      }
    },

    resetBulkForm() {
      this.bulkForm = {
        file: null,
        format: 'csv',
        update: false
      };
      this.bulkResult = null;
      document.getElementById('file').value = '';
    },

    resetSingleForm() {
      this.singleForm = {
        name: '',
        description: '',
        price: null,
        category: '',
        stock_status: 'In Stock',
        more_description: '',
        specifications: ''
      };
      this.singleResult = null;
    }
  }
};
</script>

<style scoped>
.admin-container {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 2rem 0;
}

.nav-tabs .nav-link {
  color: #6c757d;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
}

.nav-tabs .nav-link:hover {
  border-bottom-color: #0d6efd;
  color: #0d6efd;
}

.nav-tabs .nav-link.active {
  color: #0d6efd;
  border-bottom-color: #0d6efd;
  background-color: transparent;
}

.card {
  border: none;
  border-radius: 0.5rem;
}

.card-header {
  border-radius: 0.5rem 0.5rem 0 0 !important;
  padding: 1.25rem;
}

.btn-lg {
  padding: 0.75rem 2rem;
  font-size: 1rem;
}

pre {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 0.25rem;
  overflow-x: auto;
}

.input-group .form-control {
  border-left: none;
}

.input-group-text {
  background-color: #e9ecef;
  border-right: none;
}

.alert {
  border-radius: 0.5rem;
}
</style>
