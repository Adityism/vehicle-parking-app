<template>
  <div class="container mt-4">
    <h2>Parking History</h2>
    <div v-if="loading" class="text-center my-4">
      <span>Loading history...</span>
    </div>
    <div v-else>
      <table class="table table-bordered table-striped">
        <thead>
          <tr>
            <th>Lot</th>
            <th>Spot</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Cost (₹)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in history" :key="r.id">
            <td>{{ r.lot_name || '-' }}</td>
            <td>{{ r.spot_number || '-' }}</td>
            <td>{{ formatDate(r.start_time) }}</td>
            <td>{{ formatDate(r.end_time) }}</td>
            <td>{{ r.total_cost }}</td>
          </tr>
        </tbody>
      </table>
      <div v-if="history.length === 0" class="alert alert-info">No past reservations found.</div>
    </div>
    <router-link to="/dashboard" class="btn btn-link mt-3">Back to Dashboard</router-link>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'ParkingHistory',
  setup() {
    const history = ref([])
    const loading = ref(true)

    const fetchHistory = async () => {
      loading.value = true
      try {
        const res = await axios.get('/reservations/history')
        history.value = res.data
      } finally {
        loading.value = false
      }
    }

    const formatDate = (dt) => {
      if (!dt) return '-'
      return new Date(dt).toLocaleString()
    }

    onMounted(() => {
      fetchHistory()
    })

    return {
      history,
      loading,
      formatDate
    }
  }
}
</script>
