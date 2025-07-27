<template>
  <div>
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
