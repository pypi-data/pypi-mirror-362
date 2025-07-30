import { ref, shallowRef, onUnmounted } from 'vue'
import maplibregl, { type Map } from 'maplibre-gl'
import { car2wgs84 } from '@/utils/coordinates'
import type { ViewBounds } from '@/types'

export function useMapLibre(containerId: string) {
  const map = shallowRef<Map | null>(null)
  const viewBboxData = ref<Record<string, unknown> | null>(null)

  const mapSources: Record<string, Record<string, unknown>> = {
    osm: {
      type: 'raster' as const,
      tiles: [
        'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png',
        'https://b.tile.openstreetmap.org/{z}/{x}/{y}.png',
        'https://c.tile.openstreetmap.org/{z}/{x}/{y}.png',
      ],
      tileSize: 256,
      maxzoom: 18,
      attribution: '© OpenStreetMap contributors',
    },
    satellite: {
      type: 'raster' as const,
      tiles: [
        'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      ],
      tileSize: 256,
      maxzoom: 18,
      attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
    },
    gaode_normal: {
      type: 'raster' as const,
      tiles: [
        'http://wprd01.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7',
        'http://wprd02.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7',
        'http://wprd03.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7',
        'http://wprd04.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7',
      ],
      tileSize: 256,
      maxzoom: 18,
      attribution: '&copy; 高德/Gaode/AutoNavi',
    },
    gaode_satellite: {
      type: 'raster' as const,
      tiles: [
        'http://wprd01.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=6',
        'http://wprd02.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=6',
        'http://wprd03.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=6',
        'http://wprd04.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=6',
      ],
      maxzoom: 18,
      tileSize: 256,
      attribution: '&copy; Gaode/AutoNavi',
    },
  }

  function initMap(basemap: string = 'gaode_normal', basemapOpacity = 1.0) {
    const emptyStyle = {
      version: 8 as const,
      sources: {},
      layers: [],
    }

    map.value = new maplibregl.Map({
      container: containerId,
      style: emptyStyle,
      center: [116.419181, 39.901624],
      zoom: 10,
      bearing: 0,
      maplibreLogo: false,
      minZoom: 2,
      maxZoom: 24,
      pitchWithRotate: false,
      rollEnabled: false,
      touchPitch: false,
      attributionControl: false,
    })

    // @ts-expect-error - Avoid type instantiation depth issue
    map.value.on('load', () => {
      setTimeout(() => updateBasemap(basemap, basemapOpacity), 100)
    })
  }

  function updateBasemap(basemap: string, opacity = 1.0) {
    if (!map.value) return

    if (map.value.getLayer('base-layer')) {
      map.value.removeLayer('base-layer')
    }
    if (map.value.getSource('base-source')) {
      map.value.removeSource('base-source')
    }

    if (mapSources[basemap]) {
      map.value.addSource('base-source', mapSources[basemap])
    }
    map.value.addLayer({
      id: 'base-layer',
      type: 'raster',
      source: 'base-source',
      paint: {
        'raster-opacity': opacity,
      },
    })

    // Ensure viewbbox layers stay on top after basemap change
    ensureViewBboxOnTop()
  }

  function ensureViewBboxOnTop() {
    if (!map.value) return

    const viewBboxLayers = ['view_bbox', 'view_bbox_outline', 'view_bbox_xy']

    // Remove and re-add viewbbox layers to put them on top
    viewBboxLayers.forEach(layerId => {
      if (map.value?.getLayer(layerId)) {
        map.value.removeLayer(layerId)

        // Re-add the layer
        if (layerId === 'view_bbox') {
          map.value.addLayer({
            id: 'view_bbox',
            type: 'fill',
            source: 'view_bbox',
            filter: ['==', ['geometry-type'], 'Polygon'],
            paint: {
              'fill-color': 'yellow',
              'fill-opacity': 0.6,
            },
          })
        } else if (layerId === 'view_bbox_outline') {
          map.value.addLayer({
            id: 'view_bbox_outline',
            type: 'line',
            source: 'view_bbox',
            filter: ['==', ['geometry-type'], 'Polygon'],
            paint: {
              'line-color': 'red',
              'line-width': 3,
              'line-opacity': 0.8,
            },
          })
        } else if (layerId === 'view_bbox_xy') {
          map.value.addLayer({
            id: 'view_bbox_xy',
            type: 'line',
            source: 'view_bbox',
            filter: ['==', ['geometry-type'], 'LineString'],
            paint: {
              'line-color': ['get', 'stroke'],
              'line-width': 4,
              'line-opacity': 1.0,
            },
          })
        }
      }
    })
  }

  function renderViewBbox(bbox: ViewBounds, pos: [number, number], yaw: number) {
    if (!map.value || !map.value.loaded()) return

    const { xmin, ymin, xmax, ymax } = bbox
    const egoCoords: [number, number][] = [
      [xmin, ymin],
      [xmax, ymin],
      [xmax, ymax],
      [xmin, ymax],
      [xmin, ymin],
      [0, 0],
      [10, 0],
      [0, 10],
    ]

    const wgs84Coords = car2wgs84(egoCoords, pos[0], pos[1], yaw)
    const coords = wgs84Coords.slice(0, 5)
    const [center, x, y] = wgs84Coords.slice(5, 8)

    const viewBbox = map.value.getSource('view_bbox')
    if (viewBbox) {
      viewBboxData.value.features[0].geometry.coordinates = [coords]
      viewBboxData.value.features[1].geometry.coordinates = [center, x]
      viewBboxData.value.features[2].geometry.coordinates = [center, y]
      ;(viewBbox as { setData: (data: unknown) => void }).setData(viewBboxData.value)
      ensureViewBboxOnTop()
      map.value.flyTo({ center: center })
      return
    }

    viewBboxData.value = {
      type: 'FeatureCollection',
      features: [
        {
          type: 'Feature',
          geometry: {
            type: 'Polygon',
            coordinates: [coords],
          },
        },
        {
          type: 'Feature',
          geometry: {
            type: 'LineString',
            coordinates: [center, x],
          },
          properties: {
            stroke: '#ff0000',
          },
        },
        {
          type: 'Feature',
          geometry: {
            type: 'LineString',
            coordinates: [center, y],
          },
          properties: {
            stroke: '#00ff00',
          },
        },
      ],
    }

    map.value.addSource('view_bbox', {
      type: 'geojson',
      data: viewBboxData.value,
    })

    map.value.addLayer({
      id: 'view_bbox',
      type: 'fill',
      source: 'view_bbox',
      filter: ['==', ['geometry-type'], 'Polygon'],
      paint: {
        'fill-color': 'yellow',
        'fill-opacity': 0.6,
      },
    })

    map.value.addLayer({
      id: 'view_bbox_outline',
      type: 'line',
      source: 'view_bbox',
      filter: ['==', ['geometry-type'], 'Polygon'],
      paint: {
        'line-color': 'red',
        'line-width': 3,
        'line-opacity': 0.8,
      },
    })

    map.value.addLayer({
      id: 'view_bbox_xy',
      type: 'line',
      source: 'view_bbox',
      filter: ['==', ['geometry-type'], 'LineString'],
      paint: {
        'line-color': ['get', 'stroke'],
        'line-width': 4,
        'line-opacity': 1.0,
      },
    })
    ensureViewBboxOnTop()
    map.value.flyTo({ center: center, zoom: 16, bearing: 0 })
  }

  onUnmounted(() => {
    if (map.value) {
      map.value.remove()
    }
  })

  return {
    map,
    initMap,
    updateBasemap,
    renderViewBbox,
    mapSources,
  }
}
