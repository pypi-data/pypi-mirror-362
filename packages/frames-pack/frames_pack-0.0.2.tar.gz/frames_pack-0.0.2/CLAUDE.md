# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Installation and Setup
```bash
make install        # Install the package in editable mode
make lint_install   # Install pre-commit hooks and linting tools
```

### Testing
```bash
make test          # Run all tests (includes pytest and CLI tests)
make pytest        # Run pytest with parallel execution (-n 10)
make clitest       # Run CLI module tests and compile examples
```

### Linting and Code Quality
```bash
make lint          # Run pre-commit on all files and format HTML
```

### Building and Packaging
```bash
make package       # Build source distribution
make upload        # Upload to PyPI (use pypi_remote variable for different repositories)
```

### Development Server
```bash
python3 main.py    # Start FastAPI server on localhost:8000
# Use FALLBACK_FRAMES_PACK_PATH env var to specify frames pack file
FALLBACK_FRAMES_PACK_PATH=build/frames_pack2.bin python3 main.py
```

### Frontend Development
```bash
cd frontend/viewer
npm install        # Install dependencies
npm run dev        # Start Vite dev server (localhost:3000 with --host flag)
npm run build      # Build for production
npm run lint       # Run ESLint with auto-fix
npm run type-check # TypeScript type checking without emit
```

### Core Module Usage
```bash
python3 -m frames_pack                                    # Show help for available modules
python3 -m frames_pack.compile --help                    # Show compile options
python3 -m frames_pack.compile rosbag2framespack <bag>   # Convert ROS bag to frames pack
python3 -m frames_pack.compile geojson2framespack <json> # Convert GeoJSON to frames pack
python3 -m frames_pack.compile framespack2json <bin>     # Export frames pack to JSON
```

## Architecture Overview

### Core Components

**frames_pack/core.py** - Defines the main data structures:
- `FramesPack`: Top-level container with header, meta, frames, and optional tail
- `FramesPackFrame`: Individual frame with metadata and features
- `FramesPackFeature`: GeoJSON-like feature with geometry, styling, and properties
- Uses msgpack + zstd compression for efficient storage

**frames_pack/compile.py** - Data conversion utilities:
- `rosbag2framespack()`: Converts ROS bag files to frames pack format
- `geojson2framespack()`: Converts GeoJSON files to frames pack format
- `framespack2json()`: Exports frames pack to human-readable JSON

**frames_pack/utils.py** - Utility functions for interpolation, coordinate transformations, and data processing

**main.py** - FastAPI web server that serves:
- Static `index.html` viewer application
- `/frames_pack.bin` endpoint with HTTP range request support for streaming large files
- Health check endpoint

**frontend/viewer/** - Vue 3 + TypeScript SPA with:
- Vue 3 Composition API with TypeScript strict mode
- Vuetify 3 for Material Design UI components
- MapLibre GL for 2D map visualization with multiple basemap sources
- Three.js for 3D orthographic rendering with orbit controls
- @vueuse/core for reactive utilities and composables
- Real-time frame navigation with keyboard controls and URL state persistence

### Data Flow

1. Input data (ROS bags, GeoJSON) → conversion via `compile.py`
2. Compressed binary format with msgpack + zstd compression
3. Web server streams data with range requests for efficient loading
4. Client-side decompression and rendering in browser

### Key Features

- **Efficient Storage**: Uses msgpack + zstd compression with configurable compression levels
- **Streaming Support**: HTTP range requests enable loading large datasets progressively
- **Coordinate Systems**: Handles transformations between WGS84, local ENU, and vehicle coordinate frames
- **Multi-Format Support**: Can process ROS bag telemetry data and GeoJSON geographic data
- **Interactive Visualization**: Real-time frame navigation with synchronized 2D/3D views

## Testing Strategy

The project uses pytest for unit testing with parallel execution. CLI tests verify the compilation pipeline works end-to-end with sample data files in the `data/` directory.

## Frontend Architecture

### Composables Structure
The Vue frontend uses a composable-based architecture for separation of concerns:

**useFramesPack** - Handles binary data loading and decompression:
- Progressive loading with HTTP range requests for large files
- Client-side ZSTD decompression and msgpack parsing
- Frame metadata caching and indexing

**useMapLibre** - 2D map visualization:
- Multiple basemap providers (OSM, satellite, Gaode)
- Viewport synchronization with 3D view
- GeoJSON feature rendering with styling

**useThreeJS** - 3D orthographic rendering:
- Orbit controls for camera manipulation
- Coordinate system transformations (WGS84 ↔ Local ENU ↔ Vehicle)
- Feature rendering with SimpleStyle specification support

### Development Patterns
- TypeScript strict mode with full type coverage
- Vue 3 Composition API with `<script setup>` syntax
- Reactive state management using Vue's built-in reactivity
- URL-based state persistence for viewer settings and navigation

## Dependencies

**Python Backend**:
- FastAPI/uvicorn for web serving with range request support
- msgpack/msgspec for binary serialization
- zstd for compression
- pybind11-geobuf for efficient GeoJSON/geobuf processing
- numpy/scipy for numerical computations and interpolation
- loguru for structured logging

**Frontend (Vue/TypeScript)**:
- Vue 3 + Vuetify 3 for reactive UI
- MapLibre GL for 2D mapping
- Three.js for 3D rendering
- @msgpack/msgpack + @oneidentity/zstd-js for client-side data processing
- @vueuse/core for reactive utilities
