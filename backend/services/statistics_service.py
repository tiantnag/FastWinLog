#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Statistics service"""

import os
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from collections import Counter
from ..core.windows_events_database import get_event_info
from ..repositories.sqlite_repository import SqliteRepository


class StatisticsService:
    """统计服务"""
    
    def __init__(self, sqlite_repo: SqliteRepository):
        self.sqlite_repo = sqlite_repo
    
    def _get_db_path(self, file_path: str) -> str:
        """获取数据库路径"""
        return self.sqlite_repo.get_cache_path(file_path)
    
    def get_security_login_stats(self, file_path: str, time_range_hours: int = None) -> dict:
        """获取Security日志登录统计"""
        try:
            db_path = self._get_db_path(file_path)
            if not os.path.exists(db_path):
                return {'success': False, 'error': '请先加载日志文件'}
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            time_filter = ""
            if time_range_hours:
                cutoff_time = (datetime.now() - timedelta(hours=time_range_hours)).isoformat()
                time_filter = f"AND json_extract(event_json, '$.TimeCreated_SystemTime') >= '{cutoff_time}'"
            
            result = {}
            
            try:
                # 1. 失败登录Top IP
                cursor.execute(f"""
                    SELECT json_extract(event_json, '$.EventData_IpAddress') as ip, COUNT(*) as count
                    FROM events WHERE EventID = '4625' AND ip IS NOT NULL AND ip != '-' AND ip != '' {time_filter}
                    GROUP BY ip ORDER BY count DESC LIMIT 20
                """)
                result['failed_login_top_ips'] = [{"ip": row[0], "count": row[1]} for row in cursor.fetchall()]
                
                # 2. 成功登录Top IP
                cursor.execute(f"""
                    SELECT json_extract(event_json, '$.EventData_IpAddress') as ip, COUNT(*) as count
                    FROM events WHERE EventID = '4624' AND json_extract(event_json, '$.EventData_LogonType') IN ('2', '3', '10')
                    AND ip IS NOT NULL AND ip != '-' AND ip != '' {time_filter}
                    GROUP BY ip ORDER BY count DESC LIMIT 20
                """)
                result['success_login_top_ips'] = [{"ip": row[0], "count": row[1]} for row in cursor.fetchall()]
                
                # 3. 失败登录Top用户
                cursor.execute(f"""
                    SELECT json_extract(event_json, '$.EventData_TargetUserName') as user, COUNT(*) as count
                    FROM events WHERE EventID = '4625' AND user IS NOT NULL AND user != '-' AND user != '' {time_filter}
                    GROUP BY user ORDER BY count DESC LIMIT 20
                """)
                result['failed_login_top_users'] = [{"user": row[0], "count": row[1]} for row in cursor.fetchall()]
                
                # 4. 登录类型分布
                logon_type_names = {
                    '2': '交互式登录', '3': '网络登录', '4': '批处理', '5': '服务',
                    '7': '解锁', '8': '网络明文', '9': 'NewCredentials', '10': '远程交互式', '11': 'CachedInteractive'
                }
                cursor.execute(f"""
                    SELECT json_extract(event_json, '$.EventData_LogonType') as logon_type, COUNT(*) as count
                    FROM events WHERE EventID IN ('4624', '4625') AND logon_type IS NOT NULL {time_filter}
                    GROUP BY logon_type ORDER BY count DESC
                """)
                result['logon_type_distribution'] = [
                    {"type": row[0], "name": logon_type_names.get(row[0], f"类型{row[0]}"), "count": row[1]}
                    for row in cursor.fetchall()
                ]
                
                # 5. 登录时间趋势
                cursor.execute(f"""
                    SELECT strftime('%Y-%m-%d %H:00', TimeCreated) as hour,
                           SUM(CASE WHEN EventID = '4625' THEN 1 ELSE 0 END) as failed,
                           SUM(CASE WHEN EventID = '4624' THEN 1 ELSE 0 END) as success
                    FROM events WHERE EventID IN ('4624', '4625') {time_filter}
                    GROUP BY hour ORDER BY hour DESC LIMIT 168
                """)
                result['login_timeline'] = [{"hour": row[0], "failed": row[1], "success": row[2]} for row in cursor.fetchall()]
                result['login_timeline'].reverse()
                
                # 6. 总计
                cursor.execute(f"SELECT COUNT(*) FROM events WHERE EventID = '4625' {time_filter}")
                result['total_failed'] = cursor.fetchone()[0]
                cursor.execute(f"SELECT COUNT(*) FROM events WHERE EventID = '4624' {time_filter}")
                result['total_success'] = cursor.fetchone()[0]
                
                # 7. 最近成功登录记录
                cursor.execute(f"""
                    SELECT json_extract(event_json, '$.TimeCreated_SystemTime') as time,
                           json_extract(event_json, '$.EventData_TargetUserName') as user,
                           json_extract(event_json, '$.EventData_IpAddress') as ip,
                           json_extract(event_json, '$.EventData_LogonType') as logon_type
                    FROM events WHERE EventID = '4624'
                      AND json_extract(event_json, '$.EventData_IpAddress') IS NOT NULL
                      AND json_extract(event_json, '$.EventData_IpAddress') != '-'
                      AND json_extract(event_json, '$.EventData_IpAddress') != '' {time_filter}
                    ORDER BY json_extract(event_json, '$.TimeCreated_SystemTime') DESC LIMIT 10
                """)
                logon_names = {'2': '交互式', '3': '网络', '10': '远程交互式'}
                result['recent_success_logins'] = [
                    {"time": row[0][:19] if row[0] else "", "user": row[1] or "未知", "ip": row[2] or "-", "logon_type": logon_names.get(row[3], row[3] or "未知")}
                    for row in cursor.fetchall()
                ]
            finally:
                conn.close()
            
            return {'success': True, 'data': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_security_account_stats(self, file_path: str, time_range_hours: int = None) -> dict:
        """获取Security日志账户统计"""
        try:
            db_path = self._get_db_path(file_path)
            if not os.path.exists(db_path):
                return {'success': False, 'error': '请先加载日志文件或点击上方的刷新按钮'}
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            time_filter = ""
            if time_range_hours:
                cutoff_time = (datetime.now() - timedelta(hours=time_range_hours)).isoformat()
                time_filter = f"AND TimeCreated >= '{cutoff_time}'"
            
            result = {}
            
            try:
                # 账户锁定
                cursor.execute(f"""
                    SELECT json_extract(event_json, '$.EventData_TargetUserName') as user, COUNT(*) as count
                    FROM events WHERE EventID = '4740' AND user IS NOT NULL {time_filter}
                    GROUP BY user ORDER BY count DESC LIMIT 20
                """)
                result['account_lockouts'] = [{"user": row[0], "count": row[1]} for row in cursor.fetchall()]
                
                # 特权分配
                cursor.execute(f"""
                    SELECT json_extract(event_json, '$.EventData_SubjectUserName') as user, COUNT(*) as count
                    FROM events WHERE EventID = '4672' AND user IS NOT NULL {time_filter}
                    GROUP BY user ORDER BY count DESC LIMIT 20
                """)
                result['privilege_assignments'] = [{"user": row[0], "count": row[1]} for row in cursor.fetchall()]
                
                # 账户创建
                cursor.execute(f"SELECT COUNT(*) FROM events WHERE EventID = '4720' {time_filter}")
                result['account_created'] = cursor.fetchone()[0]
                
                # 账户删除
                cursor.execute(f"SELECT COUNT(*) FROM events WHERE EventID = '4726' {time_filter}")
                result['account_deleted'] = cursor.fetchone()[0]
            finally:
                conn.close()
            
            return {'success': True, 'data': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_security_process_stats(self, file_path: str, time_range_hours: int = None) -> dict:
        """获取Security日志进程统计"""
        try:
            db_path = self._get_db_path(file_path)
            if not os.path.exists(db_path):
                return {'success': False, 'error': '请先加载日志文件或点击上方的刷新按钮'}
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            result = {}
            
            try:
                time_filter = ""
                if time_range_hours:
                    cutoff_time = (datetime.now() - timedelta(hours=time_range_hours)).isoformat()
                    time_filter = f"AND json_extract(event_json, '$.TimeCreated_SystemTime') >= '{cutoff_time}'"
                
                cursor.execute(f"""
                    SELECT COALESCE(
                        json_extract(event_json, '$.EventData_ProcessName'),
                        json_extract(event_json, '$.EventData_NewProcessName'),
                        json_extract(event_json, '$.ProcessName')
                    ) as process_path
                    FROM events WHERE process_path IS NOT NULL AND process_path != '' {time_filter}
                """)
                
                process_counter = Counter()
                for row in cursor.fetchall():
                    if row[0]:
                        process_counter[row[0]] += 1
                
                result['top_processes'] = [{'process': p, 'count': c} for p, c in process_counter.most_common(10)]
            finally:
                conn.close()
            
            return {'success': True, 'data': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_system_stats(self, file_path: str, time_range_hours: int = None) -> dict:
        """获取System日志统计"""
        try:
            db_path = self._get_db_path(file_path)
            if not os.path.exists(db_path):
                return {'success': False, 'error': '请先加载日志文件或点击上方的刷新按钮'}
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            time_filter = ""
            if time_range_hours:
                cutoff_time = (datetime.now() - timedelta(hours=time_range_hours)).isoformat()
                time_filter = f"AND TimeCreated >= '{cutoff_time}'"
            
            result = {}
            
            try:
                # 级别分布
                cursor.execute(f"SELECT Level, COUNT(*) as count FROM events WHERE Level IS NOT NULL {time_filter} GROUP BY Level ORDER BY count DESC")
                result['level_distribution'] = [{"level": row[0], "count": row[1]} for row in cursor.fetchall()]
                
                # Top错误事件
                cursor.execute(f"SELECT EventID, COUNT(*) as count FROM events WHERE Level IN ('1', '2') {time_filter} GROUP BY EventID ORDER BY count DESC LIMIT 20")
                result['top_errors'] = [{"event_id": row[0], "name": get_event_info(row[0])['name'], "count": row[1]} for row in cursor.fetchall()]
                
                # 时间趋势
                cursor.execute(f"""
                    SELECT strftime('%Y-%m-%d %H:00', TimeCreated) as hour,
                           SUM(CASE WHEN Level IN ('1', '2') THEN 1 ELSE 0 END) as error,
                           SUM(CASE WHEN Level = '3' THEN 1 ELSE 0 END) as warning,
                           SUM(CASE WHEN Level = '4' THEN 1 ELSE 0 END) as info
                    FROM events WHERE Level IS NOT NULL {time_filter}
                    GROUP BY hour ORDER BY hour DESC LIMIT 168
                """)
                result['event_timeline'] = [{"hour": row[0], "error": row[1], "warning": row[2], "info": row[3]} for row in cursor.fetchall()]
                result['event_timeline'].reverse()
                
                # 开机关机事件
                cursor.execute(f"""
                    SELECT EventID, json_extract(event_json, '$.TimeCreated_SystemTime') as time,
                           json_extract(event_json, '$.EventData_param7') as user
                    FROM events WHERE EventID IN ('6005', '6006', '1074', '6008', '41') {time_filter}
                    ORDER BY json_extract(event_json, '$.TimeCreated_SystemTime') DESC LIMIT 20
                """)
                result['power_events'] = [
                    {"event_id": row[0], "time": row[1][:19] if row[1] else "",
                     "type": "开机" if row[0] == '6005' else "关机" if row[0] == '6006' else "重启/关机" if row[0] == '1074' else "意外关机" if row[0] == '6008' else "异常重启",
                     "user": row[2] or "系统"}
                    for row in cursor.fetchall()
                ]
                
                # 启动次数
                cursor.execute(f"SELECT COUNT(*) FROM events WHERE EventID = '6005' {time_filter}")
                result['boot_count'] = cursor.fetchone()[0]
                
                # 异常关机次数
                cursor.execute(f"SELECT COUNT(*) FROM events WHERE EventID IN ('6008', '41') {time_filter}")
                result['abnormal_shutdown_count'] = cursor.fetchone()[0]
            finally:
                conn.close()
            
            return {'success': True, 'data': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_application_stats(self, file_path: str, time_range_hours: int = None) -> dict:
        """获取Application日志统计"""
        try:
            db_path = self._get_db_path(file_path)
            if not os.path.exists(db_path):
                return {'success': False, 'error': '请先加载日志文件或点击上方的刷新按钮'}
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            time_filter = ""
            if time_range_hours:
                cutoff_time = (datetime.now() - timedelta(hours=time_range_hours)).isoformat()
                time_filter = f"AND TimeCreated >= '{cutoff_time}'"
            
            result = {}
            
            try:
                # Top错误来源
                cursor.execute(f"""
                    SELECT json_extract(event_json, '$.Provider_Name') as source, COUNT(*) as count
                    FROM events WHERE Level IN ('1', '2', '错误', '严重') AND source IS NOT NULL AND source != '' {time_filter}
                    GROUP BY source ORDER BY count DESC LIMIT 20
                """)
                result['top_error_sources'] = [{"source": row[0], "count": row[1]} for row in cursor.fetchall()]
                
                # Top警告来源
                cursor.execute(f"""
                    SELECT json_extract(event_json, '$.Provider_Name') as source, COUNT(*) as count
                    FROM events WHERE Level IN ('3', '警告') AND source IS NOT NULL AND source != '' {time_filter}
                    GROUP BY source ORDER BY count DESC LIMIT 20
                """)
                result['top_warning_sources'] = [{"source": row[0], "count": row[1]} for row in cursor.fetchall()]
                
                # 级别分布
                cursor.execute(f"SELECT Level, COUNT(*) as count FROM events WHERE Level IS NOT NULL {time_filter} GROUP BY Level ORDER BY count DESC")
                result['level_distribution'] = [{"level": row[0], "count": row[1]} for row in cursor.fetchall()]
                
                # 时间趋势
                cursor.execute(f"""
                    SELECT strftime('%Y-%m-%d %H:00', TimeCreated) as hour,
                           SUM(CASE WHEN Level IN ('1', '2') THEN 1 ELSE 0 END) as error,
                           SUM(CASE WHEN Level = '3' THEN 1 ELSE 0 END) as warning
                    FROM events WHERE Level IS NOT NULL {time_filter}
                    GROUP BY hour ORDER BY hour DESC LIMIT 168
                """)
                result['event_timeline'] = [{"hour": row[0], "error": row[1], "warning": row[2]} for row in cursor.fetchall()]
                result['event_timeline'].reverse()
                
                # 应用崩溃事件
                cursor.execute(f"""
                    SELECT json_extract(event_json, '$.Provider_Name') as provider, EventID,
                           json_extract(event_json, '$.TimeCreated_SystemTime') as time,
                           json_extract(event_json, '$.EventData_AppName') as app_name
                    FROM events WHERE EventID IN ('1000', '1001', '1002') {time_filter}
                    ORDER BY json_extract(event_json, '$.TimeCreated_SystemTime') DESC LIMIT 10
                """)
                result['app_crashes'] = [
                    {"provider": row[0] or "未知", "event_id": row[1], "time": row[2][:19] if row[2] else "", "app_name": row[3] or row[0] or "未知应用"}
                    for row in cursor.fetchall()
                ]
                
                # Top应用统计
                cursor.execute(f"""
                    SELECT json_extract(event_json, '$.Provider_Name') as process, COUNT(*) as count
                    FROM events WHERE process IS NOT NULL AND process != '' {time_filter}
                    GROUP BY process ORDER BY count DESC LIMIT 10
                """)
                result['top_crash_apps'] = [{"process": row[0], "count": row[1]} for row in cursor.fetchall()]
                
                # 挂起事件数
                cursor.execute(f"SELECT COUNT(*) FROM events WHERE EventID = '1002' {time_filter}")
                result['app_hang_count'] = cursor.fetchone()[0]
            finally:
                conn.close()
            
            return {'success': True, 'data': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_overview_stats(self, file_path: str, time_range_hours: int = None) -> dict:
        """获取概览统计"""
        try:
            db_path = self._get_db_path(file_path)
            if not os.path.exists(db_path):
                return {'success': False, 'error': '请先加载日志文件或点击上方的刷新按钮'}
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            time_filter = ""
            if time_range_hours:
                cutoff_time = (datetime.now() - timedelta(hours=time_range_hours)).isoformat()
                time_filter = f"WHERE TimeCreated >= '{cutoff_time}'"
            
            result = {}
            
            try:
                # 24小时分布
                cursor.execute(f"""
                    SELECT CAST(strftime('%H', TimeCreated) AS INTEGER) as hour, COUNT(*) as count
                    FROM events {time_filter} GROUP BY hour ORDER BY hour
                """)
                hourly_data = {row[0]: row[1] for row in cursor.fetchall()}
                result['hourly_distribution'] = [{"hour": h, "count": hourly_data.get(h, 0)} for h in range(24)]
                
                # 每日趋势
                cursor.execute(f"""
                    SELECT strftime('%Y-%m-%d', TimeCreated) as date, COUNT(*) as count
                    FROM events WHERE TimeCreated >= date('now', '-30 days')
                    GROUP BY date ORDER BY date DESC LIMIT 30
                """)
                result['daily_trend'] = [{"date": row[0], "count": row[1]} for row in cursor.fetchall()]
                result['daily_trend'].reverse()
            finally:
                conn.close()
            
            return {'success': True, 'data': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}
