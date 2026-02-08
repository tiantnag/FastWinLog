# API Documentation

## Overview

The Windows Log Analyzer exposes a Python API to the frontend via pywebview's JS API bridge.

## Log File Management

### `get_log_files(include_loaded=True)`
Get list of available log files.

**Parameters:**
- `include_loaded` (bool): Include already loaded files

**Returns:**
```json
{
  "files": [
    {
      "path": "C:\\Windows\\System32\\winevt\\Logs\\Security.evtx",
      "name": "Security.evtx",
      "size": 1048576,
      "modified": "2024-01-01T00:00:00"
    }
  ]
}
```

### `select_log_file()`
Open file dialog to select a log file.

**Returns:**
```json
{
  "path": "C:\\path\\to\\file.evtx",
  "name": "file.evtx"
}
```

## Event Loading

### `load_events_paginated(file_path, page=1, page_size=100, sort_field="TimeCreated", sort_direction="desc")`
Load events with pagination.

**Parameters:**
- `file_path` (str): Path to EVTX file
- `page` (int): Page number (1-based)
- `page_size` (int): Events per page
- `sort_field` (str): Field to sort by
- `sort_direction` (str): "asc" or "desc"

**Returns:**
```json
{
  "events": [...],
  "total": 1000,
  "page": 1,
  "page_size": 100,
  "total_pages": 10
}
```

### `get_load_progress(file_path)`
Get loading progress for a file.

**Returns:**
```json
{
  "loaded": 500,
  "total": 1000,
  "percentage": 50.0,
  "status": "loading"
}
```

## Search

### `search_events(file_path, keyword, page=1, page_size=100, sort_field="TimeCreated", sort_direction="desc")`
Search events by keyword.

**Parameters:**
- `file_path` (str): Path to EVTX file
- `keyword` (str): Search keyword (supports multiple keywords separated by space)
- `page` (int): Page number
- `page_size` (int): Results per page
- `sort_field` (str): Field to sort by
- `sort_direction` (str): "asc" or "desc"

**Returns:**
```json
{
  "results": [...],
  "total": 50,
  "page": 1,
  "page_size": 100
}
```

### `advanced_search_events(file_path, filters, page=1, page_size=100, sort_field="TimeCreated", sort_direction="desc")`
Advanced search with multiple filters.

**Parameters:**
- `file_path` (str): Path to EVTX file
- `filters` (dict): Filter conditions
  ```json
  {
    "EventID": "4624",
    "Level": "Information",
    "TimeCreated": {
      "start": "2024-01-01T00:00:00",
      "end": "2024-01-31T23:59:59"
    }
  }
  ```

## Alert Rules

### `get_alert_rules(file_path)`
Get alert rules for a file.

**Returns:**
```json
{
  "rules": [
    {
      "id": "rule1",
      "name": "Failed Login",
      "enabled": true,
      "conditions": {...}
    }
  ]
}
```

### `save_alert_rules(file_path, rules)`
Save alert rules.

### `scan_alerts_from_db(file_path, scan_limit=10000, rules=None)`
Scan for alerts in loaded events.

**Returns:**
```json
{
  "alerts": [...],
  "total": 10,
  "scanned": 10000
}
```

## Statistics

### `get_statistics_overview(file_path, time_range_hours=24)`
Get overview statistics.

**Returns:**
```json
{
  "total_events": 1000,
  "event_levels": {
    "Information": 800,
    "Warning": 150,
    "Error": 50
  },
  "top_event_ids": [...]
}
```

### `get_statistics_security_login(file_path, time_range_hours=24)`
Get login statistics (for Security logs).

### `get_statistics_security_account(file_path, time_range_hours=24)`
Get account management statistics.

### `get_statistics_security_process(file_path, time_range_hours=24)`
Get process creation statistics.

### `get_statistics_system(file_path, time_range_hours=24)`
Get system event statistics.

### `get_statistics_application(file_path, time_range_hours=24)`
Get application event statistics.

## Cache Management

### `get_cache_info()`
Get cache information.

**Returns:**
```json
{
  "total_size": 10485760,
  "files": [...]
}
```

### `clear_all_cache()`
Clear all cache.

### `clear_file_cache(file_path)`
Clear cache for specific file.

## Export

### `export_to_csv(evtx_file_path, visible_fields, export_type="all", search_keyword=None, advanced_filters=None)`
Export events to CSV.

**Parameters:**
- `evtx_file_path` (str): Path to EVTX file
- `visible_fields` (list): Fields to export
- `export_type` (str): "all", "search", or "advanced"
- `search_keyword` (str): Keyword for search export
- `advanced_filters` (dict): Filters for advanced export

**Returns:**
```json
{
  "success": true,
  "file_path": "C:\\path\\to\\export.csv",
  "rows": 1000
}
```
