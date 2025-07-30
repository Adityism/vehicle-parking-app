<template>
  <div class="dashboard-center">
    <div class="container mt-4">
      <h2>Parking Analytics</h2>
      <div v-if="loading" class="text-center my-4">
        <span>Loading analytics...</span>
      </div>
      <div v-else>
        <div class="row mb-4">
          <div class="col-md-4">
            <div class="card">
              <div class="card-body">
                <h5>Total Reservations</h5>
                <h3>{{ stats.total_reservations }}</h3>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card">
              <div class="card-body">
                <h5>Total Revenue</h5>
                <h3>₹{{ stats.total_revenue }}</h3>
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-6">
            <canvas id="revenueChart"></canvas>
          </div>
          <div class="col-md-6">
            <canvas id="lotChart"></canvas>
          </div>
        </div>
      </div>
      <router-link to="/admin/dashboard" class="btn btn-link mt-3">Back to Admin Dashboard</router-link>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'

export default {
  name: 'AdminAnalytics',
  setup() {
    const stats = ref({ total_reservations: 0, total_revenue: 0, lot_counts: [], spot_counts: [] })
    const loading = ref(true)

    const renderCharts = () => {
      // Bar chart for bookings per lot
      const lotLabels = stats.value.lot_counts.map(l => l.lot)
      const lotData = stats.value.lot_counts.map(l => l.count)
      new Chart(document.getElementById('lotChart'), {
        type: 'bar',
        data: {
          labels: lotLabels,
          datasets: [{ label: 'Bookings per Lot', data: lotData, backgroundColor: '#4caf50' }]
        },
        options: { responsive: true }
      })
      // Pie chart for bookings per spot
      // Uncomment if you want spot analytics
      // const spotLabels = stats.value.spot_counts.map(s => s.spot)
      // const spotData = stats.value.spot_counts.map(s => s.count)
      // new Chart(document.getElementById('spotChart'), {
      //   type: 'pie',
      //   data: {
      //     labels: spotLabels,
      //     datasets: [{ label: 'Bookings per Spot', data: spotData }]
      //   },
      //   options: { responsive: true }
      // })
      // Line chart for revenue over time (dummy, as backend does not provide time series)
      new Chart(document.getElementById('revenueChart'), {
        type: 'line',
        data: {
          labels: ['Start', 'Now'],
          datasets: [{ label: 'Revenue', data: [0, stats.value.total_revenue], borderColor: '#2196f3', fill: false }]
        },
        options: { responsive: true }
      })
    }

    onMounted(async () => {
      const res = await axios.get('/admin/stats')
      stats.value = res.data
      loading.value = false
      renderCharts()
    })

    return { stats, loading }
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
  max-width: 900px;
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
