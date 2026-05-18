<template>
  <section class="hero-section p-5 rounded-5 mb-4">
    <div class="container">
      <div class="row align-items-center g-4">
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
        <div class="col-md-6 text-center">
          <div class="emoji-float">
            <span class="emoji">✨</span>
            <span class="emoji">💖</span>
            <span class="emoji">🍀</span>
            <span class="emoji">🌸</span>
            <span class="emoji">🌼</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup></script>

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

.hero-section .emoji-float {
  position: relative;
  height: 200px;
}

.hero-section .emoji {
  position: absolute;
  font-size: 2rem;
  animation: float 3s ease-in-out infinite;
}

.hero-section .emoji:nth-child(1) {
  top: 10%;
  left: 5%;
  animation-delay: 0s;
}
.hero-section .emoji:nth-child(2) {
  top: 30%;
  right: 10%;
  animation-delay: 1s;
}
.hero-section .emoji:nth-child(3) {
  bottom: 20%;
  left: 15%;
  animation-delay: 2s;
}
.hero-section .emoji:nth-child(4) {
  top: 50%;
  right: 5%;
  animation-delay: 0.5s;
}
.hero-section .emoji:nth-child(5) {
  bottom: 10%;
  left: 30%;
  animation-delay: 1.5s;
}

@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
  100% {
    transform: translateY(0px);
  }
}

.btn-custom-primary {
  background-color: #ff9999; /* Light pink */
  border-color: #ff9999;
  color: #fff;
  border-radius: 50px; /* Pill shape */
  transition: all 0.3s ease;
}
.btn-custom-primary:hover {
  background-color: #ff69b4; /* Hot Pink on hover */
  border-color: #ff69b4;
  transform: scale(1.03);
  box-shadow: 0 5px 15px rgba(255, 153, 153, 0.4);
}
.btn-custom-primary:hover {
  background-color: #9575cd; /* Darker violet on hover */
  border-color: #9575cd;
  transform: scale(1.03);
  box-shadow: 0 5px 15px rgba(179, 157, 219, 0.4);
}
</style>
