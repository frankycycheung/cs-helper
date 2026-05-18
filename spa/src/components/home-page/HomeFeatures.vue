<template>
  <section class="home-features py-5 mb-4">
    <div class="container">
      <h2 class="section-title text-center mb-4">{{ $t('homePage.featuresTitle') }}</h2>

      <!-- Active: Upgrade News Generator row -->
      <div class="row row-cols-1 row-cols-md-3 g-4 mb-4">
        <!-- Active Feature -->
        <div class="col">
          <div class="card h-100 border-0 shadow-sm custom-card hover-lift">
            <div class="card-body p-4 d-flex flex-column h-100">
              <div class="d-flex align-items-center gap-3 mb-3">
                <div
                  class="feature-badge-icon bg-custom-pink text-white rounded-3 d-flex align-items-center justify-content-center flex-shrink-0"
                >
                  <svg
                    width="28"
                    height="28"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="1.8"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                    <polyline points="14 2 14 8 20 8" />
                    <line x1="16" y1="13" x2="8" y2="13" />
                    <line x1="16" y1="17" x2="8" y2="17" />
                    <polyline points="10 9 9 9 8 9" />
                  </svg>
                </div>
                <h5 class="card-title fw-bold text-dark mb-0">
                  {{ $t('homePage.featuresMainTitle') }}
                </h5>
              </div>
              <p class="card-text text-muted small mb-3 flex-grow-1">
                {{ $t('homePage.featuresMainDesc') }}
              </p>
              <div class="feature-tags mb-3">
                <span class="badge bg-custom-pink text-white me-1">{{
                  $t('homePage.featuresTags.bilingual')
                }}</span>
                <span class="badge bg-custom-pink text-white me-1">{{
                  $t('homePage.featuresTags.modules')
                }}</span>
                <span class="badge bg-custom-pink text-white me-1">{{
                  $t('homePage.featuresTags.structured')
                }}</span>
                <span class="badge bg-custom-pink text-white">{{
                  $t('homePage.featuresTags.warnings')
                }}</span>
              </div>
              <router-link to="/upgrade-news" class="btn btn-custom-primary w-100 mt-auto">
                {{ $t('homePage.getStarted') }}
              </router-link>
            </div>
          </div>
        </div>

        <!-- Coming Soon -->
        <div class="col">
          <div class="card h-100 border-0 shadow-sm custom-card coming-soon-card">
            <div class="card-body p-4 d-flex flex-column h-100">
              <span
                class="badge bg-custom-pink text-white mb-3 align-self-start"
                style="width: fit-content"
                >{{ $t('homePage.comingSoon') }}</span
              >
              <h5 class="card-title fw-semibold text-dark mb-2">
                {{ $t('homePage.comingSoonTitle') }}
              </h5>
              <p class="card-text text-muted small flex-grow-1">
                {{ $t('homePage.comingSoonText') }}
              </p>
              <button class="btn btn-outline-custom-pink w-100 mt-auto" disabled>
                {{ $t('homePage.comingSoon') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup></script>

<style scoped>
.feature-badge-icon {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  flex-shrink: 0;
}

.feature-tags .badge {
  font-size: 0.75rem;
  font-weight: 500;
}

.coming-soon-card {
  border: 1px dashed #ff9999;
}

.hover-lift {
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 30px rgba(223, 190, 200, 0.2) !important;
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

.btn-outline-custom-pink {
  border: 2px solid #ff9999;
  color: #ff9999;
  background-color: transparent;
  border-radius: 50px;
  transition: all 0.3s ease;
}
.btn-outline-custom-pink:hover {
  border-color: #ff69b4;
  color: #ff69b4;
  background-color: rgba(255, 153, 153, 0.1);
  transform: scale(1.03);
}
.btn-custom-primary:hover {
  background-color: #9575cd; /* Darker violet on hover */
  border-color: #9575cd;
  transform: scale(1.03);
  box-shadow: 0 5px 15px rgba(179, 157, 219, 0.4);
}

.btn-outline-custom-pink {
  border: 2px solid #b39ddb;
  color: #b39ddb;
  background-color: transparent;
  border-radius: 50px;
  transition: all 0.3s ease;
}
.btn-outline-custom-pink:hover {
  border-color: #9575cd;
  color: #9575cd;
  background-color: rgba(179, 157, 219, 0.1);
  transform: scale(1.03);
}
</style>
