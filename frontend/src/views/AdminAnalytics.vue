<template>
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
