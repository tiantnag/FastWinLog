#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""SQLite cache repository"""

import os
import sys
import sqlite3
import json
import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple


class SqliteRepository:
    """SQLite缓存仓储"""
    
    def __init__(self, cache_dir: str = 'cache'):
        # 🔥 修复：cache目录始终在程序运行目录下
        if getattr(sys, 'frozen', False):
            # 打包后：在exe所在目录
            base_dir = os.path.dirname(sys.executable)
        else:
            # 开发环境：在项目根目录
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        self.cache_dir = os.path.join(base_dir, cache_dir)
        os.makedirs(self.cache_dir, exist_ok=True)
        print(f"[Cache] 缓存目录: {self.cache_dir}")
        self.cache_valid_map = {}
        self.scan_progress_map = {}
    
    def clear_cache_status(self, evtx_file_path: str = None):
        """清除缓存状态，强制重新检查"""
        if evtx_file_path:
            if evtx_file_path in self.cache_valid_map:
                del self.cache_valid_map[evtx_file_path]
                print(f"[缓存] 已清除缓存状态: {os.path.basename(evtx_file_path)}")
        else:
            self.cache_valid_map.clear()
            print(f"[缓存] 已清除所有缓存状态")

    def get_cache_path(self, evtx_file_path: str) -> str:
        """获取缓存文件路径"""
        full_path = os.path.abspath(evtx_file_path)
        full_path = os.path.normpath(full_path).lower()
        path_hash = hashlib.md5(full_path.encode('utf-8')).hexdigest()[:8]
        filename = os.path.basename(evtx_file_path).replace('.evtx', '').replace('.EVTX', '')
        cache_name = f"{filename}_{path_hash}.cache.db"
        return os.path.join(self.cache_dir, cache_name)
    
    def is_cache_valid(self, evtx_file_path: str) -> bool:
        """检查缓存是否有效"""
        # 🔥 缩短缓存时间到 30 秒，避免长时间缓存无效状态
        if evtx_file_path in self.cache_valid_map:
            cached_result = self.cache_valid_map[evtx_file_path]
            if time.time() - cached_result['checked_at'] < 30:
                return cached_result['valid']
        
        cache_path = self.get_cache_path(evtx_file_path)
        
        if not os.path.exists(cache_path):
            self.cache_valid_map[evtx_file_path] = {'valid': False, 'checked_at': time.time()}
            return False
        
        try:
            with sqlite3.connect(cache_path, timeout=10.0) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
                if not cursor.fetchone():
                    return False
                
                cursor.execute("SELECT COUNT(*) FROM events")
                count = cursor.fetchone()[0]
                if count == 0:
                    return False
                
                cursor.execute("SELECT value FROM metadata WHERE key = 'source_mtime'")
                row = cursor.fetchone()
                if not row:
                    return False
                
                cache_mtime = float(row[0])
            
            evtx_mtime = os.path.getmtime(evtx_file_path)
            time_diff = abs(evtx_mtime - cache_mtime)
            
            if time_diff > 60:
                self.cache_valid_map[evtx_file_path] = {'valid': False, 'checked_at': time.time()}
                return False
            
            self.cache_valid_map[evtx_file_path] = {'valid': True, 'checked_at': time.time()}
            return True
            
        except Exception as e:
            print(f"[缓存] 检查失败: {e}")
            return False

    def create_cache(self, evtx_file_path: str, events_data: List[dict], show_progress: bool = True) -> str:
        """创建缓存 - 直接存储事件数据，不做字段提取"""
        cache_path = self.get_cache_path(evtx_file_path)
        
        if os.path.exists(cache_path):
            os.remove(cache_path)
        
        print(f"[缓存] 创建SQLite缓存: {os.path.basename(cache_path)}")
        start_time = time.time()
        
        conn = sqlite3.connect(cache_path, timeout=30.0)
        cursor = conn.cursor()
        
        conn.execute('PRAGMA journal_mode = DELETE')
        conn.execute('PRAGMA synchronous = NORMAL')
        conn.execute('PRAGMA cache_size = -64000')
        conn.execute('PRAGMA temp_store = MEMORY')
        
        # 简化表结构 - 直接存储JSON
        cursor.execute('''
            CREATE TABLE events (
                RecordID INTEGER PRIMARY KEY,
                EventID TEXT,
                Level TEXT,
                TimeCreated TEXT,
                Provider TEXT,
                Computer TEXT,
                Channel TEXT,
                event_json TEXT
            )
        ''')
        
        cursor.execute('CREATE INDEX idx_event_id ON events(EventID)')
        cursor.execute('CREATE INDEX idx_time ON events(TimeCreated)')
        
        cursor.execute('CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT)')
        
        evtx_mtime = os.path.getmtime(evtx_file_path)
        metadata = {
            'source_file': evtx_file_path,
            'source_mtime': str(evtx_mtime),
            'cache_created': str(time.time()),
            'total_events': str(len(events_data)),
            'version': '2.0'
        }
        
        for key, value in metadata.items():
            cursor.execute("INSERT INTO metadata (key, value) VALUES (?, ?)", (key, value))
        
        batch_size = 1000
        total = len(events_data)
        
        for i in range(0, total, batch_size):
            batch = events_data[i:i+batch_size]
            rows = []
            
            for event in batch:
                row = (
                    event.get('RecordID'),
                    event.get('EventID'),
                    event.get('Level'),
                    event.get('TimeCreated'),
                    event.get('Provider') or event.get('Provider_Name'),
                    event.get('Computer'),
                    event.get('Channel'),
                    json.dumps(event, ensure_ascii=False)
                )
                rows.append(row)
            
            cursor.executemany('''
                INSERT INTO events 
                (RecordID, EventID, Level, TimeCreated, Provider, Computer, Channel, event_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', rows)
            
            if show_progress:
                progress = min(i + batch_size, total)
                elapsed = time.time() - start_time
                speed = progress / elapsed if elapsed > 0 else 0
                print(f"  [缓存] 进度: {progress}/{total} ({progress/total*100:.1f}%) | {speed:.0f}条/秒", end='\r')
        
        conn.commit()
        conn.close()
        
        elapsed = time.time() - start_time
        print(f"\n  [缓存] 完成: {total}条 | 耗时{elapsed:.1f}秒")
        
        return cache_path

    def load_from_cache(self, evtx_file_path: str, page: int = 1, page_size: int = 100,
                        sort_field: str = None, sort_direction: str = 'asc') -> dict:
        """从缓存加载事件"""
        cache_path = self.get_cache_path(evtx_file_path)
        
        try:
            with sqlite3.connect(cache_path, timeout=10.0) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM events")
                total = cursor.fetchone()[0]
                
                order_by = "RecordID"
                allowed_fields = ['RecordID', 'EventID', 'Level', 'TimeCreated', 'Provider', 'Computer', 'Channel']
                
                if sort_field and sort_field in allowed_fields:
                    order_by = sort_field
                
                direction = "DESC" if sort_direction.lower() == 'desc' else "ASC"
                offset = (page - 1) * page_size
                
                cursor.execute(f'''
                    SELECT event_json FROM events 
                    ORDER BY {order_by} {direction} LIMIT ? OFFSET ?
                ''', (page_size, offset))
                
                events = []
                for row in cursor.fetchall():
                    try:
                        event = json.loads(row[0])
                        events.append(event)
                    except:
                        pass
            
            total_pages = (total + page_size - 1) // page_size
            
            return {
                'success': True,
                'events': events,
                'pagination': {
                    'page': page, 'page_size': page_size, 'total_count': total,
                    'total_pages': total_pages, 'has_next': page < total_pages, 'has_prev': page > 1
                },
                'from_cache': True
            }
        except Exception as e:
            print(f"[缓存] 加载失败: {e}")
            return {'success': False, 'error': str(e)}

    def search_in_cache(self, evtx_file_path: str, keyword: str, page: int = 1, page_size: int = 100,
                        sort_field: str = None, sort_direction: str = 'asc') -> dict:
        """在缓存中搜索（优先精确匹配EventID，避免误匹配）"""
        cache_path = self.get_cache_path(evtx_file_path)
        
        try:
            from ..core.log_descriptions import get_event_description
            
            conn = sqlite3.connect(cache_path)
            cursor = conn.cursor()
            
            keywords = [k.strip().lower() for k in keyword.split() if k.strip()]
            if not keywords:
                return {'success': True, 'events': [], 'pagination': {'page': page, 'page_size': page_size, 'total_count': 0, 'total_pages': 0, 'has_next': False, 'has_prev': False}}
            
            matched_events = []
            
            # 🔥 优先策略：如果是单个纯数字关键词，优先精确匹配 EventID
            if len(keywords) == 1 and keywords[0].isdigit():
                cursor.execute('SELECT event_json FROM events WHERE EventID = ?', [keywords[0]])
                
                for row in cursor.fetchall():
                    try:
                        event = json.loads(row[0])
                        matched_events.append(event)
                    except:
                        pass
                
                # 如果精确匹配到结果，直接返回
                if matched_events:
                    conn.close()
                    
                    # 排序
                    if sort_field and matched_events:
                        reverse = (sort_direction.lower() == 'desc')
                        try:
                            def sort_key(event):
                                val = event.get(sort_field, '')
                                if val == '' or val is None:
                                    return (1, '')
                                try:
                                    return (0, float(val))
                                except:
                                    return (0, str(val).lower())
                            
                            matched_events.sort(key=sort_key, reverse=reverse)
                        except Exception as e:
                            print(f"[排序警告] 无法排序字段 {sort_field}: {e}")
                    
                    total = len(matched_events)
                    offset = (page - 1) * page_size
                    page_events = matched_events[offset:offset + page_size]
                    total_pages = (total + page_size - 1) // page_size
                    
                    return {
                        'success': True, 'events': page_events,
                        'pagination': {'page': page, 'page_size': page_size, 'total_count': total, 'total_pages': total_pages, 'has_next': page < total_pages, 'has_prev': page > 1},
                        'from_cache': True
                    }
            
            # 🔥 次要策略：在JSON中模糊搜索
            conditions = []
            params = []
            for kw in keywords:
                conditions.append('event_json LIKE ? COLLATE NOCASE')
                params.append(f'%{kw}%')
            
            cursor.execute(f'''
                SELECT event_json FROM events WHERE {" AND ".join(conditions)}
            ''', params)
            
            for row in cursor.fetchall():
                try:
                    event = json.loads(row[0])
                    
                    # 🔥 过滤误匹配：如果是纯数字搜索，排除RecordID等字段的误匹配
                    if len(keywords) == 1 and keywords[0].isdigit():
                        event_id = str(event.get('EventID', '')).strip()
                        # 如果EventID不匹配，检查是否是其他数字字段误匹配
                        if event_id != keywords[0]:
                            # 检查是否在RecordID、ProcessID等字段中匹配
                            record_id = str(event.get('RecordID', '')).strip()
                            process_id = str(event.get('ProcessID', '')).strip()
                            thread_id = str(event.get('ThreadID', '')).strip()
                            
                            if (keywords[0] in record_id or 
                                keywords[0] in process_id or 
                                keywords[0] in thread_id):
                                continue  # 跳过这些字段的误匹配
                    
                    matched_events.append(event)
                except:
                    pass
            
            conn.close()
            
            # 🔥 修复：添加排序支持
            if sort_field and matched_events:
                reverse = (sort_direction.lower() == 'desc')
                try:
                    # 尝试数字排序，失败则字符串排序
                    def sort_key(event):
                        val = event.get(sort_field, '')
                        if val == '' or val is None:
                            return (1, '')  # 空值排在最后
                        try:
                            return (0, float(val))
                        except:
                            return (0, str(val).lower())
                    
                    matched_events.sort(key=sort_key, reverse=reverse)
                except Exception as e:
                    print(f"[排序警告] 无法排序字段 {sort_field}: {e}")
            
            total = len(matched_events)
            offset = (page - 1) * page_size
            page_events = matched_events[offset:offset + page_size]
            total_pages = (total + page_size - 1) // page_size
            
            return {
                'success': True, 'events': page_events,
                'pagination': {'page': page, 'page_size': page_size, 'total_count': total, 'total_pages': total_pages, 'has_next': page < total_pages, 'has_prev': page > 1},
                'from_cache': True
            }
        except Exception as e:
            print(f"[缓存] 搜索失败: {e}")
            return {'success': False, 'error': str(e)}

    def advanced_search_in_cache(self, evtx_file_path: str, filters: Dict[str, str], page: int = 1, page_size: int = 100,
                                 sort_field: str = None, sort_direction: str = 'asc') -> dict:
        """高级搜索（使用精确匹配，避免误匹配）"""
        cache_path = self.get_cache_path(evtx_file_path)
        
        try:
            conn = sqlite3.connect(cache_path)
            cursor = conn.cursor()
            
            where_clauses = []
            params = []
            
            for field, value in filters.items():
                if field in ['EventID', 'Level', 'Provider', 'Computer', 'Channel']:
                    # 核心字段：直接精确匹配
                    where_clauses.append(f"{field} = ?")
                    params.append(value)
                else:
                    # 🔥 其他字段：使用JSON精确提取匹配，避免误匹配
                    # 例如：LogonType=10 不会匹配 LogonType=100
                    where_clauses.append(f"json_extract(event_json, '$.{field}') = ?")
                    params.append(value)
            
            where_sql = ' AND '.join(where_clauses) if where_clauses else '1=1'
            
            cursor.execute(f"SELECT COUNT(*) FROM events WHERE {where_sql}", params)
            total = cursor.fetchone()[0]
            
            # 🔥 修复：添加排序支持
            order_by = "RecordID"
            allowed_fields = ['RecordID', 'EventID', 'Level', 'TimeCreated', 'Provider', 'Computer', 'Channel']
            
            if sort_field and sort_field in allowed_fields:
                order_by = sort_field
            
            direction = "DESC" if sort_direction.lower() == 'desc' else "ASC"
            offset = (page - 1) * page_size
            
            cursor.execute(f'''
                SELECT event_json FROM events WHERE {where_sql} ORDER BY {order_by} {direction} LIMIT ? OFFSET ?
            ''', params + [page_size, offset])
            
            events = []
            for row in cursor.fetchall():
                try:
                    event = json.loads(row[0])
                    events.append(event)
                except:
                    pass
            
            conn.close()
            
            total_pages = (total + page_size - 1) // page_size
            
            return {
                'success': True, 'events': events,
                'pagination': {'page': page, 'page_size': page_size, 'total_count': total, 'total_pages': total_pages, 'has_next': page < total_pages, 'has_prev': page > 1},
                'from_cache': True
            }
        except Exception as e:
            print(f"[缓存] 高级搜索失败: {e}")
            return {'success': False, 'error': str(e)}
    
    def clear_cache(self, file_path: str = None) -> None:
        """清空缓存"""
        if file_path:
            cache_path = self.get_cache_path(file_path)
            if os.path.exists(cache_path):
                os.remove(cache_path)
                print(f"[缓存] 已删除: {os.path.basename(cache_path)}")
        else:
            for f in os.listdir(self.cache_dir):
                if f.endswith('.cache.db'):
                    os.remove(os.path.join(self.cache_dir, f))
            print("[缓存] 已清空所有缓存")
    
    def get_cache_info(self) -> dict:
        """获取缓存信息"""
        if not os.path.exists(self.cache_dir):
            return {'success': True, 'total_size': 0, 'total_size_mb': 0, 'file_count': 0, 'files': []}
        
        files = []
        total_size = 0
        
        for f in os.listdir(self.cache_dir):
            if f.endswith('.cache.db'):
                path = os.path.join(self.cache_dir, f)
                size = os.path.getsize(path)
                total_size += size
                files.append({'name': f, 'size': size, 'size_mb': round(size / 1024 / 1024, 2), 'path': path})
        
        files.sort(key=lambda x: x['size'], reverse=True)
        
        return {'success': True, 'total_size': total_size, 'total_size_mb': round(total_size / 1024 / 1024, 2), 'file_count': len(files), 'files': files}
    
    def get_scan_progress(self, file_path: str) -> dict:
        """获取扫描进度"""
        return self.scan_progress_map.get(file_path, {
            'status': 'idle', 'current': 0, 'total': 0, 'message': ''
        })
    
    def scan_with_rules(self, file_path: str, rules: list, scan_limit: int = None) -> dict:
        """使用规则扫描事件"""
        cache_path = self.get_cache_path(file_path)
        
        if not os.path.exists(cache_path):
            return {'success': False, 'error': '缓存不存在，请先加载日志'}
        
        try:
            conn = sqlite3.connect(cache_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM events")
            total = cursor.fetchone()[0]
            
            file_name = os.path.basename(file_path)
            scan_count = scan_limit if scan_limit and scan_limit > 0 else total
            self.scan_progress_map[file_path] = {
                'status': 'scanning', 'current': 0, 'total': scan_count,
                'message': f'正在扫描 {file_name}'
            }
            
            BATCH_SIZE = 1000
            matched_events = []
            processed = 0
            start_time = time.time()
            
            if scan_limit and scan_limit > 0:
                cursor.execute('SELECT event_json FROM events ORDER BY RecordID LIMIT ?', [scan_limit])
            else:
                cursor.execute('SELECT event_json FROM events ORDER BY RecordID')
            
            while True:
                rows = cursor.fetchmany(BATCH_SIZE)
                if not rows:
                    break
                
                for row in rows:
                    try:
                        event = json.loads(row[0])
                        if self._match_any_rule(event, rules):
                            matched_events.append(event)
                    except:
                        pass
                    processed += 1
            
            conn.close()
            
            elapsed = time.time() - start_time
            self.scan_progress_map[file_path] = {
                'status': 'done', 'current': processed, 'total': scan_count,
                'message': f'扫描完成！扫描 {processed:,} 条，匹配 {len(matched_events):,} 条'
            }
            
            return {
                'success': True, 'events': matched_events, 'total': total,
                'scanned': processed, 'matched': len(matched_events), 'from_cache': True
            }
        
        except Exception as e:
            self.scan_progress_map[file_path] = {'status': 'error', 'current': 0, 'total': 0, 'message': f'扫描失败: {str(e)}'}
            return {'success': False, 'error': str(e)}
    
    def _match_any_rule(self, event: dict, rules: list) -> bool:
        """检查事件是否匹配任何规则"""
        for rule in rules:
            if not rule.get('enabled', True):
                continue
            
            conditions = rule.get('conditions', [])
            if not conditions:
                continue
            
            all_match = True
            for condition in conditions:
                field = condition.get('field')
                op = condition.get('op')
                value = condition.get('value')
                
                if not field or not op:
                    continue
                
                event_value = event.get(field)
                
                # 处理None值
                if event_value is None:
                    event_value = ''
                
                event_value_str = str(event_value).strip()
                value_str = str(value).strip() if value else ''
                
                if op == 'equals':
                    # 精确匹配（忽略大小写）
                    if event_value_str.lower() != value_str.lower():
                        all_match = False
                        break
                elif op == 'contains':
                    # 包含匹配（忽略大小写）
                    if not value_str or value_str.lower() not in event_value_str.lower():
                        all_match = False
                        break
                elif op == 'startswith':
                    if not event_value_str.lower().startswith(value_str.lower()):
                        all_match = False
                        break
                elif op == 'endswith':
                    if not event_value_str.lower().endswith(value_str.lower()):
                        all_match = False
                        break
                elif op == 'regex':
                    import re
                    try:
                        if not re.search(value_str, event_value_str, re.IGNORECASE):
                            all_match = False
                            break
                    except:
                        all_match = False
                        break
                elif op == 'not_equals':
                    if event_value_str.lower() == value_str.lower():
                        all_match = False
                        break
                elif op == 'not_contains':
                    if value_str.lower() in event_value_str.lower():
                        all_match = False
                        break
            
            if all_match and conditions:
                return True
        
        return False
