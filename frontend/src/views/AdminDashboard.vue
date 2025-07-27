<template>
  <div class="admin-dashboard">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
      <div class="container">
        <span class="navbar-brand">Admin Dashboard</span>
        <button @click="handleLogout" class="btn btn-outline-light">Logout</button>
      </div>
    </nav>
    
    <div class="container">
      <h2 class="text-center mb-4">Welcome, {{ user.name }}!</h2>
      <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
        <div class="col">
          <div class="card h-100 admin-card" @click="navigateTo('/admin/lot-management')">
            <div class="card-body text-center">
              <i class="bi bi-p-square-fill card-icon"></i>
              <h5 class="card-title">Lot Management</h5>
              <p class="card-text">Create, edit, and delete parking lots.</p>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card h-100 admin-card" @click="navigateTo('/admin/user-management')">
            <div class="card-body text-center">
              <i class="bi bi-people-fill card-icon"></i>
              <h5 class="card-title">User Management</h5>
              <p class="card-text">View and manage registered users.</p>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card h-100 admin-card" @click="navigateTo('/admin/spot-management')">
            <div class="card-body text-center">
              <i class="bi bi-geo-alt-fill card-icon"></i>
              <h5 class="card-title">Spot Management</h5>
              <p class="card-text">Monitor status of all parking spots.</p>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card h-100 admin-card">
            <div class="card-body">
              <h5 class="card-title text-center">Parking Occupancy</h5>
              <p class="card-text text-center">Occupied vs. Available Spots</p>
              <canvas id="occupancyChart"></canvas>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card h-100 admin-card">
            <div class="card-body">
              <h5 class="card-title text-center">Lot-wise Spot Distribution</h5>
              <p class="card-text text-center">Number of Spots in Each Lot</p>
              <canvas id="spotDistributionChart"></canvas>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card h-100 admin-card">
            <div class="card-body">
              <h5 class="card-title text-center">Reservations Trend</h5>
              <p class="card-text text-center">Reservation Activity (Last 7 Days)</p>
              <canvas id="reservationsTrendChart"></canvas>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card h-100 admin-card" @click="navigateTo('/admin/reservations')">
            <div class="card-body text-center">
              <i class="bi bi-journal-check card-icon"></i>
              <h5 class="card-title">Reservations</h5>
              <p class="card-text">View all parking reservations.</p>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card h-100 admin-card" @click="navigateTo('/admin/analytics')">
            <div class="card-body text-center">
              <i class="bi bi-graph-up card-icon"></i>
              <h5 class="card-title">Analytics</h5>
              <p class="card-text">Access detailed analytics reports.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import Chart from 'chart.js/auto';
import axios from 'axios';

export default {
  name: 'AdminDashboard',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const user = computed(() => store.state.user)

    const handleLogout = () => {
      store.commit('logout')
      router.push('/admin/login')
    }

    const navigateTo = (route) => {
      router.push(route)
    }

    onMounted(async () => {
      try {
        const token = localStorage.getItem('token');
                const response = await axios.get('http://localhost:5009/api/admin/stats', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        const stats = response.data;

        // Parking Occupancy Chart
        const occupied = stats.occupied_spots;
        const available = stats.total_spots - stats.occupied_spots;
        const occupancyData = {
          labels: ['Occupied', 'Available'],
          datasets: [{
            data: [occupied, available],
            backgroundColor: ['#FF6384', '#36A2EB'],
            hoverOffset: 4
          }]
        };

        new Chart(
          document.getElementById('occupancyChart'),
          {
            type: 'pie',
            data: occupancyData,
            options: {
              responsive: true,
              plugins: {
                legend: {
                  position: 'top',
                },
                title: {
                  display: false,
                  text: 'Parking Occupancy'
                }
              }
            },
          }
        );

        // Lot-wise Spot Distribution Chart
        const lotNames = stats.lot_spot_distribution.map(lot => lot.lot);
        const lotCounts = stats.lot_spot_distribution.map(lot => lot.count);
        const spotDistributionData = {
          labels: lotNames,
          datasets: [{
            label: 'Number of Spots',
            data: lotCounts,
            backgroundColor: [
              '#4BC0C0',
              '#FFCD56',
              '#FF9F40',
              '#9966FF',
              '#FF6384',
              '#36A2EB'
            ],
            borderColor: [
              '#4BC0C0',
              '#FFCD56',
              '#FF9F40',
              '#9966FF',
              '#FF6384',
              '#36A2EB'
            ],
            borderWidth: 1
          }]
        };

        new Chart(
          document.getElementById('spotDistributionChart'),
          {
            type: 'bar',
            data: spotDistributionData,
            options: {
              responsive: true,
              plugins: {
                legend: {
                  display: false,
                },
                title: {
                  display: false,
                  text: 'Lot-wise Spot Distribution'
                }
              },
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            },
          }
        );

        // Reservations Trend Chart
        const trendDates = stats.reservations_last_7_days.map(item => item.date);
        const trendCounts = stats.reservations_last_7_days.map(item => item.count);
        const reservationsTrendData = {
          labels: trendDates,
          datasets: [{
            label: 'Reservations',
            data: trendCounts,
            fill: false,
            borderColor: '#007bff',
            tension: 0.1
          }]
        };

        new Chart(
          document.getElementById('reservationsTrendChart'),
          {
            type: 'line',
            data: reservationsTrendData,
            options: {
              responsive: true,
              plugins: {
                legend: {
                  display: false,
                },
                title: {
                  display: false,
                  text: 'Reservations Trend'
                }
              },
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            },
          }
        );

      } catch (error) {
        console.error('Error fetching admin stats:', error);
      }
    });

    return {
      user,
      handleLogout,
      navigateTo
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
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
  overflow-y: auto; /* Enable scrolling for content */
}

.admin-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.admin-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 15px;
  color: #007bff; /* Bootstrap primary color */
}

.card-icon-lg {
  font-size: 4rem;
  opacity: 0.7;
}

.card-title {
  font-weight: bold;
  color: #333;
}

.card-text {
  color: #666;
}

/* Styles for chart cards */
.admin-card .card-body canvas {
  max-height: 250px; /* Adjust as needed */
}
</style>
