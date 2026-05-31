/**
 * Authentication Store Module (Pinia)
 *
 * This module manages the global authentication state using Pinia stores.
 * It tracks whether the user is authenticated and provides actions to update state.
 * 
 * State is persisted via localStorage for session persistence across page reloads.
 * Combines with backend session cookies for complete authentication system.
 *
 * Authentication Flow:
 * 1. User logs in via Login.vue → loginUser() API call
 * 2. Backend creates session cookie
 * 3. Frontend auth.login() sets localStorage and store state
 * 4. Navbar shows authenticated state
 * 5. Subsequent API calls include session cookie (withCredentials)
 * 6. Protected routes check isAuthenticated before rendering
 * 7. On logout, localStorage and store cleared
 */

import { defineStore } from 'pinia';

/**
 * useAuthStore: Global authentication state store
 * 
 * State Properties:
 * - isAuthenticated: Boolean flag indicating if user is logged in
 *   - Initial value: Checks localStorage for 'isAuthenticated' flag
 *   - Persists across page reloads
 *   - Used by Navbar to show/hide login/logout buttons
 *   - Used by route guards to protect authenticated pages
 *   - Used by components to conditionally show add-to-cart buttons
 * 
 * Store ID: 'auth'
 * - Used to create store instance: const auth = useAuthStore()
 * 
 * Example Usage in Components:
 * import { useAuthStore } from '@/store/auth';
 * import { storeToRefs } from 'pinia';
 * 
 * const auth = useAuthStore();
 * const { isAuthenticated } = storeToRefs(auth);
 * 
 * if (isAuthenticated.value) {
 *   // Show authenticated-only content
 * }
 */
export const useAuthStore = defineStore('auth', {
  state: () => ({
    /**
     * isAuthenticated: Boolean flag for user login state
     * 
     * Initialized from localStorage:
     * - true if 'isAuthenticated' exists in localStorage
     * - false if localStorage key doesn't exist
     * 
     * Updated by:
     * - login(): Set to true when user logs in
     * - logout(): Set to false when user logs out
     * - sync(): Updates from localStorage (for cross-tab awareness)
     * 
     * Checked by:
     * - Navbar.vue: Shows Cart/Orders/Profile links if authenticated
     * - Navbar.vue: Shows Logout link if authenticated
     * - ProductDetail.vue: Shows "Add to Cart" button if authenticated
     * - Route guards: Prevents access to protected pages
     */
    isAuthenticated: !!localStorage.getItem('isAuthenticated'),
    
    /**
     * isAdmin: Boolean flag indicating if user has admin privileges (is_superuser)
     * 
     * Initialized from localStorage:
     * - true if 'isAdmin' exists in localStorage
     * - false if localStorage key doesn't exist
     * 
     * Updated by:
     * - login(userData): Set based on userData.is_superuser when user logs in
     * - logout(): Set to false when user logs out
     * - sync(): Updates from localStorage (for cross-tab awareness)
     * 
     * Checked by:
     * - Router guards: Prevents non-admins from accessing /admin/* routes
     * - Navbar.vue: Shows admin dashboard link if isAdmin=true
     * - AdminImport.vue: Redirects non-admins to /login
     */
    isAdmin: !!localStorage.getItem('isAdmin'),
  }),
  
  actions: {
    /**
     * login(userData): Set authenticated state when user logs in
     * 
     * Called after successful POST /api/login/ API call
     * 
     * @param {Object} userData - User object from API response containing is_superuser flag
     * @param {number} userData.id - User ID
     * @param {string} userData.username - Username
     * @param {string} userData.email - Email address
     * @param {boolean} userData.is_superuser - True if user is admin, false otherwise
     * 
     * Updates both:
     * 1. Pinia store state (isAuthenticated = true, isAdmin = is_superuser)
     * 2. localStorage ('isAuthenticated' = 'true', 'isAdmin' = is_superuser)
     * 
     * Effect:
     * - Navbar shows authenticated user links (Cart, Orders, Profile, Logout)
     * - Navbar hides login/register links
     * - If isAdmin=true, navbar shows admin dashboard link
     * - Protected API endpoints work (session cookie sent)
     * - Route redirects enable access to /cart, /orders, /profile
     * - Admin-only routes become accessible if isAdmin=true
     * 
     * Frontend Flow:
     * try {
     *   const response = await loginUser(username, password);
     *   auth.login(response.data.user);  // Called with user data from API
     *   router.push('/');
     * } catch (error) {
     *   // Handle error
     * }
     */
    login(userData) {
      this.isAuthenticated = true;
      this.isAdmin = userData?.is_superuser || false;
      localStorage.setItem('isAuthenticated', 'true');
      if (this.isAdmin) {
        localStorage.setItem('isAdmin', 'true');
      } else {
        localStorage.removeItem('isAdmin');
      }
    },

    /**
     * logout(): Clear authenticated state when user logs out
     * 
     * Called when user clicks logout in Navbar.vue
     * Clears both:
     * 1. Pinia store state (isAuthenticated = false, isAdmin = false)
     * 2. localStorage (removes 'isAuthenticated' and 'isAdmin' keys)
     * 
     * Effect:
     * - Navbar shows login/register links
     * - Navbar hides authenticated user links and admin link
     * - Session cookie still valid on backend (requires server-side logout)
     * - Protected API calls return 401 Unauthorized
     * - Route guards redirect to /login
     * - CartStore and OrderStore data persists (may contain old data)
     * 
     * Frontend Flow:
     * async function logout() {
     *   try {
     *     await logoutUser();
     *   } catch {}
     *   auth.logout();  // Called here
     *   router.push('/login');
     * }
     */
    logout() {
      this.isAuthenticated = false;
      this.isAdmin = false;
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('isAdmin');
    },

    /**
     * sync(): Synchronize store state from localStorage
     *
     * Updates isAuthenticated and isAdmin from localStorage values.
     * Used for cross-tab awareness and recovery from localStorage changes.
     * 
     * Called by:
     * - Navbar.vue onMounted: Syncs state if page reloaded
     * - Window 'storage' event listener: Syncs if other tab logs in/out
     * 
     * Use Case:
     * If user logs in on tab A:
     * - localStorage 'isAuthenticated' set to 'true'
     * - localStorage 'isAdmin' set based on is_superuser
     * - Tab B detects storage event
     * - Calls sync() to update its state
     * - Tab B now shows authenticated UI and admin link (if admin) without manual refresh
     * 
     * Example Implementation in Component:
     * window.addEventListener('storage', () => {
     *   auth.sync();
     * });
     */
    sync() {
      this.isAuthenticated = !!localStorage.getItem('isAuthenticated');
      this.isAdmin = !!localStorage.getItem('isAdmin');
    }
  },
});
