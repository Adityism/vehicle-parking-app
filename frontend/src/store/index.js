import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    user: null,
    token: localStorage.getItem('token') || null,
    activeReservation: null
  },
  mutations: {
    setUser(state, user) {
      state.user = user
    },
    setToken(state, token) {
      state.token = token
      if (token) {
        localStorage.setItem('token', token)
        // The axios interceptor will handle setting the header
        console.log('Token set in store:', token)
      } else {
        localStorage.removeItem('token')
        console.log('Token removed from store')
      }
    },
    setActiveReservation(state, reservation) {
      state.activeReservation = reservation
    },
    logout(state) {
      state.user = null
      state.token = null
      state.activeReservation = null
      localStorage.removeItem('token')
      console.log('Logged out, token removed')
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await axios.post('/auth/login', credentials)
        const { user, access_token } = response.data
        console.log('Login successful:', { user, access_token })
        console.log('Setting token in store...')
        commit('setUser', user)
        commit('setToken', access_token)
        console.log('Current axios headers after login:', axios.defaults.headers.common)
        return user
      } catch (error) {
        console.error('Login failed:', error)
        throw error.response?.data?.message || 'Login failed'
      }
    },
    async register({ commit }, userData) {
      try {
        const response = await axios.post('/auth/register', userData)
        const { user, access_token } = response.data
        commit('setUser', user)
        commit('setToken', access_token)
        return user
      } catch (error) {
        throw error.response?.data?.message || 'Registration failed'
      }
    },
    async getCurrentUser({ commit, state }) {
      if (!state.token) {
        console.log('No token available for getCurrentUser')
        return null
      }
      try {
        console.log('Calling getCurrentUser with token:', state.token)
        console.log('Current axios headers:', axios.defaults.headers.common)
        const response = await axios.get('/auth/me')
        console.log('getCurrentUser response:', response.data)
        commit('setUser', response.data)
        return response.data
      } catch (error) {
        console.error('getCurrentUser failed:', error.response?.data || error)
        console.error('Response status:', error.response?.status)
        console.error('Response headers:', error.response?.headers)
        commit('logout')
        throw error.response?.data?.message || 'Failed to get user info'
      }
    },
    async fetchActiveReservation({ commit }) {
      try {
        const res = await axios.get('/reservations/active')
        commit('setActiveReservation', res.data)
        return res.data
      } catch {
        commit('setActiveReservation', null)
        return null
      }
    }
  },
  getters: {
    isAdmin: state => state.user?.role === 'admin',
    isAuthenticated: state => !!state.user,
    currentUser: state => state.user,
    activeReservation: state => state.activeReservation
  }
})
