import { ref, shallowRef, onUnmounted } from 'vue'
import * as THREE from 'three'
import { Line2 } from 'three/addons/lines/Line2.js'
import { LineMaterial } from 'three/addons/lines/LineMaterial.js'
import { LineGeometry } from 'three/addons/lines/LineGeometry.js'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'
import { normalizeColor } from '@/utils/coordinates'
import type { GeoJSONFeatureCollection, ViewBounds, CameraState } from '@/types'

export function useThreeJS(containerId: string) {
  const renderer = shallowRef<THREE.WebGLRenderer | null>(null)
  const scene = shallowRef<THREE.Scene | null>(null)
  const camera = shallowRef<THREE.OrthographicCamera | null>(null)
  const controls = shallowRef<OrbitControls | null>(null)
  const raycaster = shallowRef<THREE.Raycaster | null>(null)
  const pointer = ref(new THREE.Vector2())

  const xrange = [-20, 120]
  const yrange = [-40, 40]
  const bbox = ref<ViewBounds>({ xmin: 0, ymin: 0, xmax: 0, ymax: 0 })

  function initThreeJS() {
    const container = document.getElementById(containerId)
    if (!container) return false

    const width = container.clientWidth || container.offsetWidth
    const height = container.clientHeight || container.offsetHeight

    // Create orthographic camera
    const [xMin, xMax] = xrange
    const [yMin, yMax] = yrange
    const aspect = width / height
    const viewSize = Math.max(xMax - xMin, (yMax - yMin) / aspect)

    camera.value = new THREE.OrthographicCamera(
      (-viewSize * aspect) / 2,
      (viewSize * aspect) / 2,
      viewSize / 2,
      -viewSize / 2,
      0.1,
      1000
    )

    // Position camera at z=10, looking at origin
    camera.value.position.set(0, 0, 10)
    camera.value.up.set(1, 0, 0) // Set up vector to x-axis (so x is up)
    camera.value.lookAt(0, 0, 0)

    scene.value = new THREE.Scene()
    scene.value.background = new THREE.Color(0xffffff)

    renderer.value = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
    })
    renderer.value.setSize(width, height)
    renderer.value.setClearColor(0xffffff)

    // Setup controls
    controls.value = new OrbitControls(camera.value, renderer.value.domElement)
    controls.value.enableRotate = false
    controls.value.enableDamping = true
    controls.value.dampingFactor = 0.25
    controls.value.screenSpacePanning = true
    controls.value.minZoom = 0.25
    controls.value.maxZoom = 20.0
    controls.value.zoomToCursor = true
    controls.value.zoomSpeed = 10.0
    controls.value.panSpeed = 1.0
    controls.value.enableZoom = true
    controls.value.touches = {
      ONE: THREE.TOUCH.PAN,
      TWO: THREE.TOUCH.DOLLY_PAN,
    }
    controls.value.mouseButtons = {
      LEFT: THREE.MOUSE.PAN,
      MIDDLE: THREE.MOUSE.DOLLY,
      RIGHT: THREE.MOUSE.PAN,
    }

    // Setup raycaster
    raycaster.value = new THREE.Raycaster()

    // Add event listeners
    renderer.value.domElement.addEventListener('click', onThreeJsClick)
    window.addEventListener('resize', onWindowResize)

    container.appendChild(renderer.value.domElement)

    // Start animation loop
    animate()

    return true
  }

  function renderGeoJsonFeatures(geojson: GeoJSONFeatureCollection | null, frameIndex: number) {
    if (!geojson || !geojson.features || !scene.value) return

    scene.value.clear()
    scene.value.background = new THREE.Color(0xffffff)

    // Add grid helper
    const gridHelper = new THREE.GridHelper(240, 24)
    gridHelper.rotation.x = Math.PI / 2
    scene.value.add(gridHelper)

    // Add axes helper
    const axesHelper = new THREE.AxesHelper(10)
    axesHelper.position.set(0, 0, 1)
    scene.value.add(axesHelper)

    geojson.features.forEach((feature, index) => {
      if (!feature.geometry) return

      const { type, coordinates } = feature.geometry
      const props = feature.properties || {}
      let object: THREE.Object3D | null = null

      if (type === 'LineString') {
        object = createLine2(coordinates, props)
      } else if (type === 'MultiLineString') {
        const group = new THREE.Group()
        coordinates.forEach((lineCoords: number[][]) => {
          const line = createLine2(lineCoords, props)
          if (line) group.add(line)
        })
        object = group
      } else if (type === 'Point') {
        object = createPoint(coordinates, props)
      }

      if (object && scene.value) {
        object.userData = {
          frame_index: frameIndex,
          feature_index: index,
          feature: feature,
        }
        scene.value.add(object)
      }
    })
  }

  function createLine2(coordinates: number[][], properties: Record<string, unknown>): Line2 | null {
    if (!coordinates || coordinates.length < 2) return null

    const positions: number[] = []
    for (const point of coordinates) {
      const [x, y] = point
      positions.push(x, y, 0)
    }

    const geometry = new LineGeometry()
    geometry.setPositions(positions)

    const material = new LineMaterial({
      color: normalizeColor(properties.stroke),
      linewidth: 2.0,
      dashed: false,
    })

    return new Line2(geometry, material)
  }

  function createPoint(coordinates: number[], properties: Record<string, unknown>): THREE.Mesh | null {
    if (!coordinates || coordinates.length < 2) return null

    const [x, y] = coordinates

    // Create a circle with 1m radius
    const radius = 1.0
    const segments = 32
    const geometry = new THREE.CircleGeometry(radius, segments)
    const material = new THREE.MeshBasicMaterial({
      color: normalizeColor(properties.stroke),
      side: THREE.DoubleSide,
    })

    const circle = new THREE.Mesh(geometry, material)
    circle.position.set(x, y, 0)
    circle.rotation.x = -Math.PI / 2

    return circle
  }

  function onThreeJsClick(event: MouseEvent) {
    if (!raycaster.value || !scene.value || !camera.value) return

    const container = document.getElementById(containerId)
    if (!container) return

    const rect = container.getBoundingClientRect()
    pointer.value.x = ((event.clientX - rect.left) / container.clientWidth) * 2 - 1
    pointer.value.y = -((event.clientY - rect.top) / container.clientHeight) * 2 + 1

    raycaster.value.setFromCamera(pointer.value, camera.value)
    const intersects = raycaster.value.intersectObjects(scene.value.children, true)

    if (intersects.length > 0) {
      for (const intersect of intersects) {
        let object = intersect.object
        while (object && !object.userData.feature && object.parent) {
          object = object.parent
        }
        if (object && object.userData.feature !== undefined) {
          console.log('Clicked on feature:', object.userData)
          return
        }
      }
    }
  }

  function onWindowResize() {
    if (!renderer.value || !scene.value || !camera.value) return

    const container = document.getElementById(containerId)
    if (!container) return

    const width = container.clientWidth || container.offsetWidth
    const height = container.clientHeight || container.offsetHeight

    // Update orthographic camera with preserved aspect ratio
    const [xMin, xMax] = xrange
    const [yMin, yMax] = yrange
    const aspect = width / height
    const viewSize = Math.max(xMax - xMin, (yMax - yMin) / aspect)

    camera.value.left = (-viewSize * aspect) / 2
    camera.value.right = (viewSize * aspect) / 2
    camera.value.top = viewSize / 2
    camera.value.bottom = -viewSize / 2
    camera.value.updateProjectionMatrix()

    renderer.value.setSize(width, height)

    // Update line widths
    scene.value.traverse((object) => {
      if ((object as { isLine2?: boolean }).isLine2) {
        ;(object as Line2).material.resolution.set(width, height)
      }
    })

    updateBbox()
  }

  function updateBbox() {
    if (!camera.value) return

    const dy = (camera.value.right - camera.value.left) / 2.0 / camera.value.zoom
    const dx = (camera.value.top - camera.value.bottom) / 2.0 / camera.value.zoom

    const xmin = camera.value.position.x - dx
    const xmax = camera.value.position.x + dx
    const ymin = camera.value.position.y - dy
    const ymax = camera.value.position.y + dy

    bbox.value = { xmin, ymin, xmax, ymax }
  }

  function setCameraState(x: number, y: number, zoom: number) {
    if (!camera.value || !controls.value) return

    const z = camera.value.position.z
    camera.value.position.set(x, y, z)
    camera.value.zoom = zoom
    camera.value.updateProjectionMatrix()
    controls.value.target.set(x, y, 0)
    controls.value.update()
    updateBbox()
  }

  function getCameraState(): CameraState | null {
    if (!camera.value) return null

    return {
      x: Number(camera.value.position.x.toFixed(2)),
      y: Number(camera.value.position.y.toFixed(2)),
      zoom: Number(camera.value.zoom.toFixed(4)),
    }
  }

  function animate() {
    if (renderer.value && scene.value && camera.value) {
      if (controls.value) {
        controls.value.update()
      }
      renderer.value.render(scene.value, camera.value)
    }
    requestAnimationFrame(animate)
  }

  onUnmounted(() => {
    if (renderer.value) {
      const container = document.getElementById(containerId)
      if (container && renderer.value.domElement.parentNode === container) {
        container.removeChild(renderer.value.domElement)
      }
      renderer.value.dispose()
    }
    window.removeEventListener('resize', onWindowResize)
  })

  return {
    renderer,
    scene,
    camera,
    controls,
    bbox,
    initThreeJS,
    renderGeoJsonFeatures,
    setCameraState,
    getCameraState,
    updateBbox,
  }
}
