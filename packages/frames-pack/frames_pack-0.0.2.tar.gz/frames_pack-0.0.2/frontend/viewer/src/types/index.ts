export interface FramesPackHeader {
  version: [number, number, number]
}

export interface FramesPackMeta {
  frames: FrameInfo[]
  properties: Record<string, unknown>
  frames_length: number
}

export interface FrameInfo {
  ts: number
  pos: [number, number]
  yaw: number
  offset: number
  lengths: [number, number, number]
}

export interface GeoJSONFeature {
  type: 'Feature'
  geometry: {
    type: string
    coordinates: unknown
  }
  properties?: Record<string, unknown>
}

export interface GeoJSONFeatureCollection {
  type: 'FeatureCollection'
  features: GeoJSONFeature[]
}

export interface ViewBounds {
  xmin: number
  ymin: number
  xmax: number
  ymax: number
}

export interface CameraState {
  x: number
  y: number
  zoom: number
}
