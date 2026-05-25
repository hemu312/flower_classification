import { ref } from 'vue'

// Shared reactive state
const imageUploaded = ref(false)
const resizedImage = ref(null)
const originalFile = ref(null)
const loading = ref(false)
const predictions = ref([])
const error = ref(null)
const isFeedbackSubmitted = ref(false) // Track if feedback submission succeeded
const fileInput = ref(null)

export function useAppState() {
  const resetApp = () => {
    imageUploaded.value = false
    resizedImage.value = null
    originalFile.value = null
    fileInput.value.value = ''
    isFeedbackSubmitted.value = false
    predictions.value = []
    error.value = null
  }
  return {
    imageUploaded,
    resizedImage,
    originalFile,
    loading,
    predictions,
    error,
    isFeedbackSubmitted,
    fileInput,
    resetApp
  }
}
