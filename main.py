#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FastWinLog - High-performance Windows Event Log Analyzer
Version: 1.0.0
Repository: https://github.com/vam876/FastWinLog
License: BSD-3-Clause
"""

import os
import sys
import threading
import webview
import mimetypes
from time import time

project_root = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(project_root, 'backend')
if project_root not in sys.path:
    sys.path.insert(0, project_root)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from backend.api.main_api import LogAnalysisApi

mimetypes.init()
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('application/javascript', '.mjs')
mimetypes.add_type('text/css', '.css')


def set_interval(interval):
    """Timer decorator for periodic tasks"""
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop():
                while not stopped.wait(interval):
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True
            t.start()
            return stopped
        return wrapper
    return decorator


def get_entrypoint_path(current_file_dir: str) -> str:
    """Get the entry HTML path"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = sys._MEIPASS
        candidates = [
            os.path.join(base_path, "frontend", "index.html"),
        ]
    else:
        # Running as script
        candidates = [
            os.path.join(current_file_dir, "frontend", "index.html"),
        ]
    
    for p in candidates:
        abs_path = os.path.abspath(p)
        if os.path.exists(abs_path):
            return abs_path
    
    raise FileNotFoundError("No index.html found in frontend directory")


def resolve_webview_url(entrypoint: str) -> str:
    """Resolve webview URL"""
    print(f"✓ Using static files: {entrypoint}")
    return entrypoint


@set_interval(1)
def update_ticker():
    """Update ticker for frontend"""
    if len(webview.windows) > 0:
        webview.windows[0].evaluate_js('window.pywebview.state && window.pywebview.state.set_ticker("%d")' % time())


if __name__ == '__main__':
    print("=" * 60)
    print("FastWinLog v1.0.0")
    print("=" * 60)
    
    # Initialize API
    api = LogAnalysisApi()
    
    # Get entry point
    try:
        entry = get_entrypoint_path(os.path.dirname(__file__))
        url = resolve_webview_url(entry)
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    
    # Create window
    window = webview.create_window(
        'FastWinLog v1.0.0',
        url,
        js_api=api,
        width=1400,
        height=900,
        resizable=True,
        background_color='#1e1e1e',
        text_select=True
    )
    
    print("\n✓ Application started successfully")
    print("=" * 60)
    
    # Start webview
    webview.start(debug=False)
