<template>
  <div class="container">
    <h1>🖼️ Flower Classification using AI</h1>
    <div class="content">
      <div class="section">
        <Image />
      </div>
      <div class="section">
        <Prediction />
      </div>
    </div>
  </div>
</template>

<script setup>
import Image from './components/Image.vue'
import Prediction from './components/Prediction.vue'
</script>

<style scoped>
.container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 2rem;
  gap: 2rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

h1 {
  color: #333;
  margin-bottom: 1rem;
  font-size: clamp(1.25rem, 5vw, 2rem);
}

.content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: clamp(1.5rem, 5vw, 3rem);
  flex: 1;
}

.section {
  background: white;
  border-radius: 0.75rem;
  padding: clamp(1rem, 5vw, 2rem);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  min-width: 0;
}

@media (max-width: 768px) {
  .container {
    padding: 1rem;
    gap: 1rem;
  }

  .content {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .section {
    padding: 1.25rem;
  }
}
</style>
