<template>
  <div class="container">
    <h1>🖼️ Image Prediction</h1>

    <!-- Error Message -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- Upload Section -->
    <div class="upload-section">
      <div class="file-input-wrapper">
        <input type="file" ref="fileInput" @change="handleFileUpload" accept="image/*" :disabled="loading">
        <button class="upload-btn" @click="$refs.fileInput.click()" :disabled="loading">
          {{ imageUploaded ? '📁 Choose Another Image' : '📁 Upload Image' }}
        </button>
      </div>
      <p class="info-text">Accepted formats: JPG, PNG, GIF, WebP (max 10MB)</p>
    </div>

    <!-- Preview Section -->
    <div class="preview-section" :class="{ active: imageUploaded }">
      <span class="preview-label">Preview (224x224)</span>
      <img v-if="resizedImage" :src="resizedImage" class="preview-image" alt="preview">
    </div>

    <!-- Action Buttons -->
    <div v-if="imageUploaded" class="action-buttons">
      <button class="predict-btn" @click="predictImage" :disabled="loading">
        <span v-if="!loading">🔮 Predict</span>
        <span v-else>
          <span class="spinner"></span>Predicting...
        </span>
      </button>
      <button class="reset-btn" @click="resetApp" :disabled="loading">
        ↻ Reset
      </button>
    </div>

    <!-- Loading Message -->
    <div v-if="loading && predictions.length === 0" class="loading">
      <span class="spinner"></span>Getting predictions...
    </div>

    <!-- Results Section -->
    <div class="results-section" :class="{ active: predictions.length > 0 }">
      <div class="results-title">Top 5 Predictions</div>
      <div v-for="(result, index) in predictions" :key="index" class="result-item">
        <span class="result-rank">{{ index + 1 }}</span>
        <span class="result-label">{{ result.label }}</span>
        <span class="result-confidence">{{ (result.confidence * 100).toFixed(2) }}%</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const fileInput = ref(null)
const imageUploaded = ref(false)
const resizedImage = ref(null)
const originalFile = ref(null)
const loading = ref(false)
const predictions = ref([])
const error = ref(null)

const handleFileUpload = (event) => {
  const file = event.target.files[0]

  if (!file) return

  // Validate file type
  if (!file.type.startsWith('image/')) {
    error.value = 'Please select a valid image file.'
    setTimeout(() => (error.value = null), 3000)
    return
  }

  // Validate file size (10MB max)
  if (file.size > 10 * 1024 * 1024) {
    error.value = 'File size must be less than 10MB.'
    setTimeout(() => (error.value = null), 3000)
    return
  }

  originalFile.value = file
  error.value = null
  resizeImage(file)
}

const resizeImage = (file) => {
  const reader = new FileReader()

  reader.onload = (e) => {
    const img = new Image()

    img.onload = () => {
      const canvas = document.createElement('canvas')
      canvas.width = 224
      canvas.height = 224

      const ctx = canvas.getContext('2d')

      // Calculate dimensions to fit image in 224x224 (maintain aspect ratio)
      const scale = Math.max(224 / img.width, 224 / img.height)
      const x = 224 / 2 - (img.width / 2) * scale
      const y = 224 / 2 - (img.height / 2) * scale

      ctx.drawImage(img, x, y, img.width * scale, img.height * scale)

      resizedImage.value = canvas.toDataURL('image/jpeg', 0.9)
      imageUploaded.value = true
      predictions.value = []
    }

    img.src = e.target.result
  }

  reader.readAsDataURL(file)
}

const predictImage = async () => {
  if (!resizedImage.value) {
    error.value = 'No image to predict.'
    return
  }

  loading.value = true
  error.value = null

  try {
    // Convert base64 to blob
    const response = await fetch(resizedImage.value)
    const blob = await response.blob()

    // Create FormData for multipart/form-data request
    const formData = new FormData()
    formData.append('imgFile', blob, 'image.jpg')

    // Send POST request to /predict
    const predictResponse = await fetch('/predict', {
      method: 'POST',
      body: formData
    })

    if (!predictResponse.ok) {
      throw new Error(`Server error: ${predictResponse.status}`)
    }

    const data = await predictResponse.json()

    // Convert object { label: confidence, ... } to array and sort by confidence
    const predictionsArray = Object.entries(data).map(([label, confidence]) => ({
      label,
      confidence
    }))
    // Sort by confidence descending and take top 5
    predictions.value = predictionsArray.sort((a, b) => b.confidence - a.confidence).slice(0, 5)
  } catch (err) {
    error.value = `Error: ${err.message}`
    console.error('Prediction error:', err)
  } finally {
    loading.value = false
  }
}

const resetApp = () => {
  imageUploaded.value = false
  resizedImage.value = null
  originalFile.value = null
  predictions.value = []
  error.value = null
  fileInput.value.value = ''
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  padding: 40px;
  max-width: 600px;
  width: 100%;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 28px;
}

.upload-section {
  margin-bottom: 30px;
}

.file-input-wrapper {
  position: relative;
  overflow: hidden;
  display: inline-block;
  width: 100%;
}

.file-input-wrapper input[type='file'] {
  position: absolute;
  left: -9999px;
}

.upload-btn {
  display: block;
  width: 100%;
  padding: 14px 20px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s ease;
}

.upload-btn:hover {
  background: #5568d3;
}

.upload-btn:active {
  transform: scale(0.98);
}

.upload-btn:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
}

.preview-section {
  display: none;
  text-align: center;
  margin-bottom: 30px;
}

.preview-section.active {
  display: block;
}

.preview-label {
  display: block;
  color: #666;
  font-size: 14px;
  margin-bottom: 12px;
  font-weight: 500;
}

.preview-image {
  width: 224px;
  height: 224px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  margin: 0 auto 20px;
  background: #f5f5f5;
}

.action-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-bottom: 30px;
}

.predict-btn,
.reset-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.predict-btn {
  background: #48bb78;
  color: white;
  flex: 1;
}

.predict-btn:hover:not(:disabled) {
  background: #38a169;
}

.predict-btn:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
}

.reset-btn {
  background: #ed8936;
  color: white;
}

.reset-btn:hover {
  background: #dd6b20;
}

.loading {
  text-align: center;
  color: #667eea;
  font-weight: 500;
  margin: 20px 0;
}

.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 10px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.results-section {
  display: none;
}

.results-section.active {
  display: block;
}

.results-title {
  color: #333;
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
}

.result-item {
  background: #f7fafc;
  padding: 16px;
  margin-bottom: 12px;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.result-rank {
  display: inline-block;
  background: #667eea;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  text-align: center;
  line-height: 32px;
  margin-right: 12px;
  font-weight: 600;
}

.result-label {
  display: inline-block;
  color: #333;
  font-weight: 500;
  min-width: 200px;
}

.result-confidence {
  color: #667eea;
  font-weight: 600;
}

.error-message {
  background: #fed7d7;
  color: #c53030;
  padding: 14px;
  border-radius: 8px;
  margin-bottom: 20px;
  border-left: 4px solid #c53030;
}

.info-text {
  color: #999;
  font-size: 12px;
  text-align: center;
  margin-top: 12px;
}
</style>
