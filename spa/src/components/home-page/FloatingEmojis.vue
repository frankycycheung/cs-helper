<template>
  <div
    ref="containerRef"
    class="emoji-floating-container"
    @mousemove="onMouseMove"
    @mouseleave="onMouseLeave"
    @mouseenter="onMouseEnter"
  >
    <span v-for="emoji in emojis" :key="emoji.id" class="floating-emoji" :style="emoji.style">{{
      emoji.char
    }}</span>

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

// current mouse position (container-coords, −9999 when outside)
const mouse = reactive({ x: -9999, y: -9999, active: false })

// previous mouse position used to derive velocity each frame
const prevMouse = reactive({ x: -9999, y: -9999 })

const emojis = reactive([])

const ANCHOR_PCTS = [
  { px: 7, py: 8 },
  { px: 72, py: 14 },
  { px: 18, py: 52 },
  { px: 65, py: 38 },
  { px: 38, py: 80 },
]

let emojiIdCounter = 0

// ── physics constants ────────────────────────────────────────────────────────
const FRICTION = 0.995 // gentle per-frame velocity decay (coasting)
const SPRING_K = 1.5 // anchor pull strength (px/s²) per px displacement
const DRIFT_AMP = 22 // px peak-to-peak idle wander
const SPEED_CAP = 200 // px/s kinetic cap when mouse is active
const REPEL_R = 260 // px — max repel interaction range
const REPEL_STR = 120 // base force scale
const IDLE_SPD = 40 // px/s — relaxed drift when mouse is absent
const EMOJI_R = 22 // px — half the emoji collider radius
const PAD = 28 // px — min clamp distance from wall edge
// ────────────────────────────────────────────────────────────────────────────

function dist(a, b) {
  return Math.hypot(a.x - b.x, a.y - b.y)
}

function clamp(v, lo, hi) {
  return Math.max(lo, Math.min(hi, v))
}

// ── anchor / init ────────────────────────────────────────────────────────────

function initEmojis() {
  emojis.length = 0
  ANCHOR_PCTS.forEach((p) => {
    const seed = Math.random() * Math.PI * 2
    const ax = (p.px / 100) * areaW.value
    const ay = (p.py / 100) * areaH.value
    emojis.push({
      id: emojiIdCounter++,
      char: props.modelValue[emojis.length],
      anchorX: ax,
      anchorY: ay,
      x: ax,
      y: ay,
      vx: (Math.random() - 0.5) * 6,
      vy: (Math.random() - 0.5) * 6,
      phase: Math.random() * Math.PI * 2,
      seed,
      style: { transform: `translate3d(${ax}px, ${ay}px, 0)` },
    })
  })
}

// ── drift ─────────────────────────────────────────────────────────────────────

function applyDrift(e, dt) {
  // Lissajous figure: produces organic, non-repeating idle paths
  e.phase += dt * 0.55
  const wave = Math.sin(e.phase + e.seed) * Math.cos(e.phase * 0.573 + e.seed * 2.13) * DRIFT_AMP

  // thin curve: slowly drifts a slow irregular wandering movement
  e.vx += (Math.random() - 0.5) * 0.85 * dt

  // drift impulse — balanced by decay below so it neither explodes
  // nor fades away; the net energy added each frame is close to zero
  // but the path never repeats
  e.vx += wave * dt * 5.5
  e.vx *= 0.997 // very light per-frame decay
}

// ── mouse interaction ─────────────────────────────────────────────────────────

function applyRepel(e, dt, mSpeed) {
  if (!mouse.active) return

  const dx = e.x - mouse.x
  const dy = e.y - mouse.y
  const r = Math.hypot(dx, dy)
  if (r < 1 || r > REPEL_R) return

  // prox: 1 when mouse touches, 0 at outer edge of REPEL_R
  const prox = 1 - r / REPEL_R

  // radial repel away from cursor — stronger when close + when mouse is fast
  const force = prox * REPEL_STR * (1 + mSpeed * 0.15)
  e.vx += (dx / r) * force * dt
  e.vy += (dy / r) * force * dt
}

// ── anchor spring (gently pulls emojis back toward their home position) ──────

function applySpring(e, dt) {
  // Always apply gentle friction so emojis coast smoothly after being flung
  e.vx *= FRICTION
  e.vy *= FRICTION

  // Spring pull toward anchor — scales with distance so it's soft when close
  // and stronger when far away, giving a natural rubber-band feel
  const dx = e.anchorX - e.x
  const dy = e.anchorY - e.y
  const d = Math.hypot(dx, dy)

  // Only start pulling once the emoji has some distance from anchor
  if (d > 5) {
    // Stronger spring when mouse is gone so emojis eventually return home
    const k = mouse.active ? SPRING_K * 0.3 : SPRING_K
    e.vx += dx * k * dt
    e.vy += dy * k * dt
  }
}

// ── main loop ─────────────────────────────────────────────────────────────────

