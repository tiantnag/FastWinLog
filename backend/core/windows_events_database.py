#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FastWinLog - Windows Events Database
Version: 1.0.0
Repository: https://github.com/vam876/FastWinLog
"""

# Security Events
SECURITY_EVENTS = {
    # Audit log events (1100-1108)
    '1100': {
        'name': '事件记录服务已关闭',
        'description': '事件记录服务已关闭',
        'category': '系统',
        'severity': 'warning',
        'fields': []
    },
    '1101': {
        'name': '审计事件已被运输中断',
        'description': '审计事件已被运输中断',
        'category': '审计',
        'severity': 'error',
        'fields': []
    },
    '1102': {
        'name': '审核日志已清除',
        'description': '审核日志已清除',
        'category': '审计',
        'severity': 'critical',
        'fields': ['SubjectUserName', 'SubjectDomainName', 'SubjectLogonId']
    },
    '1104': {
        'name': '安全日志现已满',
        'description': '安全日志现已满',
        'category': '审计',
        'severity': 'warning',
        'fields': []
    },
    '1105': {
        'name': '事件日志自动备份',
        'description': '事件日志自动备份',
        'category': '审计',
        'severity': 'info',
        'fields': ['BackupPath']
    },
    '1108': {
        'name': '事件日志记录服务遇到错误',
        'description': '事件日志记录服务遇到错误',
        'category': '审计',
        'severity': 'error',
        'fields': ['ErrorCode']
    },
    
    # 系统启动/关闭事件
    '4608': {
        'name': 'Windows正在启动',
        'description': 'Windows正在启动',
        'category': '系统',
        'severity': 'info',
        'fields': []
    },
    '4609': {
        'name': 'Windows正在关闭',
        'description': 'Windows正在关闭',
        'category': '系统',
        'severity': 'info',
        'fields': []
    },
    
    # 登录/注销事件
    '4624': {
        'name': '账户成功登录',
        'description': '账户已成功登录到此计算机',
        'category': '登录',
        'severity': 'info',
        'fields': ['TargetUserName', 'TargetDomainName', 'LogonType', 'IpAddress', 'WorkstationName', 'AuthenticationPackageName', 'LogonProcessName']
    },
    '4625': {
        'name': '账户登录失败',
        'description': '账户登录失败',
        'category': '登录',
        'severity': 'warning',
        'fields': ['TargetUserName', 'TargetDomainName', 'FailureReason', 'IpAddress', 'WorkstationName']
    },
    '4634': {
        'name': '账户已注销',
        'description': '账户已注销',
        'category': '注销',
        'severity': 'info',
        'fields': ['TargetUserName', 'TargetDomainName', 'LogonType']
    },
    '4647': {
        'name': '用户启动的注销',
        'description': '用户启动了注销过程',
        'category': '注销',
        'severity': 'info',
        'fields': ['TargetUserName', 'TargetDomainName']
    },
    '4648': {
        'name': '使用显式凭据尝试登录',
        'description': '使用显式凭据尝试登录',
        'category': '登录',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetServerName', 'ProcessName']
    },
    
    # 特权使用事件
    '4672': {
        'name': '分配了特殊权限',
        'description': '为新登录分配了特殊权限',
        'category': '特权',
        'severity': 'info',
        'fields': ['SubjectUserName', 'SubjectDomainName', 'PrivilegeList']
    },
    '4673': {
        'name': '特权服务被调用',
        'description': '特权服务被调用',
        'category': '特权',
        'severity': 'info',
        'fields': ['SubjectUserName', 'ProcessName', 'Service', 'PrivilegeList']
    },
    
    # 对象访问事件
    '4656': {
        'name': '请求了对象的句柄',
        'description': '请求了对象的句柄',
        'category': '对象访问',
        'severity': 'info',
        'fields': ['SubjectUserName', 'ObjectName', 'AccessMask', 'ProcessName']
    },
    '4658': {
        'name': '对象的句柄已关闭',
        'description': '对象的句柄已关闭',
        'category': '对象访问',
        'severity': 'info',
        'fields': ['SubjectUserName', 'ObjectName', 'ProcessName']
    },
    
    # 策略更改事件
    '4719': {
        'name': '系统审核策略已更改',
        'description': '系统审核策略已更改',
        'category': '策略更改',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'CategoryId', 'SubcategoryId', 'AuditPolicyChanges']
    },
    '4739': {
        'name': '域策略已更改',
        'description': '域策略已更改',
        'category': '策略更改',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'TargetDomainName', 'DomainPolicyChanged']
    },
    
    # 账户管理事件
    '4720': {
        'name': '已创建用户账户',
        'description': '已创建用户账户',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['TargetUserName', 'TargetDomainName', 'SubjectUserName', 'SamAccountName']
    },
    '4722': {
        'name': '已启用用户账户',
        'description': '已启用用户账户',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['TargetUserName', 'TargetDomainName', 'SubjectUserName']
    },
    '4723': {
        'name': '尝试更改账户密码',
        'description': '尝试更改账户密码',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['TargetUserName', 'SubjectUserName']
    },
    '4724': {
        'name': '尝试重置账户密码',
        'description': '尝试重置账户密码',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['TargetUserName', 'SubjectUserName']
    },
    '4725': {
        'name': '已禁用用户账户',
        'description': '已禁用用户账户',
        'category': '账户管理',
        'severity': 'warning',
        'fields': ['TargetUserName', 'TargetDomainName', 'SubjectUserName']
    },
    '4726': {
        'name': '已删除用户账户',
        'description': '已删除用户账户',
        'category': '账户管理',
        'severity': 'warning',
        'fields': ['TargetUserName', 'TargetDomainName', 'SubjectUserName']
    },
    
    # 进程跟踪事件
    '4688': {
        'name': '已创建新进程',
        'description': '已创建新进程',
        'category': '进程跟踪',
        'severity': 'info',
        'fields': ['SubjectUserName', 'NewProcessName', 'CommandLine', 'ProcessId']
    },
    '4689': {
        'name': '进程已退出',
        'description': '进程已退出',
        'category': '进程跟踪',
        'severity': 'info',
        'fields': ['SubjectUserName', 'ProcessName', 'ProcessId', 'ExitStatus']
    },
    
    # 文件系统事件
    '4656': {
        'name': '请求了对象的句柄',
        'description': '请求了对象的句柄',
        'category': '对象访问',
        'severity': 'info',
        'fields': ['SubjectUserName', 'ObjectName', 'AccessMask', 'ProcessName']
    },
    '4658': {
        'name': '对象的句柄已关闭',
        'description': '对象的句柄已关闭',
        'category': '对象访问',
        'severity': 'info',
        'fields': ['SubjectUserName', 'ObjectName', 'ProcessName']
    },
    '4663': {
        'name': '尝试访问对象',
        'description': '尝试访问对象',
        'category': '对象访问',
        'severity': 'info',
        'fields': ['SubjectUserName', 'ObjectName', 'AccessMask', 'ProcessName']
    },
    
    # 注册表事件
    '4657': {
        'name': '注册表值已修改',
        'description': '注册表值已修改',
        'category': '注册表',
        'severity': 'info',
        'fields': ['SubjectUserName', 'ObjectName', 'ProcessName', 'OldValue', 'NewValue']
    },
    
    # ===== 大量补充：关键安全事件 =====
    
    # 策略更改事件（4706-4719）
    '4706': {
        'name': '已创建域的新信任',
        'description': '已创建域的新信任',
        'category': '策略更改',
        'severity': 'critical',
        'fields': ['SubjectUserName', 'DomainName', 'TrustType']
    },
    '4707': {
        'name': '已删除域的信任',
        'description': '已删除域的信任',
        'category': '策略更改',
        'severity': 'critical',
        'fields': ['SubjectUserName', 'DomainName', 'TrustType']
    },
    '4713': {
        'name': 'Kerberos策略已更改',
        'description': 'Kerberos策略已更改',
        'category': '策略更改',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'KerberosPolicy']
    },
    '4716': {
        'name': '已修改受信任的域信息',
        'description': '已修改受信任的域信息',
        'category': '策略更改',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'DomainName']
    },
    '4717': {
        'name': '已授予系统安全访问权限',
        'description': '已授予系统安全访问权限',
        'category': '策略更改',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'ObjectName', 'AccessMask']
    },
    '4718': {
        'name': '已删除系统安全访问权限',
        'description': '已删除系统安全访问权限',
        'category': '策略更改',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'ObjectName', 'AccessMask']
    },
    '4719': {
        'name': '系统审核策略已更改',
        'description': '系统审核策略已更改',
        'category': '策略更改',
        'severity': 'critical',
        'fields': ['SubjectUserName', 'CategoryId', 'SubcategoryId', 'AuditPolicyChanges']
    },
    
    # 账户管理事件补充（4738-4767）
    '4738': {
        'name': '用户账户已更改',
        'description': '用户账户已更改',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetDomainName']
    },
    '4739': {
        'name': '域策略已更改',
        'description': '域策略已更改',
        'category': '策略更改',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'DomainName']
    },
    '4741': {
        'name': '已创建计算机账户',
        'description': '已创建计算机账户',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetDomainName']
    },
    '4742': {
        'name': '已更改计算机账户',
        'description': '已更改计算机账户',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetDomainName']
    },
    '4743': {
        'name': '已删除计算机账户',
        'description': '已删除计算机账户',
        'category': '账户管理',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetDomainName']
    },
    '4754': {
        'name': '已创建启用安全性的全局组',
        'description': '已创建启用安全性的全局组',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetDomainName']
    },
    '4755': {
        'name': '已更改启用安全性的全局组',
        'description': '已更改启用安全性的全局组',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetDomainName']
    },
    '4756': {
        'name': '已将成员添加到启用安全性的全局组',
        'description': '已将成员添加到启用安全性的全局组',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'MemberName', 'TargetUserName']
    },
    '4757': {
        'name': '已从启用安全性的全局组删除成员',
        'description': '已从启用安全性的全局组删除成员',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'MemberName', 'TargetUserName']
    },
    '4764': {
        'name': '已删除启用安全性的全局组',
        'description': '已删除启用安全性的全局组',
        'category': '账户管理',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetDomainName']
    },
    '4765': {
        'name': '已将SID历史记录添加到账户',
        'description': '已将SID历史记录添加到账户',
        'category': '账户管理',
        'severity': 'critical',
        'fields': ['SubjectUserName', 'TargetUserName', 'SourceSid']
    },
    '4766': {
        'name': '尝试将SID历史记录添加到账户失败',
        'description': '尝试将SID历史记录添加到账户失败',
        'category': '账户管理',
        'severity': 'error',
        'fields': ['SubjectUserName', 'TargetUserName', 'SourceSid']
    },
    '4767': {
        'name': '已解锁用户账户',
        'description': '已解锁用户账户',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetDomainName']
    },
    
    # Kerberos票证事件（4770-4773）
    '4770': {
        'name': 'Kerberos服务票证已续订',
        'description': 'Kerberos服务票证已续订',
        'category': 'Kerberos',
        'severity': 'info',
        'fields': ['TargetUserName', 'ServiceName', 'IpAddress']
    },
    '4771': {
        'name': 'Kerberos预身份验证失败',
        'description': 'Kerberos预身份验证失败',
        'category': 'Kerberos',
        'severity': 'warning',
        'fields': ['TargetUserName', 'IpAddress', 'PreAuthType', 'FailureCode']
    },
    '4772': {
        'name': 'Kerberos身份验证票证请求失败',
        'description': 'Kerberos身份验证票证请求失败',
        'category': 'Kerberos',
        'severity': 'error',
        'fields': ['TargetUserName', 'IpAddress', 'FailureCode']
    },
    '4773': {
        'name': 'Kerberos服务票证请求失败',
        'description': 'Kerberos服务票证请求失败',
        'category': 'Kerberos',
        'severity': 'warning',
        'fields': ['TargetUserName', 'ServiceName', 'FailureCode']
    },
    
    # 证书服务事件（4868-4898）
    '4868': {
        'name': '证书管理器拒绝了挂起的证书请求',
        'description': '证书管理器拒绝了挂起的证书请求',
        'category': '证书服务',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'RequestId', 'Disposition']
    },
    '4870': {
        'name': '证书服务已吊销证书',
        'description': '证书服务已吊销证书',
        'category': '证书服务',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'RequestId', 'Reason']
    },
    '4882': {
        'name': '已更改证书服务的安全权限',
        'description': '已更改证书服务的安全权限',
        'category': '证书服务',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'OldPermissions', 'NewPermissions']
    },
    '4885': {
        'name': '已更改证书服务的审核筛选器',
        'description': '已更改证书服务的审核筛选器',
        'category': '证书服务',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'OldFilter', 'NewFilter']
    },
    '4890': {
        'name': '已更改证书管理器的证书模板设置',
        'description': '已更改证书管理器的证书模板设置',
        'category': '证书服务',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'TemplateName']
    },
    
    # WMI活动事件（5857-5861）
    '5857': {
        'name': 'WMI活动检测到的提供程序',
        'description': 'WMI活动检测到的提供程序',
        'category': 'WMI',
        'severity': 'info',
        'fields': ['User', 'Operation', 'ProviderName']
    },
    '5858': {
        'name': 'WMI活动检测到的错误',
        'description': 'WMI活动检测到的错误',
        'category': 'WMI',
        'severity': 'error',
        'fields': ['User', 'Operation', 'ResultCode']
    },
    '5859': {
        'name': 'WMI事件绑定',
        'description': 'WMI事件绑定',
        'category': 'WMI',
        'severity': 'warning',
        'fields': ['User', 'Namespace', 'Filter', 'Consumer']
    },
    '5860': {
        'name': 'WMI事件过滤器',
        'description': 'WMI事件过滤器',
        'category': 'WMI',
        'severity': 'warning',
        'fields': ['User', 'Namespace', 'Query']
    },
    '5861': {
        'name': 'WMI事件消费者',
        'description': 'WMI事件消费者',
        'category': 'WMI',
        'severity': 'warning',
        'fields': ['User', 'Namespace', 'Name', 'Type']
    },
    
    # PowerShell执行事件（4103-4104）
    '4103': {
        'name': 'PowerShell模块日志记录',
        'description': 'PowerShell模块日志记录',
        'category': 'PowerShell',
        'severity': 'info',
        'fields': ['UserName', 'HostApplication', 'EngineVersion', 'Command']
    },
    '4104': {
        'name': 'PowerShell脚本块日志记录',
        'description': 'PowerShell脚本块日志记录',
        'category': 'PowerShell',
        'severity': 'warning',
        'fields': ['UserName', 'ScriptBlockText', 'ScriptBlockId', 'Path']
    },
    
    # 隐藏账户和特权提升
    '4793': {
        'name': '调用了密码策略检查API',
        'description': '调用了密码策略检查API',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName']
    },
    '4794': {
        'name': '尝试设置目录服务还原模式的管理员密码',
        'description': '尝试设置目录服务还原模式的管理员密码',
        'category': '账户管理',
        'severity': 'critical',
        'fields': ['SubjectUserName']
    },
    
    # 访问令牌操作
    '4906': {
        'name': 'CrashOnAuditFail值已更改',
        'description': 'CrashOnAuditFail值已更改',
        'category': '策略更改',
        'severity': 'critical',
        'fields': ['SubjectUserName', 'OldValue', 'NewValue']
    },
    '4907': {
        'name': '已更改对象的审核设置',
        'description': '已更改对象的审核设置',
        'category': '策略更改',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'ObjectName', 'OldSd', 'NewSd']
    },
    '4908': {
        'name': '已更改特殊组登录表',
        'description': '已更改特殊组登录表',
        'category': '策略更改',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'SpecialGroups']
    },
    
    # BitLocker事件
    '4942': {
        'name': 'BitLocker已启用驱动器保护',
        'description': 'BitLocker已启用驱动器保护',
        'category': '加密',
        'severity': 'info',
        'fields': ['SubjectUserName', 'DriveLetter']
    },
    '4943': {
        'name': 'BitLocker已禁用驱动器保护',
        'description': 'BitLocker已禁用驱动器保护',
        'category': '加密',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'DriveLetter']
    },
    
    # DPAPI事件
    '4692': {
        'name': '尝试备份数据保护主密钥',
        'description': '尝试备份数据保护主密钥',
        'category': '加密',
        'severity': 'info',
        'fields': ['SubjectUserName', 'MasterKeyId']
    },
    '4693': {
        'name': '尝试恢复数据保护主密钥',
        'description': '尝试恢复数据保护主密钥',
        'category': '加密',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'MasterKeyId']
    },
    
    # RPC事件
    '5712': {
        'name': 'RPC尝试',
        'description': '尝试远程过程调用',
        'category': 'RPC',
        'severity': 'info',
        'fields': ['SubjectUserName', 'InterfaceUuid', 'Protocol']
    },
    
    # 网络事件
    '5156': {
        'name': '允许连接',
        'description': 'Windows筛选平台允许连接',
        'category': '网络',
        'severity': 'info',
        'fields': ['Application', 'Direction', 'SourceAddress', 'DestAddress', 'Protocol']
    },
    '5157': {
        'name': '阻止连接',
        'description': 'Windows筛选平台阻止连接',
        'category': '网络',
        'severity': 'warning',
        'fields': ['Application', 'Direction', 'SourceAddress', 'DestAddress', 'Protocol']
    },
    
    # 组策略事件
    '4704': {
        'name': '分配了用户权限',
        'description': '分配了用户权限',
        'category': '策略更改',
        'severity': 'info',
        'fields': ['SubjectUserName', 'PrivilegeName', 'Attributes']
    },
    '4705': {
        'name': '删除了用户权限',
        'description': '删除了用户权限',
        'category': '策略更改',
        'severity': 'info',
        'fields': ['SubjectUserName', 'PrivilegeName']
    },
    
    # 服务事件
    '4697': {
        'name': '已安装服务',
        'description': '系统中已安装服务',
        'category': '服务',
        'severity': 'info',
        'fields': ['SubjectUserName', 'ServiceName', 'ServiceFileName', 'ServiceType']
    },
    
    # Kerberos事件
    '4768': {
        'name': 'Kerberos身份验证票证(TGT)已请求',
        'description': 'Kerberos身份验证票证(TGT)已请求',
        'category': 'Kerberos',
        'severity': 'info',
        'fields': ['TargetUserName', 'TargetDomainName', 'IpAddress', 'TicketOptions']
    },
    '4769': {
        'name': 'Kerberos服务票证已请求',
        'description': 'Kerberos服务票证已请求',
        'category': 'Kerberos',
        'severity': 'info',
        'fields': ['TargetUserName', 'ServiceName', 'IpAddress', 'TicketOptions']
    },
    '4771': {
        'name': 'Kerberos预身份验证失败',
        'description': 'Kerberos预身份验证失败',
        'category': 'Kerberos',
        'severity': 'warning',
        'fields': ['TargetUserName', 'IpAddress', 'FailureCode']
    },
    
    # 共享访问事件
    '5140': {
        'name': '访问了网络共享对象',
        'description': '访问了网络共享对象',
        'category': '共享访问',
        'severity': 'info',
        'fields': ['SubjectUserName', 'IpAddress', 'ShareName', 'RelativeTargetName']
    },
    '5145': {
        'name': '检查了共享对象以查看是否可以授予所需访问权限',
        'description': '检查了共享对象以查看是否可以授予所需访问权限',
        'category': '共享访问',
        'severity': 'info',
        'fields': ['SubjectUserName', 'IpAddress', 'ShareName', 'RelativeTargetName', 'AccessMask']
    },
    
    # 更多登录/身份验证事件
    '4626': {
        'name': '用户/设备声明信息',
        'description': '用户/设备声明信息',
        'category': '登录',
        'severity': 'info',
        'fields': ['SubjectUserName', 'SubjectDomainName', 'Claims']
    },
    '4627': {
        'name': '组成员身份信息',
        'description': '组成员身份信息',
        'category': '登录',
        'severity': 'info',
        'fields': ['SubjectUserName', 'SubjectDomainName', 'GroupMembership']
    },
    '4649': {
        'name': '检测到重放攻击',
        'description': '检测到重放攻击',
        'category': '登录',
        'severity': 'error',
        'fields': ['SubjectUserName', 'TargetUserName', 'ServiceName']
    },
    '4778': {
        'name': '会话已重新连接到窗口站',
        'description': '会话已重新连接到窗口站',
        'category': '会话',
        'severity': 'info',
        'fields': ['AccountName', 'SessionName', 'ClientName', 'ClientAddress']
    },
    '4779': {
        'name': '会话已从窗口站断开连接',
        'description': '会话已从窗口站断开连接',
        'category': '会话',
        'severity': 'info',
        'fields': ['AccountName', 'SessionName', 'ClientName', 'ClientAddress']
    },
    '4800': {
        'name': '工作站已锁定',
        'description': '工作站已锁定',
        'category': '会话',
        'severity': 'info',
        'fields': ['TargetUserName', 'TargetDomainName', 'SessionId']
    },
    '4801': {
        'name': '工作站已解锁',
        'description': '工作站已解锁',
        'category': '会话',
        'severity': 'info',
        'fields': ['TargetUserName', 'TargetDomainName', 'SessionId']
    },
    '4802': {
        'name': '已调用屏幕保护程序',
        'description': '已调用屏幕保护程序',
        'category': '会话',
        'severity': 'info',
        'fields': ['TargetUserName', 'SessionId']
    },
    '4803': {
        'name': '已关闭屏幕保护程序',
        'description': '已关闭屏幕保护程序',
        'category': '会话',
        'severity': 'info',
        'fields': ['TargetUserName', 'SessionId']
    },
    
    # 更多账户管理事件
    '4727': {
        'name': '已创建全局安全组',
        'description': '已创建全局安全组',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetDomainName']
    },
    '4728': {
        'name': '已将成员添加到全局安全组',
        'description': '已将成员添加到全局安全组',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'MemberName']
    },
    '4729': {
        'name': '已将成员从全局安全组中删除',
        'description': '已将成员从全局安全组中删除',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'MemberName']
    },
    '4730': {
        'name': '已删除全局安全组',
        'description': '已删除全局安全组',
        'category': '账户管理',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetDomainName']
    },
    '4731': {
        'name': '已创建本地安全组',
        'description': '已创建本地安全组',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName']
    },
    '4732': {
        'name': '已将成员添加到本地安全组',
        'description': '已将成员添加到本地安全组',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'MemberName']
    },
    '4733': {
        'name': '已将成员从本地安全组中删除',
        'description': '已将成员从本地安全组中删除',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'MemberName']
    },
    '4734': {
        'name': '已删除本地安全组',
        'description': '已删除本地安全组',
        'category': '账户管理',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'TargetUserName']
    },
    '4735': {
        'name': '已更改本地安全组',
        'description': '已更改本地安全组',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName']
    },
    '4737': {
        'name': '已更改全局安全组',
        'description': '已更改全局安全组',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetDomainName']
    },
    '4738': {
        'name': '已更改用户账户',
        'description': '已更改用户账户',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetDomainName']
    },
    '4740': {
        'name': '用户账户已锁定',
        'description': '用户账户已锁定',
        'category': '账户管理',
        'severity': 'warning',
        'fields': ['TargetUserName', 'TargetDomainName', 'CallerComputerName']
    },
    '4741': {
        'name': '已创建计算机账户',
        'description': '已创建计算机账户',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetDomainName']
    },
    '4742': {
        'name': '已更改计算机账户',
        'description': '已更改计算机账户',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetDomainName']
    },
    '4743': {
        'name': '已删除计算机账户',
        'description': '已删除计算机账户',
        'category': '账户管理',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetDomainName']
    },
    '4755': {
        'name': '已创建通用安全组',
        'description': '已创建通用安全组',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetDomainName']
    },
    '4756': {
        'name': '已将成员添加到通用安全组',
        'description': '已将成员添加到通用安全组',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'MemberName']
    },
    '4757': {
        'name': '已将成员从通用安全组中删除',
        'description': '已将成员从通用安全组中删除',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'MemberName']
    },
    '4758': {
        'name': '已删除通用安全组',
        'description': '已删除通用安全组',
        'category': '账户管理',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetDomainName']
    },
    '4764': {
        'name': '已尝试更改组的类型',
        'description': '已尝试更改组的类型',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName']
    },
    '4767': {
        'name': '用户账户已解锁',
        'description': '用户账户已解锁',
        'category': '账户管理',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TargetUserName', 'TargetDomainName']
    },
    
    # 更多对象访问事件
    '4660': {
        'name': '已删除对象',
        'description': '已删除对象',
        'category': '对象访问',
        'severity': 'info',
        'fields': ['SubjectUserName', 'ObjectName', 'ProcessName']
    },
    '4661': {
        'name': '请求了对象的句柄',
        'description': '请求了对象的句柄',
        'category': '对象访问',
        'severity': 'info',
        'fields': ['SubjectUserName', 'ObjectServer', 'ObjectType', 'ObjectName']
    },
    '4662': {
        'name': '执行了对对象的操作',
        'description': '执行了对对象的操作',
        'category': '对象访问',
        'severity': 'info',
        'fields': ['SubjectUserName', 'ObjectServer', 'ObjectType', 'ObjectName', 'OperationType']
    },
    '4663': {
        'name': '尝试访问对象',
        'description': '尝试访问对象',
        'category': '对象访问',
        'severity': 'info',
        'fields': ['SubjectUserName', 'ObjectName', 'ProcessName', 'AccessMask']
    },
    '4664': {
        'name': '尝试创建硬链接',
        'description': '尝试创建硬链接',
        'category': '对象访问',
        'severity': 'info',
        'fields': ['SubjectUserName', 'FileName', 'LinkName']
    },
    '4670': {
        'name': '已更改对象的权限',
        'description': '已更改对象的权限',
        'category': '对象访问',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'ObjectName', 'ProcessName', 'OldSd', 'NewSd']
    },
    '4690': {
        'name': '尝试复制对象的句柄',
        'description': '尝试复制对象的句柄',
        'category': '对象访问',
        'severity': 'info',
        'fields': ['SubjectUserName', 'SourceHandleId', 'TargetHandleId', 'ProcessId']
    },
    '4698': {
        'name': '已创建计划任务',
        'description': '已创建计划任务',
        'category': '对象访问',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'TaskName', 'TaskContent']
    },
    '4699': {
        'name': '已删除计划任务',
        'description': '已删除计划任务',
        'category': '对象访问',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'TaskName']
    },
    '4700': {
        'name': '已启用计划任务',
        'description': '已启用计划任务',
        'category': '对象访问',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TaskName']
    },
    '4701': {
        'name': '已禁用计划任务',
        'description': '已禁用计划任务',
        'category': '对象访问',
        'severity': 'info',
        'fields': ['SubjectUserName', 'TaskName']
    },
    '4702': {
        'name': '已更新计划任务',
        'description': '已更新计划任务',
        'category': '对象访问',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'TaskName', 'TaskContent']
    },
    
    # 注册表事件
    '4657': {
        'name': '修改了注册表值',
        'description': '修改了注册表值',
        'category': '注册表',
        'severity': 'info',
        'fields': ['SubjectUserName', 'ObjectName', 'ProcessName', 'OperationType']
    },
    '5039': {
        'name': '注册表键被虚拟化',
        'description': '注册表键被虚拟化',
        'category': '注册表',
        'severity': 'info',
        'fields': ['ProcessId', 'ProcessName', 'ObjectName']
    },
    
    # 系统完整性事件
    '4817': {
        'name': '已更改对象的审核设置',
        'description': '已更改对象的审核设置',
        'category': '系统完整性',
        'severity': 'warning',
        'fields': ['SubjectUserName', 'ObjectName', 'ObjectServer', 'OldSd', 'NewSd']
    },
    '5038': {
        'name': '检测到代码完整性',
        'description': '检测到代码完整性',
        'category': '系统完整性',
        'severity': 'error',
        'fields': ['FileNameBuffer', 'FileHashValue']
    },
    '5056': {
        'name': '已执行加密自测',
        'description': '已执行加密自测',
        'category': '系统完整性',
        'severity': 'info',
        'fields': ['SubjectUserName', 'Module', 'ReturnCode']
    },
    '5057': {
        'name': '加密原始操作失败',
        'description': '加密原始操作失败',
        'category': '系统完整性',
        'severity': 'error',
        'fields': ['SubjectUserName', 'ProviderName', 'AlgorithmName', 'ReturnCode']
    },
    '5058': {
        'name': '键文件操作',
        'description': '键文件操作',
        'category': '系统完整性',
        'severity': 'info',
        'fields': ['SubjectUserName', 'ProviderName', 'KeyName', 'Operation']
    },
    
    # Windows Defender事件
    '5148': {
        'name': 'Windows筛选平台检测到DOS攻击',
        'description': 'Windows筛选平台检测到DOS攻击',
        'category': '网络安全',
        'severity': 'error',
        'fields': ['Application', 'SourceAddress', 'DestAddress']
    },
    '5149': {
        'name': '已禁用DOS攻击保护',
        'description': 'Windows筛选平台DOS攻击保护已禁用',
        'category': '网络安全',
        'severity': 'warning',
        'fields': ['Application', 'SourceAddress']
    },
    '5150': {
        'name': 'Windows筛选平台阻止了一个数据包',
        'description': 'Windows筛选平台阻止了一个数据包',
        'category': '网络安全',
        'severity': 'warning',
        'fields': ['Application', 'Direction', 'SourceAddress', 'DestAddress', 'Protocol']
    },
    '5151': {
        'name': '更具许可的Windows筛选平台筛选器阻止了一个数据包',
        'description': '更具许可的Windows筛选平台筛选器阻止了一个数据包',
        'category': '网络安全',
        'severity': 'warning',
        'fields': ['Application', 'Direction', 'SourceAddress', 'DestAddress', 'Protocol']
    },
    '5152': {
        'name': 'Windows筛选平台阻止了数据包',
        'description': 'Windows筛选平台阻止了数据包',
        'category': '网络安全',
        'severity': 'warning',
        'fields': ['Application', 'Direction', 'SourceAddress', 'DestAddress', 'Protocol']
    },
    '5153': {
        'name': '更具许可的Windows筛选平台筛选器阻止了一个数据包',
        'description': '更具许可的Windows筛选平台筛选器阻止了一个数据包',
        'category': '网络安全',
        'severity': 'warning',
        'fields': ['Application', 'Direction', 'SourceAddress', 'DestAddress', 'Protocol']
    },
    '5154': {
        'name': 'Windows筛选平台允许应用程序或服务监听端口',
        'description': 'Windows筛选平台允许应用程序或服务监听端口',
        'category': '网络安全',
        'severity': 'info',
        'fields': ['Application', 'SourceAddress', 'SourcePort', 'Protocol']
    },
    '5155': {
        'name': 'Windows筛选平台阻止了应用程序或服务监听端口',
        'description': 'Windows筛选平台阻止了应用程序或服务监听端口',
        'category': '网络安全',
        'severity': 'warning',
        'fields': ['Application', 'SourceAddress', 'SourcePort', 'Protocol']
    },
    '5158': {
        'name': 'Windows筛选平台允许绑定到本地端口',
        'description': 'Windows筛选平台允许绑定到本地端口',
        'category': '网络安全',
        'severity': 'info',
        'fields': ['Application', 'SourceAddress', 'SourcePort', 'Protocol']
    },
    '5159': {
        'name': 'Windows筛选平台阻止了绑定到本地端口',
        'description': 'Windows筛选平台阻止了绑定到本地端口',
        'category': '网络安全',
        'severity': 'warning',
        'fields': ['Application', 'SourceAddress', 'SourcePort', 'Protocol']
    },
}

# 系统事件 (System Events)
SYSTEM_EVENTS = {
    # 系统启动/关闭
    '6005': {
        'name': '事件日志服务已启动',
        'description': '事件日志服务已启动',
        'category': '系统',
        'severity': 'info',
        'fields': []
    },
    '6006': {
        'name': '事件日志服务已停止',
        'description': '事件日志服务已停止',
        'category': '系统',
        'severity': 'warning',
        'fields': []
    },
    '6009': {
        'name': '系统启动',
        'description': '系统已启动',
        'category': '系统',
        'severity': 'info',
        'fields': ['ProcessorArchitecture', 'ProcessorLevel', 'ProcessorCount']
    },
    '6013': {
        'name': '系统运行时间',
        'description': '系统运行时间',
        'category': '系统',
        'severity': 'info',
        'fields': ['UptimeSeconds']
    },
    '1074': {
        'name': '系统关机/重启',
        'description': '系统正在关机或重启',
        'category': '系统',
        'severity': 'info',
        'fields': ['User', 'Process', 'Reason', 'ShutdownType']
    },
    '1076': {
        'name': '系统关机原因',
        'description': '记录系统关机的原因',
        'category': '系统',
        'severity': 'info',
        'fields': ['User', 'Reason', 'ReasonCode']
    },
    
    # 服务事件
    '7034': {
        'name': '服务意外终止',
        'description': '服务意外终止',
        'category': '服务',
        'severity': 'error',
        'fields': ['ServiceName']
    },
    '7035': {
        'name': '服务控制命令已发送',
        'description': '服务控制命令已发送',
        'category': '服务',
        'severity': 'info',
        'fields': ['ServiceName', 'User', 'Control']
    },
    '7036': {
        'name': '服务状态已更改',
        'description': '服务已进入运行状态或已停止状态',
        'category': '服务',
        'severity': 'info',
        'fields': ['ServiceName', 'State']
    },
    '7040': {
        'name': '服务启动类型已更改',
        'description': '服务的启动类型已更改',
        'category': '服务',
        'severity': 'info',
        'fields': ['ServiceName', 'StartType', 'User']
    },
    '7000': {
        'name': '服务启动失败',
        'description': '服务未能启动',
        'category': '服务',
        'severity': 'error',
        'fields': ['ServiceName', 'ErrorCode']
    },
    '7001': {
        'name': '服务依赖失败',
        'description': '服务依赖于另一服务，该服务未能启动',
        'category': '服务',
        'severity': 'error',
        'fields': ['ServiceName', 'DependentService']
    },
    '7009': {
        'name': '服务超时',
        'description': '连接服务超时',
        'category': '服务',
        'severity': 'error',
        'fields': ['ServiceName', 'Timeout']
    },
    '7011': {
        'name': '服务响应超时',
        'description': '服务在事务中未能及时响应',
        'category': '服务',
        'severity': 'warning',
        'fields': ['ServiceName', 'Timeout']
    },
    '7022': {
        'name': '服务挂起',
        'description': '服务在启动时挂起',
        'category': '服务',
        'severity': 'error',
        'fields': ['ServiceName']
    },
    '7023': {
        'name': '服务错误终止',
        'description': '服务以错误终止',
        'category': '服务',
        'severity': 'error',
        'fields': ['ServiceName', 'ErrorCode']
    },
    '7024': {
        'name': '服务特定错误终止',
        'description': '服务以服务特定错误终止',
        'category': '服务',
        'severity': 'error',
        'fields': ['ServiceName', 'ErrorCode']
    },
    '7026': {
        'name': '引导启动或系统启动驱动程序未能加载',
        'description': '引导启动或系统启动驱动程序未能加载',
        'category': '系统',
        'severity': 'error',
        'fields': ['DriverName']
    },
    '7031': {
        'name': '服务意外终止',
        'description': '服务意外终止，系统将尝试恢复',
        'category': '服务',
        'severity': 'error',
        'fields': ['ServiceName', 'TerminationCount']
    },
    '7032': {
        'name': '服务控制管理器尝试采取纠正措施',
        'description': '服务控制管理器尝试采取纠正措施',
        'category': '服务',
        'severity': 'warning',
        'fields': ['ServiceName', 'Action']
    },
    '7045': {
        'name': '服务已安装',
        'description': '服务已安装到系统中',
        'category': '服务',
        'severity': 'info',
        'fields': ['ServiceName', 'ImagePath', 'ServiceType', 'StartType', 'AccountName']
    },
    
    # 磁盘事件
    '51': {
        'name': '磁盘警告',
        'description': '在设备上检测到错误',
        'category': '磁盘',
        'severity': 'warning',
        'fields': ['DeviceName']
    },
    '55': {
        'name': '文件系统损坏',
        'description': '文件系统结构已损坏',
        'category': '磁盘',
        'severity': 'error',
        'fields': ['VolumeName']
    },
    '98': {
        'name': 'BitLocker加密',
        'description': 'BitLocker加密卷状态',
        'category': '安全',
        'severity': 'info',
        'fields': ['VolumeName', 'Status']
    },
    '131': {
        'name': '存储重置',
        'description': '存储设备已重置',
        'category': '磁盘',
        'severity': 'warning',
        'fields': ['DeviceName', 'PathId', 'TargetId']
    },
    
    # 驱动程序事件
    '219': {
        'name': '内核模式驱动程序阻止',
        'description': '内核模式驱动程序已被阻止',
        'category': '驱动程序',
        'severity': 'warning',
        'fields': ['DriverName', 'Reason']
    },
    
    # 时间服务事件
    '1': {
        'name': 'Windows时间服务已启动',
        'description': 'Windows时间服务已启动',
        'category': '时间服务',
        'severity': 'info',
        'fields': []
    },
    '35': {
        'name': '时间同步成功',
        'description': 'Windows时间服务已成功同步系统时间',
        'category': '时间服务',
        'severity': 'info',
        'fields': ['TimeSource', 'Offset']
    },
    '37': {
        'name': '时间同步失败',
        'description': 'Windows时间服务无法同步系统时间',
        'category': '时间服务',
        'severity': 'warning',
        'fields': ['TimeSource']
    },
    '50': {
        'name': '时间提供程序停止',
        'description': '时间提供程序已停止响应',
        'category': '时间服务',
        'severity': 'warning',
        'fields': ['ProviderName']
    },
    
    # 用户配置文件服务事件
    '1500': {
        'name': '用户配置文件服务已启动',
        'description': '用户配置文件服务已成功启动',
        'category': '用户配置文件',
        'severity': 'info',
        'fields': []
    },
    '1530': {
        'name': '注册表文件正在被其他进程使用',
        'description': '注册表文件正在被其他进程使用',
        'category': '用户配置文件',
        'severity': 'warning',
        'fields': ['FileName', 'ProcessId']
    },
    '1533': {
        'name': '用户配置文件警告',
        'description': '用户配置文件警告',
        'category': '用户配置文件',
        'severity': 'warning',
        'fields': ['ErrorCode']
    },
    '1534': {
        'name': '用户配置文件错误',
        'description': '用户配置文件错误',
        'category': '用户配置文件',
        'severity': 'error',
        'fields': ['ErrorCode']
    },
    
    # DNS客户端事件
    '1014': {
        'name': 'DNS名称解析失败',
        'description': 'DNS名称解析失败',
        'category': 'DNS',
        'severity': 'warning',
        'fields': ['QueryName', 'ErrorCode']
    },
    '1015': {
        'name': 'DNS名称解析超时',
        'description': 'DNS名称解析超时',
        'category': 'DNS',
        'severity': 'warning',
        'fields': ['QueryName', 'Timeout']
    },
    
    # DHCP客户端事件
    '1001': {
        'name': 'DHCP IP地址租用',
        'description': 'DHCP客户端已成功从DHCP服务器获得IP地址租用',
        'category': 'DHCP',
        'severity': 'info',
        'fields': ['IpAddress', 'DHCPServer', 'AdapterName']
    },
    '1002': {
        'name': 'DHCP IP地址租用失败',
        'description': 'DHCP客户端未能从DHCP服务器获得IP地址租用',
        'category': 'DHCP',
        'severity': 'error',
        'fields': ['AdapterName', 'ErrorCode']
    },
    '1003': {
        'name': 'DHCP IP地址冲突',
        'description': 'DHCP客户端检测到IP地址冲突',
        'category': 'DHCP',
        'severity': 'error',
        'fields': ['IpAddress', 'ConflictingMAC']
    },
    
    # 电源管理事件
    '1': {
        'name': '系统从睡眠状态恢复',
        'description': '系统从睡眠状态恢复',
        'category': '电源',
        'severity': 'info',
        'fields': ['SleepTime', 'WakeTime']
    },
    '42': {
        'name': '系统正在进入睡眠状态',
        'description': '系统正在进入睡眠状态',
        'category': '电源',
        'severity': 'info',
        'fields': ['SleepType']
    },
    '107': {
        'name': '系统电源状态已更改',
        'description': '系统电源状态已更改',
        'category': '电源',
        'severity': 'info',
        'fields': ['PowerState']
    },
    
    # 更新事件
    '19': {
        'name': 'Windows更新安装成功',
        'description': 'Windows更新安装成功',
        'category': '更新',
        'severity': 'info',
        'fields': ['UpdateTitle', 'UpdateId']
    },
    '20': {
        'name': 'Windows更新安装失败',
        'description': 'Windows更新安装失败',
        'category': '更新',
        'severity': 'error',
        'fields': ['UpdateTitle', 'ErrorCode']
    },
    
    # ===== 大量补充System事件 =====
    
    # 更多关键系统事件
    '41': {
        'name': '系统重启未正常关机',
        'description': '系统重启但之前未正常关机',
        'category': '系统',
        'severity': 'critical',
        'fields': ['BugcheckCode']
    },
    '1001': {
        'name': 'BugCheck蓝屏',
        'description': '计算机已从检查错误后重新启动',
        'category': '系统',
        'severity': 'critical',
        'fields': ['BugCheckCode', 'BugCheckParameter1', 'DumpFile']
    },
    '6008': {
        'name': '意外关机',
        'description': '上一次系统关机是意外的',
        'category': '系统',
        'severity': 'critical',
        'fields': ['Time']
    },
    
    # 更多磁盘和存储事件
    '52': {
        'name': '磁盘写入错误',
        'description': '磁盘写入发生错误',
        'category': '磁盘',
        'severity': 'error',
        'fields': ['DiskNumber', 'ErrorCode']
    },
    '153': {
        'name': '磁盘块重新映射',
        'description': '磁盘块重新映射',
        'category': '磁盘',
        'severity': 'warning',
        'fields': ['DeviceName', 'BlockNumber']
    },
    '154': {
        'name': 'NTFS损坏',
        'description': 'NTFS文件系统遇到损坏',
        'category': '磁盘',
        'severity': 'critical',
        'fields': ['VolumeName']
    },
    
    # 更多网络事件
    '4201': {
        'name': '网络适配器检测到连接',
        'description': '网络适配器检测到媒体连接',
        'category': '网络',
        'severity': 'info',
        'fields': ['AdapterName']
    },
    '4202': {
        'name': '网络适配器断开连接',
        'description': '网络适配器检测到媒体断开',
        'category': '网络',
        'severity': 'warning',
        'fields': ['AdapterName']
    },
    '4227': {
        'name': 'DHCP无法获取IP',
        'description': 'DHCP客户端无法获得IP地址',
        'category': '网络',
        'severity': 'error',
        'fields': ['AdapterName']
    },
    '10010': {
        'name': 'DistributedCOM错误',
        'description': 'DCOM无法启动服务',
        'category': 'DCOM',
        'severity': 'error',
        'fields': ['ServiceName', 'ErrorCode']
    },
    '10016': {
        'name': 'DCOM权限错误',
        'description': 'DCOM应用程序权限错误',
        'category': 'DCOM',
        'severity': 'warning',
        'fields': ['AppId', 'UserSID']
    },
    
    # 内核和驱动程序事件
    '7030': {
        'name': '服务标记为交互式',
        'description': '服务标记为交互式服务',
        'category': '服务',
        'severity': 'warning',
        'fields': ['ServiceName']
    },
    '7042': {
        'name': '服务启动类型更改为禁用',
        'description': '服务启动类型更改为禁用',
        'category': '服务',
        'severity': 'warning',
        'fields': ['ServiceName', 'User']
    },
    '7043': {
        'name': '服务无法停止',
        'description': '服务无法停止',
        'category': '服务',
        'severity': 'error',
        'fields': ['ServiceName']
    },
    '15': {
        'name': '磁盘配置信息错误',
        'description': '磁盘配置信息无法读取',
        'category': '磁盘',
        'severity': 'critical',
        'fields': ['DiskId']
    },
    
    # 内存和性能
    '2004': {
        'name': '资源耗尽',
        'description': '服务器资源耗尽',
        'category': '性能',
        'severity': 'critical',
        'fields': ['ResourceType']
    },
    '2019': {
        'name': '服务器无法分配内存',
        'description': '服务器无法从非分页池分配内存',
        'category': '性能',
        'severity': 'critical',
        'fields': []
    },
    '2020': {
        'name': '服务器资源不足',
        'description': '服务器资源不足',
        'category': '性能',
        'severity': 'critical',
        'fields': []
    },
    
    # 打印服务
    '307': {
        'name': '打印机驱动程序已安装',
        'description': '打印机驱动程序已成功安装',
        'category': '打印',
        'severity': 'info',
        'fields': ['DriverName', 'PrinterName']
    },
    '315': {
        'name': '打印作业已删除',
        'description': '打印作业已被删除',
        'category': '打印',
        'severity': 'info',
        'fields': ['JobId', 'User', 'PrinterName']
    },
    '372': {
        'name': '打印机驱动程序更新失败',
        'description': '打印机驱动程序更新失败',
        'category': '打印',
        'severity': 'error',
        'fields': ['DriverName', 'ErrorCode']
    },
    
    # 组策略
    '1096': {
        'name': '组策略处理成功',
        'description': '组策略对象已成功处理',
        'category': '组策略',
        'severity': 'info',
        'fields': ['GPOName', 'Status']
    },
    '1097': {
        'name': '组策略处理失败',
        'description': '组策略对象处理失败',
        'category': '组策略',
        'severity': 'error',
        'fields': ['GPOName', 'Error']
    },
    '1129': {
        'name': '组策略延迟',
        'description': '组策略处理被延迟',
        'category': '组策略',
        'severity': 'warning',
        'fields': ['Reason']
    },
    
    # Hyper-V虚拟化
    '12': {
        'name': 'Hyper-V启动',
        'description': 'Hyper-V已启动',
        'category': '虚拟化',
        'severity': 'info',
        'fields': []
    },
    '18512': {
        'name': '虚拟机启动',
        'description': '虚拟机已启动',
        'category': '虚拟化',
        'severity': 'info',
        'fields': ['VMName', 'VMId']
    },
    '18514': {
        'name': '虚拟机停止',
        'description': '虚拟机已停止',
        'category': '虚拟化',
        'severity': 'info',
        'fields': ['VMName', 'VMId']
    },
    '18520': {
        'name': '虚拟机保存状态',
        'description': '虚拟机已保存状态',
        'category': '虚拟化',
        'severity': 'info',
        'fields': ['VMName']
    },
    
    # Kernel-Power事件
    '109': {
        'name': '内核已启动电源转换',
        'description': '内核电源管理器已启动电源转换',
        'category': '电源',
        'severity': 'info',
        'fields': ['TargetState']
    },
    '125': {
        'name': '设备没有响应或已断开连接',
        'description': '设备没有响应或已断开连接',
        'category': '设备',
        'severity': 'warning',
        'fields': ['DeviceName']
    },
    '137': {
        'name': '设备电源请求',
        'description': '设备请求电源',
        'category': '电源',
        'severity': 'info',
        'fields': ['DeviceName', 'RequestType']
    },
    
    # Windows Defender
    '1116': {
        'name': 'Windows Defender检测到恶意软件',
        'description': 'Windows Defender检测到恶意软件或其他潜在有害软件',
        'category': '安全',
        'severity': 'critical',
        'fields': ['ThreatName', 'Severity', 'Path']
    },
    '1117': {
        'name': 'Windows Defender已执行操作',
        'description': 'Windows Defender已执行操作以保护此计算机',
        'category': '安全',
        'severity': 'warning',
        'fields': ['ThreatName', 'Action']
    },
    '1118': {
        'name': 'Windows Defender扫描检测',
        'description': 'Windows Defender扫描检测到威胁',
        'category': '安全',
        'severity': 'critical',
        'fields': ['ThreatName', 'Path']
    },
    '1119': {
        'name': 'Windows Defender清除失败',
        'description': 'Windows Defender无法清除威胁',
        'category': '安全',
        'severity': 'error',
        'fields': ['ThreatName', 'ErrorCode']
    },
    '5001': {
        'name': 'Windows Defender实时保护已禁用',
        'description': 'Windows Defender实时保护已禁用',
        'category': '安全',
        'severity': 'critical',
        'fields': []
    },
    '5004': {
        'name': 'Windows Defender配置已更改',
        'description': 'Windows Defender配置已更改',
        'category': '安全',
        'severity': 'warning',
        'fields': ['NewValue', 'OldValue']
    },
    '5010': {
        'name': 'Windows Defender扫描病毒和间谍软件被禁用',
        'description': '扫描病毒和其他可能不需要的软件的功能已被禁用',
        'category': '安全',
        'severity': 'critical',
        'fields': []
    },
    '5012': {
        'name': 'Windows Defender扫描间谍软件被禁用',
        'description': '扫描间谍软件的功能已被禁用',
        'category': '安全',
        'severity': 'critical',
        'fields': []
    },
    
    # 防火墙事件
    '2003': {
        'name': 'Windows防火墙无法加载组策略',
        'description': 'Windows防火墙无法加载组策略',
        'category': '防火墙',
        'severity': 'error',
        'fields': ['ErrorCode']
    },
    '2004': {
        'name': 'Windows防火墙规则已添加',
        'description': 'Windows防火墙入站规则已添加',
        'category': '防火墙',
        'severity': 'info',
        'fields': ['RuleName', 'RuleId']
    },
    '2005': {
        'name': 'Windows防火墙规则已修改',
        'description': 'Windows防火墙规则已修改',
        'category': '防火墙',
        'severity': 'warning',
        'fields': ['RuleName', 'RuleId']
    },
    '2006': {
        'name': 'Windows防火墙规则已删除',
        'description': 'Windows防火墙规则已删除',
        'category': '防火墙',
        'severity': 'warning',
        'fields': ['RuleName', 'RuleId']
    },
    '2033': {
        'name': 'Windows防火墙已阻止应用程序',
        'description': 'Windows防火墙已阻止应用程序监听端口',
        'category': '防火墙',
        'severity': 'warning',
        'fields': ['Application', 'Port']
    },
    
    # Task Scheduler计划任务
    '100': {
        'name': '任务启动',
        'description': '任务计划程序启动了任务',
        'category': '计划任务',
        'severity': 'info',
        'fields': ['TaskName', 'UserName']
    },
    '101': {
        'name': '任务启动失败',
        'description': '任务计划程序未能启动任务',
        'category': '计划任务',
        'severity': 'error',
        'fields': ['TaskName', 'ErrorCode']
    },
    '102': {
        'name': '任务完成',
        'description': '任务计划程序已成功完成任务',
        'category': '计划任务',
        'severity': 'info',
        'fields': ['TaskName', 'ActionName']
    },
    '103': {
        'name': '任务失败',
        'description': '任务计划程序未能完成任务',
        'category': '计划任务',
        'severity': 'error',
        'fields': ['TaskName', 'ErrorCode']
    },
    '106': {
        'name': '任务已注册',
        'description': '用户已注册任务',
        'category': '计划任务',
        'severity': 'info',
        'fields': ['TaskName', 'UserName']
    },
    '107': {
        'name': '任务触发',
        'description': '在计划程序中触发了任务',
        'category': '计划任务',
        'severity': 'info',
        'fields': ['TaskName']
    },
    '110': {
        'name': '任务超时',
        'description': '任务已达到最大执行时间限制',
        'category': '计划任务',
        'severity': 'warning',
        'fields': ['TaskName', 'TimeLimit']
    },
    '141': {
        'name': '任务删除',
        'description': '用户已删除任务',
        'category': '计划任务',
        'severity': 'warning',
        'fields': ['TaskName', 'UserName']
    },
    '200': {
        'name': '任务操作启动',
        'description': '任务计划程序启动了任务操作',
        'category': '计划任务',
        'severity': 'info',
        'fields': ['TaskName', 'ActionName']
    },
    '201': {
        'name': '任务操作完成',
        'description': '任务计划程序已成功完成任务操作',
        'category': '计划任务',
        'severity': 'info',
        'fields': ['TaskName', 'ActionName', 'ResultCode']
    },
    
    # USB设备事件
    '20001': {
        'name': 'USB设备首次连接',
        'description': 'USB设备首次连接到系统',
        'category': 'USB',
        'severity': 'info',
        'fields': ['DeviceId', 'DeviceDescription']
    },
    '20003': {
        'name': 'USB设备无法安装',
        'description': 'USB设备无法安装',
        'category': 'USB',
        'severity': 'error',
        'fields': ['DeviceId', 'ErrorCode']
    },
    
    # 证书事件
    '11': {
        'name': '证书服务挂起的请求',
        'description': '证书服务收到挂起的证书请求',
        'category': '证书',
        'severity': 'info',
        'fields': ['RequestId']
    },
    '13': {
        'name': '证书已颁发',
        'description': '证书服务已颁发证书',
        'category': '证书',
        'severity': 'info',
        'fields': ['RequestId', 'SerialNumber']
    },
    '30': {
        'name': '证书服务已启动',
        'description': '证书服务已启动',
        'category': '证书',
        'severity': 'info',
        'fields': []
    },
    '31': {
        'name': '证书服务已停止',
        'description': '证书服务已停止',
        'category': '证书',
        'severity': 'warning',
        'fields': []
    },
    
    # Windows Backup备份
    '4': {
        'name': 'Windows备份已完成',
        'description': 'Windows备份已成功完成',
        'category': '备份',
        'severity': 'info',
        'fields': ['BackupTime', 'BackupLocation']
    },
    '517': {
        'name': 'Windows备份失败',
        'description': 'Windows备份失败',
        'category': '备份',
        'severity': 'error',
        'fields': ['ErrorCode']
    },
    
    # VSS卷影复制
    '8194': {
        'name': 'VSS卷影复制失败',
        'description': '卷影复制服务失败',
        'category': 'VSS',
        'severity': 'error',
        'fields': ['VolumeName', 'ErrorCode']
    },
    '8224': {
        'name': 'VSS卷影复制成功',
        'description': '卷影复制成功创建',
        'category': 'VSS',
        'severity': 'info',
        'fields': ['VolumeName', 'ShadowCopyId']
    },
    
    # BitLocker
    '24576': {
        'name': 'BitLocker加密已启动',
        'description': 'BitLocker加密已启动',
        'category': 'BitLocker',
        'severity': 'info',
        'fields': ['VolumeName']
    },
    '24577': {
        'name': 'BitLocker加密已完成',
        'description': 'BitLocker加密已完成',
        'category': 'BitLocker',
        'severity': 'info',
        'fields': ['VolumeName']
    },
    '24579': {
        'name': 'BitLocker解密已启动',
        'description': 'BitLocker解密已启动',
        'category': 'BitLocker',
        'severity': 'warning',
        'fields': ['VolumeName']
    },
    '24580': {
        'name': 'BitLocker解密已完成',
        'description': 'BitLocker解密已完成',
        'category': 'BitLocker',
        'severity': 'warning',
        'fields': ['VolumeName']
    },
    
    # 7016补充描述
    '7016': {
        'name': '无法启动设备驱动程序',
        'description': '无法启动引导驱动程序或系统启动驱动程序',
        'category': '系统',
        'severity': 'error',
        'fields': ['ImagePath', 'ServiceName', 'ErrorCode']
    },
    '1060': {
        'name': '服务无法通过当前配置的密码启动',
        'description': '服务无法使用当前配置的密码登录',
        'category': '服务',
        'severity': 'error',
        'fields': ['ServiceName']
    },
}

# Application Events
APPLICATION_EVENTS = {
    # Windows错误报告
    '1000': {
        'name': '应用程序错误',
        'description': '应用程序发生错误',
        'category': '应用程序',
        'severity': 'error',
        'fields': ['ApplicationName', 'ApplicationVersion', 'FaultingModule', 'ExceptionCode']
    },
    '1001': {
        'name': 'Windows错误报告',
        'description': 'Windows错误报告',
        'category': '应用程序',
        'severity': 'error',
        'fields': ['BucketId', 'EventName', 'ApplicationName']
    },
    
    # .NET Framework事件
    '1026': {
        'name': '.NET运行时错误',
        'description': '.NET Framework运行时错误',
        'category': '应用程序',
        'severity': 'error',
        'fields': ['ApplicationName', 'ExceptionType', 'ExceptionMessage']
    },
    
    # MSI安装程序事件
    '1033': {
        'name': 'MSI安装成功',
        'description': 'Windows Installer安装成功',
        'category': '安装',
        'severity': 'info',
        'fields': ['ProductName', 'ProductVersion', 'User']
    },
    '1034': {
        'name': 'MSI卸载成功',
        'description': 'Windows Installer卸载成功',
        'category': '安装',
        'severity': 'info',
        'fields': ['ProductName', 'ProductVersion', 'User']
    },
}

# 合并所有事件数据库
ALL_EVENTS = {
    **SECURITY_EVENTS,
    **SYSTEM_EVENTS,
    **APPLICATION_EVENTS
}

def get_event_info(event_id: str) -> dict:
    """
    获取事件信息
    
    Args:
        event_id: 事件ID
        
    Returns:
        dict: 事件信息
    """
    if event_id in ALL_EVENTS:
        return ALL_EVENTS[event_id]
    
    return {
        'name': f'事件 {event_id}',
        'description': '未知事件类型',
        'category': '其他',
        'severity': 'info',
        'fields': []
    }

def get_events_by_category(category: str) -> dict:
    """
    按类别获取事件
    
    Args:
        category: 类别名称
        
    Returns:
        dict: 该类别的所有事件
    """
    return {
        event_id: event_info 
        for event_id, event_info in ALL_EVENTS.items() 
        if event_info['category'] == category
    }

def search_events(keyword: str) -> dict:
    """
    搜索事件
    
    Args:
        keyword: 搜索关键词
        
    Returns:
        dict: 匹配的事件
    """
    keyword_lower = keyword.lower()
    return {
        event_id: event_info 
        for event_id, event_info in ALL_EVENTS.items() 
        if (keyword_lower in event_info['name'].lower() or 
            keyword_lower in event_info['description'].lower() or
            keyword_lower in event_info['category'].lower())
    }

def get_all_categories() -> list:
    """获取所有事件类别"""
    categories = set()
    for event_info in ALL_EVENTS.values():
        categories.add(event_info['category'])
    return sorted(list(categories))

def get_statistics() -> dict:
    """获取事件数据库统计信息"""
    categories = {}
    for event_info in ALL_EVENTS.values():
        category = event_info['category']
        if category not in categories:
            categories[category] = 0
        categories[category] += 1
    
    return {
        'total_events': len(ALL_EVENTS),
        'categories': categories,
        'category_count': len(categories)
    }

# 导出常用函数
__all__ = [
    'get_event_info',
    'get_events_by_category', 
    'search_events',
    'get_all_categories',
    'get_statistics',
    'ALL_EVENTS',
    'SECURITY_EVENTS',
    'SYSTEM_EVENTS', 
    'RDP_EVENTS',
    'APPLICATION_EVENTS'
]
