import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

// Views
import LoginPage from '../views/LoginPage.vue'
import RegisterPage from '../views/RegisterPage.vue'
import UserDashboard from '../views/UserDashboard.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import FindParking from '../views/FindParking.vue'
import ParkingHistory from '../views/ParkingHistory.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: LoginPage,
    props: { isAdmin: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage
  },
  {
    path: '/dashboard',
    name: 'UserDashboard',
    component: UserDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/find-parking',
    name: 'FindParking',
    component: FindParking,
    meta: { requiresAuth: true }
  },
  {
    path: '/parking-history',
    name: 'ParkingHistory',
    component: ParkingHistory,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    const isAuthenticated = store.getters.isAuthenticated
    const isAdmin = store.getters.isAdmin

    if (!isAuthenticated) {
      next('/login')
      return
    }

    if (to.meta.requiresAdmin && !isAdmin) {
      next('/dashboard')
      return
    }
  }

  // If trying to access login/register while already authenticated
  if ((to.name === 'Login' || to.name === 'Register' || to.name === 'AdminLogin') && store.getters.isAuthenticated) {
    const isAdmin = store.getters.isAdmin
    next(isAdmin ? '/admin/dashboard' : '/dashboard')
    return
  }

  next()
})

export default router
