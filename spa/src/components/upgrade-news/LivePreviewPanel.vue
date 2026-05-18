<template>
  <div class="card h-100">
    <div class="card-header">
      <h5 class="mb-0">{{ $t('upgradeNews.previewTitle') }}</h5>
    </div>
    <div class="card-body">
      <div class="preview-content border rounded p-3 mb-3 bg-light">
        <div class="mb-2">
          <strong>{{ formData.featureTitle || '' }}</strong>
        </div>
        <p class="mb-2 text-muted">
          {{ formData.description || '' }}
        </p>
        <div v-if="formData.usagePath?.web || formData.usagePath?.app" class="mb-3">
          <div v-if="formData.usagePath?.web" class="mb-1">
            <span class="fw-semibold">{{ $t('upgradeNews.webPathPrefix') }}</span
            ><span class="usage-path-text">{{ formData.usagePath.web }}</span>
          </div>
          <div v-if="formData.usagePath?.app">
            <span class="fw-semibold">{{ $t('upgradeNews.appPathPrefix') }}</span
            ><span class="usage-path-text">{{ formData.usagePath.app }}</span>
          </div>
        </div>
      </div>
      <button class="btn btn-pill btn-primary w-100" @click="generateNews">
        <i class="bi bi-copy me-2"></i>{{ $t('upgradeNews.btnGenerate') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const props = defineProps({
  formData: {
    type: Object,
    default: () => ({
      module: '',
      featureTitle: '',
      description: '',
      usagePath: { web: '', app: '' },
      remarks: '',
    }),
  },
})

const emit = defineEmits(['generate'])

const formattedPreview = computed(() => {
  const segments = [
    props.formData.usagePath?.web
      ? `${t('upgradeNews.webPathPrefix')}${props.formData.usagePath.web}`
      : '',
    props.formData.usagePath?.app
      ? `${t('upgradeNews.appPathPrefix')}${props.formData.usagePath.app}`
      : '',
  ].filter(Boolean)
  return `NEW: ${props.formData.featureTitle || ''}
${props.formData.description || ''}
${segments.length ? `Usage: ${segments.join('\n')}` : ''}`
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
  background-color: #fffafa;
  border-radius: 16px;
}
.usage-path-text {
  margin-inline-start: 0.5rem;
}
</style>
