<template>
  <div class="login-container">
    <div class="login-card">
      <h2 class="login-title">Login</h2>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label>Username</label>
          <input v-model="username" placeholder="J-M/C-2020" required />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input type="password" v-model="password" placeholder="Enter password" required />
        </div>
        <button type="submit" :disabled="loading" class="login-btn">
          {{ loading ? 'Authenticating...' : 'Login' }}
        </button>
        <div v-if="error" class="error-message">{{ error }}</div>
      </form>
      <div class="login-links">
        <router-link to="/register" class="login-link">Don't have an account? <strong>Register</strong></router-link>
        <router-link to="/reset-password" class="login-link-fp">Forgot password?</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { loginUser } from '../services/auth';
import { useAuthStore } from '../store/auth';

const username = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');
const router = useRouter();
const route = useRoute();
const auth = useAuthStore();

async function handleLogin() {
  loading.value = true;
  error.value = '';
  try {
    const response = await loginUser(username.value, password.value);
    // Pass user data from API response to auth store
    auth.login(response.data.user);
    const nextRoute = route.query.next;
    const redirectTarget = auth.isAdmin
      ? { name: 'AdminDashboard' }
      : (typeof nextRoute === 'string' && nextRoute) || { name: 'Profile' };
    router.push(redirectTarget);
  } catch (err) {
    if (err.response) {
      const { status, data } = err.response;
      let details = [];
      if (data && data.errors) {
        if (typeof data.errors === 'string') {
          details.push(data.errors);
        } else if (typeof data.errors === 'object') {
          details = details.concat(Object.values(data.errors).flat());
        }
      }
      if (data && data.message) {
        details.push(data.message);
      }
      if (data && data.detail) {
        details.push(data.detail);
      }
      if (details.length === 0 && data) {
        details = details.concat(Object.values(data).flat());
      }
      error.value = `Login failed (HTTP ${status}).\n` + details.join('\n');
    } else {
      error.value = 'Login failed. No response from server.';
    }
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>

@import url('https://fonts.googleapis.com/css2?family=Jersey+10&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');
:root {
  --text-color: #191919;
  --extra-color: #f15025;
  --paragraph-color: #191919;
  --background-color: #fcfffc;
  
}

/* Matching the Color Palette from ProductDetails */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh; /* Centers the card vertically on the page */
}

.login-card {
  max-width: 500px;
  width: 100%;
  background: var(--background-color);
  color: var(--paragraph-color);
  padding: 2.5rem;
  border-radius: 0;
  /* Matching the ProductDetails glowing shadow */
  box-shadow: 0 0 40px 10px rgba(82, 255, 134, 0.2); 
  border: 1px solid var(--text-color);
}

.login-title {
  font-family: "Jersey 10", sans-serif;
  letter-spacing: 1.4px;
  font-size: 2.8rem;
  color: var(--text-color);
  margin-bottom: 2.8rem;
  text-align: center;
}

.form-group {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-size: 1rem;
  font-family: "Jersey 10", sans-serif;
  letter-spacing: 1.4px;
  color: var(--text-color);
  padding: 0rem 1.4rem;
}

input {
  background: var(--background-color);
  border: 1px solid var(--paragraph-color);
  border-radius: 0;
  border-bottom: none;
  padding: 0.8rem;
  color: var(--text-color);
  outline: none;
  transition: border-color 0.7s ease;
}

input:focus {
  border-color: var(--text-color);
  background: var(--background-color);
}

input::placeholder {
  font-family: "Jersey 10", sans-serif;
  letter-spacing: 1.4px;
  font-size: 1rem;
}

.login-btn {
  width: 100%;
  font-family: "Jersey 10", sans-serif;
  letter-spacing: 1.4px;
  background: var(--extra-color);
  color: var(--text-color); /* Dark text on gold button for high contrast */
  border: none;
  border-radius: 0;
  padding: 0.8rem;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.7s ease;
  margin-top: 3rem;
}

.login-btn:hover:not(:disabled) {
  background: var(--background-color);
  color: var(--extra-color);
  border-bottom: 2px solid var(--extra-color);
  transform: translateY(-2px);
  margin-top: 1.8rem;
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  color: var(--extra-color);
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.9rem;
  background: var(--text-color);
  padding: 0.5rem;
  border-radius: 0;
}

.login-links {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  align-items: center;
  font-family: "Montserrat", sans-serif;
}

.login-link {
  color: var(--text-color);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.7s ease;
  padding: 0.4rem 0.8rem;
  border-bottom: 1.4px solid var(--extra-color);
}

.login-link strong {
  margin-left: 0.8rem;
  text-decoration: none;
  font-weight: 700;
}

.login-links .login-link-fp {
  border-bottom: 1.4px solid var(--extra-color);
  padding: 0.4rem 0.8rem;
  color: var(--text-color);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.7s ease;
}

.login-link:hover {
  border: none;
  background-color: var(--paragraph-color);
  color: var(--background-color);
}

.login-link-fp:hover {
  border: none;
  background-color: var(--paragraph-color);
  color: var(--background-color);
}

</style>