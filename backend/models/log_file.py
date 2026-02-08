#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Log file data model"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LogFileInfo:
    """日志文件描述信息"""
    name: str = ''
    description: str = ''
    category: str = '其他'
    importance: str = 'low'


@dataclass
class LogFile:
    """日志文件数据模型"""
    file_path: str = ''
    file_name: str = ''
    log_name: str = ''
    file_size: int = 0
    file_size_mb: float = 0.0
    display_name: str = ''
    description: str = ''
    category: str = ''
    importance: str = 'low'
    source: str = 'logs'  # logs | loaded | history | cached
    is_cached: bool = False
    file_exists: bool = True
    total_events: int = 0
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'file_path': self.file_path,
            'file_name': self.file_name,
            'log_name': self.log_name,
            'file_size': self.file_size,
            'file_size_mb': self.file_size_mb,
            'display_name': self.display_name,
            'description': self.description,
            'category': self.category,
            'importance': self.importance,
            'source': self.source,
            'is_cached': self.is_cached,
            'file_exists': self.file_exists,
            'total_events': self.total_events
        }


@dataclass
class LoadProgress:
    """加载进度信息"""
    status: str = 'idle'  # idle | counting | loading | done | error
    current: int = 0
    total: int = 0
    message: str = ''
    file_name: str = ''
    stage: str = ''  # counting | parsing | done | error
    speed: float = 0.0
    progress_pct: float = 0.0
    error_type: Optional[str] = None
    solution: Optional[dict] = None
    
    def to_dict(self) -> dict:
        """转换为字典"""
        result = {
            'status': self.status,
            'current': self.current,
            'total': self.total,
            'message': self.message,
            'file_name': self.file_name,
            'stage': self.stage
        }
        if self.speed > 0:
            result['speed'] = self.speed
        if self.progress_pct > 0:
            result['progress_pct'] = self.progress_pct
        if self.error_type:
            result['error_type'] = self.error_type
        if self.solution:
            result['solution'] = self.solution
        return result
