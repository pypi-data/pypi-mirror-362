/**
 * Coordinate transformation utilities
 */

export function cheapRulerK(latitude: number): [number, number] {
  const RE = 6378.137
  const FE = 1.0 / 298.257223563
  const E2 = FE * (2 - FE)
  const RAD = Math.PI / 180.0
  const MUL = RAD * RE * 1000.0
  const coslat = Math.cos(latitude * RAD)
  const w2 = 1 / (1 - E2 * (1 - coslat * coslat))
  const w = Math.sqrt(w2)
  return [MUL * w * coslat, MUL * w * w2 * (1 - E2)]
}

export function car2wgs84(
  coords: [number, number][],
  lon: number,
  lat: number,
  yaw: number
): [number, number][] {
  const k = cheapRulerK(lat)
  const kLon = 1.0 / k[0]
  const kLat = 1.0 / k[1]
  const cos = Math.cos(yaw)
  const sin = Math.sin(yaw)

  return coords.map(([x, y]) => [
    (cos * x - sin * y) * kLon + lon,
    (sin * x + cos * y) * kLat + lat,
  ])
}

export function normalizeColor(stroke?: string, fallback = 0xff0000): number {
  if (!stroke) return fallback
  if (typeof stroke !== 'string') return stroke

  try {
    if (stroke[0] === '#') {
      return parseInt(stroke.substring(1), 16)
    } else if (stroke[0] === '0' && stroke[1] === 'x') {
      return parseInt(stroke.substring(2), 16)
    } else if (stroke.startsWith('rgb(') && stroke.endsWith(')')) {
      const [r, g, b] = stroke.slice(4, -1).split(',').map(Number)
      return (r << 16) | (g << 8) | b
    } else {
      return fallback
    }
  } catch {
    return fallback
  }
}
