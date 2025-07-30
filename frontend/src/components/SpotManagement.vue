<template>
  <div class="dashboard-center">
    <div class="container">
      <h2>All Parking Spots</h2>
      <table class="table">
        <thead>
          <tr>
            <th>Spot Number</th>
            <th>Parking Lot</th>
            <th>Status</th>
            <th>Vehicle Number</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="spot in spots" :key="spot.id">
            <td>{{ spot.spot_number }}</td>
            <td>{{ spot.parking_lot_id }}</td>
            <td>{{ spot.is_occupied ? 'Occupied' : 'Available' }}</td>
            <td>{{ spot.vehicle_number || 'N/A' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../store/api'

export default {
  name: 'SpotManagement',
  setup() {
    const spots = ref([])

    const fetchSpots = async () => {
      try {
        const response = await api.get('/admin/spots/available')
        spots.value = response.data
      } catch (error) {
        console.error('Error fetching spots:', error)
      }
    }

    onMounted(fetchSpots)

    return {
      spots
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
