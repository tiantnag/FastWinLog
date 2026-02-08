#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Cache management service"""

import gc
from typing import Dict, Any, Optional
from ..repositories.sqlite_repository import SqliteRepository
from ..utils.memory_manager import MemoryManager


class CacheService:
    """缓存管理服务"""
    
    def __init__(self, sqlite_repo: SqliteRepository, memory_manager: MemoryManager):
        self.sqlite_repo = sqlite_repo
        self.memory = memory_manager
    
    def get_cache_info(self) -> dict:
        """获取缓存统计信息"""
        try:
            return self.sqlite_repo.get_cache_info()
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def clear_all_cache(self) -> dict:
        """清空所有缓存"""
        try:
            # 清理SQLite缓存
            self.sqlite_repo.clear_cache()
            
            # 清理内存缓存
            self.memory.release()
            
            # 强制垃圾回收
            gc.collect()
            
            print("[缓存管理] 已清空所有缓存")
            
            return {'success': True, 'message': '所有缓存已清空'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def clear_file_cache(self, file_path: str) -> dict:
        """清空指定文件的缓存"""
        try:
            import os
            
            # 清理SQLite缓存
            self.sqlite_repo.clear_cache(file_path)
            
            # 清理内存缓存
            self.memory.release(file_path)
            
            print(f"[缓存管理] 已清空缓存: {os.path.basename(file_path)}")
            
            return {'success': True, 'message': f'缓存已清空: {os.path.basename(file_path)}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
