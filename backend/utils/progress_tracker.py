#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Progress tracking utility"""

import os
import time
import threading
from typing import Dict, Optional, Callable


class ProgressTracker:
    """进度跟踪器"""
    
    def __init__(self):
        self.progress_map: Dict[str, dict] = {}
        self.current_loading_file: Optional[str] = None
        self._lock = threading.Lock()
    
    def start_loading(self, file_path: str, message: str = '') -> None:
        """开始加载"""
        file_name = os.path.basename(file_path)
        with self._lock:
            self.current_loading_file = file_path
            self.progress_map[file_path] = {
                'status': 'idle',
                'current': 0,
                'total': 0,
                'message': message or f'准备加载 {file_name}',
                'file_name': file_name,
                'stage': ''
            }
    
    def update_counting(self, file_path: str) -> None:
        """更新为统计阶段"""
        file_name = os.path.basename(file_path)
        with self._lock:
            self.progress_map[file_path] = {
                'status': 'counting',
                'current': 0,
                'total': 0,
                'message': f'正在统计记录总数 {file_name}...',
                'file_name': file_name,
                'stage': 'counting'
            }
    
    def update_loading(self, file_path: str, current: int, total: int, 
                       speed: float = 0, eta_seconds: float = 0) -> None:
        """更新加载进度"""
        file_name = os.path.basename(file_path)
        progress_pct = (current / total * 100) if total > 0 else 0
        
        eta_text = f" | 剩余: {int(eta_seconds)}秒" if eta_seconds > 5 else ""
        message = f'正在加载 {file_name}... {current:,}/{total:,} ({progress_pct:.1f}%) | {speed:.0f}条/秒{eta_text}'
        
        with self._lock:
            self.progress_map[file_path] = {
                'status': 'loading',
                'current': current,
                'total': total,
                'message': message,
                'file_name': file_name,
                'stage': 'parsing',
                'speed': speed,
                'progress_pct': progress_pct
            }
    
    def complete(self, file_path: str, total: int, speed: float = 0) -> None:
        """完成加载"""
        file_name = os.path.basename(file_path)
        with self._lock:
            self.progress_map[file_path] = {
                'status': 'done',
                'current': total,
                'total': total,
                'message': f'加载完成！共 {total:,} 条记录 | 速度: {speed:.0f}条/秒',
                'file_name': file_name,
                'stage': 'done'
            }
    
    def error(self, file_path: str, message: str, error_type: str = 'unknown',
              solution: Optional[dict] = None) -> None:
        """记录错误"""
        file_name = os.path.basename(file_path)
        with self._lock:
            progress = {
                'status': 'error',
                'current': 0,
                'total': 0,
                'message': message,
                'file_name': file_name,
                'stage': 'error',
                'error_type': error_type
            }
            if solution:
                progress['solution'] = solution
            self.progress_map[file_path] = progress
    
    def get_progress(self, file_path: Optional[str] = None) -> dict:
        """获取进度"""
        with self._lock:
            if file_path:
                return self.progress_map.get(file_path, {
                    'status': 'idle',
                    'current': 0,
                    'total': 0,
                    'message': '',
                    'file_name': os.path.basename(file_path) if file_path else '',
                    'stage': ''
                })
            
            if self.current_loading_file and self.current_loading_file in self.progress_map:
                return self.progress_map[self.current_loading_file]
            
            return {
                'status': 'idle',
                'current': 0,
                'total': 0,
                'message': '',
                'file_name': '',
                'stage': ''
            }
    
    def is_loading(self, file_path: str) -> bool:
        """检查是否正在加载"""
        with self._lock:
            progress = self.progress_map.get(file_path, {})
            return progress.get('status') == 'loading'
    
    def get_loading_file(self) -> Optional[str]:
        """获取当前正在加载的文件"""
        with self._lock:
            for path, progress in self.progress_map.items():
                if progress.get('status') == 'loading':
                    return path
            return None
    
    def clear(self, file_path: Optional[str] = None) -> None:
        """清除进度"""
        with self._lock:
            if file_path:
                if file_path in self.progress_map:
                    del self.progress_map[file_path]
                if self.current_loading_file == file_path:
                    self.current_loading_file = None
            else:
                self.progress_map.clear()
                self.current_loading_file = None
