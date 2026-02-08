#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FastWinLog - Data Models
Version: 1.0.0
Repository: https://github.com/vam876/FastWinLog
"""

from .event import Event, EventDescription
from .log_file import LogFile, LogFileInfo
from .pagination import Pagination, PaginatedResult
from .search_result import SearchResult, AdvancedSearchResult

__all__ = [
    'Event', 'EventDescription',
    'LogFile', 'LogFileInfo', 
    'Pagination', 'PaginatedResult',
    'SearchResult', 'AdvancedSearchResult'
]
