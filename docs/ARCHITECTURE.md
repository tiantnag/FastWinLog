# FastWinLog - Architecture

**Version**: 1.0.0  
**Repository**: https://github.com/vam876/FastWinLog

## Overview

FastWinLog is built with a clean separation between frontend and backend:

- **Frontend**: Pre-built React application (HTML/CSS/JS)
- **Backend**: Python-based API server using pywebview
- **Communication**: pywebview JS API bridge

## Backend Architecture

### Layered Architecture

```
┌─────────────────────────────────────┐
│         API Layer (main_api.py)     │  ← Exposes methods to frontend
├─────────────────────────────────────┤
│         Service Layer               │  ← Business logic
│  - LogService                       │
│  - EventService                     │
│  - SearchService                    │
│  - AlertService                     │
│  - StatisticsService                │
│  - CacheService                     │
├─────────────────────────────────────┤
│         Repository Layer            │  ← Data access
│  - SqliteRepository (cache)         │
│  - MemoryRepository (runtime)       │
│  - EvtxRepository (file parsing)    │
├─────────────────────────────────────┤
│         Core Layer                  │  ← Core functionality
│  - evtx_parser (pyevtx)            │
│  - alert_store                      │
│  - windows_events_database          │
└─────────────────────────────────────┘
```

### Key Components

#### API Layer (`api/`)
- **main_api.py**: Main API class that aggregates all services
- Exposes methods to frontend via pywebview

#### Service Layer (`services/`)
- **log_service.py**: File management and selection
- **event_service.py**: Event loading and pagination
- **search_service.py**: Search functionality
- **alert_service.py**: Alert rules and scanning
- **statistics_service.py**: Event statistics
- **cache_service.py**: Cache management

#### Repository Layer (`repositories/`)
- **sqlite_repository.py**: SQLite persistent cache
- **memory_repository.py**: In-memory event storage
- **evtx_repository.py**: EVTX file parsing

#### Core Layer (`core/`)
- **evtx_parser.py**: High-performance EVTX parsing using pyevtx
- **alert_store.py**: Alert rule storage and management
- **alert_baselines.py**: Built-in security alert rules
- **windows_events_database.py**: Windows event descriptions
- **security_presets.py**: Security analysis presets

#### Models (`models/`)
- **event.py**: Event data model
- **log_file.py**: Log file metadata
- **pagination.py**: Pagination parameters
- **search_result.py**: Search result wrapper

#### Utils (`utils/`)
- **progress_tracker.py**: Loading progress tracking
- **memory_manager.py**: Memory optimization
- **xml_parser.py**: XML parsing utilities

## Frontend Architecture

### Pre-built React Application

The frontend is a pre-built React + TypeScript application that communicates with the backend via pywebview's JS API bridge.

**Key Features:**
- Modern responsive UI
- Real-time event viewing
- Advanced search and filtering
- Alert management
- Statistics visualization
- Dark theme support

**Communication:**
```javascript
// Frontend calls Python backend
window.pywebview.api.load_events_paginated(filePath, page, pageSize)
  .then(result => {
    // Handle result
  });
```

## Data Flow

### Event Loading Flow

```
User selects file
      ↓
Frontend calls load_events_paginated()
      ↓
API Layer → EventService
      ↓
EventService checks cache (SqliteRepository)
      ↓
If not cached: EvtxRepository parses file
      ↓
Events stored in MemoryRepository
      ↓
Results returned to frontend
```

### Search Flow

```
User enters search keyword
      ↓
Frontend calls search_events()
      ↓
API Layer → SearchService
      ↓
SearchService queries MemoryRepository
      ↓
Results filtered and paginated
      ↓
Results returned to frontend
```

### Alert Scanning Flow

```
User triggers alert scan
      ↓
Frontend calls scan_alerts_from_db()
      ↓
API Layer → AlertService
      ↓
AlertService loads rules from AlertStore
      ↓
Events evaluated against rules
      ↓
Matching alerts returned to frontend
```

## Performance Optimizations

### 1. High-Performance Parsing
- Uses pyevtx library (59x faster than python-evtx)
- Parsing speed: ~14,767 events/second

### 2. Smart Caching
- SQLite persistent cache for parsed events
- Instant reload on application restart
- Automatic cache invalidation on file changes

### 3. Memory Management
- Keeps max 2 files in memory
- Automatic cleanup of old files
- Efficient pagination to reduce memory usage

### 4. Lazy Loading
- Events loaded on-demand
- Progressive loading with progress tracking
- Background parsing doesn't block UI

## Security Considerations

### Input Validation
- File path validation
- Search keyword sanitization
- Alert rule validation

### Resource Limits
- Maximum file size checks
- Memory usage monitoring
- Scan limit enforcement

### Data Privacy
- All processing done locally
- No external network calls
- Cache stored locally

## Extensibility

### Adding New Services

1. Create service in `services/` directory
2. Implement business logic
3. Add to `main_api.py`
4. Expose methods to frontend

### Adding New Alert Rules

1. Add rule to `core/alert_baselines.py`
2. Define conditions and severity
3. Rules automatically available in UI

### Adding New Statistics

1. Add method to `statistics_service.py`
2. Query events from repository
3. Return aggregated data
4. Frontend can display new stats

## Testing

### Unit Testing
- Test individual services
- Mock repositories
- Validate business logic

### Integration Testing
- Test API layer
- Verify data flow
- Check cache behavior

### Performance Testing
- Measure parsing speed
- Monitor memory usage
- Validate search performance

## Deployment

### Standalone Executable

Use PyInstaller to create standalone executable:

```bash
pyinstaller build-windows.spec
```

The spec file includes:
- Python backend
- Pre-built frontend
- All dependencies
- Application icon

### Distribution

The compiled executable is self-contained and requires no installation:
- No Python installation needed
- No npm/Node.js needed
- All dependencies bundled
- Ready to run on any Windows system
