import { ref } from 'vue'

// Shared reactive state
const imageUploaded = ref(false)
const resizedImage = ref(null)
const originalFile = ref(null)
const loading = ref(false)
const predictions = ref([])
const error = ref(null)

export function useImageState() {
  return {
    imageUploaded,
    resizedImage,
    originalFile,
    loading,
    predictions,
    error
  }
}
