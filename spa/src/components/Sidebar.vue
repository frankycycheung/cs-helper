<template>
  <button v-if="isMobile && !isOpen" class="mobile-open-btn" @click="isOpen = true" aria-label="Open menu">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <line x1="3" y1="12" x2="21" y2="12"></line>
      <line x1="3" y1="6" x2="21" y2="6"></line>
      <line x1="3" y1="18" x2="21" y2="18"></line>
    </svg>
  </button>
  <div v-if="isOpen && isMobile" class="sidebar-backdrop" @click="isOpen = false"></div>
  <nav class="sidebar" :class="{ collapsed: !isOpen, mobile: isMobile }">
    <button @click="isOpen = !isOpen" class="toggle-btn">
      <svg
        v-if="!isOpen"
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
      </svg>
      <svg
        v-else
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
      </svg>
    </button>
    <router-link to="/" class="sidebar-link" exact-active-class="active" @click="closeMobile">
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        class="link-icon"
      >
        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
      </svg>
      <span v-if="isOpen" class="link-text">{{ $t('home') }}</span>
    </router-link>
    <router-link to="/upgrade-news" class="sidebar-link" exact-active-class="active" @click="closeMobile">
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        class="link-icon"
      >
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14 2 14 8 20 8"></polyline>
      </svg>
      <span v-if="isOpen" class="link-text">{{ $t('UpgradeNews') }}</span>
    </router-link>
    <div class="locale-switcher" :class="{ collapsed: !isOpen }">
      <button
        v-for="lang in locales"
        :key="lang.value"
        :class="{ active: currentLocale === lang.value }"
        @click="setLocale(lang.value)"
        class="btn btn-pill btn-outline-secondary btn-sm me-1"
      >
        <span v-if="isOpen">{{ lang.label }}</span>
        <span v-else>{{ lang.label.charAt(0) }}</span>
      </button>
    </div>
  </nav>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
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

const isOpen = ref(true)
const isMobile = ref(false)

const closeMobile = () => {
  if (isMobile.value) {
    isOpen.value = false
  }
}

const checkMobile = () => {
  isMobile.value = window.innerWidth < 768
}

const updateSidebarWidth = () => {
  if (isMobile.value) {
    document.documentElement.style.setProperty('--sidebar-width', '0px')
  } else {
    document.documentElement.style.setProperty('--sidebar-width', isOpen.value ? '200px' : '100px')
  }
}

onMounted(() => {
  checkMobile()
  if (isMobile.value) {
    isOpen.value = false
  }
  updateSidebarWidth()
  window.addEventListener('resize', () => {
    checkMobile()
    updateSidebarWidth()
  })
})

watch(isOpen, updateSidebarWidth)
watch(isMobile, updateSidebarWidth)
</script>

<style scoped>
.mobile-open-btn {
  position: fixed;
  top: 12px;
  left: 12px;
  z-index: 1001;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background-color: #fff0f5;
  border: none;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  color: #333;
  transition: background-color 0.2s ease;
}

.mobile-open-btn:hover {
  background-color: rgba(255, 182, 193, 0.4);
}

.sidebar-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.4);
  z-index: 999;
}

.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 200px;
  height: 100vh;
  background-color: #fff0f5;
  padding: 20px 10px;
  box-shadow: 2px 0 10px rgba(223, 190, 200, 0.15);
  display: flex;
  flex-direction: column;
  gap: 15px;
  z-index: 1000;
  transition: width 0.3s ease, transform 0.3s ease;
  overflow: visible;
}

.sidebar.collapsed {
  width: 80px;
  padding: 20px 5px;
}

@media (max-width: 767px) {
  .sidebar.mobile {
    width: 250px;
    transform: translateX(0);
    box-shadow: 4px 0 20px rgba(0, 0, 0, 0.25);
  }

  .sidebar.mobile.collapsed {
    width: 250px;
    transform: translateX(-100%);
    box-shadow: none;
  }
}

.sidebar.collapsed .link-text {
  display: none;
}

.sidebar.collapsed .sidebar-link {
  justify-content: center;
}

.toggle-btn {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
  padding: 10px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #333;
  border-radius: 12px;
  transition: all 0.3s ease;
  width: 100%;
}

.sidebar.collapsed .toggle-btn {
  padding: 8px;
  justify-content: center;
}

.toggle-btn:hover {
  background-color: rgba(255, 182, 193, 0.2);
}

.btn-text {
  margin-left: 4px;
}

.sidebar-link {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 10px;
  text-decoration: none;
  color: #333;
  padding: 10px;
  border-radius: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
  width: 100%;
}

.sidebar-link:hover {
  background-color: rgba(255, 182, 193, 0.2);
  color: #ff9999;
}

.sidebar-link.active {
  background-color: #ff9999;
  color: white;
}

.link-icon {
  flex-shrink: 0;
  min-width: 18px;
  min-height: 18px;
}

.link-text {
  white-space: nowrap;
}

.locale-switcher {
  margin-top: auto;
  padding-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.sidebar.collapsed .locale-switcher {
  justify-content: center;
}

.locale-switcher .btn {
  padding: 4px 8px;
  font-size: 12px;
}
</style>
