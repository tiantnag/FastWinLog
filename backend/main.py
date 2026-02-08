#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Windows Log Analyzer - Main Entry Point
"""

import os
import sys
import threading
import webview
import mimetypes
from time import time

# 添加父目录到路径，使server成为包
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from server.api.main_api import LogAnalysisApi

# 确保正确的MIME类型设置
mimetypes.init()
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('application/javascript', '.mjs')
mimetypes.add_type('text/css', '.css')


def set_interval(interval):
    """定时器装饰器"""
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
    """获取入口HTML路径"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        candidates = [
            os.path.join(base_path, "gui", "index.html"),
        ]
    else:
        candidates = [
            os.path.join(current_file_dir, "../gui/index.html"),
            os.path.join(current_file_dir, "./gui/index.html"),
        ]
    
    for p in candidates:
        abs_path = os.path.abspath(p)
        if os.path.exists(abs_path):
            return abs_path
    
    raise FileNotFoundError("No index.html found")


def resolve_webview_url(entrypoint: str, dev_port: int = 3000) -> str:
    """解析webview URL"""
    import socket
    
    use_dev = os.getenv("PYWEBVIEW_USE_DEV_SERVER", "").strip() in {"1", "true", "True"}
    
    if use_dev:
        try:
            with socket.create_connection(("127.0.0.1", dev_port), timeout=0.25):
                return f"http://localhost:{dev_port}"
        except OSError:
            pass
    
    return entrypoint


entry = get_entrypoint_path(os.path.dirname(__file__))


@set_interval(1)
def update_ticker():
    if len(webview.windows) > 0:
        webview.windows[0].evaluate_js('window.pywebview.state && window.pywebview.state.set_ticker("%d")' % time())


if __name__ == '__main__':
    api = LogAnalysisApi()
    
    url = resolve_webview_url(entry, dev_port=3000)
    
    window = webview.create_window(
        'FastWinLog Parse v1.0.0',
        url,
        js_api=api,
        width=1400,
        height=900,
        resizable=True,
        background_color='#1e1e1e',
        text_select=True
    )
    webview.start(debug=False)
