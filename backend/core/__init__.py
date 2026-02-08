#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FastWinLog - Core Modules
Version: 1.0.0
Repository: https://github.com/vam876/FastWinLog
"""

from .log_descriptions import get_log_description, get_event_description
from .alert_store import AlertStore
from .alert_baselines import security_baseline, system_baseline, application_baseline, choose_baseline_by_filename
from .security_presets import (
    get_all_presets, 
    get_presets_by_category, 
    get_preset_by_id,
    PRESET_CATEGORIES,
    SEVERITY_LEVELS,
    OPERATORS,
    build_sql_condition
)
from .field_descriptions import (
    get_complete_field_descriptions,
    get_all_fields,
    get_default_visible_fields,
    get_field_info,
    get_recommended_fields,
    get_log_type,
    is_supported_log,
    FIELD_DICT,
    DEFAULT_VISIBLE_FIELDS,
    SUPPORTED_LOG_TYPES,
    RECOMMENDED_FIELDS_BY_TYPE
)
from .evtx_parser import EvtxParser
from .windows_events_database import ALL_EVENTS, get_event_info

__all__ = [
    'get_log_description', 'get_event_description',
    'AlertStore',
    'security_baseline', 'system_baseline', 'application_baseline', 'choose_baseline_by_filename',
    'get_all_presets', 'get_presets_by_category', 'get_preset_by_id',
    'PRESET_CATEGORIES', 'SEVERITY_LEVELS', 'OPERATORS', 'build_sql_condition',
    'get_complete_field_descriptions', 'get_all_fields', 'get_default_visible_fields', 'get_field_info',
    'get_recommended_fields', 'get_log_type', 'is_supported_log',
    'FIELD_DICT', 'DEFAULT_VISIBLE_FIELDS', 'SUPPORTED_LOG_TYPES', 'RECOMMENDED_FIELDS_BY_TYPE',
    'EvtxParser',
    'ALL_EVENTS', 'get_event_info'
]
