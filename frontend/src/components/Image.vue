<template>
  <div class="image-container">
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
      <span class="preview-label">Preview (512x512)</span>
      <img v-if="resizedImage" :src="resizedImage" class="preview-image" alt="preview">
    </div>
  </div>
</template>

<script setup>
import { useAppState } from '../composables/useAppState'
import { useImageProcessing } from '../composables/useImageProcessing'

const { imageUploaded, resizedImage, error, loading, fileInput } = useAppState()
const { handleFileUpload } = useImageProcessing()
</script>

<style scoped>
.image-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.file-input-wrapper {
  position: relative;
  overflow: hidden;
}

.file-input-wrapper input[type='file'] {
  display: none;
}

.upload-btn {
  width: 100%;
  padding: clamp(0.75rem, 2vw, 1rem);
  background: #667eea;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: clamp(0.875rem, 2vw, 1rem);
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
}

.upload-btn:hover:not(:disabled) {
  background: #5568d3;
}

.upload-btn:active:not(:disabled) {
  transform: scale(0.98);
}

.upload-btn:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
}

.preview-section {
  display: none;
  text-align: center;
}

.preview-section.active {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.preview-label {
  color: #666;
  font-size: clamp(0.75rem, 2vw, 0.875rem);
  font-weight: 500;
}

.preview-image {
  width: clamp(140px, 60vw, 512px);
  height: clamp(140px, 60vw, 512px);
  border: 2px solid #e0e0e0;
  border-radius: 0.5rem;
  background: #f5f5f5;
}

.error-message {
  background: #fed7d7;
  color: #c53030;
  padding: clamp(0.75rem, 2vw, 1rem);
  border-radius: 0.5rem;
  border-left: 4px solid #c53030;
  font-size: clamp(0.8rem, 2vw, 0.95rem);
}

.info-text {
  color: #999;
  font-size: clamp(0.7rem, 2vw, 0.75rem);
  text-align: center;
  margin-top: 0.5rem;
}
</style>
