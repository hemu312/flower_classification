import { useAppState } from './useAppState'

export function useImageProcessing() {
  const { resizedImage, originalFile, imageUploaded, error, predictions, isFeedbackSubmitted } = useAppState()
  
  const handleFileUpload = (event) => {
    const file = event.target.files[0]
    isFeedbackSubmitted.value = false

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
        canvas.width = 512
        canvas.height = 512

        const ctx = canvas.getContext('2d')

        // Calculate dimensions to fit image in 512x512 (maintain aspect ratio)
        const scale = Math.max(512 / img.width, 512 / img.height)
        const x = 512 / 2 - (img.width / 2) * scale
        const y = 512 / 2 - (img.height / 2) * scale

        ctx.drawImage(img, x, y, img.width * scale, img.height * scale)

        resizedImage.value = canvas.toDataURL('image/jpeg', 0.9)
        imageUploaded.value = true
        predictions.value = []
      }

      img.src = e.target.result
    }

    reader.readAsDataURL(file)
  }

  return { handleFileUpload }
}
