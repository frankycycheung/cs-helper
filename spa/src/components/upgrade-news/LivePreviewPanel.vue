<template>
  <div class="card h-100">
    <div class="card-header">
      <h5 class="mb-0">3. Upgrade News Live Preview</h5>
    </div>
    <div class="card-body">
      <div class="preview-content border rounded p-3 mb-3 bg-light">
        <div class="mb-2">
          <span class="badge bg-warning text-dark me-2">NEW</span>
          <strong>{{ formData.featureTitle || 'Feature Title' }}</strong>
        </div>
        <p class="mb-2 text-muted">
          {{ formData.description || 'Description will appear here...' }}
        </p>
        <div class="d-flex gap-2">
          <span v-if="formData.usagePath?.web" class="badge bg-info">Web</span>
          <span v-if="formData.usagePath?.app" class="badge bg-info">App</span>
        </div>
      </div>
      <button class="btn btn-primary w-100" @click="generateNews">
        <i class="bi bi-copy me-2"></i>Generate/Copy News
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  formData: {
    type: Object,
    default: () => ({
      module: '',
      featureTitle: '',
      description: '',
      usagePath: { web: false, app: false },
      remarks: '',
    }),
  },
})

const emit = defineEmits(['generate'])

const formattedPreview = computed(() => {
  return `NEW: ${props.formData.featureTitle || 'Feature Title'}
${props.formData.description || 'Description'}
Usage: ${[props.formData.usagePath?.web ? 'Web' : '', props.formData.usagePath?.app ? 'App' : ''].filter(Boolean).join(', ')}`
})

const generateNews = () => {
  const content = formattedPreview.value
  navigator.clipboard.writeText(content).then(() => {
    emit('generate')
  })
}
</script>

<style scoped>
.preview-content {
  min-height: 120px;
}
</style>
