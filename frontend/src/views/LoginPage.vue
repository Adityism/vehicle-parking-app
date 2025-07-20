<template>
  <div class="login-page d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <div class="form-container bg-white p-4 rounded shadow w-100" style="max-width: 400px;">
      <h2 class="mb-4 text-center">{{ isAdmin ? 'Admin Login' : 'User Login' }}</h2>
      <form @submit.prevent="handleSubmit" class="login-form">
        <div class="form-group mb-3">
          <label for="email">Email:</label>
          <input 
            type="email" 
            id="email"
            v-model="email"
            required
            class="form-control"
            :class="{'is-invalid': emailError}"
          />
          <div v-if="emailError" class="invalid-feedback">{{ emailError }}</div>
        </div>
        <div class="form-group mb-3">
          <label for="password">Password:</label>
          <input 
            type="password" 
            id="password"
            v-model="password"
            required
            class="form-control"
            :class="{'is-invalid': passwordError}"
          />
          <div v-if="passwordError" class="invalid-feedback">{{ passwordError }}</div>
        </div>
        <div class="error text-danger mb-2" v-if="error">{{ error }}</div>
        <button type="submit" class="btn btn-primary w-100">Login</button>
        <div v-if="!isAdmin" class="mt-3 text-center">
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
    const emailError = ref('')
    const passwordError = ref('')

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
      handleSubmit,
      emailError,
      passwordError
    }
  }
}
</script>

<style scoped>
.login-page {
  background-color: #f5f5f5;
}
.form-container {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
