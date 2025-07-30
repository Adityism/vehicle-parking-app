<template>
  <div class="dashboard-center">
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

<style scoped>
.dashboard-center {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  z-index: 1000;
  background: #f8f9fa;
  padding-top: 40px;
}

.container {
  padding: 32px 32px 24px 32px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  max-width: 1100px;
  width: 100%;
  margin-bottom: 40px;
}

h2 {
  font-size: 2rem;
  font-weight: 600;
  color: #222;
  margin-bottom: 18px;
  letter-spacing: 0.5px;
}

.table {
  margin-top: 24px;
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 8px;
  overflow: hidden;
  background: #f8f9fa;
  font-size: 1rem;
}

.table thead th {
  background: #007bff;
  color: #fff;
  padding: 14px 16px;
  text-align: left;
  font-size: 1rem;
  font-weight: 500;
  border: none;
}

.table tbody tr {
  border-bottom: 1px solid #e3e6f3;
}

.table tbody tr:hover {
  background: #e3e6f3;
}

.table tbody tr:nth-of-type(even) {
  background: #f3f3f3;
}

.table tbody tr:last-of-type {
  border-bottom: 2px solid #007bff;
}

.table tbody td {
  padding: 12px 16px;
  font-size: 1rem;
}
</style>
