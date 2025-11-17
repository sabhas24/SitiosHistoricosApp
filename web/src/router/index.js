import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MapView from '../views/MapView.vue'
import LoginView from '../views/LoginView.vue'
import { useAuthStore } from '../stores/auth';
import loginSuccess from '../views/LoginSuccessView.vue'
import ProfileView from '../views/ProfileView.vue'
import MyReviewsView from '../views/MyReviewsView.vue'
import FavoritesView from '../views/FavoritesView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/map',
      name: 'map',
      component: MapView,
      meta: { requiresAuth: true },
    },
    {
      path: '/login-success',
      name: 'login-success',
      component: loginSuccess,
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true },
    }
    ,
    {
      path: '/my-reviews',
      name: 'my-reviews',
      component: MyReviewsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/favorites',
      name: 'favorites',
      component: FavoritesView,
      meta: { requiresAuth: true }
    }
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isLogin = to.name === 'login';
  const requiresAuth = to.meta.requiresAuth;
  const isAuthenticated = authStore.isAuthenticated;

  if (isLogin && isAuthenticated) return next({ name: 'home' });
  if (requiresAuth && !isAuthenticated) return next({ name: 'login' });

  next();
});


export default router
