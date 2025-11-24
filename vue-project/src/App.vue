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
      <h1>Kindle Online</h1>
    </header>

    <main>
      <BookUpload @upload-success="refreshList" />
      <BookList ref="bookListRef" />
    </main>
  </div>
</template>

<style>
/* Global Kindle Optimizations */
body {
  background-color: white !important;
  color: black !important;
  font-family: Georgia, serif; /* Serif is often better for reading on e-ink */
}

#app {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
  border-bottom: 2px solid black;
  padding-bottom: 0.5rem;
}

a {
  color: black;
  text-decoration: underline;
}
</style>
