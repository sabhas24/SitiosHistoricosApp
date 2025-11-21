import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth';
import HomeView from '../views/HomeView.vue'


const MapView = () => import('../views/MapView.vue')
const SiteDetailView = () => import('../views/SiteDetailView.vue')
const SitiosListView = () => import('../views/SitiosListView.vue')
const LoginView = () => import('../views/LoginView.vue')
const ProfileView = () => import('../views/ProfileView.vue')
const LoginSuccessView = () => import('../views/LoginSuccessView.vue')
const RegisterView = () => import('../views/RegisterView.vue')

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
      component: LoginSuccessView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
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
