import { createStore } from 'vuex'
import axios from 'axios'

const API_URL = 'http://localhost:5000/api'

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
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      } else {
        localStorage.removeItem('token')
        delete axios.defaults.headers.common['Authorization']
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
      delete axios.defaults.headers.common['Authorization']
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await axios.post(`${API_URL}/auth/login`, credentials)
        const { user, access_token } = response.data
        commit('setUser', user)
        commit('setToken', access_token)
        return user
      } catch (error) {
        throw error.response?.data?.message || 'Login failed'
      }
    },
    async register({ commit }, userData) {
      try {
        const response = await axios.post(`${API_URL}/auth/register`, userData)
        const { user, access_token } = response.data
        commit('setUser', user)
        commit('setToken', access_token)
        return user
      } catch (error) {
        throw error.response?.data?.message || 'Registration failed'
      }
    },
    async getCurrentUser({ commit, state }) {
      if (!state.token) return null
      try {
        const response = await axios.get(`${API_URL}/auth/me`)
        commit('setUser', response.data)
        return response.data
      } catch (error) {
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
