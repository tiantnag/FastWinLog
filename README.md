
# FastWinLog - 轻量级Windows 事件日志分析工具

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg )
![Python](https://img.shields.io/badge/python-3.12+-green.svg )
![React](https://img.shields.io/badge/react-18.2-61dafb.svg )
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg )

**智能解析 · AI 辅助 · 上下文知识库 · 安全告警分析 · 深度统计**

[WEB日志分析工具链接](https://github.com/vam876/FastWLAT) | [Linux日志分析工具链接](https://github.com/vam876/FastLinLog)

</div>

- **最新版本**: 1.0.0
- **更新日期**: 2025/12/18
- **下载地址**:  [https://github.com/vam876/FastWinLog/releases/tag/v1.0.0](https://github.com/vam876/FastWinLog/releases/tag/v1.0.0)

---

## 功能特性
<img width="1613" height="1008" alt="image" src="https://github.com/user-attachments/assets/3cb39203-838f-4415-9a4d-3f5113477d26" />

### 软件架构

#### 技术栈

**前端**
- React 18 + TypeScript
- Vite 5.0 (构建工具)
- CSS Modules (样式隔离)
  
**后端**
- Python 3.12
- WebView (桌面容器)
- libevtx-python (EVTX 解析)
- SQLite (缓存数据库)
<img width="1510" height="822" alt="image" src="https://github.com/user-attachments/assets/c44d416e-902e-4587-a73e-694890a3a97e" />

### 运行逻辑

<img width="1683" height="550" alt="image" src="https://github.com/user-attachments/assets/f4811ac5-4afe-40f6-b3f1-2800c3eb3933" />


### 核心功能

#### 1. 智能日志解析
- **全格式支持**: Security、System、Application、PowerShell 等日志，后续版本将支持logs目录下的所有 Windows 事件日志
- **自动识别**: 基于 Channel 字段智能识别日志类型
- **深度解析**: 提取 100+ 字段，包括嵌套字段和键值对格式
- **高性能缓存**: SQLite 缓存机制，支持百万级事件加载
- **增量更新**: 智能缓存管理，避免重复解析
<img width="1613" height="1008" alt="image" src="https://github.com/user-attachments/assets/f8ecad15-f468-4f62-80ed-347103f8b343" />

#### 2. 全文搜索引擎
- **关键词搜索**: 支持全字段模糊匹配
- **高级搜索**: 多条件组合过滤（EventID、Level、Computer、时间范围等）
- **实时搜索**: 基于 SQLite FTS5 全文索引，秒级响应
- **搜索历史**: 自动保存搜索记录
- **结果高亮**: 关键词高亮显示

#### 3. 智能告警系统
- **内置规则库**: 
  - 57+ 条 Security 安全规则
  - 31+ 条 PowerShell 脚本规则
  - 31+ 条 System 系统规则
  - 15+ 条 Application 应用规则
- **自定义规则**: 
  - 匹配规则（单条件/多条件/逻辑组合）
  - 阈值规则（时间窗口 + 分组聚合）
  - 严重级别（Critical/High/Medium/Low/Info）
- **规则管理**:
  - JSON 格式导入导出
  - 规则启用/禁用
  - 规则编辑和删除
  - 批量操作
- **实时扫描**: 
  - 智能过滤，只返回匹配事件
  - 进度跟踪
  - 扫描历史记录

#### 4. AI 智能分析
<img width="1683" height="527" alt="image" src="https://github.com/user-attachments/assets/dabf4248-53d6-494e-b339-e70758ef2ac2" />

- **AI 对话助手**: 
  - 浮动 AI 面板，随时咨询
  - 流式输出，实时响应
  - 支持 OpenAI、Ollama、自定义 API
  - 支持一条或多条日志聚合分析
    
- **智能日志分析**:
  - 自动分析选中的日志事件
  - 识别安全威胁和异常行为
  - 提供修复建议和最佳实践
- **上下文工程**:
  - 知识库管理（添加/编辑/删除）
  - 自动从日志创建知识条目
  - 知识库启用/禁用控制
  - 上下文长度限制（避免 token 超限）
- **AI 配置**:
  - 支持多种 AI 模型（GPT-4、GPT-3.5、Claude 等）
  - 自定义 API 端点
  - Temperature 和 Max Tokens 调节
  - API Key 安全存储

#### 5. 可视化统计分析
- **登录分析**:
  - 成功/失败登录趋势图
  - Top IP 地址排行
  - Top 用户排行
  - 登录类型分布
  - 时间线分析（按小时/天/周）
- **进程监控**:
  - 进程创建趋势
  - 可疑进程检测
  - 进程命令行分析
  - 父子进程关系
- **账户管理**:
  - 用户创建/删除/修改统计
  - 组成员变更追踪
  - 权限提升检测
- **应用分析**:
  - 应用崩溃统计
  - 错误类型分布
  - 崩溃趋势分析
- **系统健康**:
  - 服务状态监控
  - 系统事件统计
  - 错误/警告分布

#### 6. 数据导出功能
- **CSV 导出**: 
  - 导出全部数据
  - 导出搜索结果
  - 导出高级搜索结果
  - 自定义字段选择
- **JSON 导出**: 完整事件数据导出
- **告警规则导出**: JSON 格式，方便团队共享

#### 7. 高级特性
- **字段元数据**: 100+ 字段的中文描述和说明
- **事件描述库**: 1000+ 事件 ID 的详细说明
- **内存管理**: 智能内存释放，支持大文件分析
- **进度追踪**: 实时显示解析/扫描进度
- **错误处理**: 完善的错误提示和恢复机制
- **列设置**: 自定义显示列，保存用户偏好

### 未来规划


#### 扩展支持（规划中）
- **所有 Windows 日志**: 支持所有 Windows 事件日志类型
- **Sysmon 日志**: 深度集成 Sysmon 高级监控

---

## AI 功能

### AI 对话助手

#### 1. 启用 AI 功能
```
设置 → AI 设置 → 配置 API
```

支持的 AI 服务：
- OpenAI (GPT-4, GPT-3.5-turbo)
- Azure OpenAI
- 自定义 API 端点（兼容 OpenAI 格式）

#### 2. 使用 AI 分析日志
```
选中日志事件 → 点击 AI 按钮 → 自动分析
```

AI 会自动：
- 识别事件类型和严重性
- 分析潜在的安全威胁
- 提供修复建议
- 关联相关事件

#### 3. 知识库管理
```
AI 面板 → 知识库图标 → 管理知识条目
```

功能：
- 添加自定义知识条目
- 从日志创建知识
- 启用/禁用知识库
- 控制上下文长度

### AI 配置示例

```json
{
  "provider": "openai",
  "apiKey": "sk-...",
  "model": "gpt-4",
  "temperature": 0.7,
  "maxTokens": 2000
}
```



---



<div align="center">

**如果这个项目对你有帮助，请给个 Star！**

Made with ❤️ by FastWinLog Team

</div>
