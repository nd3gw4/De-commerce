<template>
  <!-- Product Display Card Component -->
  <!-- Shows product image, name, category, price, and link to details -->
  <div class="product-card">
    <!-- Product Image Container -->
    <div class="image-container">
      <!-- Display Product Image if Available -->
      <img
        v-if="productImage"
        :src="productImage"
        :alt="product.name"
        class="product-image"
      />
      <!-- Fallback Placeholder if No Product Image -->
      <div v-else class="image-placeholder">
        <span>No Image Available</span>
      </div>
    </div>

    <!-- Product Information Section -->
    <div class="product-content">
      <div class="product-row">
        <!-- Product Details on Left: Name and Category -->
        <div class="product-info-left">
          <h3 class="product-title">{{ product.name }}</h3>
          <!-- Display Category Name - handles nested category objects -->
          <span class="product-category">
            {{ product.category?.name || product.category || 'Uncategorized' }}
          </span>
        </div>
        <!-- Product Price on Right -->
        <div class="product-info-right">
          <span class="product-price">{{ formatPrice(product.price) }}</span>
        </div>
      </div>
    </div>
    
    <!-- Product Action Footer -->
    <div class="product-footer">
      <div class="product-actions">
          <!-- Add to cart button removed; only available in ProductDetail -->
      </div>
      <!-- Link to Full Product Details Page -->
      <div class="view-details-wrapper">
        <!-- router-link navigates to ProductDetail page with product ID -->
        <!-- :to dynamically sets route based on product.id -->
        <router-link :to="`/products/${product.id}`" class="details-link">
          View Details &rarr;
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * ProductCard Component
 * 
 * Displays a product in card format for grid layouts.
 * Used by ProductList.vue to show all products.
 * Shows product preview with image, name, category, and price.
 * 
 * Props:
 * - product: Object {id, name, description, price, category, image}
 * 
 * Features:
 * - Handles missing images with placeholder
 * - Links to ProductDetail for full product view
 * - Formats price as currency
 * - Responsive grid layout
 * 
 * Click Flow:
 * User clicks "View Details" → ProductDetail.vue loaded with product ID → 
 * ProductDetail fetches product details → Shows "Add to Cart" button if authenticated
 */

import { ref, computed } from 'vue';

/**
 * Props: Component inputs
 * - product: Product object to display {id, name, description, price, category, image}
 */
const { product } = defineProps({
  product: Object
});

// Debug: log incoming product prop when component is created
// eslint-disable-next-line no-console
console.debug('ProductCard mounted product id:', product?.id, 'name:', product?.name);

const isAuthenticated = ref(!!localStorage.getItem('isAuthenticated'));
const inCart = ref(false);

/**
 * formatPrice(): Convert number to USD currency format
 * @param {number} price - Price value
 * @returns {string} Formatted price like "$99.99"
 * 
 * Uses Intl.NumberFormat for locale-aware formatting
 * Shows currency symbol and 2 decimal places
 */
function formatPrice(price) {
  if (price == null) return '';
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(price);
}

/**
 * toggleCart(): Toggle cart button state
 * Currently unused - add to cart only on ProductDetail page
 */
const productImage = computed(() => {
  return (
    product?.image ||
    product?.image1 ||
    product?.image2 ||
    product?.image3 ||
    product?.image4 ||
    ''
  );
});

function toggleCart() {
  inCart.value = !inCart.value;
}
</script>

<style scoped>


:root {
  --text-color: #191919;
  --extra-color: #f15025;
  --paragraph-color: #191919;
  --background-color: #fcfffc;
}

.product-card {
  background: var(--background-color);
  color: var(--paragraph-color);
  border-radius: 0;
  /* Balanced glow to match ProductList grid */
  box-shadow: 0 0 25px 5px var(--glow-color);
  width: 70%; /* Adjusted from 700px for better grid fit */
  height: 49vh;
  padding: 3rem;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1.1px solid var(--paragraph-color);
  margin: 2rem 0;
}

.image-container {
  width: 100%;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  overflow: hidden;
  border-radius: 0;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--background-color);
  border: 1px solid var(--text-color);
  color: var(--text-color);
  font-size: 0.9rem;
  font-weight: 600;
  text-align: center;
  padding: 1rem;
}

.product-content {
  margin-bottom: 1.5rem;
  font-family: "Montserrat", sans-serif;
}

.product-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.product-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-color);
  line-height: 1.2;
}

.product-category {
  font-size: 0.85rem;
  color: var(--paragraph-color);
  background-color: var(--extra-color);
  font-weight: 500;
  margin-top: 1rem;
  display: inline-block;
  padding: 1rem 1rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.product-price {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-color);
}

.product-footer {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.details-link {
  color: var(--text-color);
  font-weight: 700;
  text-decoration: none;
  font-size: 1rem;
  transition: color 0.2s;
}

.details-link:hover {
  color: var(--extra-color);
  text-decoration: underline;
}

@media (max-width: 600px) {
  .product-card {
    padding: 1.5rem;
  }
}
</style>

