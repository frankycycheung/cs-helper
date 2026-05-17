<template>
  <div class="card h-100">
    <div class="card-header">
      <h5 class="mb-0">1. Module & Content Configuration</h5>
    </div>
    <div class="card-body">
      <div class="mb-3">
        <label class="form-label">Module</label>
        <select class="form-select" v-model="localModule">
          <option value="">Select a module</option>
          <option value="user-management">User Management</option>
          <option value="payment">Payment</option>
          <option value="reports">Reports</option>
          <option value="settings">Settings</option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label">Feature Title</label>
        <input
          type="text"
          class="form-control"
          placeholder="Enter feature title"
          v-model="localFeatureTitle"
        />
      </div>

      <div class="mb-3">
        <label class="form-label">Description</label>
        <textarea
          class="form-control"
          rows="4"
          placeholder="Enter raw description"
          v-model="localDescription"
        ></textarea>
        <button class="btn btn-outline-primary btn-sm mt-2">
          <i class="bi bi-magic"></i> AI Polish
        </button>
      </div>

      <div class="mb-3">
        <label class="form-label">Usage Path</label>
        <div class="form-check">
          <input class="form-check-input" type="checkbox" id="web" v-model="localUsagePath.web" />
          <label class="form-check-label" for="web">Web</label>
        </div>
        <div class="form-check">
          <input class="form-check-input" type="checkbox" id="app" v-model="localUsagePath.app" />
          <label class="form-check-label" for="app">App</label>
        </div>
      </div>

      <div class="mb-3">
        <label class="form-label text-muted">Internal Remarks (Not included in preview)</label>
        <textarea
          class="form-control bg-light"
          rows="3"
          placeholder="Internal notes..."
          v-model="localRemarks"
        ></textarea>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  model: {
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

const emit = defineEmits(['update:model'])

const localModule = ref(props.model.module)
const localFeatureTitle = ref(props.model.featureTitle)
const localDescription = ref(props.model.description)
const localUsagePath = ref({ ...props.model.usagePath })
const localRemarks = ref(props.model.remarks)

watch([localModule, localFeatureTitle, localDescription, localUsagePath, localRemarks], () => {
  emit('update:model', {
    module: localModule.value,
    featureTitle: localFeatureTitle.value,
    description: localDescription.value,
    usagePath: { ...localUsagePath.value },
    remarks: localRemarks.value,
  })
})
</script>
