# PTReport v2 - 渗透测试报告生成器 / Penetration Testing Report Generator

[![版本/Version](https://img.shields.io/badge/version-v2.0-blue)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://www.python.org)
[![许可证/License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

---

## 1. 项目介绍 / Project Introduction

### PTReport 是什么 / What is PTReport

PTReport 是一款专业的**渗透测试报告自动生成工具**，旨在帮助安全工程师、网络安全学员和 CTF 玩家快速生成规范、专业的渗透测试报告。

> PTReport is a professional **penetration testing report generation tool** designed to help security engineers, cybersecurity students, and CTF players quickly generate standardized and professional penetration testing reports.

### 核心功能 / Core Features

| 功能 Feature | 描述 Description |
|-------------|-----------------|
| 自动化扫描 Automated Scanning | 低压自动化扫描目标，发现潜在漏洞 |
| 漏洞模板 Vulnerability Templates | 24+ 漏洞模板，覆盖 Web/系统/网络/信息/认证/配置 |
| 双语报告 Bilingual Reports | 支持中文/English 报告输出 |
| 工具检测 Tool Detection | 自动检测安装的安全工具 |

### 适用人群 / Target Users

- 🔐 安全工程师 / Security Engineers
- 🎓 网络安全学员 / Cybersecurity Students
- 🏆 CTF 玩家 / CTF Players
- 🛡️ 渗透测试新手 / Penetration Testing Beginners

---

## 2. 功能特点 / Features

### 24+ 漏洞模板 / 24+ Vulnerability Templates

| 类别 Category | 漏洞数量 Count | 示例 Examples |
|---------------|---------------|---------------|
| Web应用 Web Application | 8+ | SQL注入、XSS、CSRF、SSRF、SSTI、XXE |
| 系统漏洞 System | 5+ | 缓冲区溢出、权限提升、本地文件包含 |
| 网络漏洞 Network | 4+ | 中间人攻击、DNS劫持 |
| 信息泄露 Information Disclosure | 4+ | 敏感文件泄露、调试信息泄露 |
| 认证授权 Authentication & Authorization | 4+ | 弱口令、暴力破解、越权访问 |
| 配置缺陷 Configuration Issues | 3+ | 默认凭据、安全头缺失 |

### 多语言支持 / Multi-language Support

```
支持语言: 中文 (zh) / English (en)
切换方式: py ptr.py --lang zh  或  py ptr.py --lang en
```

### 自动化特性 / Automation Features

- ✅ 低压自动化扫描 (Low-pressure Automated Scanning)
- ✅ 工具检测与提示安装 (Tool Detection & Installation Hints)
- ✅ 可回退交互向导 (Interactive Wizard with Back Navigation)
- ✅ 授权报告 vs 模板报告 (Authorized Report vs Template Report)

---

## 3. 安装 / Installation

### 环境要求 / Requirements

| 要求 Requirement | 说明 Description |
|-----------------|-----------------|
| Python | 3.8 或更高版本 / 3.8 or higher |
| 操作系统 OS | Windows / Linux / macOS |

### 安装步骤 / Installation Steps

#### 方式一：完整安装 / Method 1: Full Installation

```bash
cd C:/Users/Lenovo/Desktop/PTReport
pip install -r requirements.txt
```

#### 方式二：独立安装 / Method 2: Individual Installation

```bash
pip install pyyaml jinja2
```

#### 方式三：清华镜像（推荐国内用户）/ Method 3: Tsinghua Mirror (Recommended for China)

```bash
pip install pyyaml jinja2 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 验证安装 / Verify Installation

```bash
python ptr.py --version
# 或 / or
python ptr.py --help
```

---

## 4. 快速开始 / Quick Start

### 前置依赖 / Prerequisites

| 工具 Tool | 功能 Function | 安装命令 Install | 备注 Note |
|----------|--------------|-----------------|-----------|
| **Pandoc** | PDF导出 / PDF Export | `winget install pandoc` | 可选，推荐安装 |
| Nmap | 端口扫描 | `choco install nmap` | 建议安装 |
| Nikto | Web漏洞扫描 | `choco install nikto` | 建议安装 |
| SQLMap | SQL注入检测 | `choco install sqlmap` | 建议安装 |
| WhatWeb | Web技术识别 | 手动安装 | 可选 |
| DIRB | Web目录扫描 | 手动安装 | 可选 |

> ⚠️ **注意**：Pandoc 为**可选依赖**，用于将 Markdown 报告转换为 PDF。不安装则只生成 .md 文件。

### 交互模式（推荐新手）/ Interactive Mode (Recommended for Beginners)

```bash
# 启动交互式向导
python ptr.py --interactive
# 简写 / Shortcut
python ptr.py -i
```

### 生成模板报告 / Generate Template Report

```bash
python ptr.py --template
# 简写 / Shortcut
python ptr.py -t
```

### 查看工具状态 / Check Tool Status

```bash
python ptr.py --config
# 简写 / Shortcut
python ptr.py -c
```

### 列出漏洞模板 / List Vulnerability Templates

```bash
python ptr.py --list
# 简写 / Shortcut
python ptr.py -l
```

### 扫描目标 / Scan Target

```bash
python ptr.py --scan TARGET
# 简写 / Shortcut
python ptr.py -s TARGET
```

---

## 5. 使用流程 / Usage Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    PTReport 使用流程                          │
│                 PTReport Usage Flow                          │
└─────────────────────────────────────────────────────────────┘

Step 1: 输入项目信息 / Enter Project Information
        - 项目名称 / Project Name
        - 目标资产 / Target Assets
        - 测试范围 / Scope
        - 测试工程师 / Engineer Name

Step 2: 选择授权状态 / Select Authorization Status
        ├─ 有授权 → 生成正式渗透测试报告
        └─ 无授权 → 生成漏洞模板报告

Step 3: 选择扫描模式 / Select Scan Mode
        ├─ Yes → 执行自动化低压扫描
        └─ No  → 直接生成模板报告

Step 4: 确认扫描结果 / Confirm Scan Results
        - 查看发现的漏洞
        - Review discovered vulnerabilities
        - 可回退修改 / Can go back to modify

Step 5: 生成报告 / Generate Report
        - 选择语言 / Select language
        - 输出格式 / Output format
        - 保存位置 / Save location
```

### 交互示例 / Interactive Example

```bash
$ python ptr.py --interactive --lang en

============================================================
  PTReport - Penetration Test Report Generator
  Version 2.1
============================================================
  Welcome to PTReport...

============================================================
  Step 1/7 - Project Information
============================================================
  Project Name [Penetration Test Project]: My Project
  Target Asset (Domain or IP) [example.com]: target.com
  Test Scope [All ports]: 1-1000
  Engineer Name [Security Engineer]: John

============================================================
  Step 2/7 - Authorization Status
============================================================
  Authorized or Not Authorized...

============================================================
  Step 3/7 - Enable automated scanning
============================================================
  Enable automated scanning (yes/no): yes

============================================================
  Step 4/7 - Scanning...
============================================================
  Running nmap...
  Running nikto...

============================================================
  Step 5/7 - Review Scan Results
============================================================
  Found 3 vulnerabilities
  Include "SQL Injection" in report (yes/no): yes
  Include "XSS" in report (yes/no): no
  ...

============================================================
  Step 6/7 - Generating Report
============================================================
  Report generated successfully!
  File: output\渗透测试报告_My_Project_20260522.md
  ========================================
  Export as PDF (yes/no): yes    ← 自动检测pandoc，未安装则询问安装
  PDF report generated: output\渗透测试报告_My_Project_20260522.pdf
  Open report now (yes/no): yes

============================================================
  Step 7/7 - Continue
============================================================
  Generate another report (yes/no): no
```

---

## 6. 命令详解 / Command Reference

| 命令 Command | 简写 Shortcut | 说明 Description |
|-------------|--------------|-----------------|
| `--interactive` | `-i` | 启动交互式向导 / Start interactive wizard |
| `--scan TARGET` | `-s TARGET` | 扫描指定目标 / Scan specified target |
| `--template` | `-t` | 生成漏洞模板 / Generate vulnerability template |
| `--list` | `-l` | 列出所有漏洞模板 / List all vulnerability templates |
| `--config` | `-c` | 显示工具状态 / Show tool status |
| `--lang zh\|en` | - | 设置界面语言 / Set interface language |
| `--help` | `-h` | 显示帮助信息 / Show help information |
| `--version` | `-v` | 显示版本信息 / Show version information |

### 完整命令示例 / Complete Command Examples

```bash
# 交互模式
python ptr.py --interactive
python ptr.py -i

# 扫描目标
python ptr.py --scan example.com
python ptr.py -s example.com

# 生成模板
python ptr.py --template

# 列出模板
python ptr.py --list

# 查看工具配置
python ptr.py --config

# 设置语言
python ptr.py --lang en
python ptr.py --lang zh

# 组合使用
python ptr.py -i --lang en
python ptr.py -s example.com --lang zh
```

---

## 7. 漏洞模板 / Vulnerability Templates

### Web应用漏洞 / Web Application Vulnerabilities

| 编号 ID | 漏洞名称 (中/English) | 风险等级 Risk | CVSS |
|--------|----------------------|--------------|------|
| 1 | SQL注入 / SQL Injection | 高危 Critical | 9.8 |
| 2 | XSS跨站脚本 / Cross-Site Scripting | 中危 Medium | 7.3 |
| 3 | CSRF跨站请求伪造 / CSRF | 中危 Medium | 6.5 |
| 4 | 文件上传漏洞 / File Upload | 高危 Critical | 8.1 |
| 5 | SSRF服务器端请求伪造 / Server-Side Request Forgery | 高危 Critical | 8.6 |
| 6 | SSTI服务器端模板注入 / Server-Side Template Injection | 高危 Critical | 9.8 |
| 7 | XXE XML外部实体注入 / XML External Entity Injection | 高危 Critical | 9.1 |
| 8 | 命令注入 / Command Injection | 高危 Critical | 9.8 |

### 系统漏洞 / System Vulnerabilities

| 编号 ID | 漏洞名称 (中/English) | 风险等级 Risk | CVSS |
|--------|----------------------|--------------|------|
| 9 | 缓冲区溢出 / Buffer Overflow | 高危 Critical | 9.0 |
| 10 | 权限提升 / Privilege Escalation | 高危 Critical | 8.2 |
| 11 | 本地文件包含 / Local File Inclusion | 高危 High | 7.8 |
| 12 | 远程代码执行 / Remote Code Execution | 严重 Critical | 10.0 |
| 13 | 整数溢出 / Integer Overflow | 中危 Medium | 6.5 |

### 网络漏洞 / Network Vulnerabilities

| 编号 ID | 漏洞名称 (中/English) | 风险等级 Risk | CVSS |
|--------|----------------------|--------------|------|
| 14 | 中间人攻击 / Man-in-the-Middle | 高危 High | 7.6 |
| 15 | DNS劫持 / DNS Hijacking | 高危 High | 8.1 |
| 16 | ARP欺骗 / ARP Spoofing | 中危 Medium | 6.5 |
| 17 | 网络钓鱼 / Phishing | 中危 Medium | 6.5 |

### 信息泄露 / Information Disclosure

| 编号 ID | 漏洞名称 (中/English) | 风险等级 Risk | CVSS |
|--------|----------------------|--------------|------|
| 18 | 敏感文件泄露 / Sensitive File Disclosure | 中危 Medium | 5.3 |
| 19 | 调试信息泄露 / Debug Information Disclosure | 低危 Low | 4.0 |
| 20 | 路径遍历 / Path Traversal | 高危 High | 7.5 |
| 21 | 源码泄露 / Source Code Disclosure | 高危 High | 7.5 |

### 认证授权 / Authentication & Authorization

| 编号 ID | 漏洞名称 (中/English) | 风险等级 Risk | CVSS |
|--------|----------------------|--------------|------|
| 22 | 弱口令 / Weak Password | 高危 Critical | 8.1 |
| 23 | 暴力破解 / Brute Force | 中危 Medium | 7.5 |
| 24 | 越权访问 / Unauthorized Access | 高危 High | 7.5 |
| 25 | 身份认证绕过 / Authentication Bypass | 高危 Critical | 8.0 |

### 配置缺陷 / Configuration Issues

| 编号 ID | 漏洞名称 (中/English) | 风险等级 Risk | CVSS |
|--------|----------------------|--------------|------|
| 26 | 默认凭据 / Default Credentials | 高危 High | 8.0 |
| 27 | 安全头缺失 / Missing Security Headers | 低危 Low | 3.0 |
| 28 | CORS配置错误 / CORS Misconfiguration | 中危 Medium | 6.5 |

---

## 8. 工具支持 / Tool Support

PTReport 支持以下安全工具的自动检测和使用：

### 已支持工具 / Supported Tools

| 工具 Tool | 功能 Function | 命令 Command | Windows安装 Windows Install |
|----------|--------------|--------------|---------------------------|
| **Nmap** | 端口扫描 / Port Scanning | `nmap -sV -sC TARGET` | `choco install nmap` |
| **Nikto** | Web漏洞扫描 / Web Vulnerability Scanning | `nikto -h TARGET` | `choco install nikto` |
| **SQLMap** | SQL注入检测 / SQL Injection Detection | `sqlmap -u TARGET` | `choco install sqlmap` |

### 工具检测 / Tool Detection

```bash
$ python ptr.py --config

🔧 PTReport 工具状态 / Tool Status
============================================================

✅ Nmap   - 已安装 / Installed (v7.92)
✅ Nikto  - 已安装 / Installed (v2.5.0)
✅ SQLMap - 已安装 / Installed (v1.7)

❌ DirB   - 未安装 / Not installed
   安装命令 / Install: choco install dirb

❌ OWASP ZAP - 未安装 / Not installed
   安装命令 / Install: choco install zaproxy
```

### 陆续支持 / Coming Soon

- DirB - 目录扫描 / Directory Scanning
- OWASP ZAP - Web安全扫描 / Web Security Scanning
- Burp Suite - Web代理测试 / Web Proxy Testing
- Metasploit - 渗透测试框架 / Penetration Testing Framework

---

## 9. 报告示例 / Report Example

### 报告结构 / Report Structure

```
📄 渗透测试报告封面
   Cover Page

├── 授权书 / Authorization Letter
├── 项目概述 / Project Overview
│   ├── 项目基本信息 / Basic Information
│   ├── 测试范围 / Scope of Testing
│   └── 测试目标 / Testing Objectives
├── 信息收集 / Information Gathering
│   ├── 端口扫描结果 / Port Scan Results
│   ├── 子域名枚举 / Subdomain Enumeration
│   └── 技术栈识别 / Technology Stack Identification
├── 漏洞发现 / Vulnerability Findings
│   ├── 漏洞1: SQL注入 / SQL Injection
│   ├── 漏洞2: XSS跨站脚本 / Cross-Site Scripting
│   └── 漏洞3: 敏感信息泄露 / Information Disclosure
├── 风险汇总 / Risk Summary
│   ├── CVSS评分统计 / CVSS Score Statistics
│   └── 风险分布图 / Risk Distribution
├── 修复建议 / Remediation Recommendations
│   ├── 高危漏洞修复 / Critical Fixes
│   ├── 中危漏洞修复 / Medium Fixes
│   └── 低危漏洞修复 / Low Fixes
├── 结论 / Conclusion
└── 附录 / Appendix
    ├── 测试方法 / Testing Methods
    ├── 参考标准 / Reference Standards
    └── 术语表 / Glossary
```

### 报告示例片段 / Report Sample

```markdown
# 渗透测试报告

## 项目信息

| 项目名称 | 企业安全评估项目 |
|---------|----------------|
| 目标资产 | example.com |
| 测试范围 | 全部端口 |
| 测试时间 | 2026-05-22 |
| 测试工程师 | 张三 |

## 漏洞发现

### 1. SQL注入漏洞

**风险等级**: 高危 / CVSS: 9.8

**漏洞描述**:
目标站点存在SQL注入漏洞，攻击者可通过构造恶意SQL语句获取数据库敏感信息。

**检测方法**:
使用SQLMap工具进行检测，确认参数id存在SQL注入。

**Payload**:
```sql
' OR '1'='1
```

**修复建议**:
1. 使用参数化查询
2. 实施输入验证
3. 限制数据库权限
```

---

## 10. 常见问题 / FAQ

### Q1: 提示 "No module named 'yaml'" / "No module named 'yaml'"

**问题 / Problem**:
运行时提示缺少 yaml 模块

**解决方案 / Solution**:
```bash
pip install pyyaml jinja2
```

或使用清华镜像（国内推荐）/ Or use Tsinghua mirror (Recommended for China):
```bash
pip install pyyaml jinja2 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

### Q2: 工具检测不到 / Tool Not Detected

**问题 / Problem**:
提示工具未安装或无法找到

**解决方案 / Solution**:

**Windows 用户 / Windows Users**:
```bash
# 使用 Chocolatey 安装 / Install using Chocolatey
choco install nmap
choco install nikto
choco install sqlmap

# 或手动添加到 PATH / Or manually add to PATH
```

**Linux 用户 / Linux Users**:
```bash
# Ubuntu/Debian
sudo apt-get install nmap nikto sqlmap

# CentOS/RHEL
sudo yum install nmap nikto sqlmap
```

**Mac 用户 / Mac Users**:
```bash
brew install nmap nikto sqlmap
```

---

### Q3: 生成报告乱码 / Report Shows Garbled Characters

**问题 / Problem**:
打开生成的报告出现乱码

**解决方案 / Solution**:
1. 使用 VSCode 打开，选择 **UTF-8** 编码
2. 使用 Typora 打开，默认支持 UTF-8
3. 使用 Notepad++ 打开，编码 → 转换为 UTF-8

---

### Q4: 交互模式无法回退 / Cannot Go Back in Interactive Mode

**问题 / Problem**:
在交互模式中输入错误后无法返回上一步

**解决方案 / Solution**:
按 `q` 或 `Ctrl+C` 退出程序，重新运行交互模式：
```bash
python ptr.py --interactive
```

---

### Q5: 扫描超时 / Scan Timeout

**问题 / Problem**:
扫描时间过长或超时

**解决方案 / Solution**:
1. 减少扫描范围，使用 `--ports` 指定端口
2. 使用 `--template` 直接生成模板报告
3. 检查网络连接状态

---

## 11. 更新日志 / Changelog

### v2.0 (2026-05-22) - 当前版本 / Current Version

```
🆕 新增多语言支持 / Added multi-language support (中文/English)
🆕 新增自动化低压扫描 / Added automated low-pressure scanning
🆕 新增工具检测功能 / Added tool detection
🆕 新增可回退交互向导 / Added interactive wizard with back navigation
🆕 新增授权/模板双模式 / Added authorized/template dual mode
🆕 漏洞模板扩展至28个 / Expanded to 28 vulnerability templates
🆕 新增报告预览功能 / Added report preview
🆕 优化报告格式和样式 / Optimized report format and styling
```

### v1.0 (2026-05-21) - 初始版本 / Initial Version

```
✨ 初始版本发布 / Initial release
✨ 12个漏洞模板 / 12 vulnerability templates
✨ 交互式/命令行双模式 / Interactive and command-line modes
✨ Markdown报告生成 / Markdown report generation
✨ 基础信息收集功能 / Basic information gathering
```

---

## 12. 许可 / License

```
MIT License

Copyright (c) 2026 PTReport

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 联系方式 / Contact

- **作者 / Author**: 学徒 (Apprentice)
- **领域 / Field**: 网络安全学习者 / Cybersecurity Learner
- **项目地址 / Project**: [GitHub Repository]

---

<div align="center">

**使用 PTReport，让渗透测试报告更专业！**

**Use PTReport, Make Penetration Testing Reports Professional!**

</div>
