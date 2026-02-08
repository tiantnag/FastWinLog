#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Pagination data model"""

from dataclasses import dataclass, field
from typing import List, Any, Generic, TypeVar

T = TypeVar('T')


@dataclass
class Pagination:
    """分页信息"""
    page: int = 1
    page_size: int = 100
    total_count: int = 0
    total_pages: int = 0
    has_next: bool = False
    has_prev: bool = False
    
    @classmethod
    def create(cls, page: int, page_size: int, total_count: int) -> 'Pagination':
        """创建分页信息"""
        total_pages = (total_count + page_size - 1) // page_size if total_count > 0 else 1
        return cls(
            page=page,
            page_size=page_size,
            total_count=total_count,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1
        )
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'page': self.page,
            'page_size': self.page_size,
            'total_count': self.total_count,
            'total_pages': self.total_pages,
            'has_next': self.has_next,
            'has_prev': self.has_prev
        }


@dataclass
class PaginatedResult:
    """分页结果"""
    success: bool = True
    events: List[Any] = field(default_factory=list)
    pagination: Pagination = field(default_factory=Pagination)
    from_cache: bool = False
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
        if self.error:
            result['error'] = self.error
        return result
