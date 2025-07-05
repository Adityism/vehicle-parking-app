&lt;template>
  <div class="user-dashboard">
    <nav class="navbar navbar-expand-lg navbar-dark bg-success mb-4">
      <div class="container">
        <span class="navbar-brand">User Dashboard</span>
        <button @click="handleLogout" class="btn btn-outline-light">Logout</button>
      </div>
    </nav>
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card">
            <div class="card-body text-center">
              <h2>Welcome, {{ user.name }}!</h2>
              <p class="text-muted">You are logged in as a user.</p>
              <div v-if="activeReservation && activeReservation.active">
                <h4 class="mt-4">Active Reservation</h4>
                <p><strong>Lot:</strong> {{ activeReservation.reservation.lot_name || '-' }}</p>
                <p><strong>Spot:</strong> {{ activeReservation.reservation.spot_number || '-' }}</p>
                <p><strong>Start Time:</strong> {{ formatDate(activeReservation.reservation.start_time) }}</p>
                <button class="btn btn-danger mt-2" @click="releaseSpot" :disabled="releasing">Release Spot</button>
              </div>
              <div v-else>
                <p class="mt-4">No active reservation.</p>
                <router-link to="/find-parking" class="btn btn-primary">Find Parking</router-link>
              </div>
              <router-link to="/parking-history" class="btn btn-link mt-3">View Parking History</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'UserDashboard',
  setup() {
    const store = useStore()
    const router = useRouter()
    const user = computed(() => store.state.user)
    const activeReservation = ref(null)
    const releasing = ref(false)

    const fetchActiveReservation = async () => {
      try {
        const res = await axios.get('/reservations/active')
        activeReservation.value = res.data
      } catch (e) {
        activeReservation.value = null
      }
    }

    const releaseSpot = async () => {
      if (!activeReservation.value?.reservation?.id) return
      releasing.value = true
      try {
        await axios.post('/reservations/release', { reservation_id: activeReservation.value.reservation.id })
        await fetchActiveReservation()
      } finally {
        releasing.value = false
      }
    }

    const handleLogout = () => {
      store.commit('logout')
      router.push('/login')
    }

    const formatDate = (dt) => {
      if (!dt) return '-'
      return new Date(dt).toLocaleString()
    }

    onMounted(() => {
      fetchActiveReservation()
    })

    return {
      user,
      activeReservation,
      releasing,
      handleLogout,
      releaseSpot,
      formatDate
    }
  }
}
</script>
