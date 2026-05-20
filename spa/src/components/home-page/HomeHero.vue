<template>
  <section class="hero-section p-5 rounded-5 mb-4">
    <div class="container">
      <div class="row g-4">
        <!-- Left Column: Text content -->
        <div class="col-md-6">
          <span class="badge bg-custom-pink text-white mb-3 d-inline-block">{{
            $t('homePage.badge')
          }}</span>
          <h1 class="display-5 fw-bold text-dark mb-3">{{ $t('homePage.heroTitle') }}</h1>
          <p class="lead text-muted mb-4">{{ $t('homePage.heroSubtitle') }}</p>
          <router-link to="/upgrade-news" class="btn btn-custom-primary btn-lg px-4 py-2 me-2">{{
            $t('homePage.ctaBtn')
          }}</router-link>
        </div>

        <!-- Right Column: Decorative emojis -->
        <div class="col-md-6">
          <FloatingEmojis />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import FloatingEmojis from './FloatingEmojis.vue'
</script>

<style scoped>
.hero-section {
  background: linear-gradient(
    135deg,
    #fff0f5 0%,
    #e6e6fa 100%
  ); /* Soft pink to lavender gradient */
  border-radius: 20px;
  position: relative;
  overflow: hidden;
}

.hero-section .btn-custom-primary:hover {
  background-color: #ff69b4; /* Hot Pink on hover */
  border-color: #ff69b4;
  transform: scale(1.03);
  box-shadow: 0 5px 15px rgba(255, 153, 153, 0.4);
}
</style>
