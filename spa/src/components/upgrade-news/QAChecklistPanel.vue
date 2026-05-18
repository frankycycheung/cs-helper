<template>
  <div class="card h-100">
    <div class="card-header">
      <h5 class="mb-0">{{ $t('upgradeNews.checklistTitle') }}</h5>
    </div>
    <div class="card-body">
      <div v-for="(category, key) in categories" :key="key" class="mb-4">
        <h6 class="text-primary mb-3">{{ category }}</h6>
        <div class="list-group">
          <label
            v-for="item in items[key]"
            :key="item.id"
            class="list-group-item d-flex align-items-center"
          >
            <input
              class="form-check-input me-3"
              type="checkbox"
              v-model="localChecklist[item.id]"
            />
            <span>{{ item.label }}</span>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

defineProps({
  modelValue: {
    type: Object,
    default: () => ({}),
  },
})

const emit = defineEmits(['update:modelValue'])

const localChecklist = ref({
  checkSite: false,
  checkIP: false,
  checkEJ: false,
  checkFlow: false,
  checkMobile: false,
  checkProgrammer: false,
  checkQaRecord: false,
  checkTickets: false,
})

const categories = computed(() => ({
  env: t('upgradeNews.categories.env'),
  flow: t('upgradeNews.categories.flow'),
  records: t('upgradeNews.categories.records'),
}))

const items = computed(() => ({
  env: [
    { id: 'checkSite', label: t('upgradeNews.items.checkSite') },
    { id: 'checkIP', label: t('upgradeNews.items.checkIP') },
    { id: 'checkEJ', label: t('upgradeNews.items.checkEJ') },
  ],
  flow: [
    { id: 'checkFlow', label: t('upgradeNews.items.checkFlow') },
    { id: 'checkMobile', label: t('upgradeNews.items.checkMobile') },
    { id: 'checkProgrammer', label: t('upgradeNews.items.checkProgrammer') },
  ],
  records: [
    { id: 'checkQaRecord', label: t('upgradeNews.items.checkQaRecord') },
    { id: 'checkTickets', label: t('upgradeNews.items.checkTickets') },
  ],
}))

const allItems = computed(() => {
  return [...items.value.env, ...items.value.flow, ...items.value.records]
})

watch(
  localChecklist,
  (newVal) => {
    emit('update:modelValue', { ...newVal })
  },
  { deep: true },
)

defineExpose({
  uncheckedItems: () =>
    allItems.value.filter((item) => !localChecklist.value[item.id]).map((item) => item.label),
})
</script>

<style scoped>
.list-group-item {
  border-radius: 12px !important;
  margin-bottom: 4px;
  border: 1px solid #f3e5f5;
}
</style>
