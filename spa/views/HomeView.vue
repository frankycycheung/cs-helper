<template>
  <main class="home-view">
    <HomeHero />
    <HomeValues />
    <HomeFeatures />
  </main>
</template>

<script setup>
import HomeHero from '../src/components/home-page/HomeHero.vue'
import HomeValues from '../src/components/home-page/HomeValues.vue'
import HomeFeatures from '../src/components/home-page/HomeFeatures.vue'
</script>

<style scoped>
.home-view {
  min-height: 100vh;
}

.hero-banner {
  margin-left: 20px;
  margin-right: 20px;
}

.hero-banner .container {
  max-width: 1140px;
}
</style>
