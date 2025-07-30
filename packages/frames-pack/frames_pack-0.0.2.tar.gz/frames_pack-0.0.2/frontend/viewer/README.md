# FramesPack Viewer

A modern Vue 3 + TypeScript web application for visualizing FramesPack data with 2D map and 3D orthographic views.

## Features

- **Interactive 2D Map**: MapLibre GL-based map with customizable basemaps (OSM, Satellite, Gaode)
- **3D Orthographic View**: Three.js-powered 3D visualization with orbit controls
- **Frame Navigation**: Timeline slider and keyboard controls for frame-by-frame navigation
- **Real-time Sync**: Synchronized views between 2D map and 3D scene
- **Modern UI**: Vuetify Material Design components
- **TypeScript**: Full type safety and enhanced developer experience

## Architecture

This application migrates the existing `index.html` single-file viewer to a modern Vite-based architecture:

### Core Components

- **FramesPackViewer.vue**: Main application component handling UI and state management
- **useFramesPack**: Composable for loading and parsing FramesPack binary data
- **useMapLibre**: Composable for 2D map visualization and basemap management
- **useThreeJS**: Composable for 3D rendering and scene management

### Key Features Migrated

- HTTP range request support for efficient large file streaming
- ZSTD decompression and msgpack parsing
- GeoJSON feature rendering with style support
- Coordinate transformations (WGS84 ↔ local coordinate systems)
- Camera state persistence via URL parameters
- Keyboard navigation (arrow keys)

## Development

### Prerequisites

- Node.js 18+
- npm or yarn

### Setup

```bash
npm install
```

### Development Server

```bash
npm run dev
```

The dev server runs on `http://localhost:3000` with proxy configuration to forward FramesPack requests to `http://localhost:8000`.

### Building

```bash
npm run build
```

### Type Checking

```bash
npm run type-check
```

## Usage

1. Start the Python FastAPI server (from project root):
   ```bash
   python3 main.py
   ```

2. Start the Vite dev server:
   ```bash
   cd frontend/viewer
   npm run dev
   ```

3. Open `http://localhost:3000` in your browser

### URL Parameters

- `framespack`: Path to FramesPack file (default: `frames_pack.bin`)
- `basemap`: Map style (`osm`, `satellite`, `gaode_normal`, `gaode_satellite`)
- `basemap_opacity`: Map opacity (0.0-1.0)
- `ts`: Timestamp to navigate to
- `index`: Frame index to start from
- `camera`: Camera position (`x,y,zoom`)

## Dependencies

### Runtime
- **Vue 3**: Modern reactive framework
- **Vuetify 3**: Material Design components
- **MapLibre GL**: 2D map rendering
- **Three.js**: 3D graphics and controls
- **@vueuse/core**: Composition utilities
- **@msgpack/msgpack**: Binary data parsing
- **@oneidentity/zstd-js**: Decompression
- **geobuf/pbf**: GeoJSON binary format support

### Development
- **Vite**: Build tool and dev server
- **TypeScript**: Type safety
- **Vue TSC**: TypeScript support for Vue SFCs

## Migration Notes

The migration maintains 100% functional compatibility with the original `index.html` while adding:

- Better code organization with composables
- Type safety throughout
- Modern development tooling
- Hot module reloading
- Production optimizations
- Component-based architecture

All original features including coordinate transformations, data caching, keyboard controls, and URL parameter handling are preserved.
