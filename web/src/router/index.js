import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MapView from '../views/MapView.vue'
import SiteDetailView from '../views/SiteDetailView.vue'
import SitiosListView from '../views/SitiosListView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
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
      path: '/sitio/:id',
      name: 'sitio-detail',
      component: SiteDetailView,
    }
  ],
})

export default router
