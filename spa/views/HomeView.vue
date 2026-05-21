<template>
  <main class="home-view">
    <AnnouncementBanner :message=message />
    <HomeHero />
    <HomeValues />
    <HomeFeatures />
  </main>
</template>

<script setup>
import AnnouncementBanner from '../src/components/home-page/AnnouncementBanner.vue'
import HomeHero from '../src/components/home-page/HomeHero.vue'
import HomeValues from '../src/components/home-page/HomeValues.vue'
import HomeFeatures from '../src/components/home-page/HomeFeatures.vue'
import { ref } from 'vue'

const message = ref("BB我去印尼喇~會掛住你💖")
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
