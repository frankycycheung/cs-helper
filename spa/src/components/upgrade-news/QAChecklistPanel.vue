<template>
  <div class="card h-100">
    <div class="card-header">
      <h5 class="mb-0">2. Pre-Publish Quality Checklist</h5>
    </div>
    <div class="card-body">
      <h6 class="text-primary mb-3">Environment & Scope</h6>
      <div class="list-group mb-3">
        <label
          v-for="item in envScopeItems"
          :key="item.id"
          class="list-group-item d-flex align-items-center"
        >
          <input class="form-check-input me-3" type="checkbox" v-model="localChecklist[item.id]" />
          <span>{{ item.label }}</span>
        </label>
      </div>

      <h6 class="text-primary mb-3">Function & Flow</h6>
      <div class="list-group mb-3">
        <label
          v-for="item in funcFlowItems"
          :key="item.id"
          class="list-group-item d-flex align-items-center"
        >
          <input class="form-check-input me-3" type="checkbox" v-model="localChecklist[item.id]" />
          <span>{{ item.label }}</span>
        </label>
      </div>

      <h6 class="text-primary mb-3">Records Alignment</h6>
      <div class="list-group">
        <label
          v-for="item in recordsItems"
          :key="item.id"
          class="list-group-item d-flex align-items-center"
        >
          <input class="form-check-input me-3" type="checkbox" v-model="localChecklist[item.id]" />
          <span>{{ item.label }}</span>
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

defineProps({
  modelValue: {
    type: Object,
    default: () => ({}),
  },
})

const emit = defineEmits(['update:modelValue'])

const localChecklist = ref({
  env_prod: false,
  env_test: false,
  scope_limited: false,
  func_basic: false,
  func_edge: false,
  flow_complete: false,
  records_sync: false,
  records_verify: false,
})

const envScopeItems = [
  { id: 'env_prod', label: 'Production environment verified' },
  { id: 'env_test', label: 'Test environment validated' },
  { id: 'scope_limited', label: 'Target audience scoped' },
]

const funcFlowItems = [
  { id: 'func_basic', label: 'Basic functions working' },
  { id: 'func_edge', label: 'Edge cases covered' },
  { id: 'flow_complete', label: 'Complete user flow tested' },
]

const recordsItems = [
  { id: 'records_sync', label: 'Records synchronization confirmed' },
  { id: 'records_verify', label: 'Data verification completed' },
]

const allItems = [...envScopeItems, ...funcFlowItems, ...recordsItems]

watch(
  localChecklist,
  (newVal) => {
    emit('update:modelValue', { ...newVal })
  },
  { deep: true },
)

defineExpose({
  uncheckedItems: () =>
    allItems.filter((item) => !localChecklist.value[item.id]).map((item) => item.label),
})
</script>
