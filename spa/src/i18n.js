import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import zhHK from './locales/zh-HK.json'

const messages = {
  en,
  'zh-HK': zhHK,
  zh: zhHK, // alias: resolve both 'zh' and 'zh-HK' to the same bundle
}

const i18n = createI18n({
  legacy: false,
  locale: 'zh-HK',
  fallbackLocale: 'zh-HK',
  missingWarn: false, // suppress noise while keys settle
  messages,
})

export default i18n
