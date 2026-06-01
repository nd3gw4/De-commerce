<template>
  <div class="product-detail" v-if="product">
    <div class="detail-header">
      <button class="back-btn" @click="$router.back()">&larr; Back</button>
    </div>
    <div class="detail-main">
      <div class="detail-image-container">
        <img v-if="selectedImage" :src="selectedImage" :alt="product.name" class="product-image" />
      </div>
      <div class="image-thumbnails mt-3" v-if="images.length > 1">
        <img
          v-for="(img, idx) in images"
          :key="idx"
          :src="img"
          :alt="`Product image ${idx + 1}`"
          class="thumbnail"
          :class="{ active: selectedIndex === idx }"
          @click="selectedIndex = idx"
        />
      </div>
      <div class="detail-info">
        <div class="detail-row">
          <div class="detail-info-left">
            <h2 class="product-title">{{ product.name }}</h2>
            <span class="product-category">{{ product.category?.name || 'Uncategorized' }}</span>
          </div>
        </div>
        <p class="product-description">{{ product.description }}</p>

        <!-- Accordions Section -->
        <div class="accordions">
          <div class="accordion" v-for="(accordion, index) in accordions" :key="index">
            <button class="accordion-header" @click="toggleAccordion(index)">
              {{ accordion.title }}
              <span>{{ accordion.open ? '-' : '^' }}</span>
            </button>
            <div class="accordion-body" v-if="accordion.open">
              <p>{{ accordion.content }}</p>
            </div>
          </div>
        </div>

        <div class="add-to-cart-btn-wrapper">
          <button class="add-to-cart-btn" @click="toggleCart">
            {{ inCart ? 'Delete' : 'Add' }}
          </button>
          <router-link to="/cart" class="go-to-cart-link">View Cart &rarr;</router-link>
        </div>
        <div class="detail-info-right">
          
          <!-- Add an a smooth animation to make the product-price appear to be blinking -->

          <span class="product-price">{{ formatPrice(product.price) }}</span>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <p>Loading product...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { fetchProduct } from '../services/products';
import { useAuthStore } from '../store/auth';
import { useCartStore } from '../store/cart';
import { storeToRefs } from 'pinia';

const props = defineProps({
  id: {
    type: String,
    required: true
  }
});

const route = useRoute();
const router = useRouter();
const product = ref(null);
const selectedIndex = ref(0);
const cart = useCartStore();
const auth = useAuthStore();
const { isAuthenticated } = storeToRefs(auth);

const inCart = computed(() => {
  return cart.items.some(i => i.product.id === product.value?.id);
});

const images = computed(() => {
  if (!product.value) return [];
  return [
    product.value.image,
    product.value.image1,
    product.value.image2,
    product.value.image3,
    product.value.image4
  ].filter(Boolean);
});

const selectedImage = computed(() => {
  return images.value[selectedIndex.value] || images.value[0] || '';
});

function formatPrice(price) {
  if (price == null) return '';
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(price);
}

function toggleCart() {
  if (!product.value) return;
  if (inCart.value) {
    cart.remove(product.value.id);
  } else {
    cart.add(product.value, 1);
  }
}

// Accordion state
const accordionOpenStates = ref([false, false, false]);

const accordions = computed(() => [
  { title: 'More Description', content: product.value?.more_description || 'No additional information available.', open: accordionOpenStates.value[0] },
  { title: 'Specifications', content: product.value?.specifications || 'No specifications available.', open: accordionOpenStates.value[1] },
  { title: 'Stock Status', content: product.value?.stock_status || 'Stock status not available.', open: accordionOpenStates.value[2] },
]);

function toggleAccordion(index) {
  accordionOpenStates.value[index] = !accordionOpenStates.value[index];
}

onMounted(async () => {
  try {
    const response = await fetchProduct(props.id);
    product.value = response.data;
    cart.load();
  } catch (error) {
    product.value = null;
  }
});
</script>

<style scoped>

@import url('https://fonts.googleapis.com/css2?family=Jersey+10&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');
:root {
  --text-color: #191919;
  --extra-color: #f15025;
  --paragraph-color: #191919;
  --background-color: #fcfffc;
  
}

