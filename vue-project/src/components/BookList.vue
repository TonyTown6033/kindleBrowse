<script setup>
import { ref, onMounted } from 'vue'

const books = ref([])
const loading = ref(false)

const fetchBooks = async () => {
  loading.value = true
  const token = localStorage.getItem('token')
  
  try {
    const response = await fetch('/api/books', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.ok) {
      books.value = await response.json()
    } else if (response.status === 401) {
       // Handle unauthorized (maybe event bus logout or just silent fail)
       console.error('Unauthorized')
    }
  } catch (error) {
    console.error('Failed to fetch books:', error)
  } finally {
    loading.value = false
  }
}

// Helper to format date if we had it, but we'll just stick to size for now
const formatSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const getDownloadUrl = (book) => {
   // We need to append auth token? 
   // Standard browser download via <a> tag cannot add headers.
   // Solution 1: Use a query param token ?token=... (Less secure but works for simple apps)
   // Solution 2: The download endpoint could check cookie? (We are using Bearer header)
   // Solution 3: Fetch blob and save (Works but heavier for large files on Kindle browser?)
   
   // Given Kindle's limited browser, fetch blob might crash or not trigger download UI properly.
   // Simple token in query param is pragmatic for this use case.
   
   // Let's update backend to accept token in query param for download endpoint as fallback?
   // OR: Just assume users are fine with `fetch` blob if file size is reasonable.
   // BUT Kindle browser is quirky.
   
   // Let's stick to href but we need a way to authenticate.
   // The simplest way for file download with auth is cookies.
   // But we implemented Header auth.
   
   // WORKAROUND: Implement a "signed URL" or temporary download token?
   // Or just allow download with `?token=` query param.
   // I will update backend to allow `token` query param for the download endpoint.
   
   const token = localStorage.getItem('token')
   return `${book.url}?token=${token}`
}

defineExpose({ fetchBooks })

onMounted(() => {
  fetchBooks()
})
</script>

<template>
  <div class="library-section">
    <div class="section-header">
      <h2>Your Library</h2>
      <span class="count">{{ books.length }} items</span>
    </div>

    <div v-if="loading" class="state-message">Loading library...</div>
    <div v-else-if="books.length === 0" class="state-message empty">
      <p>No books yet.</p>
      <p class="hint">Upload some books to get started.</p>
    </div>
    
    <ul v-else class="book-list">
      <li v-for="book in books" :key="book.id" class="book-item">
        <div class="book-details">
          <span class="book-title">{{ book.name }}</span>
          <span class="book-meta">{{ formatSize(book.size) }}</span>
        </div>
        <a :href="getDownloadUrl(book)" class="download-button" download>
          Download
        </a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.library-section {
  background-color: white;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  border-bottom: 2px solid #000;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
}

h2 {
  font-size: 1.5rem;
  font-weight: normal;
  font-family: var(--font-main);
}

.count {
  color: #666;
  font-size: 0.9rem;
  font-family: var(--font-ui);
}

.state-message {
  text-align: center;
  padding: 3rem 1rem;
  color: #666;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.state-message.empty .hint {
  font-size: 0.9rem;
  color: #999;
  margin-top: 0.5rem;
}

.book-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.book-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem;
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.02);
  transition: border-color 0.2s;
}

.book-item:hover {
  border-color: #ccc;
}

.book-details {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  flex: 1;
  padding-right: 1rem;
}

.book-title {
  font-size: 1.1rem;
  color: #000;
  font-family: var(--font-main);
  line-height: 1.3;
  word-break: break-word;
}

.book-meta {
  font-size: 0.85rem;
  color: #666;
  font-family: var(--font-ui);
}

.download-button {
  background-color: #000;
  color: #fff;
  padding: 10px 20px;
  border-radius: 50px; /* Pill shape */
  text-decoration: none;
  font-size: 0.9rem;
  font-family: var(--font-ui);
  font-weight: 500;
  white-space: nowrap;
  transition: background-color 0.2s;
}

.download-button:hover {
  background-color: #333;
  color: #fff;
}

/* Kindle Touch Optimization */
@media (hover: none) {
  .book-item {
    padding: 1.5rem; /* Larger touch area */
  }
  
  .download-button {
    padding: 12px 24px;
    background-color: white;
    color: black;
    border: 2px solid black;
  }
}
</style>
