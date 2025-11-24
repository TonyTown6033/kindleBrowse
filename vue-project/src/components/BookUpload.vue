<script setup>
import { ref } from 'vue'

const emit = defineEmits(['upload-success'])
const fileInput = ref(null)
const uploading = ref(false)
const message = ref('')

const uploadFile = async () => {
  const files = fileInput.value.files
  if (files.length === 0) return

  uploading.value = true
  message.value = ''

  const formData = new FormData()
  formData.append('file', files[0])

  try {
    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData
    })
    
    if (response.ok) {
      message.value = 'Uploaded successfully!'
      fileInput.value.value = '' // Clear input
      emit('upload-success')
    } else {
      message.value = 'Upload failed.'
    }
  } catch (error) {
    message.value = 'Error: ' + error.message
  } finally {
    uploading.value = false
  }
}
</script>

<template>
  <div class="upload-container">
    <h3>Upload Book</h3>
    <div class="input-group">
      <input type="file" ref="fileInput" accept=".pdf,.epub,.mobi,.azw3,.txt" />
      <button @click="uploadFile" :disabled="uploading">
        {{ uploading ? 'Uploading...' : 'Upload' }}
      </button>
    </div>
    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<style scoped>
.upload-container {
  border: 1px solid #ccc;
  padding: 1rem;
  margin-bottom: 1rem;
  background-color: #f9f9f9;
}

.input-group {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
}

button {
  padding: 8px 16px;
  background-color: #000;
  color: #fff;
  border: none;
  cursor: pointer;
}

button:disabled {
  background-color: #999;
}

.message {
  margin-top: 0.5rem;
  font-size: 0.9rem;
}
</style>

