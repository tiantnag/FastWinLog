# FastWinLog - Installation Guide

**Version**: 1.0.0  
**Repository**: https://github.com/vam876/FastWinLog

## Quick Install (Recommended)

### For End Users

1. **Download the executable** (when available)
   - Download `WindowsLogAnalyzer.exe` from releases
   - No installation required
   - Double-click to run

### For Developers

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/windows-log-analyzer.git
   cd windows-log-analyzer
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```
   Or double-click `start.bat`

## Detailed Installation

### Prerequisites

- **Operating System**: Windows 7 or later
- **Python**: 3.8 or higher (for source installation)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 100MB for application, additional space for cache

### Step-by-Step Installation

#### Option 1: Using Pre-built Executable (Easiest)

1. Download `WindowsLogAnalyzer.exe` from the releases page
2. Place it in a folder of your choice
3. Double-click to run
4. No Python installation needed!

#### Option 2: From Source (For Development)

1. **Install Python**
   - Download from https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Verify installation:
     ```bash
     python --version
     ```

2. **Clone or Download the Project**
   ```bash
   git clone https://github.com/yourusername/windows-log-analyzer.git
   cd windows-log-analyzer
   ```
   Or download and extract the ZIP file

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   This will install:
   - pywebview (desktop framework)
   - pyevtx (EVTX parser)
   - pywin32 (Windows API)

4. **Verify Installation**
   ```bash
   python main.py
   ```
   
   You should see:
   ```
   ============================================
   Windows Log Analyzer v1.0.0
   ============================================
   [Cache] 缓存目录: ...
   [API初始化] 模块化版本已启用
   ✓ Using static files: ...
   ✓ Application started successfully
   ============================================
   ```

### Building Executable

To create a standalone executable:

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Build the executable**
   ```bash
   pyinstaller build-windows.spec
   ```

3. **Find the executable**
   - Location: `dist/WindowsLogAnalyzer/WindowsLogAnalyzer.exe`
   - The entire `dist/WindowsLogAnalyzer/` folder is portable

4. **Distribute**
   - Zip the `dist/WindowsLogAnalyzer/` folder
   - Users can extract and run without installation

## Troubleshooting

### Python Not Found

**Error**: `'python' is not recognized as an internal or external command`

**Solution**:
1. Reinstall Python and check "Add Python to PATH"
2. Or use full path: `C:\Python38\python.exe main.py`

### Missing Dependencies

**Error**: `ModuleNotFoundError: No module named 'pywebview'`

**Solution**:
```bash
pip install -r requirements.txt
```

### Permission Denied

**Error**: `PermissionError: [Errno 13] Permission denied`

**Solution**:
- Run as Administrator (right-click → Run as administrator)
- Or change the cache directory in settings

### pyevtx Installation Failed

**Error**: `error: Microsoft Visual C++ 14.0 or greater is required`

**Solution**:
1. Install Visual C++ Build Tools
2. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
3. Or use pre-built wheels:
   ```bash
   pip install --only-binary :all: pyevtx
   ```

### Application Won't Start

**Checklist**:
- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip list`)
- [ ] No antivirus blocking
- [ ] Run as Administrator
- [ ] Check console for error messages

### Slow Performance

**Tips**:
- First load is always slow (parsing)
- Subsequent loads use cache (fast)
- Close other applications to free memory
- Use SSD for better performance
- Clear old cache files

## Verification

After installation, verify everything works:

1. **Start the application**
   ```bash
   python main.py
   ```

2. **Load a test file**
   - Click "Select Log File"
   - Navigate to: `C:\Windows\System32\winevt\Logs\`
   - Select `Application.evtx` (usually small)

3. **Test features**
   - View events (should load quickly)
   - Search for a keyword
   - View statistics
   - Export results

If all steps work, installation is successful!

## Uninstallation

### For Executable Version
- Simply delete the folder

### For Source Version
1. Delete the project folder
2. (Optional) Uninstall Python packages:
   ```bash
   pip uninstall pywebview pyevtx pywin32
   ```

## Getting Help

If you encounter issues:

1. Check this guide
2. Read [QUICKSTART.md](docs/QUICKSTART.md)
3. Search [GitHub Issues]
4. Create a new issue with:
   - Error message
   - Python version
   - Windows version
   - Steps to reproduce

## Next Steps

After installation:
- Read [QUICKSTART.md](docs/QUICKSTART.md) for usage guide
- Check [API.md](docs/API.md) for API reference
- See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for technical details
