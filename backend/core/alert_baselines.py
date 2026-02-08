#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FastWinLog - Built-in Alert Rules
Version: 1.0.0
Repository: https://github.com/vam876/FastWinLog
"""

import os
from datetime import datetime


def _now():
    return datetime.utcnow().isoformat() + "Z"


def _rule(
    id,
    name,
    severity="warning",
    enabled=True,
    kind="match",
    conditions=None,
    groupByField=None,
    threshold=None,
    timeWindowMinutes=None,
):
    t = _now()
    return {
        "id": id,
        "name": name,
        "enabled": enabled,
        "severity": severity,
        "kind": kind,
        "conditions": conditions or [],
        "groupByField": groupByField,
        "threshold": threshold,
        "timeWindowMinutes": timeWindowMinutes,
        "createdAt": t,
        "updatedAt": t,
    }


def security_baseline():
    """Security日志告警基线"""
    return [
        # === 日志篡改检测 ===
        _rule("sec_log_cleared_1102", "安全日志被清除（1102）", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "1102"}
        ]),
        _rule("sec_log_cleared_104", "系统日志被清除（104）", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "104"}
        ]),
        
        # === 登录/注销事件 ===
        _rule("sec_successful_logon_4624", "成功登录（4624）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "4624"}
        ]),
        _rule("sec_failed_logon_4625", "失败登录（4625）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4625"}
        ]),
        _rule("sec_logoff_4634", "注销（4634）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "4634"}
        ]),
        _rule("sec_account_locked_4625_lockout", "账户被锁定（4625 + Status 0xC0000234）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4625"},
            {"field": "EventData_Status", "op": "contains", "value": "0xC0000234"}
        ]),
        _rule("sec_account_locked_4740", "账户被锁定（4740）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4740"}
        ]),
        _rule("sec_user_initiated_logoff_4647", "用户主动注销（4647）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "4647"}
        ]),
        _rule("sec_explicit_credential_logon_4648", "显式凭据登录（4648）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4648"}
        ]),
        
        # === 权限和特权 ===
        _rule("sec_sensitive_privilege_use_4673", "敏感特权使用（4673）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4673"}
        ]),
        
        # === 审核策略 ===
        _rule("sec_audit_policy_changed_4719", "审核策略被修改（4719）", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4719"}
        ]),
        _rule("sec_system_audit_changed_4902", "系统审核策略变更（4902）", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4902"}
        ]),
        
        # === 用户账户管理 ===
        _rule("sec_user_created_4720", "创建用户（4720）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4720"}
        ]),
        _rule("sec_user_enabled_4722", "启用用户（4722）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4722"}
        ]),
        _rule("sec_password_change_4723", "密码修改（4723）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "4723"}
        ]),
        _rule("sec_password_reset_4724", "密码重置（4724）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4724"}
        ]),
        _rule("sec_user_disabled_4725", "禁用用户（4725）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4725"}
        ]),
        _rule("sec_user_deleted_4726", "删除用户（4726）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4726"}
        ]),
        _rule("sec_user_changed_4738", "用户账户变更（4738）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4738"}
        ]),
        
        # === 组管理 ===
        _rule("sec_group_created_4727", "创建安全组（4727）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4727"}
        ]),
        _rule("sec_group_added_global_4728", "添加到全局组（4728）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4728"}
        ]),
        _rule("sec_group_removed_global_4729", "从全局组移除（4729）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4729"}
        ]),
        _rule("sec_group_deleted_4730", "删除安全组（4730）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4730"}
        ]),
        _rule("sec_group_created_global_4731", "创建全局组（4731）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4731"}
        ]),
        _rule("sec_group_added_local_4732", "添加到本地组（4732）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4732"}
        ]),
        _rule("sec_group_removed_local_4733", "从本地组移除（4733）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4733"}
        ]),
        _rule("sec_group_deleted_local_4734", "删除本地组（4734）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4734"}
        ]),
        _rule("sec_group_changed_4735", "安全组更改（4735）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4735"}
        ]),
        _rule("sec_group_added_universal_4756", "添加到通用组（4756）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4756"}
        ]),
        _rule("sec_group_removed_universal_4757", "从通用组移除（4757）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4757"}
        ]),
        _rule("sec_group_enumerate_users_4798", "枚举用户组成员（4798）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4798"}
        ]),
        _rule("sec_group_enumerate_groups_4799", "枚举安全组成员（4799）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4799"}
        ]),
        
        # === 服务和进程 ===
        _rule("sec_service_installed_4697", "安装服务（4697）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4697"}
        ]),
        _rule("sec_process_created_4688", "创建进程（4688）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "4688"}
        ]),
        _rule("sec_scheduled_task_created_4698", "创建计划任务（4698）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4698"}
        ]),
        _rule("sec_scheduled_task_enabled_4700", "启用计划任务（4700）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4700"}
        ]),
        _rule("sec_scheduled_task_deleted_4699", "删除计划任务（4699）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4699"}
        ]),
        
        # === 对象访问 ===
        _rule("sec_registry_modified_4657", "注册表值修改（4657）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "4657"}
        ]),
        _rule("sec_file_deleted_4660", "文件删除（4660）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "4660"}
        ]),
        _rule("sec_file_share_accessed_5140", "文件共享访问（5140）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "5140"}
        ]),
        _rule("sec_file_share_modified_5145", "文件共享对象访问（5145）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "5145"}
        ]),
        
        # === Windows Defender ===
        _rule("sec_defender_malware_detected_1116", "检测到恶意软件（1116）", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "1116"}
        ]),
        _rule("sec_defender_action_taken_1117", "恶意软件处理（1117）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "1117"}
        ]),
        _rule("sec_defender_failed_1118", "扫描失败（1118）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "1118"}
        ]),
        _rule("sec_defender_realtime_disabled_5001", "实时保护已禁用（5001）", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "5001"}
        ]),
        
        # === Windows Firewall ===
        _rule("sec_firewall_rule_added_2004", "防火墙规则添加（2004）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "2004"}
        ]),
        _rule("sec_firewall_rule_deleted_2006", "防火墙规则删除（2006）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "2006"}
        ]),
        
        # === Kerberos ===
        _rule("sec_kerberos_tgt_requested_4768", "Kerberos TGT请求（4768）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "4768"}
        ]),
        _rule("sec_kerberos_service_ticket_4769", "Kerberos服务票据（4769）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "4769"}
        ]),
        _rule("sec_kerberos_failed_4771", "Kerberos预认证失败（4771）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4771"}
        ]),
        
        # === RDP远程桌面 ===
        _rule("sec_rdp_logon_success_4624_type10", "RDP登录成功（4624 Type 10）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4624"},
            {"field": "EventData_LogonType", "op": "equals", "value": "10"}
        ]),
        _rule("sec_rdp_reconnection_4778", "RDP会话重连（4778）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "4778"}
        ]),
        _rule("sec_rdp_disconnect_4779", "RDP会话断开（4779）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "4779"}
        ]),
        
        # === 聚合阈值：攻击检测 ===
        _rule(
            "sec_failed_logon_bruteforce_by_ip_20_in_5m",
            "疑似爆破：同一IP失败登录≥20（5分钟）",
            "critical",
            True,
            "threshold",
            [{"field": "EventID", "op": "equals", "value": "4625"}],
            groupByField="EventData_IpAddress",
            threshold=20,
            timeWindowMinutes=5,
        ),
        _rule(
            "sec_failed_logon_spray_by_user_12_in_10m",
            "疑似撞库：同一用户失败登录≥12（10分钟）",
            "warning",
            True,
            "threshold",
            [{"field": "EventID", "op": "equals", "value": "4625"}],
            groupByField="EventData_TargetUserName",
            threshold=12,
            timeWindowMinutes=10,
        ),
        _rule(
            "sec_multiple_users_created_5_in_10m",
            "批量创建用户：10分钟内创建≥5个账户",
            "critical",
            True,
            "threshold",
            [{"field": "EventID", "op": "equals", "value": "4720"}],
            groupByField="Computer",
            threshold=5,
            timeWindowMinutes=10,
        ),
        _rule(
            "sec_multiple_tasks_created_10_in_30m",
            "批量创建计划任务：30分钟内≥10个",
            "warning",
            True,
            "threshold",
            [{"field": "EventID", "op": "equals", "value": "4698"}],
            groupByField="Computer",
            threshold=10,
            timeWindowMinutes=30,
        ),
    ]


def system_baseline():
    """System日志告警基线"""
    return [
        # === 服务管理 ===
        _rule("sys_service_installed_7045", "系统服务被安装（7045）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "7045"}
        ]),
        _rule("sys_service_start_fail_7000", "服务启动失败（7000）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "7000"}
        ]),
        _rule("sys_service_stop_fail_7001", "服务停止失败（7001）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "7001"}
        ]),
        _rule("sys_service_crash_7034", "服务意外终止（7034）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "7034"}
        ]),
        _rule("sys_service_timeout_7009", "服务启动超时（7009）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "7009"}
        ]),
        _rule("sys_service_hung_7011", "服务挂起（7011）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "7011"}
        ]),
        _rule("sys_service_control_fail_7023", "服务控制失败（7023）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "7023"}
        ]),
        _rule("sys_service_restart_7031", "服务意外重启（7031）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "7031"}
        ]),
        _rule("sys_service_logon_fail_7041", "服务登录失败（7041）", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "7041"}
        ]),
        
        # === 系统启动/关机 ===
        _rule("sys_boot_start_12", "系统启动（12）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "12"}
        ]),
        _rule("sys_boot_end_13", "系统启动完成（13）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "13"}
        ]),
        _rule("sys_shutdown_clean_1074", "正常关机（1074）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "1074"}
        ]),
        _rule("sys_shutdown_unexpected_1076", "意外关机原因（1076）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "1076"}
        ]),
        _rule("sys_unexpected_shutdown_6008", "意外关机（6008）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "6008"}
        ]),
        _rule("sys_kernel_power_41", "内核电源异常（41）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "41"}
        ]),
        _rule("sys_sleep_1", "系统进入睡眠（1）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "1"}
        ]),
        
        # === 事件日志服务 ===
        _rule("sys_eventlog_shutdown_1100", "事件日志服务关闭（1100）", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "1100"}
        ]),
        _rule("sys_eventlog_started_6005", "事件日志服务启动（6005）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "6005"}
        ]),
        _rule("sys_eventlog_stopped_6006", "事件日志服务停止（6006）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "6006"}
        ]),
        _rule("sys_eventlog_cleared_104", "事件日志被清除（104）", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "104"}
        ]),
        
        # === 驱动和硬件 ===
        _rule("sys_driver_load_fail_219", "驱动加载失败（219）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "219"}
        ]),
        _rule("sys_disk_error_7", "磁盘错误（7）", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "7"}
        ]),
        _rule("sys_disk_bad_sector_9", "磁盘坏扇区（9）", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "9"}
        ]),
        _rule("sys_disk_timeout_129", "磁盘I/O超时（129）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "129"}
        ]),
        
        # === 时间同步 ===
        _rule("sys_time_sync_fail_129", "时间同步失败（129）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "129"}
        ]),
        
        # === 内存和性能 ===
        _rule("sys_memory_exhausted_2020", "内存资源耗尽（2020）", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "2020"}
        ]),
        _rule("sys_virtual_memory_low_2004", "虚拟内存不足（2004）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "2004"}
        ]),
        
        # === 用户配置文件 ===
        _rule("sys_profile_load_fail_1500", "用户配置文件加载失败（1500）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "1500"}
        ]),
        _rule("sys_profile_unload_fail_1502", "用户配置文件卸载失败（1502）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "1502"}
        ]),
        
        # === Windows Update ===
        _rule("sys_update_fail_20", "Windows更新失败（20）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "20"}
        ]),
        _rule("sys_update_install_19", "Windows更新安装（19）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "19"}
        ]),
    ]


def application_baseline():
    """Application日志告警基线"""
    return [
        # === 应用程序错误 ===
        _rule("app_crash_1000", "应用崩溃（1000 Application Error）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "1000"}
        ]),
        _rule("app_hang_1002", "应用无响应（1002 Application Hang）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "1002"}
        ]),
        
        # === .NET 运行时 ===
        _rule("app_dotnet_1026", ".NET 运行时异常（1026）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "1026"}
        ]),
        _rule("app_dotnet_unhandled_1025", ".NET 未处理异常（1025）", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "1025"}
        ]),
        _rule("app_dotnet_crash_1023", ".NET 应用崩溃（1023）", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "1023"}
        ]),
        
        # === Windows Installer (MSI) ===
        _rule("app_msi_install_success_1033", "MSI 安装成功（1033）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "1033"}
        ]),
        _rule("app_msi_install_fail_1024", "MSI 安装失败（1024）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "1024"}
        ]),
        _rule("app_msi_uninstall_1034", "MSI 卸载（1034）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "1034"}
        ]),
        _rule("app_msi_rollback_1023", "MSI 安装回滚（1023）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "1023"}
        ]),
        _rule("app_msi_product_apply_11707", "MSI 产品应用（11707）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "11707"}
        ]),
        
        # === COM/DCOM ===
        _rule("app_dcom_error_10016", "DCOM 权限错误（10016）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "10016"}
        ]),
        
        # === Windows Error Reporting (WER) ===
        _rule("app_wer_report_1001", "Windows 错误报告（1001）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "1001"}
        ]),
        
        # === 浏览器崩溃 ===
        _rule("app_browser_crash", "浏览器崩溃检测", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "1000"},
            {"field": "EventData_AppName", "op": "contains", "value": "chrome"}
        ]),
        _rule("app_ie_crash", "IE浏览器崩溃", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "1000"},
            {"field": "EventData_AppName", "op": "contains", "value": "iexplore"}
        ]),
        
        # === 聚合检测：应用稳定性 ===
        _rule(
            "app_frequent_crashes_5_in_10m",
            "频繁应用崩溃：10分钟内≥5次",
            "critical",
            True,
            "threshold",
            [{"field": "EventID", "op": "equals", "value": "1000"}],
            groupByField="Computer",
            threshold=5,
            timeWindowMinutes=10,
        ),
    ]


def powershell_baseline():
    """PowerShell日志告警基线"""
    return [
        # === 脚本执行 ===
        _rule("ps_script_block_4104", "PowerShell脚本块执行（4104）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"}
        ]),
        _rule("ps_script_block_suspicious", "可疑PowerShell脚本（含Invoke-）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "Invoke-"}
        ]),
        _rule("ps_encoded_command", "Base64编码命令执行", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "-EncodedCommand"}
        ]),
        _rule("ps_download_cradle", "下载执行（DownloadString）", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "DownloadString"}
        ]),
        _rule("ps_download_file", "下载文件（DownloadFile）", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "DownloadFile"}
        ]),
        _rule("ps_webclient", "WebClient网络请求", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "Net.WebClient"}
        ]),
        _rule("ps_invoke_expression", "动态代码执行（Invoke-Expression）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "Invoke-Expression"}
        ]),
        _rule("ps_iex", "动态代码执行（IEX）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "IEX"}
        ]),
        
        # === 引擎状态 ===
        _rule("ps_engine_start_400", "PowerShell引擎启动（400）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "400"}
        ]),
        _rule("ps_engine_stop_403", "PowerShell引擎停止（403）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "403"}
        ]),
        
        # === 远程执行 ===
        _rule("ps_remote_command_4103", "远程命令执行（4103）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4103"}
        ]),
        _rule("ps_invoke_command", "远程命令执行（Invoke-Command）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "Invoke-Command"}
        ]),
        _rule("ps_enter_pssession", "远程会话（Enter-PSSession）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "Enter-PSSession"}
        ]),
        
        # === 凭据和认证 ===
        _rule("ps_mimikatz", "疑似Mimikatz执行", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "mimikatz"}
        ]),
        _rule("ps_credential_dump", "凭据获取（Get-Credential）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "Get-Credential"}
        ]),
        _rule("ps_convertto_securestring", "密码转换（ConvertTo-SecureString）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "ConvertTo-SecureString"}
        ]),
        _rule("ps_password_plain", "明文密码（-Password）", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "-Password"}
        ]),
        
        # === 进程和系统操作 ===
        _rule("ps_start_process", "启动进程（Start-Process）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "Start-Process"}
        ]),
        _rule("ps_invoke_wmimethod", "WMI方法调用（Invoke-WmiMethod）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "Invoke-WmiMethod"}
        ]),
        _rule("ps_get_process", "进程枚举（Get-Process）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "Get-Process"}
        ]),
        _rule("ps_stop_process", "停止进程（Stop-Process）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "Stop-Process"}
        ]),
        
        # === 文件和注册表操作 ===
        _rule("ps_remove_item", "删除文件/注册表（Remove-Item）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "Remove-Item"}
        ]),
        _rule("ps_set_itemproperty", "修改注册表（Set-ItemProperty）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "Set-ItemProperty"}
        ]),
        _rule("ps_new_item", "创建文件/注册表（New-Item）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "New-Item"}
        ]),
        
        # === 绕过和隐藏 ===
        _rule("ps_bypass_execution_policy", "绕过执行策略（-ExecutionPolicy Bypass）", "critical", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "ExecutionPolicy Bypass"}
        ]),
        _rule("ps_hidden_window", "隐藏窗口（-WindowStyle Hidden）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "WindowStyle Hidden"}
        ]),
        _rule("ps_noprofile", "无配置文件启动（-NoProfile）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "-NoProfile"}
        ]),
        
        # === 网络和扫描 ===
        _rule("ps_test_connection", "网络连接测试（Test-Connection）", "info", False, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "Test-Connection"}
        ]),
        _rule("ps_invoke_webrequest", "Web请求（Invoke-WebRequest）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "Invoke-WebRequest"}
        ]),
        _rule("ps_invoke_restmethod", "REST API调用（Invoke-RestMethod）", "warning", True, "match", [
            {"field": "EventID", "op": "equals", "value": "4104"},
            {"field": "EventData_ScriptBlockText", "op": "contains", "value": "Invoke-RestMethod"}
        ]),
        
        # === 聚合检测 ===
        _rule(
            "ps_frequent_scripts_10_in_5m",
            "频繁脚本执行：5分钟内≥10次",
            "warning",
            True,
            "threshold",
            [{"field": "EventID", "op": "equals", "value": "4104"}],
            groupByField="Computer",
            threshold=10,
            timeWindowMinutes=5,
        ),
    ]


def choose_baseline_by_filename(file_name: str):
    """
    根据文件名选择告警基线
    
    Args:
        file_name: 文件名或完整路径
    
    Returns:
        对应的告警规则列表
    """
    if not file_name:
        return []
    
    # 只取文件名部分（不包含路径）
    base_name = os.path.basename(file_name).lower()
    
    # 精确匹配（优先）
    if base_name == "security.evtx":
        return security_baseline()
    if base_name == "system.evtx":
        return system_baseline()
    if base_name == "application.evtx":
        return application_baseline()
    if "powershell" in base_name:
        return powershell_baseline()
    
    # 模糊匹配（次优）
    if "security" in base_name:
        return security_baseline()
    if "system" in base_name:
        return system_baseline()
    if "application" in base_name:
        return application_baseline()
    
    # 未匹配
    return []


def choose_baseline_by_channel(channel: str):
    """
    根据Channel选择告警基线（推荐使用）
    
    Args:
        channel: 日志Channel字段值
    
    Returns:
        对应的告警规则列表
    """
    if not channel:
        return []
    
    channel_lower = channel.lower()
    
    if channel_lower == "security":
        return security_baseline()
    if channel_lower == "system":
        return system_baseline()
    if channel_lower == "application":
        return application_baseline()
    if "powershell" in channel_lower:
        return powershell_baseline()
    
    # 未匹配
    return []
