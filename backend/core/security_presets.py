#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FastWinLog - Security Analysis Presets
Version: 1.0.0
Repository: https://github.com/vam876/FastWinLog
"""

# Security alert presets
SECURITY_PRESETS = {
    "login_failures": {
        "name": "登录失败告警",
        "description": "检测多次登录失败事件（可能的暴力破解）",
        "icon": "🔐",
        "category": "登录安全",
        "severity": "high",
        "conditions": [
            {"field": "EventID", "operator": "equals", "value": "4625"},
            {"field": "LogonType", "operator": "in", "value": "2,3,10"}
        ],
        "logic": "AND"
    },
    "privilege_escalation": {
        "name": "权限提升检测",
        "description": "检测特权分配事件",
        "icon": "🔺",
        "category": "权限管理",
        "severity": "critical",
        "conditions": [
            {"field": "EventID", "operator": "equals", "value": "4672"}
        ],
        "logic": "AND"
    },
    "account_lockout": {
        "name": "账户锁定事件",
        "description": "检测账户被锁定的事件",
        "icon": "🔒",
        "category": "登录安全",
        "severity": "medium",
        "conditions": [
            {"field": "EventID", "operator": "equals", "value": "4740"}
        ],
        "logic": "AND"
    },
    "user_account_created": {
        "name": "新账户创建",
        "description": "检测新用户账户创建事件",
        "icon": "👤",
        "category": "账户管理",
        "severity": "medium",
        "conditions": [
            {"field": "EventID", "operator": "equals", "value": "4720"}
        ],
        "logic": "AND"
    },
    "audit_log_cleared": {
        "name": "审计日志清除",
        "description": "检测审计日志被清除的事件（高度可疑）",
        "icon": "🚨",
        "category": "审计完整性",
        "severity": "critical",
        "conditions": [
            {"field": "EventID", "operator": "equals", "value": "1102"}
        ],
        "logic": "AND"
    },
    "network_login": {
        "name": "网络登录",
        "description": "检测网络登录事件",
        "icon": "🌐",
        "category": "远程访问",
        "severity": "medium",
        "conditions": [
            {"field": "EventID", "operator": "equals", "value": "4624"},
            {"field": "LogonType", "operator": "equals", "value": "10"}
        ],
        "logic": "AND"
    },
    "service_installed": {
        "name": "服务安装事件",
        "description": "检测新服务安装（可能的持久化手段）",
        "icon": "⚙️",
        "category": "持久化",
        "severity": "medium",
        "conditions": [
            {"field": "EventID", "operator": "equals", "value": "4697"}
        ],
        "logic": "AND"
    },
}

# 预设分类
PRESET_CATEGORIES = {
    "登录安全": {"icon": "🔐", "description": "登录、注销、认证相关事件", "color": "#f44336"},
    "账户管理": {"icon": "👤", "description": "用户账户创建、删除、修改", "color": "#2196f3"},
    "权限管理": {"icon": "🔺", "description": "权限提升、组成员变更", "color": "#ff9800"},
    "审计完整性": {"icon": "🚨", "description": "审计日志清除等高危事件", "color": "#e91e63"},
    "持久化": {"icon": "⚙️", "description": "服务、计划任务等持久化手段", "color": "#9c27b0"},
    "远程访问": {"icon": "🌐", "description": "网络登录等远程访问", "color": "#4caf50"},
}

# 严重程度定义
SEVERITY_LEVELS = {
    "critical": {"label": "严重", "color": "#d32f2f", "icon": "🚨"},
    "high": {"label": "高", "color": "#f57c00", "icon": "⚠️"},
    "medium": {"label": "中", "color": "#fbc02d", "icon": "⚡"},
    "low": {"label": "低", "color": "#388e3c", "icon": "ℹ️"},
    "info": {"label": "信息", "color": "#1976d2", "icon": "📌"}
}

# 操作符定义
OPERATORS = {
    "equals": {"label": "等于", "symbol": "=", "sql": "="},
    "not_equals": {"label": "不等于", "symbol": "≠", "sql": "!="},
    "contains": {"label": "包含", "symbol": "∋", "sql": "LIKE"},
    "in": {"label": "在列表中", "symbol": "∈", "sql": "IN"},
}


def get_presets_by_category():
    """按分类组织预设"""
    result = {cat: [] for cat in PRESET_CATEGORIES.keys()}
    
    for preset_id, preset in SECURITY_PRESETS.items():
        category = preset.get('category', '其他')
        if category in result:
            result[category].append({'id': preset_id, **preset})
    
    return result


def get_preset_by_id(preset_id):
    """根据ID获取预设"""
    return SECURITY_PRESETS.get(preset_id)


def get_all_presets():
    """获取所有预设列表"""
    return [{'id': k, **v} for k, v in SECURITY_PRESETS.items()]


def build_sql_condition(condition):
    """将预设条件转换为SQL WHERE子句"""
    field = condition['field']
    operator = condition['operator']
    value = condition['value']
    
    op_info = OPERATORS.get(operator, OPERATORS['equals'])
    sql_op = op_info['sql']
    
    if operator == 'contains':
        return f"{field} LIKE '%{value}%'"
    elif operator in ['in', 'not_in']:
        values = [f"'{v.strip()}'" for v in value.split(',')]
        values_str = ','.join(values)
        return f"{field} {sql_op} ({values_str})"
    else:
        return f"{field} {sql_op} '{value}'"
