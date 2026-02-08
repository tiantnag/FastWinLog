#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Search result data model"""

from dataclasses import dataclass, field
from typing import List, Any, Dict, Optional
from .pagination import Pagination


@dataclass
class SearchResult:
    """搜索结果"""
    success: bool = True
    events: List[Any] = field(default_factory=list)
    pagination: Pagination = field(default_factory=Pagination)
    from_cache: bool = False
    search_info: Optional[Dict] = None
    error: str = ''
    
    def to_dict(self) -> dict:
        """转换为字典"""
        result = {
            'success': self.success,
            'events': self.events,
            'pagination': self.pagination.to_dict()
        }
        if self.from_cache:
            result['from_cache'] = self.from_cache
        if self.search_info:
            result['search_info'] = self.search_info
        if self.error:
            result['error'] = self.error
        return result


@dataclass
class AdvancedSearchResult:
    """高级搜索结果"""
    success: bool = True
    events: List[Any] = field(default_factory=list)
    pagination: Pagination = field(default_factory=Pagination)
    filters_applied: Dict[str, Any] = field(default_factory=dict)
    from_cache: bool = False
    error: str = ''
    
    def to_dict(self) -> dict:
        """转换为字典"""
        result = {
            'success': self.success,
            'events': self.events,
            'pagination': self.pagination.to_dict()
        }
        if self.filters_applied:
            result['filters_applied'] = self.filters_applied
        if self.from_cache:
            result['from_cache'] = self.from_cache
        if self.error:
            result['error'] = self.error
        return result


@dataclass
class FilterInfo:
    """过滤信息"""
    scanned: int = 0
    matched: int = 0
