<template>
  <div v-if="!dismissed" class="announcement-banner">
    <div class="announcement-banner__content">
      <span class="announcement-banner__icon">📢</span>
      <span class="announcement-banner__text">{{ message }}</span>
    </div>
    <button
      class="announcement-banner__close"
      type="button"
      aria-label="Close"
      @click="dismissed = true"
    >
      ✕
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  message: {
    type: String,
    default: '',
  },
})

const dismissed = ref(false)
</script>

<style scoped>
.announcement-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 20px;
  margin-bottom: 16px;
  border-radius: 14px;
  background: linear-gradient(135deg, #fff0f5 0%, #e6e6fa 100%);
  box-shadow: 0 2px 12px rgba(223, 190, 200, 0.18);
  font-size: 0.92rem;
  color: #5a3e4b;
  line-height: 1.5;
}

.announcement-banner__content {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.announcement-banner__icon {
  flex-shrink: 0;
  font-size: 1.15rem;
}

.announcement-banner__text {
  flex: 1 1 auto;
  min-width: 0;
}

.announcement-banner__close {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 153, 153, 0.18);
  color: #7b1a35;
  font-size: 0.75rem;
  cursor: pointer;
  transition: background-color 0.18s ease, transform 0.18s ease;
}

.announcement-banner__close:hover {
  background: rgba(255, 153, 153, 0.38);
  transform: scale(1.1);
}

@media (max-width: 767px) {
  .announcement-banner {
    padding: 10px 16px;
    font-size: 0.85rem;
    text-align: center;
  }

  .announcement-banner__content {
    justify-content: center;
    flex-wrap: wrap;
  }
}
</style>
