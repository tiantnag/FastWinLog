#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Search service"""

import os
from typing import Dict, Any, Optional
from ..core.log_descriptions import get_event_description
from ..repositories.sqlite_repository import SqliteRepository
from ..repositories.memory_repository import MemoryRepository
from ..repositories.evtx_repository import EvtxRepository


class SearchService:
    """搜索服务"""
    
    def __init__(self, sqlite_repo: SqliteRepository, memory_repo: MemoryRepository,
                 evtx_repo: EvtxRepository):
        self.sqlite_repo = sqlite_repo
        self.memory_repo = memory_repo
        self.evtx_repo = evtx_repo
    
    def search_events(self, file_path: str, keyword: str, page: int = 1, page_size: int = 100,
                      sort_field: str = None, sort_direction: str = 'asc') -> dict:
        """搜索事件"""
        try:
            print(f"\n[搜索] 关键词: '{keyword}' | 文件: {os.path.basename(file_path)}")
            
            # 策略1：SQLite缓存搜索
            if self.sqlite_repo.is_cache_valid(file_path):
                print(f"[SQLite搜索] 使用缓存 | 排序: {sort_field} {sort_direction}")
                result = self.sqlite_repo.search_in_cache(file_path, keyword, page, page_size, sort_field, sort_direction)
                
                if result['success']:
                    self._add_event_descriptions(result['events'])
                    return result
            
            # 策略2：内存搜索
            if not self.memory_repo.has_cache(file_path):
                events, stats = self.evtx_repo.parse_file(file_path)
                self.memory_repo.set_events(file_path, events, stats)
                
                try:
                    self.sqlite_repo.create_cache(file_path, events, show_progress=True)
                except Exception as e:
                    print(f"[SQLite缓存] 创建失败: {e}")
            
            events, total = self.memory_repo.search(file_path, keyword, page, page_size)
            
            # 排序
            if sort_field and events:
                reverse = (sort_direction == 'desc')
                try:
                    if sort_field in events[0]:
                        events.sort(key=lambda x: str(x.get(sort_field, '')), reverse=reverse)
                except Exception as e:
                    print(f"[排序警告] 无法排序字段 {sort_field}: {e}")
            
            self._add_event_descriptions(events)
            
            return self._build_result(events, page, page_size, total)
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}

    def advanced_search_events(self, file_path: str, filters: Dict[str, str], page: int = 1,
                               page_size: int = 100, sort_field: str = None, sort_direction: str = 'asc') -> dict:
        """高级搜索事件"""
        try:
            print(f"\n[高级搜索] 条件: {filters} | 文件: {os.path.basename(file_path)}")
            
            # 策略1：SQLite缓存搜索
            if self.sqlite_repo.is_cache_valid(file_path):
                print(f"[SQLite高级搜索] 使用缓存 | 排序: {sort_field} {sort_direction}")
                result = self.sqlite_repo.advanced_search_in_cache(file_path, filters, page, page_size, sort_field, sort_direction)
                
                if result['success']:
                    self._add_event_descriptions(result['events'])
                    return result
            
            # 策略2：内存搜索
            if not self.memory_repo.has_cache(file_path):
                events, stats = self.evtx_repo.parse_file(file_path)
                self.memory_repo.set_events(file_path, events, stats)
                
                try:
                    self.sqlite_repo.create_cache(file_path, events, show_progress=True)
                except Exception as e:
                    print(f"[SQLite缓存] 创建失败: {e}")
            
            events, total = self.memory_repo.advanced_search(file_path, filters, page, page_size)
            
            # 排序
            if sort_field and events:
                reverse = (sort_direction == 'desc')
                try:
                    if sort_field in events[0]:
                        events.sort(key=lambda x: str(x.get(sort_field, '')), reverse=reverse)
                except Exception as e:
                    print(f"[排序警告] 无法排序字段 {sort_field}: {e}")
            
            self._add_event_descriptions(events)
            
            result = self._build_result(events, page, page_size, total)
            result['filters_applied'] = filters
            return result
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}
    
    def _add_event_descriptions(self, events: list) -> None:
        """为事件添加描述"""
        for event in events:
            event_id = event.get('EventID')
            if event_id:
                desc = get_event_description(event_id)
                event['_event_name'] = desc['name']
                event['_event_description'] = desc['description']
                event['_event_category'] = desc['category']
                event['_event_severity'] = desc.get('severity', 'info')
    
    def _build_result(self, events: list, page: int, page_size: int, total: int) -> dict:
        """构建搜索结果"""
        total_pages = (total + page_size - 1) // page_size if total > 0 else 1
        return {
            'success': True,
            'events': events,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_count': total,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }
