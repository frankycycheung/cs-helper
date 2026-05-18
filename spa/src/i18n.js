import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import zhHK from './locales/zh-HK.json'

const messages = {
  en,
  'zh-HK': zhHK,
}

const i18n = createI18n({
  legacy: false,
  locale: 'zh-HK', // set locale
  fallbackLocale: 'zh-HK', // set fallback locale
  messages, // set locale messages
})

export default i18n
