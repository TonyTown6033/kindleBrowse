<script setup>
import BookUpload from './components/BookUpload.vue'
import BookList from './components/BookList.vue'
import Auth from './components/Auth.vue'
import { ref, onMounted } from 'vue'

const bookListRef = ref(null)
const isAuthenticated = ref(false)
const currentUsername = ref('')

onMounted(() => {
  const token = localStorage.getItem('token')
  if (token) {
    // Optionally verify token valid here
    isAuthenticated.value = true
  }
})

const handleLoginSuccess = (username) => {
  isAuthenticated.value = true
  currentUsername.value = username
}

const logout = () => {
  localStorage.removeItem('token')
  isAuthenticated.value = false
  currentUsername.value = ''
}

const refreshList = () => {
  if (bookListRef.value) {
    bookListRef.value.fetchBooks()
  }
}
</script>

<template>
  <div class="app-container">
    <header>
      <div class="logo-area">
        <h1>Kindle Online</h1>
        <p class="subtitle">Your Personal E-book Cloud</p>
      </div>
      
      <div v-if="isAuthenticated" class="user-controls">
        <span>Hello, User</span>
        <button @click="logout" class="logout-btn">Logout</button>
      </div>
    </header>

    <main v-if="isAuthenticated">
      <BookUpload @upload-success="refreshList" />
      <BookList ref="bookListRef" />
    </main>
    
    <main v-else>
      <Auth @login-success="handleLoginSuccess" />
    </main>
    
    <footer>
      <p>&copy; {{ new Date().getFullYear() }} Kindle Online</p>
    </footer>
  </div>
</template>

<style>
/* Global Layout */
body {
  background-color: white !important;
  color: black !important;
}

#app {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px 20px 40px;
}

header {
  margin-bottom: 3rem;
  text-align: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 2rem;
  position: relative;
}

.user-controls {
  position: absolute;
  top: 0;
  right: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  font-size: 0.9rem;
}

.logout-btn {
  background: none;
  border: none;
  text-decoration: underline;
  cursor: pointer;
  padding: 0;
  margin-top: 5px;
  font-size: 0.8rem;
  color: #666;
}

h1 {
  font-size: 2.5rem;
  font-weight: normal;
  margin-bottom: 0.5rem;
  letter-spacing: -0.5px;
}

.subtitle {
  font-family: var(--font-ui);
  color: #666;
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

main {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

footer {
  margin-top: 4rem;
  text-align: center;
  font-size: 0.8rem;
  color: #999;
  font-family: var(--font-ui);
}

a {
  color: black;
  text-decoration: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 3px;
}

a:hover {
  color: #444;
}
</style>
