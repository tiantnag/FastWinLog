#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""EVTX file parsing repository"""

import os
import time
from typing import Dict, List, Optional, Callable, Tuple
from ..core.evtx_parser import EvtxParser
from ..utils.progress_tracker import ProgressTracker


class EvtxRepository:
    """EVTX文件解析仓储"""
    
    def __init__(self, base_dir: str, progress_tracker: ProgressTracker):
        self.base_dir = base_dir
        self.logs_dir = os.path.join(base_dir, 'logs')
        self.parser = EvtxParser()
        self.progress = progress_tracker
    
    def parse_file(self, file_path: str) -> Tuple[List[dict], Optional[dict]]:
        """
        解析EVTX文件
        
        Returns:
            Tuple[events, stats]
        """
        file_name = os.path.basename(file_path)
        
        # 权限检查
        try:
            with open(file_path, 'rb') as test_file:
                test_file.read(1)
        except PermissionError:
            error_msg = self._build_permission_error(file_path)
            self.progress.error(file_path, error_msg, 'permission', {
                'type': 'copy_to_logs',
                'source': file_path,
                'target': os.path.join(self.logs_dir, file_name),
                'logs_dir': self.logs_dir
            })
            raise PermissionError(error_msg)
        except FileNotFoundError:
            error_msg = f'文件不存在：{file_name}'
            self.progress.error(file_path, error_msg, 'not_found')
            raise FileNotFoundError(error_msg)
        
        # 统计总数
        self.progress.update_counting(file_path)
        print(f"[第一步] 使用 pyevtx 快速统计总数...")
        count_start = time.time()
        
        total_records = self.parser.count_records(file_path)
        
        count_elapsed = time.time() - count_start
        print(f"[第一步完成] 总数: {total_records:,} 条，耗时: {count_elapsed:.1f}秒")
        
        # 解析文件
        print(f"[第二步] 使用 pyevtx 高速解析...")
        start_time = time.time()
        events = []
        
        import pyevtx
        evtx_file = pyevtx.file()
        evtx_file.open(file_path)
        
        try:
            processed = 0
            last_update = start_time
            last_count = 0
            UPDATE_INTERVAL = 0.2
            BATCH_SIZE = 100
            
            for i in range(total_records):
                try:
                    record = evtx_file.get_record(i)
                    event_data = self.parser.parse_record(record)
                    xml_string = record.get_xml_string()
                    
                    event = {
                        'RecordID': event_data.get('RecordID', str(i)),
                        'xml_content': xml_string,
                        **event_data
                    }
                    
                    events.append(event)
                    processed += 1
                    
                    # 更新进度
                    should_update = (processed % BATCH_SIZE == 0) or (time.time() - last_update > UPDATE_INTERVAL)
                    
                    if should_update:
                        elapsed = time.time() - start_time
                        speed = processed / elapsed if elapsed > 0 else 0
                        eta_seconds = (total_records - processed) / speed if speed > 0 else 0
                        
                        self.progress.update_loading(file_path, processed, total_records, speed, eta_seconds)
                        
                        if processed - last_count >= 5000:
                            print(f"[pyevtx解析] {processed:,}/{total_records:,} | {speed:.0f}条/秒")
                            last_count = processed
                        
                        last_update = time.time()
                except Exception as e:
                    print(f"[解析错误] 记录 {i}: {e}")
                    continue
        finally:
            evtx_file.close()
        
        elapsed = time.time() - start_time
        speed = len(events) / elapsed if elapsed > 0 else 0
        
        stats = {
            'total_events': len(events),
            'load_time': elapsed,
            'load_speed': speed,
            'file_path': file_path,
            'loaded_at': time.time(),
            'parser': 'pyevtx'
        }
        
        self.progress.complete(file_path, len(events), speed)
        print(f"[pyevtx加载完成] 共{len(events):,}条 | 耗时{elapsed:.1f}秒 | {speed:.0f}条/秒")
        
        return events, stats
    
    def count_records(self, file_path: str) -> int:
        """统计记录数"""
        return self.parser.count_records(file_path)
    
    def get_file_info(self, file_path: str) -> dict:
        """获取文件信息"""
        if not os.path.exists(file_path):
            return {'error': '文件不存在'}
        
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        
        try:
            total_records = self.parser.count_records(file_path)
        except:
            total_records = 0
        
        return {
            'file_path': file_path,
            'file_name': file_name,
            'file_size': file_size,
            'file_size_mb': round(file_size / (1024 * 1024), 2),
            'total_records': total_records
        }
    
    def _build_permission_error(self, file_path: str) -> str:
        """构建权限错误消息"""
        file_name = os.path.basename(file_path)
        system_path = r'C:\Windows\System32\winevt\Logs'
        
        return f'''无法访问系统日志文件：{file_name}

📋 解决方法：
1. 以管理员身份打开【命令提示符】或【PowerShell】
2. 复制日志到程序目录：
   
   copy "{file_path}" "{self.logs_dir}\\{file_name}"
   
3. 刷新页面重新加载

💡 提示：将日志复制到 logs 目录后，程序会优先使用本地日志文件。

默认系统日志位置：{system_path}'''
