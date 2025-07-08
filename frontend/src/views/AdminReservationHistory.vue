<template>
  <div class="container mt-4">
    <h2>Admin Reservation History</h2>
    <div v-if="loading" class="text-center my-4">
      <span>Loading all reservations...</span>
    </div>
    <div v-else>
      <table class="table table-bordered table-striped">
        <thead>
          <tr>
            <th>User Email</th>
            <th>Lot</th>
            <th>Spot</th>
            <th>Parked At</th>
            <th>Left At</th>
            <th>Duration (min)</th>
            <th>Cost (₹)</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in reservations" :key="r.id">
            <td>{{ r.user_email }}</td>
            <td>{{ r.lot_name || '-' }}</td>
            <td>{{ r.spot_number || '-' }}</td>
            <td>{{ formatDate(r.parking_timestamp) }}</td>
            <td>{{ formatDate(r.leaving_timestamp) }}</td>
            <td>{{ r.duration_minutes }}</td>
            <td>{{ r.cost }}</td>
            <td>{{ r.status }}</td>
          </tr>
        </tbody>
      </table>
      <div v-if="reservations.length === 0" class="alert alert-info">No reservations found.</div>
    </div>
    <router-link to="/admin/dashboard" class="btn btn-link mt-3">Back to Admin Dashboard</router-link>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'AdminReservationHistory',
  setup() {
    const reservations = ref([])
    const loading = ref(true)

    const fetchReservations = async () => {
      loading.value = true
      try {
        const res = await axios.get('/admin/reservations')
        reservations.value = res.data
      } finally {
        loading.value = false
      }
    }

    const formatDate = (dt) => {
      if (!dt) return '-'
      return new Date(dt).toLocaleString()
    }

    onMounted(() => {
      fetchReservations()
    })

    return {
      reservations,
      loading,
      formatDate
    }
  }
}
</script>
