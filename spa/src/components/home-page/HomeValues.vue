<template>
  <section class="home-values py-4">
    <div class="container">
      <h2 class="section-title text-center mb-4">{{ $t('homePage.sectionTitle') }}</h2>
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <!-- Card 1: Magic Translator -->
        <div class="col">
          <div class="card h-100 border-0 shadow-sm custom-card">
            <div class="card-body text-center p-4">
              <div class="card-icon mb-3">
                <span class="emoji-lg">🔮</span>
              </div>
              <h5 class="card-title fw-semibold text-dark mb-2">{{ $t('homePage.card1Title') }}</h5>
              <p class="card-text text-muted">{{ $t('homePage.card1Text') }}</p>
            </div>
          </div>
        </div>

        <!-- Card 2: Guardian Checklist -->
        <div class="col">
          <div class="card h-100 border-0 shadow-sm custom-card">
            <div class="card-body text-center p-4">
              <div class="card-icon mb-3">
                <span class="emoji-lg">🛡️</span>
              </div>
              <h5 class="card-title fw-semibold text-dark mb-2">{{ $t('homePage.card2Title') }}</h5>
              <p class="card-text text-muted">{{ $t('homePage.card2Text') }}</p>
            </div>
          </div>
        </div>

        <!-- Card 3: Smart Path Splitter -->
        <div class="col">
          <div class="card h-100 border-0 shadow-sm custom-card">
            <div class="card-body text-center p-4">
              <div class="card-icon mb-3">
                <span class="emoji-lg">🤖</span>
              </div>
              <h5 class="card-title fw-semibold text-dark mb-2">{{ $t('homePage.card3Title') }}</h5>
              <p class="card-text text-muted">{{ $t('homePage.card3Text') }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup></script>

<style scoped>
.section-title {
  color: #ff9999; /* Light pink for title */
  position: relative;
  display: inline-block;
  margin-bottom: 1.5rem;
}
.section-title::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 50px;
  height: 3px;
  background-color: #ff9999;
  border-radius: 2px;
}
.section-title::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 50px;
  height: 3px;
  background-color: #b39ddb;
  border-radius: 2px;
}

.custom-card {
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(223, 190, 200, 0.2);
  background-color: #fff;
  border: none;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}
.custom-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(223, 190, 200, 0.3);
}

.card-icon .emoji-lg {
  font-size: 3rem;
}
</style>