function tickFrame(time) {
  const dt = Math.min((time - lastTime) * 0.001, 0.05)
  lastTime = time

  // compute mouse velocity BEFORE overwriting prevMouse
  const mx = mouse.x,
    my = mouse.y
  const mSpeed = Math.hypot(mx - prevMouse.x, my - prevMouse.y) // px since last frame
  prevMouse.x = mx
  prevMouse.y = my

  for (const e of emojis) {
    // reset micro-velocity noise just once when mouse just left
    if (!mouse.active && Math.abs(e.vx) < 0.05 && Math.abs(e.vy) < 0.05) {
      /* still — no intervention; drift keeps them moving gently on its own */
    }

    applyDrift(e, dt)
    applyRepel(e, dt, mSpeed)
    applySpring(e, dt)

    // integrate: px/s * s = px
    e.x += e.vx * dt
    e.y += e.vy * dt

    // ── speed cap ────────────────────────────────────────────────────────
    const cap = mouse.active ? SPEED_CAP : IDLE_SPD // px/s (same unit as vx/vy)
    const spd = Math.hypot(e.vx, e.vy)
    if (spd > cap) {
      const s = cap / spd
      e.vx *= s
      e.vy *= s
    }

    // ── wall collision ────────────────────────────────────────────────────
    // gently nudge inward when an emoji bumps a boundary so it doesn't stick
    const nudge = 4
    if (e.x <= PAD) {
      e.x = PAD
      e.vx = Math.abs(e.vx) + nudge
    }
    if (e.x >= areaW.value - PAD) {
      e.x = areaW.value - PAD
      e.vx = -Math.abs(e.vx) - nudge
    }
    if (e.y <= PAD) {
      e.y = PAD
      e.vy = Math.abs(e.vy) + nudge
    }
    if (e.y >= areaH.value - PAD) {
      e.y = areaH.value - PAD
      e.vy = -Math.abs(e.vy) - nudge
    }

    // compose as a single GPU-layer transform — no layout/repaint
    e.style.transform = `translate3d(${e.x}px, ${e.y}px, 0)`
  }

  rafId = requestAnimationFrame(tickFrame)
}

// ── mouse helpers ─────────────────────────────────────────────────────────────

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
  // flush prev BEFORE writing new so tickFrame sees a real incremental delta
  prevMouse.x = mouse.x
  prevMouse.y = mouse.y
  mouse.x = clamp(e.clientX - rect.left, 0, areaW.value)
  mouse.y = clamp(e.clientY - rect.top, 0, areaH.value)
}

function onMouseLeave() {
  mouse.active = false
  // prevMouse stays where the mouse was; delta will read 0 next frame = no spike
}

function onMouseEnter(e) {
  const rect = containerRef.value.getBoundingClientRect()
  mouse.x = clamp(e.clientX - rect.left, 0, areaW.value)
  mouse.y = clamp(e.clientY - rect.top, 0, areaH.value)
  prevMouse.x = mouse.x // ← AFTER writes, so next tickFrame sees 0 velocity
  prevMouse.y = mouse.y
  mouse.active = true
}

// ── add emoji ─────────────────────────────────────────────────────────────────

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
    vx: (Math.random() - 0.5) * 6,
    vy: (Math.random() - 0.5) * 6,
    phase: Math.random() * Math.PI * 2,
    seed: Math.random() * Math.PI * 2,
    style: { transform: `translate3d(${x}px, ${y}px, 0)` },
  })

  emit(
    'update:modelValue',
    emojis.map((e) => e.char),
  )
  newEmojiText.value = ''
  inputRef.value?.focus()
}

/**
 * scanDisk / scanGrid / findFreeSpot — unchanged placement helpers
 */
function scanDisk(emojis, w, h, n = 180) {
  const cx = w / 2,
    cy = h / 2
  const rx = w / 2 - PAD,
    ry = h / 2 - PAD
  if (rx < EMOJI_R || ry < EMOJI_R) return null
  for (let i = 0; i < n; i++) {
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

function scanGrid(emojis, w, h) {
  const P = EMOJI_R + 2
  const xMin = P,
    xMax = w - P,
    yMin = P,
    yMax = h - P
  if (xMin >= xMax || yMin >= yMax) return null
  const best = { x: 0, y: 0, gap: -Infinity }
  for (let x = xMin; x <= xMax; x += (xMax - xMin) / 9) {
    for (let y = yMin; y <= yMax; y += (yMax - yMin) / 9) {
      const gap = Math.min(...emojis.map((e) => dist(e, { x, y }) - EMOJI_R * 2))
      if (gap > best.gap) {
        best.x = x
        best.y = y
        best.gap = gap
      }
    }
  }
  return best.gap >= 0 ? { x: best.x, y: best.y } : null
}

function findFreeSpot(emojis, w, h) {
  let spot = scanDisk(emojis, w, h)
  if (spot) return spot
  spot = scanGrid(emojis, w, h)
  if (spot) return spot
  const cx = w / 2,
    cy = h / 2
  return {
    x: clamp(cx + (Math.random() - 0.5) * w * 0.3, PAD, w - PAD),
    y: clamp(cy + (Math.random() - 0.5) * h * 0.3, PAD, h - PAD),
  }
}

// ── lifecycle ─────────────────────────────────────────────────────────────────

let rafId
let lastTime = 0

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
  /* transform-driven animation — no layout/repaint between frames */
  will-change: transform;
  top: 0;
  left: 0;
}

/* ── add bar ───────────────────────────────────────────────────────────────── */

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
  background: rgba(255, 255, 255, 0.9);
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
