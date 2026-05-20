<template>
  <div
    ref="containerRef"
    class="emoji-floating-container"
    @mousemove="onMouseMove"
    @mouseleave="onMouseLeave"
    @mouseenter="onMouseEnter"
  >
    <!-- floating emojis -->
    <span v-for="emoji in emojis" :key="emoji.id" class="floating-emoji" :style="emoji.style">{{
      emoji.char
    }}</span>

    <!-- add bar -->
    <div class="emoji-add-bar">
      <input
        ref="inputRef"
        v-model="newEmojiText"
        type="text"
        class="emoji-input"
        :placeholder="$t('emoji.addPlaceholder')"
        @keyup.enter="addEmoji"
      />
      <button class="emoji-add-btn" type="button" @click="addEmoji">
        <svg class="emoji-add-btn__icon" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path
            d="M10 3a1 1 0 0 1 1 1v5h5a1 1 0 1 1 0 2h-5v5a1 1 0 1 1-2 0v-5H4a1 1 0 1 1 0-2h5V4a1 1 0 0 1 1-1z"
          />
        </svg>
        <span>{{ $t('emoji.addButton') }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onBeforeUnmount } from 'vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => ['✨', '💖', '🍀', '🌸', '🌼'],
  },
})

const emit = defineEmits(['update:modelValue'])

const inputRef = ref(null)
const containerRef = ref(null)
const newEmojiText = ref('')

const areaW = ref(400)
const areaH = ref(200)

const mouse = reactive({
  x: -9999,
  y: -9999,
  active: false,
})

const emojis = reactive([])

const ANCHOR_PCTS = [
  { px: 7, py: 8 },
  { px: 72, py: 14 },
  { px: 18, py: 52 },
  { px: 65, py: 38 },
  { px: 38, py: 80 },
]

let emojiIdCounter = 0

// ── physics constants ────────────────────────────────────────────────────
const DAMPING = 0.88 // velocity decay per frame
const SPRING_K = 2.8 // fraction-of-container spring pull (1/s)
const DRIFT_AMP_PX = 9 // natural Lissajous wander amplitude (px)
const SPEED_CAP = 110 // max px/s
const REPEL_STR = 30 // base repel scale
const EMOJI_R = 22 // assumed collision radius (px) ≈ 44 px width
const PAD = 28 // min px distance from wall edge
// ───────────────────────────────────────────────────────────────────────────

function dist(a, b) {
  return Math.hypot(a.x - b.x, a.y - b.y)
}

function normalize(vx, vy) {
  const d = Math.hypot(vx, vy) || 1
  return [vx / d, vy / d]
}

function initEmojis() {
  emojis.length = 0
  ANCHOR_PCTS.forEach((p, i) => {
    const seed = Math.random() * Math.PI * 2
    emojis.push({
      id: emojiIdCounter++,
      char: props.modelValue[i],
      anchorX: (p.px / 100) * areaW.value,
      anchorY: (p.py / 100) * areaH.value,
      x: (p.px / 100) * areaW.value,
      y: (p.py / 100) * areaH.value,
      vx: (Math.random() - 0.5) * 18,
      vy: (Math.random() - 0.5) * 18,
      driftPhase: Math.random() * Math.PI * 2,
      driftAmp: DRIFT_AMP_PX,
      seed,
      style: { left: '0px', top: '0px' },
    })
  })
}

/**
 * Random candidate positions within a dense circular disk.
 * Returns a candidate {x,y} that is at least 2*EMOJI_R away from every
 * existing emoji in `emojis`. Returns null if none found after `n` tries.
 */
function scanDisk(emojis, w, h, n = 180) {
  const cx = w / 2
  const cy = h / 2
  const rx = w / 2 - PAD // inner-circle half-width
  const ry = h / 2 - PAD

  if (rx < EMOJI_R || ry < EMOJI_R) return null

  for (let i = 0; i < n; i++) {
    // rej-fraction sampling → uniform disk by rejection
    let px, py
    for (let retry = 0; retry < 12; retry++) {
      px = cx + (Math.random() * 2 - 1) * rx
      py = cy + (Math.random() * 2 - 1) * ry
      if (((px - cx) / rx) ** 2 + ((py - cy) / ry) ** 2 <= 1) break
    }
    if (emojis.every((e) => dist(e, { x: px, y: py }) >= EMOJI_R * 2)) return { x: px, y: py }
  }
  return null
}

/**
 * Expand candidate list by a low-res grid in expanded bounds.
 */
