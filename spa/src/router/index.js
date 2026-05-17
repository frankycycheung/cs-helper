import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../../views/HomeView.vue'
import UpgradeNewsView from '../../views/UpgradeNewsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/upgrade-news',
      name: 'upgrade-news',
      component: UpgradeNewsView,
    },
  ],
})

export default router
