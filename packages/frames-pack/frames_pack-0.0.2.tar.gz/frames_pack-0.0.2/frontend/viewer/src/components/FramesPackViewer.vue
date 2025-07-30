<template>
  <div id="layout">
    <div id="left-panel">
      <div id="map" />
      <div id="threejs" />
    </div>
    <div id="right-panel">
      <v-card
        class="ma-2 pa-4"
        elevation="2"
      >
        <v-card-title class="text-h6 pa-2">
          FramesPack Viewer
        </v-card-title>

        <v-card-text>
          <div class="text-caption mb-2">
            {{ status }}
          </div>

          <div
            v-if="!framesPackReady"
            class="text-center py-4"
          >
            <v-progress-circular
              indeterminate
              color="primary"
            />
            <div class="mt-2">
              {{ framesPackMessage }}
            </div>
          </div>

          <div v-else>
            <!-- Frame Index Slider -->
            <v-slider
              v-model="frameIndex"
              :min="frameIndexMin"
              :max="frameIndexMax"
              :step="1"
              thumb-label
              hide-details
              class="mb-4"
              @update:model-value="onFrameIndexChange"
            >
              <template #prepend>
                <v-text-field
                  v-model.number="frameIndex"
                  label="Frame"
                  density="compact"
                  type="number"
                  :min="frameIndexMin"
                  :max="frameIndexMax"
                  prefix="#"
                  hide-details
                  single-line
                  style="width: 100px;"
                  @blur="validateFrameIndex"
                  @keyup.enter="validateFrameIndex"
                />
              </template>
            </v-slider>

            <!-- Timestamp -->
            <v-text-field
              v-model.number="currentTs"
              label="Timestamp"
              density="compact"
              type="number"
              suffix="s"
              hide-details
              single-line
              readonly
              class="mb-2"
            />

            <!-- Position -->
            <v-row dense>
              <v-col cols="6">
                <v-text-field
                  :model-value="currentPos[0].toFixed(6)"
                  label="Longitude"
                  density="compact"
                  readonly
                  hide-details
                />
              </v-col>
              <v-col cols="6">
                <v-text-field
                  :model-value="currentPos[1].toFixed(6)"
                  label="Latitude"
                  density="compact"
                  readonly
                  hide-details
                />
              </v-col>
            </v-row>

            <!-- Yaw -->
            <v-text-field
              :model-value="`${currentYaw.toFixed(3)} (${(currentYaw * 180 / Math.PI).toFixed(1)}°)`"
              label="Yaw"
              density="compact"
              readonly
              hide-details
              class="mt-2"
            />

            <!-- Controls -->
            <v-row
              dense
              class="mt-4"
            >
              <v-col cols="6">
                <v-btn
                  :disabled="frameIndex <= frameIndexMin"
                  block
                  variant="outlined"
                  size="small"
                  title="←"
                  @click="previousFrame"
                >
                  <v-icon>mdi-chevron-left</v-icon>
                  Previous
                </v-btn>
              </v-col>
              <v-col cols="6">
                <v-btn
                  :disabled="frameIndex >= frameIndexMax"
                  block
                  variant="outlined"
                  size="small"
                  title="→"
                  @click="nextFrame"
                >
                  Next
                  <v-icon>mdi-chevron-right</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </div>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useUrlSearchParams, useDebounceFn, useThrottleFn, useMagicKeys } from '@vueuse/core'
import { useFramesPack } from '@/composables/useFramesPack'
import { useMapLibre } from '@/composables/useMapLibre'
import { useThreeJS } from '@/composables/useThreeJS'

// URL parameters
const params = useUrlSearchParams('hash-params')
params.framespack = params.framespack || 'frames_pack.bin'
params.basemap = params.basemap || 'gaode_normal'
params.basemap_opacity = params.basemap_opacity || '1.0'

// Composables
const {
  ready: framesPackReady,
  message: framesPackMessage,
  meta,
  frameIndexMin,
  frameIndexMax,
  initFramesPack,
  getFrameFeatures,
} = useFramesPack()

const { initMap, renderViewBbox } = useMapLibre('map')
const {
  initThreeJS,
  renderGeoJsonFeatures,
  setCameraState,
  getCameraState,
  bbox
} = useThreeJS('threejs')

// State
const frameIndex = ref(0)
const currentPos = ref<[number, number]>([0, 0])
const currentYaw = ref(0)
const currentTs = ref(0)

