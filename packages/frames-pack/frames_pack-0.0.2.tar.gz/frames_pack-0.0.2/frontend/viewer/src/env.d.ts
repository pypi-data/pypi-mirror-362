/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<Record<string, never>, Record<string, never>, unknown>
  export default component
}

// Declare global types for libraries that might not have perfect TypeScript support
declare module 'geobuf' {
  export function decode(buffer: unknown): unknown
  export function encode(geojson: unknown, options?: unknown): ArrayBuffer
}

declare module 'jmespath' {
  export function search(expression: string, data: unknown): unknown
}
