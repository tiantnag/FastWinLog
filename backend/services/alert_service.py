#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Alert rules service"""

import os
from typing import Dict, Any, List, Optional
from ..core.alert_store import AlertStore
from ..core.alert_baselines import choose_baseline_by_filename, choose_baseline_by_channel
from ..repositories.sqlite_repository import SqliteRepository
from ..core.evtx_parser import EvtxParser


class AlertService:
    """告警规则服务"""
    
    def __init__(self, alert_store: AlertStore, sqlite_repo: SqliteRepository, logs_dir: str):
        self.alert_store = alert_store
        self.sqlite_repo = sqlite_repo
        self.logs_dir = logs_dir
        self.evtx_parser = EvtxParser()
    
    def get_alert_rules(self, file_path: str) -> dict:
        """获取告警规则"""
        try:
            return self.alert_store.get_rules(file_path)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def save_alert_rules(self, file_path: str, rules: List[dict]) -> dict:
        """保存告警规则"""
        try:
            return self.alert_store.save_rules(file_path, rules)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def clear_alert_rules(self, file_path: str) -> dict:
        """清空告警规则"""
        try:
            return self.alert_store.clear_rules(file_path)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_last_alert_scan(self, file_path: str) -> dict:
        """获取最近一次扫描摘要"""
        try:
            return self.alert_store.get_last_scan(file_path)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def save_last_alert_scan(self, file_path: str, summary: dict) -> dict:
        """保存扫描摘要"""
        try:
            return self.alert_store.save_last_scan(file_path, summary)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def init_builtin_alert_rules(self, overwrite: bool = False, file_path: str = None) -> dict:
        """初始化内置告警规则 - 优先从数据库读取Channel"""
        try:
            updated = 0
            skipped = 0
            
            if file_path:
                if not os.path.exists(file_path):
                    return {"success": False, "error": f"文件不存在: {file_path}"}
                
                baseline = None
                channel = None
                
                # 🔥 优先方案：从缓存数据库读取Channel字段
                try:
                    cache_path = self.sqlite_repo.get_cache_path(file_path)
                    if os.path.exists(cache_path):
                        import sqlite3
                        conn = sqlite3.connect(cache_path)
                        cursor = conn.cursor()
                        cursor.execute("SELECT Channel FROM events LIMIT 1")
                        row = cursor.fetchone()
                        conn.close()
                        
                        if row and row[0]:
                            channel = row[0]
                            baseline = choose_baseline_by_channel(channel)
                            print(f"[告警规则] ✓ 从数据库读取Channel: {channel} -> {len(baseline) if baseline else 0} 条规则")
                except Exception as e:
                    print(f"[告警规则] 从数据库读取Channel失败: {e}")
                
                # 备选方案1：解析EVTX文件获取Channel
                if not baseline:
                    try:
                        channel, log_type, is_supported = self.evtx_parser.detect_log_type(file_path)
                        if channel:
                            baseline = choose_baseline_by_channel(channel)
                            print(f"[告警规则] ✓ 从EVTX解析Channel: {channel} -> {len(baseline) if baseline else 0} 条规则")
                    except Exception as e:
                        print(f"[告警规则] EVTX解析失败: {e}")
                
                # 备选方案2：文件名匹配
                if not baseline:
                    filename = os.path.basename(file_path)
                    baseline = choose_baseline_by_filename(filename)
                    print(f"[告警规则] ✓ 通过文件名匹配: {filename} -> {len(baseline) if baseline else 0} 条规则")
                
                if not baseline:
                    return {"success": True, "updated": 0, "skipped": 0, "message": f"未找到匹配的规则集"}
                
                existing = self.alert_store.get_rules(file_path)
                has_rules = bool(existing.get("rules"))
                
                if has_rules and not overwrite:
                    return {"success": True, "updated": 0, "skipped": 1, "message": "规则已存在"}
                
                self.alert_store.save_rules(file_path, baseline)
                return {"success": True, "updated": 1, "skipped": 0, "message": f"已初始化 {len(baseline)} 条规则"}
            
            # 初始化logs目录所有文件
            if os.path.exists(self.logs_dir):
                for filename in os.listdir(self.logs_dir):
                    if not filename.endswith('.evtx'):
                        continue
                    fp = os.path.join(self.logs_dir, filename)
                    
                    # 优先使用Channel识别
                    baseline = None
                    try:
                        channel, log_type, is_supported = self.evtx_parser.detect_log_type(fp)
                        if channel:
                            baseline = choose_baseline_by_channel(channel)
                    except:
                        pass
                    
                    # 回退到文件名匹配
                    if not baseline:
                        baseline = choose_baseline_by_filename(filename)
                    
                    if not baseline:
                        continue
                    
                    existing = self.alert_store.get_rules(fp)
                    has_rules = bool(existing.get("rules"))
                    if has_rules and not overwrite:
                        skipped += 1
                        continue
                    self.alert_store.save_rules(fp, baseline)
                    updated += 1
            
            return {"success": True, "updated": updated, "skipped": skipped}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def scan_alerts_from_db(self, file_path: str, scan_limit: int = None, rules: List[dict] = None) -> dict:
        """
        从数据库扫描告警（高性能 + 进度支持 + 智能过滤）
        
        优化：只返回匹配告警规则的事件，避免数据量过大导致溢出
        
        Args:
            file_path: 日志文件路径
            scan_limit: 扫描限制数量，None表示全部，0表示全部
            rules: 告警规则列表（可选），如果提供则只返回匹配的事件
        
        Returns:
            {'success': True, 'events': [...], 'total': int, 'scanned': int, 'matched': int}
        """
        try:
            file_name = os.path.basename(file_path)
            
            if rules and len(rules) > 0:
                print(f"[智能扫描] 文件: {file_name} | 规则数: {len(rules)} | 限制: {scan_limit}")
                result = self.sqlite_repo.scan_with_rules(file_path, rules, scan_limit)
            else:
                # 如果没有提供规则，尝试从存储中获取
                stored_rules = self.alert_store.get_rules(file_path)
                if stored_rules.get('rules'):
                    print(f"[智能扫描] 使用存储的规则 | 文件: {file_name} | 规则数: {len(stored_rules['rules'])}")
                    result = self.sqlite_repo.scan_with_rules(file_path, stored_rules['rules'], scan_limit)
                else:
                    print(f"[警告] 未提供规则，返回空结果 | 文件: {file_name}")
                    return {
                        'success': True,
                        'events': [],
                        'total': 0,
                        'scanned': 0,
                        'matched': 0,
                        'message': '未配置告警规则'
                    }
            
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_scan_progress(self, file_path: str) -> dict:
        """
        获取扫描进度（供前端轮询）
        
        Returns:
            {
                'success': True,
                'status': 'idle'|'scanning'|'done',
                'current': int,
                'total': int,
                'message': str
            }
        """
        progress = self.sqlite_repo.get_scan_progress(file_path)
        return {'success': True, **progress}
