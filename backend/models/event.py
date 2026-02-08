#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Event data model"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class EventDescription:
    """事件描述信息"""
    name: str = ''
    description: str = ''
    category: str = '其他'
    severity: str = 'info'
    fields: List[str] = field(default_factory=list)


@dataclass
class Event:
    """事件数据模型"""
    RecordID: str = ''
    EventID: str = ''
    Level: str = ''
    TimeCreated: str = ''
    Provider: str = ''
    Computer: str = ''
    Channel: str = ''
    
    # 扩展字段
    _event_name: str = ''
    _event_description: str = ''
    _event_category: str = ''
    _event_severity: str = 'info'
    _xml: str = ''
    
    # 动态字段存储
    extra_fields: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            'RecordID': self.RecordID,
            'EventID': self.EventID,
            'Level': self.Level,
            'TimeCreated': self.TimeCreated,
            'Provider': self.Provider,
            'Computer': self.Computer,
            'Channel': self.Channel,
            '_event_name': self._event_name,
            '_event_description': self._event_description,
            '_event_category': self._event_category,
            '_event_severity': self._event_severity,
        }
        # 合并额外字段
        result.update(self.extra_fields)
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        """从字典创建事件"""
        known_fields = {
            'RecordID', 'EventID', 'Level', 'TimeCreated', 
            'Provider', 'Computer', 'Channel',
            '_event_name', '_event_description', '_event_category', '_event_severity', '_xml'
        }
        
        event = cls(
            RecordID=str(data.get('RecordID', '')),
            EventID=str(data.get('EventID', '')),
            Level=str(data.get('Level', '')),
            TimeCreated=str(data.get('TimeCreated', '')),
            Provider=str(data.get('Provider', '')),
            Computer=str(data.get('Computer', '')),
            Channel=str(data.get('Channel', '')),
            _event_name=str(data.get('_event_name', '')),
            _event_description=str(data.get('_event_description', '')),
            _event_category=str(data.get('_event_category', '')),
            _event_severity=str(data.get('_event_severity', 'info')),
            _xml=str(data.get('_xml', '')),
        )
        
        # 收集额外字段
        for key, value in data.items():
            if key not in known_fields:
                event.extra_fields[key] = value
        
        return event


@dataclass
class FieldCompleteness:
    """字段完整性信息"""
    expected_count: int = 0
    present_count: int = 0
    missing_fields: List[str] = field(default_factory=list)
    present_fields: List[str] = field(default_factory=list)
    completeness_ratio: float = 1.0
