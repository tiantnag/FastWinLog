# FastWinLog - Quick Start Guide

**Version**: 1.0.0  
**Repository**: https://github.com/vam876/FastWinLog

## Installation

### Option 1: Run from Source

1. **Install Python 3.8+**
   - Download from https://www.python.org/

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```
   Or double-click `start.bat`

### Option 2: Use Pre-built Executable

1. Download `WindowsLogAnalyzer.exe` from releases
2. Double-click to run
3. No installation required!

## First Steps

### 1. Load a Log File

- Click "Select Log File" button
- Navigate to Windows log directory:
  ```
  C:\Windows\System32\winevt\Logs\
  ```
- Select a log file (e.g., `Security.evtx`, `System.evtx`)
- Wait for parsing to complete

### 2. View Events

- Events are displayed in a table
- Use pagination to navigate
- Click on an event to see details
- Sort by clicking column headers

### 3. Search Events

**Simple Search:**
- Enter keyword in search box
- Press Enter or click Search
- Supports multiple keywords (space-separated)

**Advanced Search:**
- Click "Advanced Search" button
- Add multiple filter conditions
- Combine filters with AND/OR logic
- Filter by Event ID, Level, Time, etc.

### 4. Security Analysis

**Use Security Presets:**
- Click "Security Presets" button
- Select a preset (e.g., "Failed Logins", "Account Changes")
- View filtered results instantly

**Alert Rules:**
- Switch to "Alert Center" tab
- View built-in security alert rules
- Enable/disable rules as needed
- Click "Scan Alerts" to find matches

### 5. View Statistics

- Switch to "Statistics" tab
- Select time range (24h, 7d, 30d, All)
- View charts and graphs:
  - Event distribution by level
  - Top event IDs
  - Timeline charts
  - Security-specific stats (for Security logs)

### 6. Export Results

**Export Current View:**
- Click "Export" button
- Choose CSV or JSON format
- Select visible columns
- Save to file

**Export Search Results:**
- Perform a search
- Click "Export Search Results"
- All matching events exported

## Tips & Tricks

### Performance

- **First load is slow**: Parsing large files takes time
- **Subsequent loads are fast**: Cache is used
- **Clear cache**: If file is updated, clear cache to reload

### Search

- **Multiple keywords**: "login failed" searches for both words
- **Case insensitive**: Search is not case-sensitive
- **Field-specific**: Use advanced search for specific fields

### Alerts

- **Built-in rules**: 20+ security alert rules included
- **Custom rules**: Create your own alert rules
- **Export/Import**: Share rules between systems

### Memory

- **Large files**: Application handles files with millions of events
- **Memory limit**: Keeps max 2 files in memory
- **Auto cleanup**: Old files automatically unloaded

## Common Tasks

### Analyze Failed Logins

1. Load `Security.evtx`
2. Click "Security Presets" → "Failed Logins"
3. View all Event ID 4625 (failed login attempts)
4. Check for suspicious patterns

### Find System Errors

1. Load `System.evtx`
2. Use Advanced Search:
   - Level = Error
   - Time Range = Last 24 hours
3. Review error events
4. Export for further analysis

### Monitor Account Changes

1. Load `Security.evtx`
2. Click "Security Presets" → "Account Management"
3. View all account creation/deletion/modification events
4. Check for unauthorized changes

### Track Process Creation

1. Load `Security.evtx`
2. Use Advanced Search:
   - Event ID = 4688
   - Time Range = Custom
3. View all process creation events
4. Look for suspicious processes

## Troubleshooting

### Application Won't Start

- **Check Python version**: Must be 3.8+
- **Install dependencies**: Run `pip install -r requirements.txt`
- **Check logs**: Look for error messages in console

### File Won't Load

- **Check file format**: Must be .evtx file
- **Check permissions**: Run as Administrator if needed
- **Check file size**: Very large files (>2GB) may take time

### Search Not Working

- **Clear cache**: Old cache may be corrupted
- **Reload file**: Close and reopen the file
- **Check keyword**: Try simpler search terms

### Slow Performance

- **Large file**: Parsing takes time on first load
- **Low memory**: Close other applications
- **Clear cache**: Remove old cached files

## Keyboard Shortcuts

- **Ctrl+O**: Open file
- **Ctrl+F**: Focus search box
- **Ctrl+E**: Export results
- **Ctrl+R**: Reload file
- **Ctrl+Q**: Quit application

## Next Steps

- Read [API Documentation](API.md) for advanced usage
- Check [Architecture](ARCHITECTURE.md) to understand internals
- See [CONTRIBUTING.md](../CONTRIBUTING.md) to contribute

## Support

For issues and questions:
- GitHub Issues: https://github.com/yourusername/windows-log-analyzer/issues
- Documentation: https://github.com/yourusername/windows-log-analyzer/wiki
