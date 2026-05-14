<template>
  <div>
    <h1>Vue + Flask</h1>
    <p>Backend says: {{ message }}</p>
    <router-view />
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const message = ref('Loading...')

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/data')
    message.value = response.data.message
  } catch (error) {
    console.error("Error fetching data:", error)
    message.value = "Failed to connect to backend."
  }
})
</script>