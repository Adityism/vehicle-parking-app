<template>
  <div class="user-dashboard">
    <nav class="navbar navbar-expand-lg navbar-dark bg-success mb-4">
      <div class="container">
        <span class="navbar-brand">User Dashboard</span>
        <button @click="handleLogout" class="btn btn-outline-light">Logout</button>
      </div>
    </nav>
    <div class="container">
      <ul class="nav nav-tabs mb-4" id="myTab" role="tablist">
        <li class="nav-item" role="presentation">
          <button class="nav-link active" id="dashboard-tab" data-bs-toggle="tab" data-bs-target="#dashboard" type="button" role="tab" aria-controls="dashboard" aria-selected="true">Dashboard</button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" id="book-spot-tab" data-bs-toggle="tab" data-bs-target="#book-spot" type="button" role="tab" aria-controls="book-spot" aria-selected="false">Book Spot</button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" id="history-tab" data-bs-toggle="tab" data-bs-target="#history" type="button" role="tab" aria-controls="history" aria-selected="false">History</button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" id="charts-tab" data-bs-toggle="tab" data-bs-target="#charts" type="button" role="tab" aria-controls="charts" aria-selected="false">Charts</button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" id="profile-tab" data-bs-toggle="tab" data-bs-target="#profile" type="button" role="tab" aria-controls="profile" aria-selected="false">Profile</button>
        </li>
      </ul>
      <div class="tab-content" id="myTabContent">
        <div class="tab-pane fade show active" id="dashboard" role="tabpanel" aria-labelledby="dashboard-tab">
          <div class="card">
            <div class="card-body text-center">
              <h2>Welcome, {{ user.name }}!</h2>
              <p class="text-muted">You are logged in as a user.</p>
              <p>Email: {{ user.email }}</p>
              <div v-if="activeReservation && activeReservation.active">
                <h4 class="mt-4">Active Reservation</h4>
                <p><strong>Lot:</strong> {{ activeReservation.reservation.lot_name || '-' }}</p>
                <p><strong>Spot:</strong> {{ activeReservation.reservation.spot_number || '-' }}</p>
                <p><strong>Start Time:</strong> {{ formatDate(activeReservation.reservation.parking_timestamp) }}</p>
                <button class="btn btn-danger mt-2" @click="releaseSpot" :disabled="releasing">Release Spot</button>
              </div>
              <div v-else>
                <p class="mt-4">No active reservation.</p>
              </div>
            </div>
          </div>
        </div>
        <div class="tab-pane fade" id="book-spot" role="tabpanel" aria-labelledby="book-spot-tab">
          <!-- Book Spot Content -->
          <div class="card">
            <div class="card-body">
              <h3>Book a Parking Spot</h3>
              <div v-if="loadingLots" class="text-center my-4">
                <span>Loading lots...</span>
              </div>
              <div v-else>
                <div v-if="lots.length === 0" class="alert alert-info">No lots with available spots.</div>
                <div class="row">
                  <div class="col-md-6 mb-4" v-for="lot in lots" :key="lot.id">
                    <div class="card">
                      <div class="card-body">
                        <h5 class="card-title">{{ lot.name }}</h5>
                        <p class="card-text">Address: {{ lot.address }}</p>
                        <p class="card-text">Price: ₹{{ lot.rate_per_hour }}/hr</p>
                        <p class="card-text">Available Spots: {{ lot.available_spots }}</p>
                        <input v-model="vehicleNumber" class="form-control mb-2" placeholder="Enter Vehicle Number" />
                        <button class="btn btn-success" :disabled="booking || lot.available_spots === 0" @click="bookSpot(lot)">Book Spot</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="tab-pane fade" id="history" role="tabpanel" aria-labelledby="history-tab">
          <!-- Parking History Content -->
          <div class="card">
            <div class="card-body">
              <h3>Parking History</h3>
              <button class="btn btn-primary mb-3" @click="exportHistory">Export as CSV</button>
              <table class="table table-striped">
                <thead>
                  <tr>
                    <th>Lot Name</th>
                    <th>Spot Number</th>
                    <th>Vehicle</th>
                    <th>Parked At</th>
                    <th>Left At</th>
                    <th>Duration (min)</th>
                    <th>Cost (₹)</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="res in parkingHistory" :key="res.id">
                    <td>{{ res.lot_name || '-' }}</td>
                    <td>{{ res.spot_number || '-' }}</td>
                    <td>{{ res.vehicle_number }}</td>
                    <td>{{ formatDate(res.parking_timestamp) }}</td>
                    <td>{{ formatDate(res.leaving_timestamp) }}</td>
                    <td>{{ res.duration_minutes }}</td>
                    <td>{{ res.cost }}</td>
                    <td>{{ res.status }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="tab-pane fade" id="charts" role="tabpanel" aria-labelledby="charts-tab">
          <!-- Charts Content -->
          <div class="card">
            <div class="card-body">
              <h3>Monthly Summary Charts</h3>
              <div class="row">
                <div class="col-md-6">
                  <canvas id="totalSpentChart"></canvas>
                </div>
                <div class="col-md-6">
                  <canvas id="totalHoursChart"></canvas>
                </div>
                <div class="col-md-6">
                  <canvas id="bookingsPerMonthChart"></canvas>
                </div>
                <div class="col-md-6">
                  <canvas id="mostVisitedLotsChart"></canvas>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="tab-pane fade" id="profile" role="tabpanel" aria-labelledby="profile-tab">
          <!-- Profile Settings Content -->
          <div class="card">
            <div class="card-body">
              <h3>Profile Settings</h3>
              <p><strong>Name:</strong> {{ user.name }}</p>
              <p><strong>Email:</strong> {{ user.email }}</p>
              <!-- Add password change form here -->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import api from '../store/api'
import Chart from 'chart.js/auto'

export default {
  name: 'UserDashboard',
  setup() {
    const store = useStore()
    const router = useRouter()
    const user = computed(() => store.state.user)
    const activeReservation = ref(null)
    const releasing = ref(false)
    const lots = ref([])
    const loadingLots = ref(true)
    const booking = ref(false)
    const vehicleNumber = ref('')
    const parkingHistory = ref([])
    const totalSpentChart = ref(null)
    const totalHoursChart = ref(null)
    const bookingsPerMonthChart = ref(null)
    const mostVisitedLotsChart = ref(null)

    const fetchActiveReservation = async () => {
      try {
        const res = await api.get('/reservations/active')
        activeReservation.value = res.data
      } catch (e) {
        console.error('Error fetching active reservation:', e)
        activeReservation.value = null
      }
    }

    const releaseSpot = async () => {
      if (!activeReservation.value?.reservation?.id) return
      releasing.value = true
      try {
        await api.post('/reservations/release', { reservation_id: activeReservation.value.reservation.id })
        alert('Spot released!')
        await fetchActiveReservation()
        await fetchParkingHistory()
        await fetchSummaryData()
      } catch (e) {
        alert(e.response?.data?.error || 'Release failed')
      } finally {
        releasing.value = false
      }
    }

    const fetchLots = async () => {
      loadingLots.value = true
      try {
        const res = await api.get('/reservations/lots')
        lots.value = res.data.filter(lot => lot.available_spots > 0)
      } catch (e) {
        console.error('Error fetching lots:', e)
      } finally {
        loadingLots.value = false
      }
    }

    const bookSpot = async (lot) => {
      if (!vehicleNumber.value) {
        alert('Please enter your vehicle number.')
        return
      }
      booking.value = true
      try {
        await api.post('/reservations/book', { lot_id: lot.id, vehicle_number: vehicleNumber.value })
        alert('Spot booked!')
        vehicleNumber.value = ''
        await fetchActiveReservation()
        await fetchLots()
      } catch (e) {
        alert(e.response?.data?.error || 'Booking failed')
      } finally {
        booking.value = false
      }
    }

    const fetchParkingHistory = async () => {
      try {
        const res = await api.get('/reservations/history')
        parkingHistory.value = res.data
      } catch (e) {
        console.error('Error fetching parking history:', e)
      }
    }

    const exportHistory = async () => {
      try {
        await api.post('/reservations/export')
        alert('Parking history export started. You will receive an email with the CSV file.')
      } catch (e) {
        alert(e.response?.data?.error || 'Export failed')
      }
    }

    const fetchSummaryData = async () => {
      try {
        const res = await api.get('/reservations/summary')
        const summary = res.data

        // Destroy existing charts if they exist
        if (totalSpentChart.value) totalSpentChart.value.destroy()
        if (totalHoursChart.value) totalHoursChart.value.destroy()
        if (bookingsPerMonthChart.value) bookingsPerMonthChart.value.destroy()
        if (mostVisitedLotsChart.value) mostVisitedLotsChart.value.destroy()

        nextTick(() => {
          // Total Amount Spent
          const totalSpentCtx = document.getElementById('totalSpentChart')
          if (totalSpentCtx) {
            totalSpentChart.value = new Chart(totalSpentCtx, {
              type: 'bar',
              data: {
                labels: ['Total Spent'],
                datasets: [{
                  label: 'Amount (₹)',
                  data: [summary.total_spent],
                  backgroundColor: 'rgba(75, 192, 192, 0.6)'
                }]
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                  y: { beginAtZero: true }
                }
              }
            })
          }

          // Total Hours Parked
          const totalHoursCtx = document.getElementById('totalHoursChart')
          if (totalHoursCtx) {
            totalHoursChart.value = new Chart(totalHoursCtx, {
              type: 'bar',
              data: {
                labels: ['Total Hours'],
                datasets: [{
                  label: 'Hours',
                  data: [summary.total_hours],
                  backgroundColor: 'rgba(153, 102, 255, 0.6)'
                }]
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                  y: { beginAtZero: true }
                }
              }
            })
          }

          // Bookings Per Month
          const bookingsPerMonthCtx = document.getElementById('bookingsPerMonthChart')
          if (bookingsPerMonthCtx) {
            bookingsPerMonthChart.value = new Chart(bookingsPerMonthCtx, {
              type: 'line',
              data: {
                labels: Object.keys(summary.bookings_per_month),
                datasets: [{
                  label: 'Bookings',
                  data: Object.values(summary.bookings_per_month),
                  borderColor: 'rgba(255, 159, 64, 0.6)',
                  fill: false
                }]
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                  y: { beginAtZero: true }
                }
              }
            })
          }

          // Most Visited Lots
          const mostVisitedLotsCtx = document.getElementById('mostVisitedLotsChart')
          if (mostVisitedLotsCtx) {
            mostVisitedLotsChart.value = new Chart(mostVisitedLotsCtx, {
              type: 'pie',
              data: {
                labels: Object.keys(summary.most_visited_lots),
                datasets: [{
                  label: 'Visits',
                  data: Object.values(summary.most_visited_lots),
                  backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966CC'
                  ]
                }]
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,
              }
            })
          }
        })
      } catch (e) {
        console.error('Error fetching summary data:', e)
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
      fetchLots()
      fetchParkingHistory()
      fetchSummaryData()
    })

    return {
      user,
      activeReservation,
      releasing,
      lots,
      loadingLots,
      booking,
      vehicleNumber,
      parkingHistory,
      handleLogout,
      releaseSpot,
      bookSpot,
      exportHistory,
      formatDate
    }
  }
}
</script>

<style scoped>
.user-dashboard {
  /* Override global app styles */
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  z-index: 1000;
  background-color: #f8f9fa;
}
</style>
