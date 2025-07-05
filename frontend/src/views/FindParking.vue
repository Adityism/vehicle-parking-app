<template>
  <div class="container mt-4">
    <h2>Find Parking</h2>
    <div v-if="loading" class="text-center my-4">
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
              <p class="card-text">Price: ₹{{ lot.spots.length > 0 ? lot.spots[0].rate_per_hour : lot.rate_per_hour }}/hr</p>
              <p class="card-text">Available Spots: {{ lot.available_spots }}</p>
              <input v-model="vehicleNumber" class="form-control mb-2" placeholder="Enter Vehicle Number" />
              <button class="btn btn-success" :disabled="booking || lot.available_spots === 0" @click="bookSpot(lot)">Book Spot</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <router-link to="/dashboard" class="btn btn-link mt-3">Back to Dashboard</router-link>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

export default {
  name: 'FindParking',
  setup() {
    const lots = ref([])
    const loading = ref(true)
    const booking = ref(false)
    const vehicleNumber = ref('')
    const router = useRouter()

    const fetchLots = async () => {
      loading.value = true
      try {
        const res = await axios.get('/admin/lots')
        lots.value = res.data.filter(lot => lot.available_spots > 0)
      } finally {
        loading.value = false
      }
    }

    const bookSpot = async (lot) => {
      if (!vehicleNumber.value) {
        alert('Please enter your vehicle number.')
        return
      }
      booking.value = true
      try {
        await axios.post('/reservations/book', { lot_id: lot.id, vehicle_number: vehicleNumber.value })
        alert('Spot booked!')
        router.push('/dashboard')
      } catch (e) {
        alert(e.response?.data?.error || 'Booking failed')
      } finally {
        booking.value = false
      }
    }

    onMounted(() => {
      fetchLots()
    })

    return {
      lots,
      loading,
      booking,
      vehicleNumber,
      bookSpot
    }
  }
}
</script>
