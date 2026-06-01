<template>
  <!-- Navigation Bar with Dynamic Links Based on Authentication Status -->
  <nav class="navbar navbar-expand-lg sticky-top">
    <div class="container d-flex justify-content-between align-items-center">
      <!-- Brand/Logo - Always Visible -->
      <div class="navbar-brand">
        <!-- router-link: Navigate to home without page reload -->
        <router-link to="/" class="brandName">Jirani Merchants</router-link>
      </div>

      <!-- Navigation Links -->
      <ul class="navbar-nav flex-row align-items-center">
        <!-- Home Link - Visible only for unauthenticated users -->
        <li class="nav-item" v-if="!isAuthenticated">
          <router-link class="nav-link" to="/" exact-active-class="active-page">
            Home
          </router-link>
        </li>

        <!-- Products Link - Always Visible (No Login Required) -->
        <li class="nav-item">
          <router-link class="nav-link" to="/products" active-class="active-page">
            Products
          </router-link>
        </li>

        <!-- Cart Link - ONLY FOR NON-ADMIN AUTHENTICATED USERS -->
        <li class="nav-item" v-if="isAuthenticated && !isAdmin">
          <router-link class="nav-link" to="/cart" active-class="active-page">
            Cart
          </router-link>
        </li>

        <!-- Orders Link - ONLY FOR NON-ADMIN AUTHENTICATED USERS -->
        <li class="nav-item" v-if="isAuthenticated && !isAdmin">
          <router-link class="nav-link" to="/orders" active-class="active-page">
            Orders
          </router-link>
        </li>

        <!-- Conditional Authentication Links -->
        <!-- v-if="!isAuthenticated": Show for logged-out users -->
        <li class="nav-item" v-if="!isAuthenticated">
          <router-link class="nav-link" to="/login" active-class="active-page">
            Login
          </router-link>
        </li>

        <!-- Authenticated User Menu: Profile and Logout -->
        <!-- v-else (implicit from v-if): Show for logged-in users -->
        <template v-else>
          <li class="nav-item" v-if="isAdmin">
            <router-link class="nav-link" to="/admin" active-class="active-page">
              Admin
            </router-link>
          </li>

          <!-- Profile Link - ONLY FOR AUTHENTICATED USERS -->
          <!-- Links to /profile route with user information and order history -->
          <li class="nav-item" v-if="!isAdmin">
            <router-link class="nav-link" to="/profile" active-class="active-page">
              Profile
            </router-link>
          </li>

          <!-- Logout Link - ONLY FOR AUTHENTICATED USERS -->
          <!-- @click.prevent="logout": Calls logout function on click -->
          <!-- .prevent: Prevents default link behavior (navigation) -->
          <li class="nav-item">
            <a class="nav-link" href="#" @click.prevent="logout">
              Logout
            </a>
          </li>
        </template>
      </ul>
    </div>
  </nav>
</template>

<script setup>
/**
 * Navbar Component Script
 * 
 * Displays navigation bar with links to main pages.
 * Links dynamically shown/hidden based on authentication status.
 * Uses reactive state from useAuthStore (Pinia) for isAuthenticated flag.
 */

import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { logoutUser } from '../services/auth';
import { useAuthStore } from '../store/auth';
import { storeToRefs } from 'pinia';

const auth = useAuthStore();
/**
 * storeToRefs: Convert Pinia store properties to Vue reactive refs
 * Allows using isAuthenticated directly in template
 * When auth.isAuthenticated changes, template automatically updates
 */
const { isAuthenticated, isAdmin } = storeToRefs(auth);
const router = useRouter();

/**
 * logout(): Handle user logout
 * 
 * Called when user clicks "Logout" link
 * Steps:
 * 1. Call logoutUser() API to server (destroy session)
 * 2. Call auth.logout() to update Pinia store
 * 3. Redirect to /login page
 * 
 * Error Handling:
 * - Try-catch silently ignores API errors
 * - Store logout still executes even if API fails
 * - User always redirected to login page
 * 
 * Effects After Logout:
 * - isAuthenticated set to false
 * - localStorage 'isAuthenticated' key removed
 * - Navbar shows Login link instead of Cart/Orders/Profile
 * - Protected routes redirect to /login if accessed
 * - API calls include session cookie but will return 401
 */
async function logout() {
  try {
    await logoutUser();
  } catch {}  // Silently handle API errors
  auth.logout();  // Clear frontend auth state
  router.push('/login');  // Redirect to login page
}

/**
 * onMounted(): Lifecycle hook - runs after component rendered
 * 
 * Responsibilities:
 * 1. Load Font Awesome icons if not already loaded
 * 2. Set up cross-tab authentication sync
 */
onMounted(() => {
  auth.sync(); // Ensure authentication state is synchronized on component mount
  window.addEventListener('storage', () => {
    auth.sync();
  });
});
</script>

<style scoped>

@import url('https://fonts.googleapis.com/css2?family=Jersey+10&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

:root {
  --text-color: #191919;
  --extra-color: #f15025;
  --paragraph-color: #191919;
  --background-color: #fcfffc;
  /* semi-transparent version for the glass effect */
  --navbar-bg: rgba(252, 255, 252, 0.9); 
}

.navbar {
  height: 14vh; /* Adjusted for better visibility */
  background-color: var(--navbar-bg);
  /* The Blur Effect */
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  
  /* Border and Box Shadow */
  border-bottom: 1.4px solid var(--text-color);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
  
  transition: all 0.3s ease;
  z-index: 1000;
}

.navbar-brand .brandName {
  color: var(--text-color);
  text-decoration: none;
  font-size: 2.1rem;
  font-family: "Jersey 10", sans-serif;
  font-weight: 600;
  letter-spacing: 3px;
}

.navbar-nav .nav-item {
  margin: 0 0.5rem;
  transition: transform 0.3s ease;
}

.nav-link {
  font-size: 1.4rem;
  color: var(--text-color) !important;
  font-family: "Jersey 10", sans-serif;
  font-weight: 400;
  padding: 10px 18px !important;
  display: flex;
  align-items: center;
}

/* Hover Effect */
.nav-link:hover {
  background-color: rgba(146, 20, 12, 0.10);
  transform: translateY(-2px);
}

/* --- ACTIVE PAGE STYLING --- */
.active-page {
  background-color: var(--text-color) !important;
  color: var(--background-color) !important; /* Dark text for contrast */
  box-shadow: 0 4px 15px rgba(146, 20, 12, 0.34); /* Glowing shadow */
  font-weight: 700;
}

.active-page i {
  color: var(--background-color) !important;
}

/* Ensures the icon inherits the link's color */
.nav-item i {
  transition: color 0.3s ease;
}
</style>