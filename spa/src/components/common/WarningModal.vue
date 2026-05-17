<template>
  <div
    class="modal fade show d-block"
    tabindex="-1"
    style="background-color: rgba(0, 0, 0, 0.5)"
    v-if="show"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title text-warning">
            <i class="bi bi-exclamation-triangle me-2"></i>Incomplete Checklist
          </h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <p class="mb-3">Please review the following unchecked items:</p>
          <ul class="list-group list-group-flush">
            <li v-for="item in uncheckedItems" :key="item" class="list-group-item text-danger">
              <i class="bi bi-x-circle me-2"></i>{{ item }}
            </li>
          </ul>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">Go Back</button>
          <button type="button" class="btn btn-warning" @click="$emit('proceed')">
            Proceed Anyway
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  uncheckedItems: {
    type: Array,
    default: () => [],
  },
})

defineEmits(['close', 'proceed'])
</script>

<style scoped>
.modal {
  display: block;
}
</style>
