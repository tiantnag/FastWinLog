#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FastWinLog - Field Descriptions
Version: 1.0.0
Repository: https://github.com/vam876/FastWinLog
"""

from .static_field_dict import (
    FIELD_DICT,
    DEFAULT_VISIBLE_FIELDS,
    SUPPORTED_LOG_TYPES,
    RECOMMENDED_FIELDS_BY_TYPE,
    CHANNEL_TO_LOG_TYPE,
    FIELDS_BY_LOG_TYPE,
    get_field_info,
    get_all_fields,
    get_default_visible_fields,
    get_recommended_fields,
    get_log_type_by_channel,
    is_supported_channel,
    get_fields_for_log_type,
)


def get_log_type(file_name: str) -> str:
    """
    根据文件名猜测日志类型（备用方法）
    推荐使用 get_log_type_by_channel() 通过Channel识别
    """
    import os
    base_name = os.path.basename(file_name).lower()
    
    if 'security' in base_name:
        return 'Security'
    if 'application' in base_name:
        return 'Application'
    if 'system' in base_name:
        return 'System'
    if 'powershell' in base_name:
        return 'PowerShell'
    
    return 'Unknown'


def is_supported_log(file_name: str) -> bool:
    """
    Check if log type is supported (all types are supported)
    Recommended to use is_supported_channel() for Channel-based detection
    """
    return True  # All log types are now supported


def get_complete_field_descriptions():
    """获取完整的字段描述列表"""
    return get_all_fields()


__all__ = [
    'FIELD_DICT',
    'DEFAULT_VISIBLE_FIELDS',
    'SUPPORTED_LOG_TYPES',
    'RECOMMENDED_FIELDS_BY_TYPE',
    'CHANNEL_TO_LOG_TYPE',
    'FIELDS_BY_LOG_TYPE',
    'get_field_info',
    'get_all_fields',
    'get_default_visible_fields',
    'get_recommended_fields',
    'get_log_type',
    'is_supported_log',
    'get_log_type_by_channel',
    'is_supported_channel',
    'get_fields_for_log_type',
    'get_complete_field_descriptions'
]
