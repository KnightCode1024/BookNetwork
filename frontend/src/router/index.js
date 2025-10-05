import { createRouter, createWebHistory } from 'vue-router'
import ActivationPage from '../views/ActivationPage.vue'

const routes = [
  {
    path: '/activate/:uid/:token',
    name: 'activation',
    component: ActivationPage,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router