<script setup>
import { ref } from 'vue'

const emit = defineEmits(['upload-success'])
const fileInput = ref(null)
const uploading = ref(false)
const message = ref('')
const isSuccess = ref(false)

const triggerFileInput = () => {
  fileInput.value.click()
}

const handleFileChange = () => {
  const files = fileInput.value.files
  if (files.length > 0) {
    uploadFile()
  }
}

const uploadFile = async () => {
  const files = fileInput.value.files
  if (files.length === 0) return

  uploading.value = true
  message.value = 'Uploading...'
  isSuccess.value = false

  const formData = new FormData()
  formData.append('file', files[0])
  
  const token = localStorage.getItem('token')

  try {
    const response = await fetch('/api/upload', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    })
    
    if (response.ok) {
      message.value = 'Book added successfully'
      isSuccess.value = true
      fileInput.value.value = '' // Clear input
      emit('upload-success')
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        if (isSuccess.value) message.value = ''
      }, 3000)
    } else {
      if (response.status === 401) {
        message.value = 'Session expired. Please login again.'
        // Optionally emit logout event
      } else {
        message.value = 'Upload failed. Please try again.'
      }
      isSuccess.value = false
    }
  } catch (error) {
    message.value = 'Connection error. Please check your network.'
    isSuccess.value = false
  } finally {
    uploading.value = false
  }
}
</script>

<template>
  <div class="upload-section">
    <div class="upload-card" @click="triggerFileInput" :class="{ 'is-loading': uploading }">
      <input 
        type="file" 
        ref="fileInput" 
        accept=".pdf,.epub,.mobi,.azw3,.txt" 
        @change="handleFileChange"
      />
      
      <div class="upload-content">
        <div class="icon" v-if="!uploading">+</div>
        <div class="icon spinner" v-else>⟳</div>
        
        <span class="action-text">{{ uploading ? 'Uploading...' : 'Tap to Upload New Book' }}</span>
        <span class="sub-text" v-if="!uploading">Supports PDF, EPUB, MOBI, AZW3</span>
      </div>
    </div>
    
    <div v-if="message" class="status-message" :class="{ success: isSuccess, error: !isSuccess }">
      {{ message }}
    </div>
  </div>
</template>

<style scoped>
.upload-section {
  margin-bottom: 1rem;
}

.upload-card {
  border: 2px dashed #ccc;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #fafafa;
}

.upload-card:hover {
  border-color: #000;
  background-color: #fff;
}

.upload-card.is-loading {
  cursor: wait;
  opacity: 0.7;
}

input[type="file"] {
  display: none;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.icon {
  font-size: 2.5rem;
  line-height: 1;
  color: #666;
  margin-bottom: 0.5rem;
}

.spinner {
  animation: spin 1s linear infinite;
  display: inline-block;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.action-text {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
  font-family: var(--font-ui);
}

.sub-text {
  color: #888;
  font-size: 0.9rem;
}

.status-message {
  margin-top: 1rem;
  padding: 10px;
  border-radius: 6px;
  text-align: center;
  font-family: var(--font-ui);
  font-size: 0.9rem;
}

.status-message.success {
  background-color: #f0fdf4;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.status-message.error {
  background-color: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecaca;
}
</style>
