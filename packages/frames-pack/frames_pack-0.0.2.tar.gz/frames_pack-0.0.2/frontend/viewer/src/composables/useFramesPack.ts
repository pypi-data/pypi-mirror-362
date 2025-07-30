import { ref, computed } from 'vue'
import { decode as msgpackUnpack } from '@msgpack/msgpack'
import { ZstdInit, ZstdSimple } from '@oneidentity/zstd-js/decompress'
import * as geobuf from 'geobuf'
import Pbf from 'pbf'
import type { FramesPackMeta, GeoJSONFeatureCollection } from '@/types'

// Initialize ZSTD
await ZstdInit()
// @ts-expect-error - Property access workaround
ZstdSimple.zstdFrameHeaderSizeMax = 0

export function useFramesPack() {
  const ready = ref(false)
  const message = ref('')
  const version = ref<[number, number, number] | null>(null)
  const meta = ref<FramesPackMeta | null>(null)

  const headerLength = 26
  const metaLength = ref(0)
  const reqHeaders = { 'Cache-Control': 'max-age=3600' }

  // Caches
  const frameMetaCache = new Map<number, unknown>()
  const frameFeaturesCache = new Map<number, GeoJSONFeatureCollection>()
  const framePropsCache = new Map<number, unknown[]>()

  const frameCount = computed(() => meta.value?.frames?.length ?? 0)
  const frameIndexMin = computed(() => 0)
  const frameIndexMax = computed(() => Math.max(0, frameCount.value - 1))

  async function initFramesPack(framespackUrl: string): Promise<boolean> {
    try {
      message.value = `Loading FramesPack from ${framespackUrl}...`

      // Load header
      const headerResponse = await fetch(framespackUrl, {
        headers: {
          Range: `bytes=0-${headerLength - 1}`,
          ...reqHeaders,
        },
      })

      if (!headerResponse.ok) {
        message.value = `Failed to fetch framespack header: ${headerResponse.status} ${headerResponse.statusText}`
        return false
      }

      const headerData = await headerResponse.arrayBuffer()
      const header = new Uint8Array(headerData)
      const magic = new TextDecoder().decode(header.slice(0, 10))

      if (magic !== 'FramesPack') {
        message.value = `Invalid framespack file: expected "FramesPack", got "${magic}"`
        return false
      }

      const dataView = new DataView(headerData)
      const versionArray: [number, number, number] = [
        dataView.getInt32(10, true),
        dataView.getInt32(14, true),
        dataView.getInt32(18, true),
      ]
      version.value = versionArray
      metaLength.value = dataView.getInt32(22, true)

      message.value = `FramesPack Header, Version: ${versionArray[0]}.${versionArray[1]}.${versionArray[2]}, Meta Length: ${metaLength.value}`

      // Load meta
      const metaResponse = await fetch(framespackUrl, {
        headers: {
          Range: `bytes=${headerLength}-${headerLength + metaLength.value - 1}`,
          ...reqHeaders,
        },
      })

      if (!metaResponse.ok) {
        return false
      }

      const metaData = await metaResponse.arrayBuffer()
      message.value = `Meta data size: ${metaData.byteLength} bytes`

      const decompressed = ZstdSimple.decompress(new Uint8Array(metaData))
      const metaJson = msgpackUnpack(decompressed) as FramesPackMeta
      meta.value = metaJson

      message.value = `Loaded ${metaJson.frames.length} frames`
      ready.value = true
      return true

    } catch (error) {
      message.value = `Error loading FramesPack: ${error}`
      return false
    }
  }

  async function getFrameMeta(index: number): Promise<unknown> {
    if (frameMetaCache.has(index)) {
      return frameMetaCache.get(index)
    }

    if (!meta.value) return null

    const frame = meta.value.frames[index]
    const begin = headerLength + metaLength.value + frame.offset
    const end = begin + frame.lengths[0] - 1

    const response = await fetch('/frames_pack.bin', {
      headers: {
        Range: `bytes=${begin}-${end}`,
        ...reqHeaders
      },
    })

    if (!response.ok) {
      console.error(`Failed to fetch frame (#${index}) meta: ${response.status} ${response.statusText}`)
      return null
    }

    const bytes = await response.arrayBuffer()
    const decompressed = ZstdSimple.decompress(new Uint8Array(bytes))
    const json = msgpackUnpack(decompressed)

    frameMetaCache.set(index, json)
    return json
  }

  async function getFrameFeatures(index: number): Promise<GeoJSONFeatureCollection | null> {
    if (frameFeaturesCache.has(index)) {
      return frameFeaturesCache.get(index)!
    }

    if (!meta.value) return null

    const frame = meta.value.frames[index]
    const [frameMetaLen, frameFeaturesLen] = frame.lengths
    const begin = headerLength + metaLength.value + frame.offset + frameMetaLen
    const end = begin + frameFeaturesLen - 1

    const response = await fetch('/frames_pack.bin', {
      headers: {
        Range: `bytes=${begin}-${end}`,
        ...reqHeaders
      },
    })

    if (!response.ok) {
      console.error(`Failed to fetch frame (#${index}) features: ${response.status} ${response.statusText}`)
      return null
    }

    const bytes = await response.arrayBuffer()
    const decompressed = ZstdSimple.decompress(new Uint8Array(bytes))
    const geojson = geobuf.decode(new Pbf(decompressed)) as GeoJSONFeatureCollection

    frameFeaturesCache.set(index, geojson)
    return geojson
  }

  async function getFrameProps(index: number): Promise<unknown[] | null> {
    if (framePropsCache.has(index)) {
      return framePropsCache.get(index)!
    }

    if (!meta.value) return null

    const frame = meta.value.frames[index]
    const [frameMetaLen, frameFeaturesLen, framePropsLen] = frame.lengths
    const begin = headerLength + metaLength.value + frame.offset + frameMetaLen + frameFeaturesLen
    const end = begin + framePropsLen - 1

    const response = await fetch('/frames_pack.bin', {
      headers: {
        Range: `bytes=${begin}-${end}`,
        ...reqHeaders
      },
    })

    if (!response.ok) {
      console.error(`Failed to fetch frame (#${index}) props: ${response.status} ${response.statusText}`)
      return null
    }

    const bytes = await response.arrayBuffer()
    const decompressed = ZstdSimple.decompress(new Uint8Array(bytes))
    const json = msgpackUnpack(decompressed) as unknown[]

    framePropsCache.set(index, json)
    return json
  }

  return {
    ready,
    message,
    version,
    meta,
    metaLength,
    frameCount,
    frameIndexMin,
    frameIndexMax,
    initFramesPack,
    getFrameMeta,
    getFrameFeatures,
    getFrameProps,
  }
}
