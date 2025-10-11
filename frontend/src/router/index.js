import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import LoginPage from '../views/LoginPage.vue'
import RegisterPage from '../views/RegisterPage.vue'
import ActivationPage from '../views/ActivationPage.vue'
import PasswordResetPage from '../views/PasswordResetPage.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage
  },
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