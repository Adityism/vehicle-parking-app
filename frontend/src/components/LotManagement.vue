<template>
  <div class="dashboard-center">
    <div class="container">
      <h2>Lot Management</h2>
      <button class="btn btn-primary mb-3" @click="showCreateModal = true">Create Lot</button>

      <table class="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Address</th>
            <th>Pincode</th>
            <th>Capacity</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lot in lots" :key="lot.id">
            <td>{{ lot.name }}</td>
            <td>{{ lot.address }}</td>
            <td>{{ lot.pincode }}</td>
            <td>{{ lot.capacity }}</td>
            <td>
              <button class="btn btn-sm btn-warning me-2" @click="editLot(lot)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="deleteLot(lot.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Create/Edit Modal -->
      <div class="modal" :class="{ 'd-block': showCreateModal || showEditModal }">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">{{ editingLot ? 'Edit Lot' : 'Create Lot' }}</h5>
              <button type="button" class="btn-close" @click="closeModal"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="saveLot">
                <div class="mb-3">
                  <label for="name" class="form-label">Name</label>
                  <input type="text" class="form-control" id="name" v-model="lotForm.name" required>
                </div>
                <div class="mb-3">
                  <label for="address" class="form-label">Address</label>
                  <input type="text" class="form-control" id="address" v-model="lotForm.address" required>
                </div>
                <div class="mb-3">
                  <label for="pincode" class="form-label">Pincode</label>
                  <input type="text" class="form-control" id="pincode" v-model="lotForm.pincode" required>
                </div>
                <div class="mb-3">
                  <label for="capacity" class="form-label">Capacity</label>
                  <input type="number" class="form-control" id="capacity" v-model.number="lotForm.capacity" required>
                </div>
                <button type="submit" class="btn btn-primary">Save</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import api from '../store/api'

export default {
  name: 'LotManagement',
  setup() {
    const lots = ref([])
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const editingLot = ref(null)
    const lotForm = ref({
      name: '',
      address: '',
      pincode: '',
      capacity: 0
    })

    const fetchLots = async () => {
      try {
        const response = await api.get('/admin/lots')
        lots.value = response.data
      } catch (error) {
        console.error('Error fetching lots:', error)
      }
    }

    const createLot = async () => {
      try {
        await api.post('/admin/lots', lotForm.value)
        fetchLots()
        closeModal()
      } catch (error) {
        console.error('Error creating lot:', error)
      }
    }

    const editLot = (lot) => {
      editingLot.value = lot
      lotForm.value = { ...lot }
      showEditModal.value = true
    }

    const updateLot = async () => {
      try {
        await api.put(`/admin/lots/${editingLot.value.id}`, lotForm.value)
        fetchLots()
        closeModal()
      } catch (error) {
        console.error('Error updating lot:', error)
      }
    }

    const deleteLot = async (id) => {
      try {
        await api.delete(`/admin/lots/${id}`)
        fetchLots()
        alert('Lot deleted successfully!')
      } catch (error) {
        const errorMessage = error.response?.data?.error || 'Error deleting lot.'
        alert(errorMessage)
        console.error('Error deleting lot:', error)
      }
    }

    const saveLot = () => {
      if (editingLot.value) {
        updateLot()
      } else {
        createLot()
      }
    }

    const closeModal = () => {
      showCreateModal.value = false
      showEditModal.value = false
      editingLot.value = null
      lotForm.value = {
        name: '',
        address: '',
        pincode: '',
        capacity: 0
      }
      document.body.classList.remove('modal-open');
    }

    // Watch for modal state changes to add/remove body class
    watch([showCreateModal, showEditModal], ([newCreate, newEdit]) => {
      if (newCreate || newEdit) {
        document.body.classList.add('modal-open');
      } else {
        document.body.classList.remove('modal-open');
      }
    });

    onMounted(fetchLots)

    return {
      lots,
      showCreateModal,
      showEditModal,
      editingLot,
      lotForm,
      createLot,
      editLot,
      updateLot,
      deleteLot,
      saveLot,
      closeModal
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

.btn {
  padding: 9px 20px;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  box-shadow: none;
  transition: background 0.2s, box-shadow 0.2s;
}

.btn:active {
  transform: scale(0.98);
}

.btn-primary {
  background: #007bff;
  border: none;
  color: #fff;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-warning {
  background: #ffc107;
  border: none;
  color: #212529;
}

.btn-warning:hover {
  background: #e0a800;
}

.btn-danger {
  background: #dc3545;
  border: none;
  color: #fff;
}

.btn-danger:hover {
  background: #c82333;
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

.form-label {
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #222;
}

.form-control {
  display: block;
  width: 100%;
  padding: 0.4rem 0.8rem;
  font-size: 1rem;
  line-height: 1.5;
  color: #495057;
  background-color: #fff;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  box-shadow: none;
  transition: border-color 0.15s;
}

.form-control:focus {
  border-color: #80bdff;
  outline: 0;
}

.mb-3 {
  margin-bottom: 1rem !important;
}

.me-2 {
  margin-right: 0.5rem !important;
}

/* Modal Enhancements */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.35);
  display: none;
  justify-content: center;
  align-items: center;
  z-index: 1050;
  animation: fadeInModal 0.5s ease;
}

@keyframes fadeInModal {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal.d-block {
  display: flex;
}

.modal-dialog {
  margin: auto;
  max-width: 500px;
  width: 95%;
}

.modal-content {
  border-radius: 0.7rem;
  box-shadow: 0 0.5rem 2rem rgba(0,0,0,0.18);
  background: #fff;
  animation: fadeInContainer 0.7s cubic-bezier(.4,0,.2,1);
}

.modal-header {
  border-bottom: 1.5px solid #dee2e6;
  padding: 1.2rem 1.2rem;
  background: #f8f9fa;
}

.modal-title {
  margin-bottom: 0;
  line-height: 1.5;
  font-size: 1.25rem;
  font-weight: 600;
  color: #343a40;
}

.btn-close {
  background: transparent;
  border: 0;
  opacity: 0.5;
  padding: 0.5rem 0.5rem;
  margin: -0.5rem -0.5rem -0.5rem auto;
  cursor: pointer;
  font-size: 1.3rem;
  transition: opacity 0.2s;
}

.btn-close:hover {
  opacity: 0.75;
}
</style>
