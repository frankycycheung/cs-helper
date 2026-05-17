<template>
  <div class="container-fluid py-4">
    <div class="row g-4">
      <div class="col-lg-4 col-md-12">
        <InputConfigPanel v-model:model="formData" />
      </div>
      <div class="col-lg-4 col-md-12">
        <QAChecklistPanel v-model:modelValue="checklistData" ref="checklistRef" />
      </div>
      <div class="col-lg-4 col-md-12">
        <LivePreviewPanel :formData="formData" @generate="onGenerate" />
      </div>
    </div>

    <WarningModal
      :show="showWarning"
      :unchecked-items="uncheckedItems"
      @close="showWarning = false"
      @proceed="proceedAnyway"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import InputConfigPanel from './InputConfigPanel.vue'
import QAChecklistPanel from './QAChecklistPanel.vue'
import LivePreviewPanel from './LivePreviewPanel.vue'
import WarningModal from '../common/WarningModal.vue'

const formData = ref({
  module: '',
  featureTitle: '',
  description: '',
  usagePath: { web: false, app: false },
  remarks: '',
})

const checklistData = ref({})
const checklistRef = ref(null)
const showWarning = ref(false)
const uncheckedItems = ref([])

const onGenerate = () => {
  const items = checklistRef.value?.uncheckedItems() || []
  if (items.length > 0) {
    uncheckedItems.value = items
    showWarning.value = true
  } else {
    alert('News generated successfully!')
  }
}

const proceedAnyway = () => {
  showWarning.value = false
  alert('News generated anyway!')
}
</script>
