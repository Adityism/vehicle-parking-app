import axios from 'axios'

export default async function rehydrateUser(store) {
  const token = localStorage.getItem('token')
  if (token && !store.state.user) {
    try {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      await store.dispatch('getCurrentUser')
    } catch (e) {
      store.commit('logout')
    }
  }
}
