<template>
    <div>
        Hello {{name}}! 
        {{ t('hello') }}
    </div>
</template>

<script setup>
import { ref } from 'vue'

const name = ref('Sally')
</script>