.product-detail {
  max-width: 1000px;
  margin: 4rem auto 2rem auto;
  background: var(--background-color);
  color: var(--paragraph-color) ;
  padding: 2.5rem 2.5rem 2rem 2.5rem;
  border-radius: 0;
  position: relative;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;
}

.back-btn {
  font-family: "Jersey 10", sans-serif;
  background: none;
  border: none;
  color: var(--extra-color);
  font-size: 1.4rem;
  cursor: pointer;
  padding: 0.5rem 1.2rem;
  border-radius: 0;
  transition: background 0.7s;
}

.back-btn:hover {
  color: var(--background-color);
  background: var(--extra-color);
}

.add-to-cart-btn {
  background: var(--text-color);
  color: var(--background-color);
  border: none;
  border-radius: 0;
  padding: 0.7rem 2.2rem;
  margin: 0 2rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.7s;
}

.add-to-cart-btn:hover {
  background: var(--extra-color);
}

.add-to-cart-btn-wrapper {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-start;
}

.go-to-cart-link {
  padding: 0.5rem 1rem;
  border: 1.4px solid var(--extra-color);
  transition: all 0.7s ease;
}

.go-to-cart-link:hover {
  background-color: var(--paragraph-color);
  color: var(--background-color);
}

.detail-main {
  display: flex;
  flex-direction: row;
  gap: 2.5rem;
}

.detail-image-container {
  flex: 0 0 240px;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  background: var(--background-color);
  border-radius: 12px;
  min-height: 220px;
  max-height: 260px;
  overflow: hidden;
}

.product-image {
  width: 100%;
  max-width: 320px;
  height: 320px;
  object-fit: contain;
  border-radius: 12px;
  background: var(--background-color);
}

.image-thumbnails {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}

.image-thumbnails .thumbnail {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
  border: 2px solid transparent;
  cursor: pointer;
}

.image-thumbnails .thumbnail.active {
  border-color: var(--extra-color);
}

.detail-info {
  font-family: "Montserrat", sans-serif;
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.detail-row {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 2.8rem;
}

.detail-info-left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.3rem;
}

.product-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-color);
  margin: 0;
  line-height: 1.2;
}

.product-category {
  font-family: "Jersey 10", sans-serif;
  font-size: 1.5rem;
  color: var(--paragraph-color);
  background: var(--extra-color);
  border-radius: 0;
  padding: 0.2rem 0.8rem;
  margin-top: 1.2rem;
  display: inline-block;
  transition: background 0.7s ease, color 0.7s ease;
}

.product-category:hover {
  background: var(--text-color);
  color: var(--background-color);
}

.product-description {
  font-size: 1.08rem;
  color: var(--paragraph-color);
  margin-top: 0.5rem;
  line-height: 1.6;
  letter-spacing:1px;
}


.detail-info-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
  min-width: 90px;
}

.product-price {
  font-size: 1.7rem;
  font-family: "Jersey 10", sans-serif;
  border: 1.4px solid var(--extra-color);
  padding: 0.7rem 1.4rem;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 0.5rem;
}

/* Accordions Section */

.accordions {
  display: inline-block;
  justify-content: flex-start;
  align-items: center;
}

.accordions .accordion {
  padding: 2.1rem;
}

.accordions .accordion .accordion-header {
  font-family: "Jersey 10", sans-serif;
  border-left: 1.4px solid var(--extra-color);
  background-color: var(--background-color);
  border-radius: 0;
  font-size: 1.2rem;
  transition: all 0.7s ease;
}

.accordions .accordion .accordion-body {
  font-family: "Montserrat", sans-serif;
  border-bottom: 1.4px solid var(--extra-color);
  border-left: 1.4px solid var(--extra-color);
}


@media (max-width: 900px) {
  .product-detail {
    padding: 1.2rem;
  }
  .detail-main {
    flex-direction: column;
    gap: 1.5rem;
  }
  .detail-image-container {
    min-height: 160px;
    max-height: 180px;
  }
  .product-image {
    max-width: 100%;
    height: 160px;
  }
}
</style>
