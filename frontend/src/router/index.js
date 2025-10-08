import { createRouter, createWebHistory } from 'vue-router'
import ActivationPage from '../views/ActivationPage.vue'
import PasswordResetPage from '../views/PasswordResetPage.vue'

const routes = [
  {
    path: '/activate/:uid/:token',
    name: 'activation',
    component: ActivationPage,
    props: true
  },
  {
    path: '/password-reset',
    name: 'password-reset',
    component: PasswordResetPage
  },
  {
    path: '/password-reset-confirm/:uid/:token',
    name: 'password-reset-confirm',
    component: PasswordResetPage,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router