function scanGrid(emojis, w, h) {
  const P = EMOJI_R + 2
  const xMin = P,
    xMax = w - P
  const yMin = P,
    yMax = h - P
  if (xMin >= xMax || yMin >= yMax) return null

  const best = { x: 0, y: 0, minGap: -Infinity }

  for (let x = xMin; x <= xMax; x += (xMax - xMin) / 8) {
    for (let y = yMin; y <= yMax; y += (yMax - yMin) / 8) {
      const minGap = Math.min(...emojis.map((e) => dist(e, { x, y }) - EMOJI_R * 2))
      if (minGap > best.minGap) {
        best.x = x
        best.y = y
        best.minGap = minGap
      }
    }
  }
  return best.minGap >= 0 ? { x: best.x, y: best.y } : null
}

function findFreeSpot(emojis, w, h) {
  let spot = scanDisk(emojis, w, h)
  if (spot != null) return spot

  spot = scanGrid(emojis, w, h)
  if (spot != null) return spot

  // last resort: push toward nearest free diagonal from centre
  const cx = w / 2,
    cy = h / 2
  return {
    x: Math.min(w - PAD, Math.max(PAD, cx + (Math.random() - 0.5) * w * 0.3)),
    y: Math.min(h - PAD, Math.max(PAD, cy + (Math.random() - 0.5) * h * 0.3)),
  }
}

function applyDrift(e, dt) {
  e.driftPhase += dt * 0.65
  const d =
    Math.sin(e.driftPhase + e.seed) * Math.cos(e.driftPhase * 0.57 + e.seed * 2.1) * e.driftAmp
  e.vx += d * dt * 0.38

  // slow lateral sweep so the path isn't a closed loop
  // halve sweep when idle so natural drift alone sets the upper speed
  e.vx += (Math.random() - 0.5) * (mouse.active ? 0.0009 : 0.0) * dt * 120

  // decay + counter-decay: keeps drift energy alive without net collateral
  e.vx *= 1 - dt * 1.18
  e.vx += d * dt * 0.38
}

function applyRepel(e, dt) {
  if (!mouse.active) return

  const [ux, uy] = normalize(e.x - mouse.x, e.y - mouse.y)
  const r = dist(e, mouse)
  if (r < 14 || r > Math.min(areaW.value, areaH.value) * 0.55) return

  const proximity = Math.max(0, 1 - r / 220)
  const mouseSpeed = Math.hypot(mouse.vx, mouse.vy)
  const force = proximity * REPEL_STR * (0.18 + mouseSpeed * 0.28 + 0.12 * (220 / (r + 20)))

  e.vx += ux * force * dt
  e.vy += uy * force * dt
}

function applySpring(e, dt) {
  if (!mouse.active) return

  const maxDim = Math.max(areaW.value, areaH.value) || 1
  const pullX = ((e.anchorX - e.x) / maxDim) * SPEED_CAP * SPRING_K * dt
  const pullY = ((e.anchorY - e.y) / maxDim) * SPEED_CAP * SPRING_K * dt

  e.vx += pullX
  e.vy += pullY
  e.vx *= DAMPING
  e.vy *= DAMPING
}

function tickFrame(time) {
  const elapsed = Math.min(time - lastTime, 0.05)
  lastTime = time
  const dt = elapsed

  mouse.vx = mouse.x - mousePrevX.value
  mouse.vy = mouse.y - mousePrevY.value
  mousePrevX.value = mouse.x
  mousePrevY.value = mouse.y

  for (const e of emojis) {
    applyDrift(e, dt)
    applyRepel(e, dt)
    applySpring(e, dt)

    e.x += e.vx * dt
    e.y += e.vy * dt

    // speed cap — convert SPEED_CAP (px/s) → px/frame
    // idle runs at ~100 px/s (still gently drifting), active at full SPEED_CAP
    const IDLE_SPD = 100
    const spdCap = (mouse.active ? SPEED_CAP : IDLE_SPD) / 60
    const spd = Math.hypot(e.vx, e.vy)
    if (spd > spdCap) {
      const s = spdCap / spd
      e.vx *= s
      e.vy *= s
    }

    // wall collision with outward nudge
    if (e.x <= 0) {
      e.x = 0
      e.vx = Math.abs(e.vx) + 3
    }
    if (e.x >= areaW.value - 1) {
      e.x = areaW.value - 1
      e.vx = -Math.abs(e.vx) - 3
    }
    if (e.y <= 0) {
      e.y = 0
      e.vy = Math.abs(e.vy) + 3
    }
    if (e.y >= areaH.value - 1) {
      e.y = areaH.value - 1
      e.vy = -Math.abs(e.vy) - 3
    }

    e.style.left = `${e.x}px`
    e.style.top = `${e.y}px`
  }

  rafId = requestAnimationFrame(tickFrame)
}

