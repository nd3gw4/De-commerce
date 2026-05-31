import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import ProductList from '../views/ProductList.vue';
import ProductDetail from '../views/ProductDetail.vue';
import Cart from '../views/Cart.vue';
import Checkout from '../views/Checkout.vue';

import OrderHistory from '../views/OrderHistory.vue';
import OrderDetail from '../views/OrderDetail.vue';
import Profile from '../views/Profile.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import ResetPassword from '../views/ResetPassword.vue';
import CookiePolicy from '../views/CookiePolicy.vue';
import TermsOfUse from '../views/TermsOfUse.vue';
import PrivacyPolicy from '../views/PrivacyPolicy.vue';
import Contact from '../views/Contact.vue';
import AdminImport from '../views/AdminImport.vue';
import { useAuthStore } from '../store/auth';

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/products', name: 'ProductList', component: ProductList },
  { path: '/products/:id', name: 'ProductDetail', component: ProductDetail, props: true },
  { path: '/cart', name: 'Cart', component: Cart, meta: { requiresAuth: true } },
  { path: '/checkout', name: 'Checkout', component: Checkout, meta: { requiresAuth: true } },
  { path: '/orders', name: 'OrderHistory', component: OrderHistory, meta: { requiresAuth: true } },
  { path: '/orders/:id', name: 'OrderDetail', component: OrderDetail, props: true, meta: { requiresAuth: true } },
  { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true } },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/reset-password', name: 'ResetPassword', component: ResetPassword },
  { path: '/admin/import', name: 'AdminImport', component: AdminImport, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/cookie-policy', name: 'CookiePolicy', component: CookiePolicy },
  { path: '/terms-of-use', name: 'TermsOfUse', component: TermsOfUse },
  { path: '/privacy-policy', name: 'PrivacyPolicy', component: PrivacyPolicy },
  { path: '/contact', name: 'Contact', component: Contact },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard for authentication-protected routes
router.beforeEach((to, from, next) => {
  const auth = useAuthStore();

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next({ name: 'Login', query: { next: to.fullPath } });
    return;
  }

  // Check for admin-only routes
  if (to.meta.requiresAdmin && !auth.isAdmin) {
    next({ name: 'Home' });  // Redirect non-admins to home page
    return;
  }

  if ((to.name === 'Login' || to.name === 'Register') && auth.isAuthenticated) {
    next({ name: 'Profile' });
    return;
  }

  if (to.name === 'Home' && auth.isAuthenticated) {
    next({ name: 'Profile' });
    return;
  }

  next();
});

export default router;
