<template>
  <div class="prediction-container">
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

    <!-- Feedback Section -->
    <div class="feedback-section" :class="{ active: predictions.length > 0 }">
        <button v-if="!isFeedbackSubmitted" class="submit-feedback-btn" @click="submitFeedback(predictions[selectedIndex]?.label); selectedIndex = null" :disabled="loading">Submit Feedback</button>
        <div v-if="isFeedbackSubmitted" class="feedback-response">Feedback submitted successfully!</div>
    </div>

  </div>
</template>

<script setup>
import { useImageState } from '../composables/useImageState'
import { usePrediction } from '../composables/usePrediction'
import { useImageProcessing } from '../composables/useImageProcessing'

const { imageUploaded, loading, predictions } = useImageState()
const { predictImage } = usePrediction()
const { resetApp } = useAppState()
const { submitFeedback } = useFeedback()

// Track the selected index (null means nothing is selected)
const selectedIndex = ref(null)
</script>

<style scoped>
.prediction-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
  width: 100%;
}

.predict-btn,
.reset-btn {
  flex: 1;
  padding: clamp(0.75rem, 2vw, 1rem);
  border: none;
  border-radius: 0.5rem;
  font-size: clamp(0.875rem, 2vw, 1rem);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.predict-btn {
  background: #48bb78;
  color: white;
}

.predict-btn:hover:not(:disabled) {
  background: #38a169;
}

.reset-btn {
  background: #ed8936;
  color: white;
}

.reset-btn:hover:not(:disabled) {
  background: #dd6b20;
}

.predict-btn:disabled,
.reset-btn:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  color: #667eea;
  font-weight: 500;
  padding: 1rem 0;
}

.spinner {
  display: inline-block;
  width: clamp(16px, 3vw, 20px);
  height: clamp(16px, 3vw, 20px);
  border: 3px solid #f3f3f3;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 0.5rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.results-section {
  display: none;
}

.results-section.active {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.results-list {
  max-height: 300px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.results-title {
  color: #333;
  font-size: clamp(1rem, 2.5vw, 1.125rem);
  font-weight: 600;
}

.result-item {
  background: #f7fafc;
  padding: clamp(0.75rem, 2vw, 1rem);
  border-radius: 0.5rem;
  border-left: 4px solid #667eea;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: clamp(0.8rem, 2vw, 0.95rem);
}

/* Hover feedback */
.result-item:hover {
  background: #edf2f7;
  transform: translateX(2px);
}

/* Selected state styling */
.result-item.selected {
  background: #7ac87e;
  border-left-color: #4c51bf; /* Darker purple accent */
  box-shadow: 0 0 0 2px #667eea; /* Clean border focus effect */
}

.result-rank {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #667eea;
  color: white;
  width: clamp(24px, 6vw, 32px);
  height: clamp(24px, 6vw, 32px);
  border-radius: 50%;
  flex-shrink: 0;
  font-weight: 600;
  font-size: clamp(0.7rem, 2vw, 0.875rem);
}

.result-label {
  flex: 1;
  color: #333;
  font-weight: 500;
}

.result-confidence {
  color: #667eea;
  font-weight: 600;
  flex-shrink: 0;
}

.feedback-section {
  display: none;
  justify-content: center;
}

.feedback-section.active {
  display: flex;
}

.submit-feedback-btn {
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

@media (max-width: 768px) {
  .action-buttons {
    flex-direction: column;
  }

  .predict-btn,
  .reset-btn {
    width: 100%;
  }
}
</style>
