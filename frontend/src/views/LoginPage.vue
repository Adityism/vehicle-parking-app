<template>
  <div class="login-page d-flex justify-content-center align-items-center min-vh-100">
    <div class="form-container bg-white p-4 p-md-5 rounded shadow-lg">
      <h2 class="mb-5 text-center fw-bold h3">{{ isAdmin ? 'Admin Login' : 'User Login' }}</h2>
      
      <!-- Login Mode Toggle -->
      <div class="text-center mb-4">
        <div class="btn-group" role="group">
          <button 
            type="button" 
            class="btn" 
            :class="!isAdmin ? 'btn-primary' : 'btn-outline-primary'"
            @click="setLoginMode(false)"
          >
            User Login
          </button>
          <button 
            type="button" 
            class="btn" 
            :class="isAdmin ? 'btn-primary' : 'btn-outline-primary'"
            @click="setLoginMode(true)"
          >
            Admin Login
          </button>
        </div>
      </div>
      
      <form @submit.prevent="handleSubmit" class="login-form">
        <div class="form-group mb-4">
          <label for="email" class="d-block fw-medium mb-2">Email</label>
          <input 
            type="email" 
            id="email"
            v-model="email"
            required
            class="form-control form-control-lg"
            :class="{'is-invalid': emailError}"
            placeholder="e.g., admin@parking.com"
          />
          <div v-if="emailError" class="invalid-feedback">{{ emailError }}</div>
        </div>
        <div class="form-group mb-4">
          <label for="password" class="d-block fw-medium mb-2">Password</label>
          <input 
            type="password" 
            id="password"
            v-model="password"
            required
            class="form-control form-control-lg"
            :class="{'is-invalid': passwordError}"
            placeholder="••••••••"
          />
          <div v-if="passwordError" class="invalid-feedback">{{ passwordError }}</div>
        </div>
        
        <div class="error text-danger mb-3" v-if="error">{{ error }}</div>

        <button type="submit" class="btn btn-primary w-100 btn-lg mt-2">Login</button>
        
        <div v-if="!isAdmin" class="mt-4 text-center">
          <span class="text-muted">Don't have an account? </span>
          <router-link to="/register">Register here</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
// The script section is intentionally left unchanged to preserve all functionality.
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
    const emailError = ref('')
    const passwordError = ref('')
    const isAdminMode = ref(props.isAdmin)

    const setLoginMode = (adminMode) => {
      isAdminMode.value = adminMode
      // Update the route if needed
      if (adminMode && route.name !== 'AdminLogin') {
        router.push('/admin/login')
      } else if (!adminMode && route.name !== 'Login') {
        router.push('/login')
      }
    }

    const validate = () => {
      emailError.value = ''
      passwordError.value = ''
      let valid = true
      if (!email.value) {
        emailError.value = 'Email is required.'
        valid = false
      } else if (!/^\S+@\S+\.\S+$/.test(email.value)) {
        emailError.value = 'Enter a valid email.'
        valid = false
      }
      if (!password.value) {
        passwordError.value = 'Password is required.'
        valid = false
      }
      return valid
    }

    const handleSubmit = async () => {
      if (!validate()) return
      try {
        const user = await store.dispatch('login', {
          email: email.value,
          password: password.value
        })
        // Check if user is admin based on role
        if (user.role === 'admin') {
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
      handleSubmit,
      emailError,
      passwordError,
      isAdmin: isAdminMode,
      setLoginMode
    }
  }
}
</script>

<style scoped>
/* Modern UI enhancements */
.login-page {
  background-color: #f8f9fa;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  /* Override global app styles */
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.form-container {
  width: 100%;
  max-width: 420px;
  border: 1px solid #dee2e6;
  transition: all 0.3s ease;
}

@media (max-width: 576px) {
  .form-container {
    margin: 1rem;
    max-width: calc(100% - 2rem);
  }
}

@media (min-width: 768px) {
  .form-container:hover {
    transform: scale(1.02);
    box-shadow: 0 1rem 3rem rgba(0,0,0,.175)!important;
  }
}

.form-control-lg {
  padding: 0.8rem 1.1rem;
  font-size: 1rem;
  transition: border-color .15s ease-in-out, box-shadow .15s ease-in-out;
}

.form-control:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
  padding: 0.8rem 1rem;
  font-weight: 500;
  transition: all .2s ease-in-out;
}

.btn-primary:hover {
  background-color: #0b5ed7;
  border-color: #0a58ca;
  transform: translateY(-2px);
}

.btn-group .btn {
  border-radius: 0;
  transition: all .2s ease-in-out;
}

.btn-group .btn:first-child {
  border-top-left-radius: 0.375rem;
  border-bottom-left-radius: 0.375rem;
}

.btn-group .btn:last-child {
  border-top-right-radius: 0.375rem;
  border-bottom-right-radius: 0.375rem;
}

.btn-group .btn:hover {
  transform: translateY(-1px);
}

.form-container a {
  color: #0d6efd;
  text-decoration: none;
  font-weight: 500;
}

.form-container a:hover {
  text-decoration: underline;
}
</style>