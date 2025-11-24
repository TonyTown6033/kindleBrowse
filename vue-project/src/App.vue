<script setup>
import BookUpload from './components/BookUpload.vue'
import BookList from './components/BookList.vue'
import { ref } from 'vue'

const bookListRef = ref(null)

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
    </header>

    <main>
      <BookUpload @upload-success="refreshList" />
      <BookList ref="bookListRef" />
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
