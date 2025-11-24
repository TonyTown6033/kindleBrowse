<script setup>
import { ref, onMounted } from 'vue'

const books = ref([])
const loading = ref(false)

const fetchBooks = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/books')
    if (response.ok) {
      books.value = await response.json()
    }
  } catch (error) {
    console.error('Failed to fetch books:', error)
  } finally {
    loading.value = false
  }
}

// Expose fetchBooks so parent can call it
defineExpose({ fetchBooks })

onMounted(() => {
  fetchBooks()
})
</script>

<template>
  <div class="book-list">
    <h3>Library</h3>
    <div v-if="loading">Loading...</div>
    <div v-else-if="books.length === 0">No books found.</div>
    <ul v-else class="list">
      <li v-for="book in books" :key="book.name" class="book-item">
        <div class="book-info">
          <span class="book-name">{{ book.name }}</span>
          <span class="book-size">{{ (book.size / 1024 / 1024).toFixed(2) }} MB</span>
        </div>
        <a :href="book.url" class="download-btn" download>Download</a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.book-list {
  margin-top: 1rem;
}

.list {
  list-style: none;
  padding: 0;
}

.book-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid #eee;
}

.book-info {
  display: flex;
  flex-direction: column;
}

.book-name {
  font-weight: bold;
  font-size: 1.1rem;
  word-break: break-all;
}

.book-size {
  color: #666;
  font-size: 0.9rem;
}

.download-btn {
  background-color: black;
  color: white;
  padding: 8px 12px;
  text-decoration: none;
  border-radius: 4px;
  font-size: 0.9rem;
  white-space: nowrap;
  margin-left: 10px;
}

.download-btn:hover {
  background-color: #333;
}

/* Kindle optimization */
@media (hover: none) {
  .download-btn {
    padding: 12px 20px; /* Larger touch target */
  }
}
</style>

