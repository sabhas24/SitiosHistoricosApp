import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MapView from '../views/MapView.vue'
import SiteDetailView from '../views/SiteDetailView.vue'
import SitiosListView from '../views/SitiosListView.vue'
import LoginView from '../views/LoginView.vue'
import ProfileView from '../views/ProfileView.vue'
import { useAuthStore } from '../stores/auth';
import loginSuccess from '../views/LoginSuccessView.vue'

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
      path: '/sitios',
      name: 'sitios-list',
      component: SitiosListView,
    },
    {
      path: '/map',
      name: 'map',
      component: MapView,
      meta: { requiresAuth: true },
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true },
    },
    {
      path: '/sitio/:id',
      name: 'sitio-detail',
      component: SiteDetailView,
    },
    {
      path: '/login-success',
      name: 'login-success',
      component: loginSuccess,
    }
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    if (to.name !== 'login') {
      // Redirige al login y guarda la ruta original
      return next({ name: 'login', query: { redirect: to.fullPath } });
    }
  }
  next();
});

export default router
