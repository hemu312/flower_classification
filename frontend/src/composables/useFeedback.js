import { useAppState } from './useAppState'


export function useFeedback() {
    const { resizedImage, predictions, error, isFeedbackSubmitted } = useAppState()
    const submitFeedback = async (correctValue) => {
        if (!resizedImage.value) {
            error.value = 'No image to send feedback for.'
            return
        }
        if (predictions.value.length === 0) {
            error.value = 'No predictions to send feedback for.'
            return
        }

        const predictedValue = predictions.value[0].label // Take the top prediction

        try {
            // Convert base64 to blob
            const response = await fetch(resizedImage.value)
            const blob = await response.blob()

            // Create FormData for multipart/form-data request
            const formData = new FormData()
            formData.append('image', blob, 'image.jpg')
            formData.append('predicted_value', predictedValue)
            formData.append('correct_value', correctValue)

            // Send POST request to /feedback
            await fetch('/feedback', {
                method: 'POST',
                body: formData
            }).then(res => {
                if (res.ok) {
                    isFeedbackSubmitted.value = true
                } else {
                    throw new Error(`Server error: ${res.status}`)
                }
            })
        } catch (err) {
            error.value = `Error: ${err.message}`
            console.error('Feedback error:', err)
        }
    }

    return { submitFeedback }
}