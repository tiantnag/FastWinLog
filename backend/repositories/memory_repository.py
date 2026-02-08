#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Memory cache repository"""

import os
from typing import Dict, List, Any, Optional, Tuple
from ..utils.memory_manager import MemoryManager
from ..core.log_descriptions import get_event_description


class MemoryRepository:
    """内存缓存仓储"""
    
    def __init__(self, memory_manager: MemoryManager):
        self.memory = memory_manager
    
    def has_cache(self, file_path: str) -> bool:
        """检查是否有缓存"""
        return self.memory.has(file_path)
    
    def get_events(self, file_path: str) -> Optional[List[dict]]:
        """获取所有事件"""
        return self.memory.get(file_path)
    
    def set_events(self, file_path: str, events: List[dict], stats: Optional[dict] = None) -> None:
        """设置事件缓存"""
        self.memory.set(file_path, events, stats)
    
    def get_paginated(self, file_path: str, page: int = 1, page_size: int = 100) -> Tuple[List[dict], int]:
        """分页获取事件"""
        events = self.memory.get(file_path)
        if not events:
            return [], 0
        
        total = len(events)
        start = (page - 1) * page_size
        end = start + page_size
        page_events = events[start:end]
        
        # 添加事件描述
        result_events = []
        for event in page_events:
            event_copy = event.copy()
            event_id = event_copy.get('EventID')
            if event_id:
                desc = get_event_description(event_id)
                event_copy['_event_name'] = desc['name']
                event_copy['_event_description'] = desc['description']
                event_copy['_event_category'] = desc['category']
                event_copy['_event_severity'] = desc.get('severity', 'info')
            result_events.append(event_copy)
        
        return result_events, total
    
    def search(self, file_path: str, keyword: str, page: int = 1, page_size: int = 100) -> Tuple[List[dict], int]:
        """搜索事件 - 优先精确匹配EventID，避免误匹配"""
        events = self.memory.get(file_path)
        if not events:
            return [], 0
        
        keywords = [k.strip().lower() for k in keyword.split() if k.strip()]
        if not keywords:
            return [], 0
        
        matched_events = []
        
        # 🔥 优先策略：如果是单个纯数字关键词，优先精确匹配 EventID
        if len(keywords) == 1 and keywords[0].isdigit():
            for event in events:
                event_id = str(event.get('EventID', '')).strip()
                if event_id == keywords[0]:
                    matched_events.append(event)
            
            # 如果精确匹配到结果，直接返回
            if matched_events:
                total = len(matched_events)
                start = (page - 1) * page_size
                end = start + page_size
                page_events = matched_events[start:end]
                
                # 添加事件描述
                result_events = []
                for event in page_events:
                    event_copy = event.copy()
                    event_id = event_copy.get('EventID')
                    if event_id:
                        desc = get_event_description(event_id)
                        event_copy['_event_name'] = desc['name']
                        event_copy['_event_description'] = desc['description']
                        event_copy['_event_category'] = desc['category']
                        event_copy['_event_severity'] = desc.get('severity', 'info')
                    result_events.append(event_copy)
                
                return result_events, total
        
        # 🔥 次要策略：在关键字段中模糊搜索（排除容易误匹配的字段）
        for event in events:
            # 构建搜索文本（排除容易误匹配的字段）
            search_parts = []
            for key, value in event.items():
                # 排除容易误匹配的字段
                if key in ['RecordID', 'ProcessID', 'ThreadID', 'Version', 'Task', 'Opcode', 'Keywords', 'Correlation_ActivityID', 'Execution_ProcessID', 'Execution_ThreadID']:
                    continue
                if value:
                    search_parts.append(str(value).lower())
            
            # 添加事件描述
            event_id = event.get('EventID')
            if event_id:
                desc = get_event_description(event_id)
                search_parts.append(desc.get('name', '').lower())
                search_parts.append(desc.get('description', '').lower())
            
            search_text = ' '.join(search_parts)
            
            # 多关键词匹配
            if all(kw in search_text for kw in keywords):
                matched_events.append(event)
        
        total = len(matched_events)
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        page_events = matched_events[start:end]
        
        # 添加事件描述
        result_events = []
        for event in page_events:
            event_copy = event.copy()
            event_id = event_copy.get('EventID')
            if event_id:
                desc = get_event_description(event_id)
                event_copy['_event_name'] = desc['name']
                event_copy['_event_description'] = desc['description']
                event_copy['_event_category'] = desc['category']
                event_copy['_event_severity'] = desc.get('severity', 'info')
            result_events.append(event_copy)
        
        return result_events, total
    
    def advanced_search(self, file_path: str, filters: Dict[str, str], 
                        page: int = 1, page_size: int = 100) -> Tuple[List[dict], int]:
        """高级搜索 - 使用精确匹配，避免误匹配"""
        events = self.memory.get(file_path)
        if not events:
            return [], 0
        
        matched_events = []
        for event in events:
            match = True
            for field, value in filters.items():
                if not field or not value:
                    continue
                
                search_value = str(value).strip().lower()
                event_value = str(event.get(field, '')).strip().lower()
                
                # 🔥 所有字段都使用精确匹配，避免误匹配
                # 例如：LogonType=10 不会匹配 LogonType=100
                if event_value != search_value:
                    match = False
                    break
            
            if match:
                matched_events.append(event)
        
        total = len(matched_events)
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        page_events = matched_events[start:end]
        
        # 添加事件描述
        result_events = []
        for event in page_events:
            event_copy = event.copy()
            event_id = event_copy.get('EventID')
            if event_id:
                desc = get_event_description(event_id)
                event_copy['_event_name'] = desc['name']
                event_copy['_event_description'] = desc['description']
                event_copy['_event_category'] = desc['category']
                event_copy['_event_severity'] = desc.get('severity', 'info')
            result_events.append(event_copy)
        
        return result_events, total
    
    def release(self, file_path: Optional[str] = None) -> None:
        """释放缓存"""
        self.memory.release(file_path)
