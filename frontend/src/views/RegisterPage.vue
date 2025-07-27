<template>
  <div class="register-page d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <div class="form-container bg-white p-4 rounded shadow w-100" style="max-width: 400px;">
      <h2 class="mb-4 text-center">User Registration</h2>
      <form @submit.prevent="handleSubmit" class="register-form">
        <div class="form-group mb-3">
          <label for="name">Full Name:</label>
          <input 
            type="text" 
            id="name"
            v-model="name"
            required
            class="form-control"
            :class="{'is-invalid': nameError}"
          />
          <div v-if="nameError" class="invalid-feedback">{{ nameError }}</div>
        </div>
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
          <label for="phone">Phone:</label>
          <input 
            type="tel" 
            id="phone"
            v-model="phone"
            required
            class="form-control"
            :class="{'is-invalid': phoneError}"
          />
          <div v-if="phoneError" class="invalid-feedback">{{ phoneError }}</div>
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
        <button type="submit" class="btn btn-primary w-100">Register</button>
        <div class="mt-3 text-center">
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
    const nameError = ref('')
    const emailError = ref('')
    const phoneError = ref('')
    const passwordError = ref('')

    const validate = () => {
      nameError.value = ''
      emailError.value = ''
      phoneError.value = ''
      passwordError.value = ''
      let valid = true
      if (!name.value) {
        nameError.value = 'Name is required.'
        valid = false
      }
      if (!email.value) {
        emailError.value = 'Email is required.'
        valid = false
      } else if (!/^\S+@\S+\.\S+$/.test(email.value)) {
        emailError.value = 'Enter a valid email.'
        valid = false
      }
      if (!phone.value) {
        phoneError.value = 'Phone is required.'
        valid = false
      } else if (!/^\d{10}$/.test(phone.value)) {
        phoneError.value = 'Enter a valid 10-digit phone number.'
        valid = false
      }
      if (!password.value) {
        passwordError.value = 'Password is required.'
        valid = false
      } else if (password.value.length < 6) {
        passwordError.value = 'Password must be at least 6 characters.'
        valid = false
      }
      return valid
    }

    const handleSubmit = async () => {
      if (!validate()) return
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
      handleSubmit,
      nameError,
      emailError,
      phoneError,
      passwordError
    }
  }
}
</script>

<style scoped>
.register-page {
  background-color: #f5f5f5;
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
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
