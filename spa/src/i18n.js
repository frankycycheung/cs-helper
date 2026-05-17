import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import zhHK from './locales/zh-HK.json'

const messages = {
  en,
  'zh-HK': zhHK,
}

const i18n = createI18n({
  legacy: false,
  locale: 'en', // set locale
  fallbackLocale: 'en', // set fallback locale
  messages, // set locale messages
})

export default i18n
