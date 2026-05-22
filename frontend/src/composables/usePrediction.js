import { useImageState } from './useImageState'

export function usePrediction() {
  const { resizedImage, loading, predictions, error } = useImageState()

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
      predictions.value = predictionsArray
        .sort((a, b) => b.confidence - a.confidence)
        .slice(0, 5)
    } catch (err) {
      error.value = `Error: ${err.message}`
      console.error('Prediction error:', err)
    } finally {
      loading.value = false
    }
  }

  return { predictImage }
}
