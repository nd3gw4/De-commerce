<template>
  <div class="register-container">
    <div class="register-card">
      <h2 class="register-title">Register</h2>
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label>Username</label>
          <input v-model="form.username" placeholder="Choose a username" required />
        </div>
        <div class="form-group">
          <label>Email</label>
          <input v-model="form.email" type="email" placeholder="Email@gmail.com" required />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input type="password" v-model="form.password1" placeholder="Create a password" required />
        </div>
        <div class="form-group">
          <label>Confirm Password</label>
          <input type="password" v-model="form.password2" placeholder="Repeat your password" required />
        </div>
        
        <button type="submit" :disabled="loading" class="register-btn">
          {{ loading ? 'Creating Account...' : 'Register' }}
        </button>

        <div v-if="error" class="error-message">{{ error }}</div>
          <div v-if="error" class="text-red-500 text-sm mb-2">
            <template v-if="Array.isArray(error)">
              <ul class="list-disc ml-5">
                <li v-for="(errMsg, idx) in error" :key="idx">{{ errMsg }}</li>
              </ul>
            </template>
            <template v-else>
              {{ error }}
            </template>
          </div>
        <div v-if="success" class="success-message">Registration successful! Redirecting to login...</div>
      </form>
      <div class="register-links">
        <router-link to="/login" class="register-link">Already have an account? Login</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { registerUser } from '../services/auth';

const form = ref({ username: '', email: '', password1: '', password2: '' });
const loading = ref(false);
const error = ref('');
const success = ref(false);
const router = useRouter();

async function handleRegister() {
  loading.value = true;
  error.value = '';
  success.value = false;
  if (form.value.password1 !== form.value.password2) {
    error.value = 'Passwords do not match.';
    loading.value = false;
    return;
  }
  try {
    await registerUser({
      username: form.value.username,
      email: form.value.email,
      password1: form.value.password1,
      password2: form.value.password2
    });
    success.value = true;
    setTimeout(() => router.push('/login'), 1500);
  } catch (err) {
    // Improved error extraction
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
      if (data && data.detail) {
        details.push(data.detail);
      }
      if (data && data.non_field_errors) {
        details = details.concat(data.non_field_errors);
      }
      if (details.length === 0 && data) {
        // Show all serializer errors
        details = details.concat(Object.values(data).flat());
      }
      error.value = `Registration failed (HTTP ${status}).\n` + details.join('\n');
    } else {
      error.value = 'Registration failed. No response from server.';
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

.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.register-card {
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

.register-title {
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
  padding: 0 1.4rem;
}

input {
  background: var(--background-color);
  border: 1px solid var(--paragraph-color);
  border-radius: 0;
  border-bottom: none;
  padding: 0.8rem;
  color: var(--text-color);
  outline: none;
  transition: all 0.7s ease;
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

.register-btn {
  width: 100%;
  font-family: "Jersey 10", sans-serif;
  letter-spacing: 1.4px;
  background: var(--extra-color);
  color: var(--text-color);
  border: none;
  border-radius: 0;
  padding: 0.8rem;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.7s ease;
  margin-top: 3rem;
}

.register-btn:hover:not(:disabled) {
  background: var(--background-color);
  color: var(--extra-color);
  border-bottom: 2px solid var(--extra-color);
  transform: translateY(-2px);
  margin-top: 1.8rem;
}

.register-btn:disabled {
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

.success-message {
  color: var(--extra-color);
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.9rem;
  background: var(--background-color);
  padding: 0.7rem;
  border-radius: 0;
  border: 1px solid var(--text-color);
}

.register-links {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  align-items: center;
  font-family: "Montserrat", sans-serif;
}

.register-link {
  color: var(--text-color);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.7s ease;
  padding: 0.4rem 0.8rem;
  border-bottom: 1.4px solid var(--extra-color);
}

.register-link:hover {
  border: none;
  background-color: var(--paragraph-color);
  color: var(--background-color);
}

@media (max-width: 480px) {
  .register-card {
    padding: 1.5rem;
  }
}
</style>