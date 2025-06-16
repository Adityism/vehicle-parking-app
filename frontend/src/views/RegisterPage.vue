&lt;template>
  <div class="register-page">
    <div class="form-container">
      <h2>User Registration</h2>
      <form @submit.prevent="handleSubmit" class="register-form">
        <div class="form-group">
          <label for="name">Full Name:</label>
          <input 
            type="text" 
            id="name"
            v-model="name"
            required
            class="form-control"
          />
        </div>
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
          <label for="phone">Phone:</label>
          <input 
            type="tel" 
            id="phone"
            v-model="phone"
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
        <button type="submit" class="btn btn-primary">Register</button>
        <div class="mt-3">
          <router-link to="/login">Already have an account? Login here</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'RegisterPage',
  setup() {
    const store = useStore()
    const router = useRouter()

    const name = ref('')
    const email = ref('')
    const phone = ref('')
    const password = ref('')
    const error = ref('')

    const handleSubmit = async () => {
      try {
        await store.dispatch('register', {
          name: name.value,
          email: email.value,
          phone: phone.value,
          password: password.value
        })
        router.push('/dashboard')
      } catch (err) {
        error.value = err.toString()
      }
    }

    return {
      name,
      email,
      phone,
      password,
      error,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.register-page {
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
