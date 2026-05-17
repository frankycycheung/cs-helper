<template>
  <div class="main-content">
    <div>
        Hello {{name}}! 
        {{ $t('hello') }}
        <button @click="goToUpgradeNews">{{ $t('UpgradeNews') }}</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const name = ref('Sally')

const goToUpgradeNews = () => {
  router.push({ name: 'upgrade-news' })
}
</script>