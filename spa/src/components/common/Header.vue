<template>
  <nav class="navbar navbar-expand-lg navbar-light border-bottom">
    <div class="container-fluid">
      <a class="navbar-brand fw-bold" href="#">{{ brand }}</a>
      <span v-if="badgeText" class="badge bg-primary ms-2">{{ badgeText }}</span>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav ms-auto">
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
  z-index: 900;
  background: linear-gradient(135deg, #fff0f5 0%, #e6e6fa 100%);
}

@media (max-width: 767px) {
  .navbar .container-fluid {
    padding-left: 60px;
  }
}
</style>
