<script setup>
import { ref } from 'vue'

const emit = defineEmits(['login-success'])

const isLogin = ref(true)
const username = ref('')
const password = ref('')
const message = ref('')
const loading = ref(false)

const toggleMode = () => {
  isLogin.value = !isLogin.value
  message.value = ''
  username.value = ''
  password.value = ''
}

const handleSubmit = async () => {
  if (!username.value || !password.value) {
    message.value = 'Please fill in all fields'
    return
  }

  loading.value = true
  message.value = ''

  try {
    let res, data
    
    if (isLogin.value) {
      // Login
      const params = new URLSearchParams()
      params.append('username', username.value)
      params.append('password', password.value)

      res = await fetch('/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: params
      })
    } else {
      // Register
      res = await fetch('/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: username.value,
          password: password.value
        })
      })
    }

    const contentType = res.headers.get("content-type");
    if (contentType && contentType.indexOf("application/json") !== -1) {
      data = await res.json()
    } else {
      const text = await res.text()
      throw new Error(`Server Error (${res.status}): ${text || res.statusText}`)
    }

    if (res.ok) {
      if (isLogin.value) {
        localStorage.setItem('token', data.access_token)
        emit('login-success', username.value)
      } else {
        message.value = 'Registration successful! Please login.'
        isLogin.value = true
        password.value = ''
      }
    } else {
      message.value = data.detail || 'Operation failed'
    }

  } catch (err) {
    console.error(err)
    message.value = err.message || 'Network error'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>{{ isLogin ? 'Welcome Back' : 'Create Account' }}</h2>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Username</label>
          <input type="text" v-model="username" required :disabled="loading" />
        </div>
        
        <div class="form-group">
          <label>Password</label>
          <input type="password" v-model="password" required :disabled="loading" />
        </div>
        
        <p v-if="message" class="message" :class="{ error: !message.includes('successful') }">{{ message }}</p>
        
        <button type="submit" :disabled="loading">
          {{ loading ? 'Please wait...' : (isLogin ? 'Login' : 'Register') }}
        </button>
      </form>
      
      <p class="switch-mode">
        {{ isLogin ? "Don't have an account?" : "Already have an account?" }}
        <a href="#" @click.prevent="toggleMode">{{ isLogin ? 'Register' : 'Login' }}</a>
      </p>
    </div>
  </div>
</template>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 50vh;
}

.auth-card {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  border: 1px solid #eee;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  font-family: var(--font-main);
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #666;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

button {
  width: 100%;
  padding: 12px;
  background: #000;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1rem;
}

button:disabled {
  background: #ccc;
}

.message {
  font-size: 0.9rem;
  margin-top: 0.5rem;
  text-align: center;
  color: green;
}

.message.error {
  color: red;
}

.switch-mode {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: #666;
}
</style>
