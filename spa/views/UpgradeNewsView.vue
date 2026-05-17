<template>
  <div class="upgrade-news-view">
    <Header :badge-text="$t('UpgradeNews')" />
    <UpgradeNewsDashboard />
  </div>
</template>

<script setup>
import Header from '../src/components/common/Header.vue'
import UpgradeNewsDashboard from '../src/components/upgrade-news/UpgradeNewsDashboard.vue'
</script>

<style scoped>
.upgrade-news-view {
  min-height: 100vh;
  background-color: #f8f9fa;
}
</style>
