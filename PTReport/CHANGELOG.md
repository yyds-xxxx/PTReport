# PTReport 更新日志 / CHANGELOG

---

## AI/AGENT 维护规则（针对 AI/Agent）

**规则 / Rule**: 当 AI 或 Agent 对本项目进行了任何代码修改、功能增减、bug修复等任何变更时，执行以下步骤：

1. **立即在本文件顶部插入新条目**，格式如下：
2. **引用本次修改的所有文件路径和关键改动点**
3. **保持时间戳在最新**

---

## 2026-05-22 - v2.1 更新

### 新增功能 / New Features

| 功能 | 文件 | 说明 |
|------|------|------|
| PDF导出 | `ptr.py` | Markdown生成后询问是否导出PDF，自动检测pandoc并可自动安装 |
| 详细字段 | `report_builder.py` | 漏洞输出改为表格，新增CVSS评分、漏洞类别、Payload、修复建议、参考资料 |
| 英文界面 | `i18n.py` | 中英文界面切换，`--lang en` 参数 |

### 改动点 / Changes

**`report_builder.py`**
- `_format_vulnerability_zh()` - 中英文漏洞输出改为表格格式
- `_format_vulnerability_en()` - 同上
- 新增字段：CVSS评分、漏洞类别、漏洞Payload（如果有）、修复建议、参考资料

**`ptr.py`**
- PDF导出流程：生成MD后询问 `是否导出PDF格式 (yes/no)`
- pandoc未安装时询问是否自动安装（`winget install pandoc`）
- 安装后自动执行转换

**`i18n.py`**
- 新增 `export_pdf`, `pdf_generated`, `pdf_skipped`, `pdf_error`, `install_now` 翻译键

---

## 2026-05-21 - v2.0 更新

### 新增功能 / New Features

| 功能 | 文件 | 说明 |
|------|------|------|
| 双语支持 | `i18n.py` | 中英文界面独立字符串字典 |
| 工具检测 | `tools/checker.py` | 自动检测nmap/nikto/sqlmap/whatweb/dirb |
| 漏洞模板 | `vuln_templates.py` | 24+漏洞模板，覆盖6大类别 |
| 报告生成器 | `report_builder.py` | Markdown格式渗透测试报告 |
| 交互向导 | `ptr.py` | 7步骤交互式报告生成流程 |

### 改动点 / Changes

**`ptr.py`**
- 重写为主程序，7步骤交互流程
- argparse命令行参数：`--interactive`, `--scan`, `--template`, `--list`, `--config`, `--lang`

**`tools/checker.py`**
- 新增whatweb和dirb检测支持
- ToolChecker类封装

---

## 2026-05-20 - v1.0 初始版本

### 初始功能 / Initial Features

- 基础端口扫描（nmap）
- 基础Nikto扫描
- 基础SQLMap检测
- 简单Markdown报告输出