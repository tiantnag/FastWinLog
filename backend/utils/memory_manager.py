#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Memory management utility"""

import gc
import os
import time
import threading
from typing import Dict, List, Any, Optional


class MemoryManager:
    """内存管理器"""
    
    MAX_CACHED_FILES = 2  # 最多保留2个文件在内存中
    
    def __init__(self):
        self.memory_cache: Dict[str, List[dict]] = {}
        self.cache_stats: Dict[str, dict] = {}
        self.fields_cache: Dict[str, dict] = {}
        self.current_file: Optional[str] = None
        self._lock = threading.Lock()
    
    def get(self, file_path: str) -> Optional[List[dict]]:
        """获取缓存的事件数据"""
        with self._lock:
            return self.memory_cache.get(file_path)
    
    def set(self, file_path: str, events: List[dict], stats: Optional[dict] = None) -> None:
        """设置缓存"""
        with self._lock:
            self.memory_cache[file_path] = events
            self.current_file = file_path
            
            if stats:
                self.cache_stats[file_path] = stats
            else:
                self.cache_stats[file_path] = {
                    'total_events': len(events),
                    'loaded_at': time.time(),
                    'file_path': file_path
                }
            
            # 智能释放旧文件
            self._release_old_files()
    
    def has(self, file_path: str) -> bool:
        """检查是否有缓存"""
        with self._lock:
            return file_path in self.memory_cache
    
    def get_stats(self, file_path: str) -> Optional[dict]:
        """获取缓存统计"""
        with self._lock:
            return self.cache_stats.get(file_path)
    
    def get_fields_cache(self, file_path: str) -> Optional[dict]:
        """获取字段缓存"""
        with self._lock:
            return self.fields_cache.get(file_path)
    
    def set_fields_cache(self, file_path: str, fields: dict) -> None:
        """设置字段缓存"""
        with self._lock:
            self.fields_cache[file_path] = fields
    
    def release(self, file_path: Optional[str] = None) -> None:
        """释放内存缓存"""
        with self._lock:
            if file_path:
                if file_path in self.memory_cache:
                    del self.memory_cache[file_path]
                if file_path in self.cache_stats:
                    del self.cache_stats[file_path]
                if file_path in self.fields_cache:
                    del self.fields_cache[file_path]
                if self.current_file == file_path:
                    self.current_file = None
                print(f"[内存缓存] 已释放: {os.path.basename(file_path)}")
            else:
                count = len(self.memory_cache)
                self.memory_cache.clear()
                self.cache_stats.clear()
                self.fields_cache.clear()
                self.current_file = None
                print(f"[内存缓存] 已释放所有缓存 ({count}个文件)")
            
            gc.collect()
    
    def _release_old_files(self) -> None:
        """智能释放旧文件"""
        if len(self.memory_cache) > self.MAX_CACHED_FILES:
            # 按最后访问时间排序
            sorted_files = sorted(
                self.cache_stats.items(),
                key=lambda x: x[1].get('loaded_at', 0)
            )
            
            # 释放最旧的文件
            files_to_release = len(self.memory_cache) - self.MAX_CACHED_FILES
            for file_path, _ in sorted_files[:files_to_release]:
                if file_path in self.memory_cache:
                    del self.memory_cache[file_path]
                if file_path in self.cache_stats:
                    del self.cache_stats[file_path]
                if file_path in self.fields_cache:
                    del self.fields_cache[file_path]
                print(f"[智能释放] 释放旧文件: {os.path.basename(file_path)}")
    
    def get_all_cached_files(self) -> List[str]:
        """获取所有缓存的文件路径"""
        with self._lock:
            return list(self.memory_cache.keys())
    
    def get_cache_size(self) -> int:
        """获取缓存文件数量"""
        with self._lock:
            return len(self.memory_cache)
