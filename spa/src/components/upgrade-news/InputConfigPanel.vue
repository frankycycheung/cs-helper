<template>
  <div class="card h-100">
    <div class="card-header">
      <h5 class="mb-0">{{ $t('upgradeNews.configTitle') }}</h5>
    </div>
    <div class="card-body">
      <div class="mb-3">
        <label class="form-label">{{ $t('upgradeNews.moduleLabel') }}</label>
        <select class="form-select form-control-pill" v-model="localModule">
          <option value="">{{ $t('upgradeNews.modulePlaceholder') }}</option>
          <option v-for="module in moduleLabel" :key="module.id" :value="module.id">
            {{ module.label }}
          </option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label">{{ $t('upgradeNews.featureTitleLabel') }}</label>
        <input type="text" class="form-control" placeholder="" v-model="localFeatureTitle" />
      </div>

      <div class="mb-3">
        <label class="form-label">{{ $t('upgradeNews.rawInputLabel') }}</label>
<textarea
           class="form-control"
           rows="4"
           placeholder=""
           v-model="localDescription"
         ></textarea>
         <button class="btn btn-pill btn-primary btn-sm mt-2" @click="polishWithAI" :disabled="isPolishing">
           <i class="bi bi-magic"></i>{{ isPolishing ? $t('upgradeNews.btnAiLoading') : $t('upgradeNews.btnAi') }}
         </button>
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">{{ $t('upgradeNews.pathWebLabel') }}</label>
        <div class="btn-group btn-group-sm mb-3" role="group">
          <button
            type="button"
            class="btn btn-pill"
            :class="pathInputMode === 'manual' ? 'btn-primary' : 'btn-outline-primary'"
            @click="pathInputMode = 'manual'"
          >
            {{ $t('upgradeNews.pathModeManual') }}
          </button>
          <button
            type="button"
            class="btn btn-pill"
            :class="pathInputMode === 'smart' ? 'btn-primary' : 'btn-outline-primary'"
            @click="pathInputMode = 'smart'"
          >
            {{ $t('upgradeNews.pathModeSmart') }}
          </button>
        </div>

        <template v-if="pathInputMode === 'manual'">
          <div class="input-group input-group-sm mb-2">
            <span class="input-group-text">{{ $t('upgradeNews.webPathPrefix') }}</span>
            <input
              type="text"
              class="form-control"
              :placeholder="$t('upgradeNews.pathWebPlaceholder')"
              v-model="manualWebPath"
            />
          </div>
          <div class="input-group input-group-sm">
            <span class="input-group-text">{{ $t('upgradeNews.appPathPrefix') }}</span>
            <input
              type="text"
              class="form-control"
              :placeholder="$t('upgradeNews.pathAppPlaceholder')"
              v-model="manualAppPath"
            />
          </div>
        </template>

        <template v-else>
          <textarea
            class="form-control"
            rows="4"
            :placeholder="$t('upgradeNews.pathSmartPlaceholder')"
            v-model="rawPathTextBlock"
          ></textarea>
          <button
            type="button"
            class="btn btn-pill btn-primary btn-sm mt-2"
            @click="extractPathsFromBlock"
          >
            {{ $t('upgradeNews.btnExtractPaths') }}
          </button>
        </template>
      </div>

      <div class="mb-3">
        <label class="form-label text-muted">{{ $t('upgradeNews.remarksLabel') }}</label>
        <textarea
          class="form-control bg-light"
          rows="3"
          placeholder=""
          v-model="localRemarks"
        ></textarea>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

