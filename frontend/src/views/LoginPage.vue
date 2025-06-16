&lt;template>
  <div class="login-page">
    <div class="form-container">
      <h2>{{ isAdmin ? 'Admin Login' : 'User Login' }}</h2>
      <form @submit.prevent="handleSubmit" class="login-form">
        <div class="form-group">
          <label for="email">Email:</label>
          <input 
            type="email" 
            id="email"
            v-model="email"
            required
            class="form-control"
          />
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input 
            type="password" 
            id="password"
            v-model="password"
            required
            class="form-control"
          />
        </div>
        <div class="error" v-if="error">{{ error }}</div>
        <button type="submit" class="btn btn-primary">Login</button>
        <div v-if="!isAdmin" class="mt-3">
          <router-link to="/register">Don't have an account? Register here</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'LoginPage',
  props: {
    isAdmin: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const store = useStore()
    const router = useRouter()
    const route = useRoute()

    const email = ref('')
    const password = ref('')
    const error = ref('')

    const handleSubmit = async () => {
      try {
        const user = await store.dispatch('login', {
          email: email.value,
          password: password.value
        })

        // Redirect based on user role
        if (user.is_admin) {
          router.push('/admin/dashboard')
        } else {
          router.push('/dashboard')
        }
      } catch (err) {
        error.value = err.toString()
      }
    }

    return {
      email,
      password,
      error,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.form-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 1rem;
}

.error {
  color: red;
  margin: 1rem 0;
}
</style>
