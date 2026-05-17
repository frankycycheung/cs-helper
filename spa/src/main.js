import { createApp } from 'vue'
import { createPinia } from 'pinia'
import i18n from './i18n'

import App from './App.vue'
import router from './router'

document.documentElement.style.setProperty('--sidebar-width', '200px')

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n)

app.config.globalProperties.$t = (key, ...args) => i18n.global.t(key, ...args)

app.mount('#app')