const eClassModules = [
  { id: 'eNotice', zh: 'eNotice 電子通告系統', en: 'eNotice Electronic Notice' },
  { id: 'eEnrolment', zh: 'eEnrolment 課外活動管理', en: 'eEnrolment Activities Management' },
  { id: 'KPM', zh: 'KPM 學校表現評量', en: 'KPM Key Performance Measures' },
  { id: 'iPortfolio', zh: 'iPortfolio 學生學習概覽', en: 'iPortfolio Student Profile' },
  { id: 'eAttendance', zh: 'eAttendance 考勤系統', en: 'eAttendance Attendance System' },
  { id: 'eSports', zh: 'eSports 運動會管理系統', en: 'eSports Sports Day Management' },
  { id: 'eHomework', zh: 'eHomework 家課表', en: 'eHomework Homework Diary' },
  { id: 'staffAttendance', zh: 'Staff Attendance 職員考勤', en: 'Staff Attendance System' },
  { id: 'incentive', zh: 'Incentive Scheme 學生獎勵計劃', en: 'Incentive Scheme Reward Program' },
  { id: 'groupMessage', zh: 'Group Message 小組訊息', en: 'Group Message System' },
]

const moduleLabel = computed(() => {
  return eClassModules.map((m) => ({
    id: m.id,
    label: locale.value === 'en' ? m.en : m.zh,
  }))
})

const props = defineProps({
  model: {
    type: Object,
    default: () => ({
      module: '',
      featureTitle: '',
      description: '',
      usagePath: { web: '', app: '' },
      remarks: '',
    }),
  },
})

const emit = defineEmits(['update:model'])

const localModule = ref(props.model.module)
const localFeatureTitle = ref(props.model.featureTitle)
const localDescription = ref(props.model.description)

const pathInputMode = ref('manual')
const manualWebPath = ref('')
const manualAppPath = ref('')
const rawPathTextBlock = ref('')
const localRemarks = ref(props.model.remarks)
const isPolishing = ref(false)

const polishWithAI = async () => {
  if (!localDescription.value.trim()) return

  isPolishing.value = true
  try {
    const response = await fetch('/api/upgrade_news/polish', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        description: localDescription.value,
        module: localModule.value
      })
    })
    const data = await response.json()
    if (data.status === 'success') {
      localDescription.value = data.reply
    } else {
      alert(data.message || 'AI polish failed')
    }
  } catch (error) {
    alert('Failed to connect to AI service')
  } finally {
    isPolishing.value = false
  }
}

watch([localModule, localFeatureTitle, localDescription], () => {
  emit('update:model', {
    module: localModule.value,
    featureTitle: localFeatureTitle.value,
    description: localDescription.value,
    usagePath: {
      web: manualWebPath.value.trim(),
      app: manualAppPath.value.trim(),
    },
    remarks: localRemarks.value,
  })
})

watch([manualWebPath, manualAppPath], () => {
  emit('update:model', {
    module: localModule.value,
    featureTitle: localFeatureTitle.value,
    description: localDescription.value,
    usagePath: {
      web: manualWebPath.value.trim(),
      app: manualAppPath.value.trim(),
    },
    remarks: localRemarks.value,
  })
})

watch(localRemarks, () => {
  emit('update:model', {
    module: localModule.value,
    featureTitle: localFeatureTitle.value,
    description: localDescription.value,
    usagePath: {
      web: manualWebPath.value.trim(),
      app: manualAppPath.value.trim(),
    },
    remarks: localRemarks.value,
  })
})

const extractPathsFromBlock = () => {
  const block = rawPathTextBlock.value || ''
  const webMatch = block.match(
    /(?:網頁版使用路徑[：:]\s*|Web[^\n]*?(?:使用路徑|Usage Path)[：:]\s*)([\s\S]*?)(?:\n|$)/i,
  )
  const appMatch = block.match(
    /(?:App 使用路徑[：:]\s*|eClass[\s\w]*?Teacher\s*App[\s\w]*?(?:使用路徑|Usage Path)[：:]\s*|Teacher\s*App[^\n]*?(?:使用路徑|Usage Path)[：:]\s*|filter[：:]\s*)([\s\S]*?)(?:\n|$)/i,
  )

  manualWebPath.value = webMatch ? webMatch[1].trim() : ''
  manualAppPath.value = appMatch ? appMatch[1].trim() : ''

  rawPathTextBlock.value = ''
  pathInputMode.value = 'manual'
}
</script>

<style scoped>
.form-control-pill {
  border-radius: 50px !important;
}

.input-group-text {
  border-radius: 12px 0 0 12px !important;
}

.card-body textarea.form-control {
  resize: vertical;
}
</style>
