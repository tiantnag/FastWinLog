#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FastWinLog - Alert Rules Storage
Version: 1.0.0
Repository: https://github.com/vam876/FastWinLog
"""

import os
import sqlite3
import time
import json


class AlertStore:
    """告警规则存储"""
    
    def __init__(self, base_dir: str):
        os.makedirs(base_dir, exist_ok=True)
        self.db_path = os.path.join(base_dir, "alerts.db")
        self._init_db()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        return conn

    def _init_db(self):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS alert_rules (
              file_path TEXT PRIMARY KEY,
              rules_json TEXT NOT NULL,
              updated_at REAL NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS alert_last_scan (
              file_path TEXT PRIMARY KEY,
              summary_json TEXT NOT NULL,
              scanned_at REAL NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def get_rules(self, file_path: str):
        """获取告警规则"""
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT rules_json, updated_at FROM alert_rules WHERE file_path = ?", (file_path,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return {"success": True, "rules": [], "updated_at": None}
        try:
            rules = json.loads(row[0])
        except Exception:
            rules = []
        return {"success": True, "rules": rules, "updated_at": row[1]}

    def save_rules(self, file_path: str, rules):
        """保存告警规则"""
        ts = time.time()
        payload = json.dumps(rules, ensure_ascii=False)
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO alert_rules(file_path, rules_json, updated_at)
            VALUES(?, ?, ?)
            ON CONFLICT(file_path) DO UPDATE SET
              rules_json=excluded.rules_json,
              updated_at=excluded.updated_at
        """, (file_path, payload, ts))
        conn.commit()
        conn.close()
        return {"success": True, "updated_at": ts}

    def clear_rules(self, file_path: str):
        """清空告警规则"""
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM alert_rules WHERE file_path = ?", (file_path,))
        conn.commit()
        conn.close()
        return {"success": True}

    def save_last_scan(self, file_path: str, summary):
        """保存最近一次扫描摘要"""
        ts = time.time()
        payload = json.dumps(summary, ensure_ascii=False)
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO alert_last_scan(file_path, summary_json, scanned_at)
            VALUES(?, ?, ?)
            ON CONFLICT(file_path) DO UPDATE SET
              summary_json=excluded.summary_json,
              scanned_at=excluded.scanned_at
        """, (file_path, payload, ts))
        conn.commit()
        conn.close()
        return {"success": True, "scanned_at": ts}

    def get_last_scan(self, file_path: str):
        """获取最近一次扫描摘要"""
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT summary_json, scanned_at FROM alert_last_scan WHERE file_path = ?", (file_path,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return {"success": True, "summary": None, "scanned_at": None}
        try:
            summary = json.loads(row[0])
        except Exception:
            summary = None
        return {"success": True, "summary": summary, "scanned_at": row[1]}
