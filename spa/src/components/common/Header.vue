<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom">
    <div class="container-fluid">
      <a class="navbar-brand fw-bold" href="#">{{ brand }}</a>
      <span v-if="badgeText" class="badge bg-primary ms-2">{{ badgeText }}</span>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav ms-auto">
          <slot name="locale-switcher">
            <li class="nav-item ms-2">
              <div class="locale-switcher">
                <button
                  v-for="lang in locales"
                  :key="lang.value"
                  :class="{ active: currentLocale === lang.value }"
                  @click="setLocale(lang.value)"
                  class="btn btn-outline-secondary btn-sm me-1"
                >
                  {{ lang.label }}
                </button>
              </div>
            </li>
          </slot>
          <slot name="nav-items">
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                User
              </a>
              <ul class="dropdown-menu dropdown-menu-end">
                <slot name="dropdown-items">
                  <li><a class="dropdown-item" href="#">Profile</a></li>
                  <li><a class="dropdown-item" href="#">Settings</a></li>
                  <li><hr class="dropdown-divider" /></li>
                  <li><a class="dropdown-item" href="#">Logout</a></li>
                </slot>
              </ul>
            </li>
          </slot>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()
const currentLocale = ref(locale.value)

watch(
  () => locale.value,
  (newVal) => {
    currentLocale.value = newVal
  },
)

const locales = [
  { value: 'en', label: 'EN' },
  { value: 'zh-HK', label: '中文' },
]

const setLocale = (lang) => {
  locale.value = lang
  currentLocale.value = lang
}

defineProps({
  brand: {
    type: String,
    default: 'CS Helper',
  },
  badgeText: {
    type: String,
    default: '',
  },
})
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
}
</style>
