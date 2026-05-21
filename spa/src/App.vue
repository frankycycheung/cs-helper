<template>
  <div>
    <Sidebar />
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import Sidebar from './components/Sidebar.vue'
</script>

<style scoped>
.main-content {
  margin-left: var(--sidebar-width, 200px);
  transition: margin-left 0.3s ease;
  min-height: 100vh;
  padding: 20px;
}

@media (max-width: 767px) {
  .main-content {
    margin-left: 0;
    padding: 15px;
  }
}
</style>
