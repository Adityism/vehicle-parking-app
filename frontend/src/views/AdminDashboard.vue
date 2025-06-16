&lt;template>
  <div class="admin-dashboard">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
      <div class="container">
        <span class="navbar-brand">Admin Dashboard</span>
        <button @click="handleLogout" class="btn btn-outline-light">Logout</button>
      </div>
    </nav>
    
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card">
            <div class="card-body text-center">
              <h2>Welcome, {{ user.name }}!</h2>
              <p class="text-muted">You are logged in as an administrator.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

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

    return {
      user,
      handleLogout
    }
  }
}
</script>
