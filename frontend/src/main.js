import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'

axios.defaults.baseURL = 'http://localhost:5009/api'

// Add request interceptor to ensure Authorization header is always set
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      console.log('Axios interceptor: Added Authorization header')
    } else {
      console.log('Axios interceptor: No token found')
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

if (localStorage.getItem('token')) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('token')}`
}

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js')
  })
}

const app = createApp(App)
app.use(router)
app.use(store)
app.mount('#app')