// Computed
const status = computed(() => {
  if (!framesPackReady.value || !meta.value) return 'Loading...'

  const lon = currentPos.value[0].toFixed(6)
  const lat = currentPos.value[1].toFixed(6)
  const yaw = currentYaw.value.toFixed(3)
  const bboxStr = `${bbox.value.xmin.toFixed(2)},${bbox.value.ymin.toFixed(2)},${bbox.value.xmax.toFixed(2)},${bbox.value.ymax.toFixed(2)}`

  return `Frame: ${frameIndex.value}/${frameIndexMax.value}, TS: ${currentTs.value}, Pos: ${lon},${lat}, Yaw: ${yaw}, BBox: ${bboxStr}`
})

// Keyboard controls
const keys = useMagicKeys()

// Methods
function previousFrame() {
  if (frameIndex.value > frameIndexMin.value) {
    frameIndex.value--
  }
}

function nextFrame() {
  if (frameIndex.value < frameIndexMax.value) {
    frameIndex.value++
  }
}

const updateFrame = useThrottleFn(async (index: number) => {
  if (!meta.value || index < 0 || index >= meta.value.frames.length) return

  const frame = meta.value.frames[index]
  currentPos.value = frame.pos
  currentYaw.value = frame.yaw
  currentTs.value = frame.ts

  // Update URL params
  params.ts = frame.ts.toString()

  // Load and render frame data
  const geojson = await getFrameFeatures(index)
  renderGeoJsonFeatures(geojson, index)
  renderViewBbox(bbox.value, currentPos.value, currentYaw.value)
}, 50)

function onFrameIndexChange(newIndex: number) {
  updateFrame(newIndex)
}

function validateFrameIndex() {
  if (frameIndex.value < frameIndexMin.value) {
    frameIndex.value = frameIndexMin.value
  } else if (frameIndex.value > frameIndexMax.value) {
    frameIndex.value = frameIndexMax.value
  }
}

// Watchers
watch(frameIndex, (newVal) => {
  updateFrame(newVal)
})

// Keyboard navigation
let keyInterval: number | null = null
let keyTimeout: number | null = null

const handleArrowKeys = () => {
  if (keys.ArrowLeft.value) {
    previousFrame()
  } else if (keys.ArrowRight.value) {
    nextFrame()
  }
}

watch([keys.ArrowLeft, keys.ArrowRight], ([left, right]) => {
  if ((left || right) && !keyInterval && !keyTimeout) {
    handleArrowKeys()
    keyTimeout = setTimeout(() => {
      keyInterval = setInterval(handleArrowKeys, 50)
      keyTimeout = null
    }, 100)
  } else if (!left && !right) {
    if (keyInterval) {
      clearInterval(keyInterval)
      keyInterval = null
    }
    if (keyTimeout) {
      clearTimeout(keyTimeout)
      keyTimeout = null
    }
  }
})

// Lifecycle
onMounted(async () => {
  try {
    const success = await initFramesPack(params.framespack as string)
    if (!success) return

    // Set initial frame index
    if (params.ts) {
      const ts = parseFloat(params.ts as string)
      const foundIndex = meta.value?.frames.findIndex((frame: { ts: number }) => frame.ts === ts)
      if (foundIndex !== undefined && foundIndex >= 0) {
        frameIndex.value = foundIndex
      }
    }

    await nextTick()

    // Initialize Three.js and Map
    initThreeJS()
    initMap(params.basemap as string, parseFloat(params.basemap_opacity as string))

    // Set camera state from URL if available
    if (params.camera) {
      try {
        const [x, y, zoom] = (params.camera as string).split(',').map(parseFloat)
        setCameraState(x, y, zoom)
      } catch {
        console.warn('Invalid camera parameters:', params.camera)
      }
    }

    // Update camera params when changed
    const updateCameraParams = useDebounceFn(() => {
      const state = getCameraState()
      if (state) {
        params.camera = `${state.x},${state.y},${state.zoom}`
      }
    }, 200)

    // Watch for camera changes (this would need to be implemented in the Three.js composable)
    // For now, we'll update on frame changes
    watch(frameIndex, () => {
      setTimeout(updateCameraParams, 100)
    })

    // Initial frame load
    updateFrame(frameIndex.value)

  } catch (error) {
    console.error('Error initializing viewer:', error)
    framesPackMessage.value = `Error: ${error}`
  }
})
</script>

<style scoped>
#layout {
  display: flex;
  height: 100vh;
}

#left-panel {
  width: 70%;
  display: flex;
  flex-direction: column;
}

#map {
  flex: 2;
  box-shadow: 0 0 2px 1px rgba(0, 0, 255, 0.5);
  min-height: 200px;
}

#threejs {
  flex: 8;
  min-height: 400px;
  position: relative;
}

#right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 300px;
  max-width: 400px;
  overflow-y: auto;
}
</style>