function onResize() {
  const el = containerRef.value
  if (!el) return
  const rect = el.getBoundingClientRect()
  areaW.value = rect.width
  areaH.value = rect.height
  emojis.forEach((e, i) => {
    const p = ANCHOR_PCTS[i] || ANCHOR_PCTS[0]
    e.anchorX = (p.px / 100) * areaW.value
    e.anchorY = (p.py / 100) * areaH.value
  })
}

function onMouseMove(e) {
  mouse.active = true
  const rect = containerRef.value.getBoundingClientRect()
  mouse.x = Math.max(0, Math.min(areaW.value, e.clientX - rect.left))
  mouse.y = Math.max(0, Math.min(areaH.value, e.clientY - rect.top))
}

function onMouseLeave() {
  mouse.active = false
  mouse.x = -9999
  mouse.y = -9999
}

function onMouseEnter(e) {
  const rect = containerRef.value.getBoundingClientRect()
  mouse.x = e.clientX - rect.left
  mouse.y = e.clientY - rect.top
  mouse.active = true
}

function addEmoji() {
  const char = newEmojiText.value.trim()
  if (!char) return

  const { x, y } = findFreeSpot(emojis, areaW.value, areaH.value)

  emojis.push({
    id: emojiIdCounter++,
    char,
    anchorX: x,
    anchorY: y,
    x,
    y,
    vx: (Math.random() - 0.5) * 22,
    vy: (Math.random() - 0.5) * 22,
    driftPhase: Math.random() * Math.PI * 2,
    driftAmp: DRIFT_AMP_PX,
    seed: Math.random() * Math.PI * 2,
    style: { left: `${x}px`, top: `${y}px` },
  })

  emit(
    'update:modelValue',
    emojis.map((e) => e.char),
  )
  newEmojiText.value = ''
  inputRef.value?.focus()
}

// ── lifecycle ─────────────────────────────────────────────────────────
let rafId
let lastTime = 0
const mousePrevX = ref(0)
const mousePrevY = ref(0)

onBeforeUnmount(() => {
  cancelAnimationFrame(rafId)
  window.removeEventListener('resize', onResize)
})

initEmojis()
rafId = requestAnimationFrame(tickFrame)
window.addEventListener('resize', onResize)
onResize()
</script>

<style scoped>
.emoji-floating-container {
  position: relative;
  height: 100%;
  min-height: 200px;
  cursor: default;
  user-select: none;
  border-radius: 14px;
  overflow: hidden;
}

.floating-emoji {
  position: absolute;
  font-size: 2rem;
  pointer-events: none;
  z-index: 1;
  will-change: transform;
}

/* ── add bar ─────────────────────────────────────────────────────── */
.emoji-add-bar {
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 5px;
  align-items: center;
  z-index: 10;
  padding: 3px 6px 3px 10px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.89);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  box-shadow: 0 2px 10px rgba(180, 130, 160, 0.18);
}

.emoji-input {
  width: 90px;
  min-width: 0;
  height: 26px;
  padding: 0 8px;
  font-size: 0.78rem;
  font-family: inherit;
  border: 1.5px solid #f0c4d2;
  border-radius: 18px;
  outline: none;
  background: transparent;
  color: #444;
  transition:
    border-color 0.18s ease,
    box-shadow 0.18s ease,
    width 0.18s ease;
}

.emoji-input:focus {
  border-color: #ff85a2;
  box-shadow: 0 0 0 2.5px rgba(255, 135, 162, 0.18);
  width: 130px;
}

.emoji-input::placeholder {
  color: #c5a0b4;
}

.emoji-input--error {
  animation: shake 0.36s ease-in-out;
  border-color: #e0556a;
}

@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }
  20% {
    transform: translateX(-5px);
  }
  40% {
    transform: translateX(5px);
  }
  60% {
    transform: translateX(-4px);
  }
  80% {
    transform: translateX(4px);
  }
}

.emoji-add-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  height: 26px;
  padding: 0 10px;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  border: 1.5px solid transparent;
  border-radius: 18px;
  background: #ffc2d1;
  color: #7b1a35;
  cursor: pointer;
  white-space: nowrap;
  transition:
    background-color 0.18s ease,
    border-color 0.18s ease,
    transform 0.18s ease,
    box-shadow 0.18s ease;
  user-select: none;
  -webkit-user-select: none;
}

.emoji-add-btn:hover {
  background: #ffb3c6;
  border-color: #ffa0b8;
  transform: scale(1.04);
  box-shadow: 0 3px 10px rgba(255, 133, 162, 0.32);
}

.emoji-add-btn:active {
  transform: scale(0.97);
  box-shadow: none;
}

.emoji-add-btn__icon {
  width: 12px;
  height: 12px;
  flex-shrink: 0;
}
</style>
