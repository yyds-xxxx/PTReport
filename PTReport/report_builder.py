#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PTReport report_builder.py - Bilingual penetration test report generator
Supports authorized report and unauthorized template modes
"""

import tempfile
from datetime import datetime
from pathlib import Path


class ReportBuilder:
    """Generate bilingual penetration test reports in Markdown format"""

    def __init__(self, i18n=None, language='zh'):
        self.i18n = i18n
        self.language = language
        self.report_sections = []
        self.authorization_info = None
        self.project_info = None
        self.scan_results = []
        self.templates = {}

    def add_authorization_page(self, project_info, authorized=True):
        """
        Add authorization page section
        authorized=True: Formal authorized report
        authorized=False: Template report with disclaimer
        """
        self.authorization_info = {
            'authorized': authorized,
            'project_info': project_info,
            'generated_at': datetime.now()
        }

        if self.language == 'zh':
            if authorized:
                auth_text = """## 授权书

**项目名称**: {project_name}
**目标资产**: {target}
**测试范围**: {scope}
**测试工程师**: {engineer}
**授权日期**: {date}

---

### 授权声明

本渗透测试项目已获得目标资产所有者的正式授权。测试工程师被授权对上述目标进行安全评估测试，包括但不限于：

- 网络端口和服务识别
- Web应用漏洞检测
- 数据库安全评估
- 社会工程学测试（如适用）

### 免责声明

本报告仅供授权方内部使用，未经书面许可，不得向第三方披露。如因使用本报告造成的任何损失，本报告作者不承担任何责任。

**授权方签字**: ___________________

**日期**: ___________________""".format(
                    project_name=project_info.get('name', 'N/A'),
                    target=project_info.get('target', 'N/A'),
                    scope=project_info.get('scope', 'N/A'),
                    engineer=project_info.get('engineer', 'N/A'),
                    date=project_info.get('date', datetime.now().strftime('%Y-%m-%d'))
                )
            else:
                auth_text = """## 授权书

### 模板声明

**WARNING / 警告**: 此报告为模板版本，不具有任何法律效力。

---

### 免责声明 / DISCLAIMER

本渗透测试报告为模板文档，仅供学习和参考使用。

**重要提示 / IMPORTANT NOTICE**:

1. 本报告不构成任何形式的授权或批准
2. 未经书面授权，不得对任何系统进行渗透测试
3. 未经授权的渗透测试行为可能违反相关法律法规
4. 使用本模板产生的任何后果由使用者自行承担

### 占位信息 / Placeholder Information

- 项目名称 / Project Name: [项目名称]
- 目标资产 / Target: [目标资产]
- 测试范围 / Scope: [测试范围]
- 工程师 / Engineer: [工程师姓名]
- 日期 / Date: [日期]

**授权方签字 / Authorized Signature**: ___________________"""
        else:
            if authorized:
                auth_text = """## Authorization Page

**Project Name**: {project_name}
**Target Asset**: {target}
**Test Scope**: {scope}
**Test Engineer**: {engineer}
**Authorization Date**: {date}

---

### Authorization Statement

This penetration testing project has received formal authorization from the target asset owner. The test engineer is authorized to conduct security assessment testing on the aforementioned target, including but not limited to:

- Network port and service identification
- Web application vulnerability detection
- Database security assessment
- Social engineering testing (if applicable)

### Disclaimer

This report is for internal use by the authorized party only and shall not be disclosed to third parties without written permission. The report's authors assume no liability for any damages arising from the use of this report.

**Authorized Signature**: ___________________

**Date**: ___________________""".format(
                    project_name=project_info.get('name', 'N/A'),
                    target=project_info.get('target', 'N/A'),
                    scope=project_info.get('scope', 'N/A'),
                    engineer=project_info.get('engineer', 'N/A'),
                    date=project_info.get('date', datetime.now().strftime('%Y-%m-%d'))
                )
            else:
                auth_text = """## Authorization Page

### Template Declaration

**WARNING**: This report is a template version and has no legal effect.

---

### Disclaimer

This penetration testing report is a template document for reference and learning purposes only.

**Important Notice**:
1. This report does not constitute any form of authorization or approval
2. Penetration testing on any system without written authorization is prohibited
3. Unauthorized penetration testing may violate applicable laws and regulations
4. Any consequences arising from the use of this template are the sole responsibility of the user

### Placeholder Information

- Project Name: [Project Name]
- Target Asset: [Target]
- Test Scope: [Scope]
- Engineer: [Engineer Name]
- Date: [Date]

**Authorized Signature**: ___________________"""

        self.authorization_info['text'] = auth_text
        return auth_text

    def add_project_info(self, project_info):
        """Add project information section"""
        self.project_info = project_info

        if self.language == 'zh':
            text = """## 项目信息 / Project Information

| 字段 | 内容 |
|------|------|
| 项目名称 | {name} |
| 目标资产 | {target} |
| 测试范围 | {scope} |
| 测试工程师 | {engineer} |
| 报告日期 | {date} |
| 报告版本 | {version} |

### 测试目标

{objectives}

### 测试方法

{methodology}
""".format(
                name=project_info.get('name', 'N/A'),
                target=project_info.get('target', 'N/A'),
                scope=project_info.get('scope', 'N/A'),
                engineer=project_info.get('engineer', 'N/A'),
                date=project_info.get('date', datetime.now().strftime('%Y-%m-%d')),
                version=project_info.get('version', '1.0'),
                objectives=project_info.get('objectives', '识别目标系统中的安全漏洞和风险'),
                methodology=project_info.get('methodology', '自动化扫描结合人工验证')
            )
        else:
            text = """## Project Information

| Field | Content |
|-------|---------|
| Project Name | {name} |
| Target Asset | {target} |
| Test Scope | {scope} |
| Test Engineer | {engineer} |
| Report Date | {date} |
| Report Version | {version} |

### Test Objectives

{objectives}

### Methodology

{methodology}
""".format(
                name=project_info.get('name', 'N/A'),
                target=project_info.get('target', 'N/A'),
                scope=project_info.get('scope', 'N/A'),
                engineer=project_info.get('engineer', 'N/A'),
                date=project_info.get('date', datetime.now().strftime('%Y-%m-%d')),
                version=project_info.get('version', '1.0'),
                objectives=project_info.get('objectives', 'Identify security vulnerabilities and risks in target systems'),
                methodology=project_info.get('methodology', 'Automated scanning combined with manual verification')
            )

        self.project_info['text'] = text
        return text

    def add_scan_results(self, results):
        """Add scan results section with confirmed vulnerabilities"""
        self.scan_results = results

        if not results:
            return self._add_no_findings()

        if self.language == 'zh':
            sections = ["## 扫描结果 / Scan Results\n"]

            # Summary table
            summary = self._get_results_summary(results)
            sections.append("### 执行摘要 / Executive Summary\n")
            sections.append(f"**发现总数**: {summary['total']} | ")
            sections.append(f"**高危**: {summary['high']} | ")
            sections.append(f"**中危**: {summary['medium']} | ")
            sections.append(f"**低危**: {summary['low']} | ")
            sections.append(f"**信息**: {summary['info']}\n\n")

            # Group by severity
            for severity in ['high', 'medium', 'low', 'info']:
                items = [r for r in results if r.get('severity') == severity]
                if items:
                    sections.append(f"### {self._severity_label(severity)} ({len(items)})\n")
                    for item in items:
                        sections.append(self._format_vulnerability_zh(item))
                    sections.append("\n")

        else:
            sections = ["## Scan Results\n"]

            summary = self._get_results_summary(results)
            sections.append("### Executive Summary\n")
            sections.append(f"**Total Found**: {summary['total']} | ")
            sections.append(f"**High**: {summary['high']} | ")
            sections.append(f"**Medium**: {summary['medium']} | ")
            sections.append(f"**Low**: {summary['low']} | ")
            sections.append(f"**Info**: {summary['info']}\n\n")

            for severity in ['high', 'medium', 'low', 'info']:
                items = [r for r in results if r.get('severity') == severity]
                if items:
                    sections.append(f"### {self._severity_label_en(severity)} ({len(items)})\n")
                    for item in items:
                        sections.append(self._format_vulnerability_en(item))
                    sections.append("\n")

        return "".join(sections)

    def _severity_label(self, severity):
        labels = {
            'high': '高危漏洞 / High Severity',
            'medium': '中危漏洞 / Medium Severity',
            'low': '低危漏洞 / Low Severity',
            'info': '信息收集 / Information'
        }
        return labels.get(severity, severity)

    def _severity_label_en(self, severity):
        labels = {
            'high': 'High Severity',
            'medium': 'Medium Severity',
            'low': 'Low Severity',
            'info': 'Information'
        }
        return labels.get(severity, severity)

    def _format_vulnerability_zh(self, item):
        """Format vulnerability in Chinese"""
        tool = item.get('tool', 'unknown')
        title = item.get('title', item.get('name', 'Unknown'))
        desc = item.get('description', '')
        port = item.get('port', '')
        service = item.get('service', '')

        text = f"""#### {title}

| 字段 | 内容 |
|------|------|
| 严重程度 | {item.get('severity', 'info').upper()} |
| CVSS评分 | {item.get('cvss', 'N/A')} |
| 漏洞类别 | {item.get('category', item.get('tool', 'N/A').upper())} |
| 检测工具 | {tool.upper()} |
| 目标 | {item.get('target', 'N/A')} |
"""

        if port:
            text += f"| 端口 | {port}"
            if service:
                text += f" ({service})"
            text += " |\n"

        if desc:
            text += f"| 描述 | {desc} |\n"

        if item.get('cve'):
            text += f"| CVE | {item['cve']} |\n"
        if item.get('payload'):
            text += f"| 漏洞Payload | `{item['payload']}` |\n"
        if item.get('fix') or item.get('solution'):
            text += f"| 修复建议 | {item.get('fix', item.get('solution', 'N/A'))} |\n"
        if item.get('reference_url'):
            text += f"| 参考资料 | {item['reference_url']} |\n"

        text += "\n"
        return text

    def _format_vulnerability_en(self, item):
        """Format vulnerability in English"""
        tool = item.get('tool', 'unknown')
        title = item.get('title', item.get('name', 'Unknown'))
        desc = item.get('description', '')
        port = item.get('port', '')
        service = item.get('service', '')

        text = f"""#### {title}

| Field | Content |
|-------|---------|
| Severity | {item.get('severity', 'info').upper()} |
| CVSS Score | {item.get('cvss', 'N/A')} |
| Category | {item.get('category', item.get('tool', 'N/A').upper())} |
| Tool | {tool.upper()} |
| Target | {item.get('target', 'N/A')} |
"""

        if port:
            text += f"| Port | {port}"
            if service:
                text += f" ({service})"
            text += " |\n"

        if desc:
            text += f"| Description | {desc} |\n"

        if item.get('cve'):
            text += f"| CVE | {item['cve']} |\n"
        if item.get('payload'):
            text += f"| Payload | `{item['payload']}` |\n"
        if item.get('fix') or item.get('solution'):
            text += f"| Recommendation | {item.get('fix', item.get('solution', 'N/A'))} |\n"
        if item.get('reference_url'):
            text += f"| Reference | {item['reference_url']} |\n"

        text += "\n"
        return text

    def _add_no_findings(self):
        """Return no findings section"""
        if self.language == 'zh':
            return """## 扫描结果 / Scan Results

### 执行摘要 / Executive Summary

**发现总数**: 0 | **高危**: 0 | **中危**: 0 | **低危**: 0 | **信息**: 0

### 测试结论

本次扫描未发现明显的安全漏洞。建议继续关注系统安全更新，并定期进行安全评估。

---
"""
        else:
            return """## Scan Results

### Executive Summary

**Total Found**: 0 | **High**: 0 | **Medium**: 0 | **Low**: 0 | **Info**: 0

### Conclusion

No obvious security vulnerabilities were found in this scan. Continue to monitor system security updates and conduct regular security assessments.

---
"""

    def add_template_section(self, templates=None):
        """
        Add template placeholder sections for unauthorized mode
        Generates empty templates that users fill in themselves
        """
        if templates is None:
            templates = ['network', 'web', 'database', 'api', 'social']

        sections = []

        if self.language == 'zh':
            sections.append("## 漏洞模板区域 / Vulnerability Template Area\n")
            sections.append("*以下区域需手动填写，仅供模板参考*\n\n")

            for template in templates:
                sections.append(self._get_template_zh(template))
        else:
            sections.append("## Vulnerability Template Area\n")
            sections.append("*The following sections require manual completion. For reference only.*\n\n")

            for template in templates:
                sections.append(self._get_template_en(template))

        return "".join(sections)

    def _get_template_zh(self, template_type):
        templates = {
            'network': """### 网络漏洞 / Network Vulnerability

> **测试方法**: 使用 nmap -sV -sC TARGET 进行端口扫描，识别版本后搜索已知CVE。对检测到的每个端口服务，使用对应工具进行版本比对。
> **常用工具**: nmap, netcat, metasploit, searchsploit
> **CWE参考**: CWE-200(信息泄露), CWE-310(加密问题), CWE-119(缓冲区溢出)

#### [漏洞名称]

| 字段 | 内容 | 填写指导 |
|------|------|---------|
| CVE ID | CVE-YYYY-XXXXX | 访问 cve.mitre.org 查询 |
| CVSS评分 | X.X (0-10) | 使用 CVSS Calculator v3.1 |
| CVSS向量 | CVSS:3.1/AV:N/AC:L... | 完整向量决定精确评分 |
| 严重程度 | Critical/High/Medium/Low | 根据CVSS分值自动判定 |
| 漏洞类型 | [类型] | 如: 中间人攻击/DNS劫持/ARP欺骗 |
| 目标端口 | [端口] | 如: 80, 443, 22, 3306 |
| 影响服务 | [服务名+版本] | 如: OpenSSH 7.2p1 |
| 描述 | [详细描述] | 漏洞原理、利用条件、影响范围 |
| 发现时间 | YYYY-MM-DD | 发现漏洞的日期 |
| 影响版本 | [受影响版本范围] | 如: openssh < 7.4 |
| 复现步骤 | 1. [命令1]<br>2. [命令2]<br>3. [验证方法] | 使用实际命令，可复制执行 |
| 测试工具 | [工具+版本] | 如: nmap 7.92, metasploit |
| PoC代码 | ```[python/bash/curl命令]``` | 实际可运行的Exploit代码 |
| 修复建议 | [具体修复方案] | 版本升级/配置修改/打补丁 |
| 参考文献 | [CVE链接, CWE链接, 厂商公告] | 至少包含2个以上参考链接 |

**快速检测命令示例:**
```bash
# 端口扫描
nmap -sV -sC -Pn TARGET

# 版本漏洞搜索
searchsploit OpenSSH 7.2
nmap --script vuln TARGET
```

**修复优先级参考:**
- Critical (9.0-10.0): 立即修复，24小时内
- High (7.0-8.9): 紧急修复，72小时内
- Medium (4.0-6.9): 计划修复，一周内
- Low (0.1-3.9): 常规修复，下个维护周期

---
""",
            'web': """### Web应用漏洞 / Web Application Vulnerability

> **测试方法**: 手工测试结合自动化工具( Nikto, SQLMap, BurpSuite )。对每个输入点尝试常见payload，观察响应变化。对比OWASP Top 10 2021分类。
> **常用工具**: burpsuite, sqlmap, nikto, xssstrike, ffuf
> **CWE参考**: CWE-79(XSS), CWE-89(SQLi), CWE-352(CSRF), CWE-22(LFI/RFI)

#### [漏洞名称]

| 字段 | 内容 | 填写指导 |
|------|------|---------|
| CVE ID | CVE-YYYY-XXXXX | 访问 cve.mitre.org 查询 |
| CVSS评分 | X.X (0-10) | 使用 CVSS Calculator v3.1 |
| CVSS向量 | CVSS:3.1/AV:N/AC:L... | 完整向量决定精确评分 |
| 严重程度 | Critical/High/Medium/Low | 根据CVSS分值自动判定 |
| 漏洞类型 | [类型] | 如: SQL注入/XSS/CSRF/SSRF/文件上传 |
| 目标URL | https://target.com/[path] | 完整的受影响URL |
| 影响参数 | [参数名] | 如: id, user, q, search |
| HTTP方法 | GET/POST/PUT/DELETE | 发现漏洞的请求方法 |
| 描述 | [详细描述] | 漏洞原理、利用条件、影响范围 |
| 发现时间 | YYYY-MM-DD | 发现漏洞的日期 |
| 复现步骤 | 1. [构造请求]<br>2. [发送 payload]<br>3. [观察响应] | 请求-响应完整流程 |
| 测试工具 | [工具+版本] | 如: BurpSuite 2022.1, SQLMap 1.7 |
| PoC代码 | ```[实际可运行的Exploit代码]``` | 可直接复制使用的完整请求 |
| 修复建议 | [具体修复方案] | 参数化查询/输入过滤/输出编码 |
| 参考文献 | [CVE, CWE, OWASP, 厂商公告] | 至少包含2个以上参考链接 |

**快速检测命令示例:**
```bash
# SQL注入检测
sqlmap -u "https://target.com/product?id=1" --batch --level=3

# XSS检测
sqlmap -u "https://target.com/search?q=test" --batch

# 目录枚举
ffuf -w wordlist.txt -u https://target.com/FUZZ

# 检测命令注入
curl -s "https://target.com/ping?host=127.0.0.1|ls"
```

**OWASP Top 10 2021 对照:**
| 分类 | 常见漏洞 |
|------|---------|
| A01: Broken Access Control | IDOR, 越权, 水平/垂直越权 |
| A02: Cryptographic Failures | 明文传输, 弱加密, 硬编码密码 |
| A03: Injection | SQLi, XSS, Command Injection, LDAPi |
| A04: Insecure Design | 业务逻辑漏洞, 认证绕过 |
| A05: Security Misconfiguration | 默认凭据, 错误配置, 不安全头 |

---
""",
            'database': """### 数据库漏洞 / Database Vulnerability

> **测试方法**: 使用 sqlmap --batch 进行基础检测，结合手动SQL注入测试。对识别出的数据库进行版本比对，搜索已知CVE。
> **常用工具**: sqlmap, nmap (mysql, mongodb, postgres端口), metasploit
> **CWE参考**: CWE-89(SQL注入), CWE-94(代码注入), CWE-200(信息泄露)

#### [漏洞名称]

| 字段 | 内容 | 填写指导 |
|------|------|---------|
| CVE ID | CVE-YYYY-XXXXX | 访问 cve.mitre.org 查询 |
| CVSS评分 | X.X (0-10) | 使用 CVSS Calculator v3.1 |
| CVSS向量 | CVSS:3.1/AV:N/AC:L... | 完整向量决定精确评分 |
| 严重程度 | Critical/High/Medium/Low | 根据CVSS分值自动判定 |
| 数据库类型 | MySQL/PostgreSQL/MongoDB/Redis/Oracle | 如: MySQL 5.7.29 |
| 影响端口 | [端口] | 默认: MySQL 3306, PostgreSQL 5432, MongoDB 27017, Redis 6379 |
| 漏洞类型 | [类型] | 如: SQL注入/未授权访问/弱口令/默认密码 |
| 描述 | [详细描述] | 漏洞原理、利用条件、影响范围 |
| 发现时间 | YYYY-MM-DD | 发现漏洞的日期 |
| 测试工具 | [工具+版本] | 如: sqlmap 1.7, nmap 7.92 |
| PoC代码 | ```[数据库-specific payload]``` | 数据库类型的实际Exploit |
| 修复建议 | [具体修复方案] | 升级版本/配置访问控制/强密码策略 |
| 参考文献 | [CVE链接, 官方手册, 相关漏洞报告] | 至少包含2个以上参考链接 |

**快速检测命令示例:**
```bash
# MySQL枚举
nmap -sV -p 3306 TARGET
mysql -h TARGET -u root -p

# MongoDB检测
nmap -sV -p 27017 TARGET
mongo TARGET:27017/db --eval "db.version()"

# SQL注入
sqlmap -u "https://target.com/db?id=1" --batch --dbs

# Redis未授权
redis-cli -h TARGET INFO
```

---
""",
            'api': """### API漏洞 / API Vulnerability

> **测试方法**: 使用 BurpSuite 拦截API请求，分析JSON/XML参数。对比OWASP API Security Top 10。使用自动化工具如sqlmap,ffuf进行测试。
> **常用工具**: burpsuite, postman, sqlmap, ffuf, zap
> **CWE参考**: CWE-89(SQLi), CWE-306(认证缺失), CWE-862(授权缺失)

#### [漏洞名称]

| 字段 | 内容 | 填写指导 |
|------|------|---------|
| CVE ID | CVE-YYYY-XXXXX | 访问 cve.mitre.org 查询 |
| CVSS评分 | X.X (0-10) | 使用 CVSS Calculator v3.1 |
| CVSS向量 | CVSS:3.1/AV:N/AC:L... | 完整向量决定精确评分 |
| 严重程度 | Critical/High/Medium/Low | 根据CVSS分值自动判定 |
| API端点 | /api/v1/[endpoint] | 完整的API路径 |
| HTTP方法 | GET/POST/PUT/DELETE/PATCH | 发现漏洞的请求方法 |
| Content-Type | application/json/XML/form-data | 请求的数据格式 |
| 参数位置 | Path/Query/Body/Header | 参数在请求中的位置 |
| 描述 | [详细描述] | 漏洞原理、利用条件、影响范围 |
| 发现时间 | YYYY-MM-DD | 发现漏洞的日期 |
| 测试工具 | [工具+版本] | 如: BurpSuite 2022.1, Postman |
| PoC请求 | ```[完整可执行的HTTP请求]``` | 复制可直接在浏览器/Burp中发送 |
| 修复建议 | [具体修复方案] | 认证/授权/输入验证/速率限制 |
| 参考文献 | [CVE, OWASP API Top 10, 厂商公告] | 至少包含2个以上参考链接 |

**API安全测试清单:**
```
□ 认证端点: /api/auth/login, /api/auth/register
□ 令牌位置: Header (Authorization: Bearer <token>)
□ 速率限制: 测试超过限制是否返回429
□ 暴力破解: 测试多次失败是否锁定账户
□ BOLA: 测试是否可通过其他用户ID访问他人数据
□ SQLi: 测试参数是否被直接拼入SQL
□ XXE: 测试XML payload是否被解析
□ SSRF: 测试是否可访问内网资源
```

---
""",
            'social': """### 社会工程学 / Social Engineering

> **测试方法**: 钓鱼邮件测试( Spear Phishing )、电话诈骗测试( Vishing )、物理渗透( Physical )。收集目标信息使用 OSINT 工具。
> **常用工具**: theHarvester, recon-ng, SET (Social Engineering Toolkit), maltego
> **CWE参考**: CWE-330(弱随机), CWE-312(敏感信息泄露), CWE-601(钓鱼)

#### [漏洞名称]

| 字段 | 内容 | 填写指导 |
|------|------|---------|
| CVE ID | N/A 或钓鱼活动ID | 社会工程通常无CVE，可用自定义ID |
| CVSS评分 | X.X (0-10) | 使用 CVSS Calculator v3.1 |
| CVSS向量 | CVSS:3.1/AV:P/AC:L... | 攻击路径P=Physical |
| 严重程度 | Critical/High/Medium/Low | 根据CVSS分值自动判定 |
| 攻击类型 | [类型] | 如: 钓鱼邮件/电话诈骗/物理入侵/短信诈骗 |
| 目标人员 | [职位/姓名] | 如: HR经理, 财务专员 |
| 攻击向量 | [钓鱼内容形式] | 如: 伪造邮件/虚假电话/伪装身份卡 |
| 描述 | [详细描述] | 攻击手法、目标选择理由、成功率评估 |
| 发现时间 | YYYY-MM-DD | 发现漏洞的日期 |
| 收集的情报 | [通过OSINT收集到的信息] | 邮箱/社交账号/电话/公司信息 |
| 攻击过程 | 1. [收集情报]<br>2. [构造攻击]<br>3. [实施测试]<br>4. [记录结果] | 完整攻击链 |
| 钓鱼Payload | ```[钓鱼邮件原文/钓鱼网站URL]``` | 实际使用的钓鱼内容 |
| 修复建议 | [具体修复方案] | 安全意识培训/邮件验证/门禁系统 |
| 参考文献 | [OSINT工具链接, 钓鱼案例, 培训材料] | 参考资料 |

**OSINT情报收集命令:**
```bash
# 邮箱收集
theHarvester -d target.com -b google

# 子域名枚举
amass enum -passive -d target.com

# LinkedIn搜索
https://www.linkedin.com/search/results/people/?keywords=target.com

# 钓鱼工具
setoolkit
```

**常见钓鱼特征:**
- 发件人域名与官方相似 (例: admin@ta1get.com vs admin@target.com)
- 紧急语气 ("立即行动，否则账户被封")
- 链接悬停显示不一致的目标URL
- 附件名称诱惑性 (如 "薪资调整通知.xlsx.exe")

---
"""
        }
        return templates.get(template_type, templates['network'])

    def _get_template_en(self, template_type):
        templates = {
            'network': """### Network Vulnerability

> **Testing Method**: Use nmap -sV -sC TARGET for port scanning, identify versions, search known CVEs. Compare each detected service version against CVE databases.
> **Tools**: nmap, netcat, metasploit, searchsploit
> **CWE Reference**: CWE-200(Info Disclosure), CWE-310(Crypto Issues), CWE-119(Buffer Overflow)

#### [Vulnerability Name]

| Field | Content | Guidance |
|-------|---------|----------|
| CVE ID | CVE-YYYY-XXXXX | Search at cve.mitre.org |
| CVSS Score | X.X (0-10) | Use CVSS Calculator v3.1 |
| CVSS Vector | CVSS:3.1/AV:N/AC:L... | Complete vector for exact score |
| Severity | Critical/High/Medium/Low | Auto-determined from CVSS |
| Vuln Type | [Type] | e.g.: MITM/DNS Hijacking/ARP Spoofing |
| Target Port | [Port] | e.g.: 80, 443, 22, 3306 |
| Affected Service | [Service+Version] | e.g.: OpenSSH 7.2p1 |
| Description | [Detailed description] | Vuln mechanism, exploitation conditions, impact |
| Date Found | YYYY-MM-DD | Date vulnerability was discovered |
| Affected Versions | [Version range] | e.g.: openssh < 7.4 |
| Reproduction Steps | 1. [Command 1]<br>2. [Command 2]<br>3. [Verification] | Executable commands |
| Testing Tools | [Tool+Version] | e.g.: nmap 7.92, metasploit |
| PoC Code | ```[python/bash/curl command]``` | Runnable Exploit code |
| Recommendation | [Fix method] | Version upgrade/config change/patch |
| References | [CVE link, CWE link, vendor advisory] | At least 2 references |

**Quick Detection Commands:**
```bash
# Port scanning
nmap -sV -sC -Pn TARGET

# Version vuln search
searchsploit OpenSSH 7.2
nmap --script vuln TARGET
```

**Remediation Priority:**
- Critical (9.0-10.0): Immediate, within 24h
- High (7.0-8.9): Urgent, within 72h
- Medium (4.0-6.9): Scheduled, within 1 week
- Low (0.1-3.9): Routine, next maintenance cycle

---
""",
            'web': """### Web Application Vulnerability

> **Testing Method**: Manual testing + automation (Nikto, SQLMap, BurpSuite). Test every input with common payloads, observe response. Map to OWASP Top 10 2021.
> **Tools**: burpsuite, sqlmap, nikto, xssstrike, ffuf
> **CWE Reference**: CWE-79(XSS), CWE-89(SQLi), CWE-352(CSRF), CWE-22(LFI/RFI)

#### [Vulnerability Name]

| Field | Content | Guidance |
|-------|---------|----------|
| CVE ID | CVE-YYYY-XXXXX | Search at cve.mitre.org |
| CVSS Score | X.X (0-10) | Use CVSS Calculator v3.1 |
| CVSS Vector | CVSS:3.1/AV:N/AC:L... | Complete vector for exact score |
| Severity | Critical/High/Medium/Low | Auto-determined from CVSS |
| Vuln Type | [Type] | e.g.: SQL Injection/XSS/CSRF/SSRF/File Upload |
| Target URL | https://target.com/[path] | Complete affected URL |
| Affected Parameter | [Parameter name] | e.g.: id, user, q, search |
| HTTP Method | GET/POST/PUT/DELETE | Request method with vuln |
| Description | [Detailed description] | Vuln mechanism, exploitation conditions, impact |
| Date Found | YYYY-MM-DD | Date vulnerability was discovered |
| Reproduction Steps | 1. [Craft request]<br>2. [Send payload]<br>3. [Observe response] | Complete request-response flow |
| Testing Tools | [Tool+Version] | e.g.: BurpSuite 2022.1, SQLMap 1.7 |
| PoC Code | ```[Runnable exploit code]``` | Copy-paste ready HTTP request |
| Recommendation | [Fix method] | Parameterized queries/input filter/output encoding |
| References | [CVE, CWE, OWASP, vendor advisory] | At least 2 references |

**Quick Detection Commands:**
```bash
# SQL injection detection
sqlmap -u "https://target.com/product?id=1" --batch --level=3

# XSS detection
sqlmap -u "https://target.com/search?q=test" --batch

# Directory enumeration
ffuf -w wordlist.txt -u https://target.com/FUZZ

# Command injection test
curl -s "https://target.com/ping?host=127.0.0.1|ls"
```

**OWASP Top 10 2021 Mapping:**
| Category | Common Vulns |
|----------|--------------|
| A01: Broken Access Control | IDOR, privilege escalation, horiz/vert bypass |
| A02: Cryptographic Failures | Plaintext transmission, weak crypto, hardcoded secrets |
| A03: Injection | SQLi, XSS, Command Injection, LDAPi |
| A04: Insecure Design | Biz logic flaws, auth bypass |
| A05: Security Misconfiguration | Default creds, misconfig, missing security headers |

---
""",
            'database': """### Database Vulnerability

> **Testing Method**: Use sqlmap --batch for basic detection, combine with manual SQL injection testing. Compare identified DB version against known CVEs.
> **Tools**: sqlmap, nmap (mysql/mongodb/postgres ports), metasploit
> **CWE Reference**: CWE-89(SQL Injection), CWE-94(Code Injection), CWE-200(Info Disclosure)

#### [Vulnerability Name]

| Field | Content | Guidance |
|-------|---------|----------|
| CVE ID | CVE-YYYY-XXXXX | Search at cve.mitre.org |
| CVSS Score | X.X (0-10) | Use CVSS Calculator v3.1 |
| CVSS Vector | CVSS:3.1/AV:N/AC:L... | Complete vector for exact score |
| Severity | Critical/High/Medium/Low | Auto-determined from CVSS |
| Database Type | MySQL/PostgreSQL/MongoDB/Redis/Oracle | e.g.: MySQL 5.7.29 |
| Affected Port | [Port] | Defaults: MySQL 3306, PostgreSQL 5432, MongoDB 27017, Redis 6379 |
| Vuln Type | [Type] | e.g.: SQL Injection/Unauth Access/Weak Password/Default Creds |
| Description | [Detailed description] | Vuln mechanism, exploitation conditions, impact |
| Date Found | YYYY-MM-DD | Date vulnerability was discovered |
| Testing Tools | [Tool+Version] | e.g.: sqlmap 1.7, nmap 7.92 |
| PoC Code | ```[database-specific payload]``` | DB-type specific exploit |
| Recommendation | [Fix method] | Version upgrade/access control config/strong password policy |
| References | [CVE link, official docs, related reports] | At least 2 references |

**Quick Detection Commands:**
```bash
# MySQL enumeration
nmap -sV -p 3306 TARGET
mysql -h TARGET -u root -p

# MongoDB detection
nmap -sV -p 27017 TARGET
mongo TARGET:27017/db --eval "db.version()"

# SQL injection
sqlmap -u "https://target.com/db?id=1" --batch --dbs

# Redis unauth
redis-cli -h TARGET INFO
```

---
""",
            'api': """### API Vulnerability

> **Testing Method**: Use BurpSuite to intercept API requests, analyze JSON/XML params. Compare against OWASP API Security Top 10. Use sqlmap, ffuf for automated testing.
> **Tools**: burpsuite, postman, sqlmap, ffuf, zap
> **CWE Reference**: CWE-89(SQLi), CWE-306(Missing Auth), CWE-862(AuthZ Issues)

#### [Vulnerability Name]

| Field | Content | Guidance |
|-------|---------|----------|
| CVE ID | CVE-YYYY-XXXXX | Search at cve.mitre.org |
| CVSS Score | X.X (0-10) | Use CVSS Calculator v3.1 |
| CVSS Vector | CVSS:3.1/AV:N/AC:L... | Complete vector for exact score |
| Severity | Critical/High/Medium/Low | Auto-determined from CVSS |
| API Endpoint | /api/v1/[endpoint] | Complete API path |
| HTTP Method | GET/POST/PUT/DELETE/PATCH | Request method with vuln |
| Content-Type | application/json/xml/form-data | Request data format |
| Parameter Location | Path/Query/Body/Header | Where param is in request |
| Description | [Detailed description] | Vuln mechanism, exploitation conditions, impact |
| Date Found | YYYY-MM-DD | Date vulnerability was discovered |
| Testing Tools | [Tool+Version] | e.g.: BurpSuite 2022.1, Postman |
| PoC Request | ```[Complete executable HTTP request]``` | Copy-paste ready for browser/Burp |
| Recommendation | [Fix method] | Auth/AuthZ/input validation/rate limiting |
| References | [CVE, OWASP API Top 10, vendor advisory] | At least 2 references |

**API Security Testing Checklist:**
```
□ Auth endpoints: /api/auth/login, /api/auth/register
□ Token location: Header (Authorization: Bearer <token>)
□ Rate limiting: Test if 429 returned on limit breach
□ Brute force: Test if account locks after multiple failures
□ BOLA: Test if other user's ID can access their data
□ SQLi: Test if params are directly concatenated to SQL
□ XXE: Test if XML payload is parsed
□ SSRF: Test if internal network resources can be accessed
```

---
""",
            'social': """### Social Engineering

> **Testing Method**: Phishing emails (Spear Phishing), phone fraud (Vishing), physical penetration (Physical). Use OSINT tools to gather target information.
> **Tools**: theHarvester, recon-ng, SET (Social Engineering Toolkit), maltego
> **CWE Reference**: CWE-330(Weak Random), CWE-312(Cleartext Storage), CWE-601(Phishing)

#### [Vulnerability Name]

| Field | Content | Guidance |
|-------|---------|----------|
| CVE ID | N/A or Campaign ID | SE usually has no CVE, use custom ID |
| CVSS Score | X.X (0-10) | Use CVSS Calculator v3.1 |
| CVSS Vector | CVSS:3.1/AV:P/AC:L... | Attack vector P=Physical |
| Severity | Critical/High/Medium/Low | Auto-determined from CVSS |
| Attack Type | [Type] | e.g.: Phishing/Vishing/Physical/Smishing |
| Target Person | [Title/Name] | e.g.: HR Manager, Finance Staff |
| Attack Vector | [Phishing content type] | e.g.: Spoofed email/Fake phone/ID card |
| Description | [Detailed description] | Attack method, target selection rationale, success rate |
| Date Found | YYYY-MM-DD | Date vulnerability was discovered |
| OSINT Findings | [Info gathered via OSINT] | Email/social accounts/phone/company info |
| Attack Process | 1. [Gather intel]<br>2. [Craft attack]<br>3. [Execute test]<br>4. [Document results] | Complete attack chain |
| Phishing Payload | ```[Phishing email/URL]``` | Actual phishing content used |
| Recommendation | [Fix method] | Security awareness training/email validation/physical access control |
| References | [OSINT tools, phishing cases, training materials] | References |

**OSINT Intel Gathering Commands:**
```bash
# Email harvesting
theHarvester -d target.com -b google

# Subdomain enumeration
amass enum -passive -d target.com

# LinkedIn search
https://www.linkedin.com/search/results/people/?keywords=target.com

# Phishing toolkit
setoolkit
```

**Common Phishing Indicators:**
- Sender domain similar to official (e.g.: admin@ta1get.com vs admin@target.com)
- Urgent tone ("Act immediately or account will be suspended")
- Link hover shows URL inconsistent with displayed text
- Attachment names with double extensions (e.g.: "Salary_2024.xlsx.exe")

---
"""
        }
        return templates.get(template_type, templates['network'])

    def _get_template_style(self, style, templates=None):
        """Dispatch to the appropriate template generator by style"""
        if templates is None:
            templates = ['network', 'web', 'database', 'api', 'social']
        style_map = {
            'standard': self._get_template_standard,
            'executive': self._get_template_executive,
            'checklist': self._get_template_checklist,
            'ctf': self._get_template_ctf,
            'full': self._get_template_full,
        }
        gen = style_map.get(style, style_map['standard'])
        return gen(templates)

    def _get_template_standard(self, templates):
        """Standard placeholder template (original style)"""
        if self.language == 'zh':
            sections = ["## 漏洞模板区域 / Vulnerability Template Area\n"]
            sections.append("*以下区域需手动填写，仅供模板参考*\n\n")
            for t in templates:
                sections.append(self._get_template_zh(t))
        else:
            sections = ["## Vulnerability Template Area\n"]
            sections.append("*The following sections require manual completion. For reference only.*\n\n")
            for t in templates:
                sections.append(self._get_template_en(t))
        return "".join(sections)

    def _get_template_executive(self, templates):
        """Executive Summary style - big stats, charts, low on detail"""
        if self.language == 'zh':
            return """## 执行摘要 / Executive Summary

> **使用说明**: 执行摘要面向决策者，重点展示风险等级、影响范围、修复优先级。文字简洁，配合数据图表，让非技术人员也能快速理解安全态势。

### 一、风险总览 / Risk Overview

#### 1.1 CVSS 评分分布

| 评分范围 | 漏洞数 | 占比 | 图形分布 |
|---------|-------|------|---------|
| 9.0 - 10.0 (Critical) | [X] | [X]% | 🔴🔴🔴 |
| 7.0 - 8.9 (High) | [X] | [X]% | 🔴🔴 |
| 4.0 - 6.9 (Medium) | [X] | [X]% | 🟡🟡🟡 |
| 0.1 - 3.9 (Low) | [X] | [X]% | 🟢 |
| 0.0 (Info) | [X] | [X]% | 🔵 |

**平均CVSS**: [X.X] &nbsp;&nbsp; **最高CVSS**: [X.X] &nbsp;&nbsp; **风险指数**: [低/中/高/严重]

#### 1.2 漏洞趋势时间线 (近6个月)

```
月份        高危    中危    低危    信息
-----------------------------------------
2025-11    [X]     [X]     [X]     [X]
2025-12    [X]     [X]     [X]     [X]
2026-01    [X]     [X]     [X]     [X]
2026-02    [X]     [X]     [X]     [X]
2026-03    [X]     [X]     [X]     [X]
2026-04    [X]     [X]     [X]     [X]
```

### 二、业务影响评估 / Business Impact Assessment

#### 2.1 受影响资产

| 资产名称 | 资产类型 | 漏洞数 | 业务关键程度 | 优先级 |
|---------|---------|-------|-------------|--------|
| [系统名] | Web应用/数据库/网络设备 | [X] | 🔴极高/🟡高/🟢中 | P1/P2/P3 |

#### 2.2 潜在业务风险

| 风险场景 | 影响描述 | 发生概率 | 潜在损失 | 风险等级 |
|---------|---------|---------|---------|--------|
| 数据泄露 | 敏感数据被窃取 | 高/中/低 | [金额/级别] | 🔴严重 |
| 服务中断 | 系统不可用 | 高/中/低 | [金额/级别] | 🟡高 |
| 合规处罚 | 违反等保/GDPR等 | 高/中/低 | [金额/级别] | 🟡高 |
| 声誉损失 | 用户信任度下降 | 高/中/低 | [金额/级别] | 🟢中 |

#### 2.3 合规差距分析

| 合规标准 | 要求等级 | 当前达标率 | 差距描述 | 整改成本 |
|---------|---------|-----------|---------|---------|
| 等保2.0 | 三级 | [X]% | [描述] | [金额] |
| ISO 27001 | - | [X]% | [描述] | [金额] |
| GDPR | - | [X]% | [描述] | [金额] |

### 三、行业对比 / Industry Comparison

#### 3.1 与行业平均值对比

| 指标 | 本系统 | 行业平均 | 对比结果 |
|------|-------|---------|---------|
| 平均CVSS | [X.X] | 6.8 | [优于/低于/持平] |
| 高危漏洞比例 | [X]% | 15% | [优于/低于/持平] |
| 漏洞修复周期 | [X]天 | 45天 | [优于/低于/持平] |
| 资产覆盖率 | [X]% | 80% | [优于/低于/持平] |

#### 3.2 OWASP Top 10 2021 对照

| OWASP分类 | 本系统是否存在 | 漏洞数 | 最高CVSS | 是否需紧急处理 |
|-----------|--------------|-------|---------|--------------|
| A01: Broken Access Control | ☐ 是 ☐ 否 | [X] | [X.X] | ☐ |
| A02: Cryptographic Failures | ☐ 是 ☐ 否 | [X] | [X.X] | ☐ |
| A03: Injection | ☐ 是 ☐ 否 | [X] | [X.X] | ☐ |
| A04: Insecure Design | ☐ 是 ☐ 否 | [X] | [X.X] | ☐ |
| A05: Security Misconfiguration | ☐ 是 ☐ 否 | [X] | [X.X] | ☐ |

### 四、修复计划 / Remediation Plan

#### 4.1 修复时间线

| 阶段 | 时间范围 | 目标漏洞 | 负责人 | 状态 |
|------|---------|---------|--------|------|
| 紧急修复 | 0-7天 | Critical + High | [负责人] | ☐ 已完成 ☐ 进行中 |
| 短期修复 | 7-30天 | Medium (高可利用性) | [负责人] | ☐ 已完成 ☐ 进行中 |
| 中期修复 | 30-90天 | Medium (低可利用性) | [负责人] | ☐ 已完成 ☐ 进行中 |
| 长期加固 | 90天+ | Low + Info | [负责人] | ☐ 已完成 ☐ 进行中 |

#### 4.2 关键里程碑

```
[#######-----] 紧急修复  70%完成  (7/10漏洞已修复)
[###-------] 短期修复  30%完成  (3/10漏洞已修复)
[---------] 中期修复   0%完成
[---------] 长期加固   0%完成
```

### 五、关键指标 / Key Metrics

| 指标 | 当前值 | 目标值 | 变化趋势 |
|------|-------|-------|---------|
| 漏洞总数 | [X] | 减少50% | ↓ |
| Critical漏洞 | [X] | 0 | ↓ |
| 平均修复时间 | [X]天 | <30天 | → |
| 漏洞复发率 | [X]% | <5% | → |
| 安全测试覆盖率 | [X]% | 100% | ↑ |

### 六、建议行动 / Recommended Actions

#### 6.1 立即行动 (0-7天)

1. 🔴 **[紧急] 隔离受影响系统** - 立即隔离 [系统名]，防止漏洞扩散
2. 🔴 **[紧急] 启动应急响应** - 召集安全团队，分析漏洞根因
3. 🔴 **[紧急] 通知相关方** - 按照预案通知管理层/法务/公关

#### 6.2 短期行动 (7-30天)

1. 🟡 **[重要] 制定修复计划** - 为每个高危漏洞制定具体修复方案和时间表
2. 🟡 **[重要] 代码审计** - 对 [系统名] 进行深度代码审计，查找类似漏洞
3. 🟡 **[重要] 安全培训** - 对开发团队进行安全编码培训

#### 6.3 中长期行动 (30天+)

1. 🟢 **[常规] 建立安全流程** - 将安全测试集成到CI/CD流程
2. 🟢 **[常规] 定期渗透测试** - 每季度进行一次全面的渗透测试
3. 🟢 **[常规] 安全监控升级** - 部署/升级安全信息和事件监控系统(SIEM)

### 七、漏洞总览 / Vulnerability Overview

| 类别 Category | 高危 Critical | 中危 Medium | 低危 Low | 合计 Total |
|--------------|--------------|-------------|---------|-----------|
| Web应用 Web | [X] | [X] | [X] | [X] |
| 网络安全 Network | [X] | [X] | [X] | [X] |
| 系统安全 System | [X] | [X] | [X] | [X] |
| 信息泄露 Info | [X] | [X] | [X] | [X] |
| 认证授权 Auth | [X] | [X] | [X] | [X] |
| 配置缺陷 Config | [X] | [X] | [X] | [X] |

### 八、下一步 / Next Steps

- [ ] 与 [负责人] 确认修复时间表
- [ ] 安排下次安全会议：[日期]
- [ ] 获取修复进度更新：[频率]
- [ ] 安排复测日期：[日期]

---
*本执行摘要报告模板 - 适用于向决策者汇报安全态势*
"""
        else:
            return """## Executive Summary

> **Usage**: Executive Summary is for decision-makers. Focus on risk level, impact scope, and remediation priority. Concise text with data charts helps non-technical stakeholders quickly understand the security posture.

### 1. Risk Overview

#### 1.1 CVSS Score Distribution

| Score Range | Count | Percentage | Visual |
|------------|-------|-----------|--------|
| 9.0 - 10.0 (Critical) | [X] | [X]% | 🔴🔴🔴 |
| 7.0 - 8.9 (High) | [X] | [X]% | 🔴🔴 |
| 4.0 - 6.9 (Medium) | [X] | [X]% | 🟡🟡🟡 |
| 0.1 - 3.9 (Low) | [X] | [X]% | 🟢 |
| 0.0 (Info) | [X] | [X]% | 🔵 |

**Average CVSS**: [X.X] &nbsp;&nbsp; **Highest CVSS**: [X.X] &nbsp;&nbsp; **Risk Index**: [Low/Medium/High/Critical]

#### 1.2 Vulnerability Timeline (Last 6 Months)

```
Month        High    Medium  Low     Info
--------------------------------------------
2025-11     [X]     [X]     [X]     [X]
2025-12     [X]     [X]     [X]     [X]
2026-01     [X]     [X]     [X]     [X]
2026-02     [X]     [X]     [X]     [X]
2026-03     [X]     [X]     [X]     [X]
2026-04     [X]     [X]     [X]     [X]
```

### 2. Business Impact Assessment

#### 2.1 Affected Assets

| Asset Name | Asset Type | Vuln Count | Business Criticality | Priority |
|------------|-----------|-----------|---------------------|----------|
| [System name] | Web App/DB/Network Device | [X] | 🔴Very High/🟡High/🟢Medium | P1/P2/P3 |

#### 2.2 Potential Business Risks

| Risk Scenario | Impact Description | Probability | Potential Loss | Risk Level |
|--------------|-------------------|-------------|----------------|------------|
| Data Breach | Sensitive data stolen | High/Med/Low | [Amount/Level] | 🔴Critical |
| Service Outage | System unavailable | High/Med/Low | [Amount/Level] | 🟡High |
| Compliance Penalty | Violation of etc/GDPR | High/Med/Low | [Amount/Level] | 🟡High |
| Reputation Damage | User trust decline | High/Med/Low | [Amount/Level] | 🟢Medium |

#### 2.3 Compliance Gap Analysis

| Standard | Required Level | Current Compliance | Gap Description | Remediation Cost |
|---------|---------------|-------------------|-----------------|-------------------|
| 等保2.0 Level 3 | 三级 | [X]% | [Description] | [Amount] |
| ISO 27001 | - | [X]% | [Description] | [Amount] |
| GDPR | - | [X]% | [Description] | [Amount] |

### 3. Industry Comparison

#### 3.1 vs Industry Average

| Metric | This System | Industry Avg | Result |
|--------|------------|--------------|--------|
| Average CVSS | [X.X] | 6.8 | [Better/Worse/On Par] |
| High-severity Ratio | [X]% | 15% | [Better/Worse/On Par] |
| Avg Remediation Time | [X] days | 45 days | [Better/Worse/On Par] |
| Asset Coverage | [X]% | 80% | [Better/Worse/On Par] |

#### 3.2 OWASP Top 10 2021 Mapping

| OWASP Category | Present in System | Count | Highest CVSS | Needs Urgent Action |
|----------------|-------------------|-------|--------------|---------------------|
| A01: Broken Access Control | ☐ Yes ☐ No | [X] | [X.X] | ☐ |
| A02: Cryptographic Failures | ☐ Yes ☐ No | [X] | [X.X] | ☐ |
| A03: Injection | ☐ Yes ☐ No | [X] | [X.X] | ☐ |
| A04: Insecure Design | ☐ Yes ☐ No | [X] | [X.X] | ☐ |
| A05: Security Misconfiguration | ☐ Yes ☐ No | [X] | [X.X] | ☐ |

### 4. Remediation Plan

#### 4.1 Timeline

| Phase | Timeframe | Target Vulns | Owner | Status |
|-------|-----------|-------------|-------|--------|
| Urgent Fix | 0-7 days | Critical + High | [Owner] | ☐ Complete ☐ In Progress |
| Short-term Fix | 7-30 days | Medium (high exploitability) | [Owner] | ☐ Complete ☐ In Progress |
| Mid-term Fix | 30-90 days | Medium (low exploitability) | [Owner] | ☐ Complete ☐ In Progress |
| Long-term Hardening | 90+ days | Low + Info | [Owner] | ☐ Complete ☐ In Progress |

#### 4.2 Progress Bar

```
[#######-----] Urgent Fix    70% complete  (7/10 vulns fixed)
[###-------] Short-term Fix  30% complete  (3/10 vulns fixed)
[---------] Mid-term Fix    0% complete
[---------] Long-term       0% complete
```

### 5. Key Metrics

| Metric | Current | Target | Trend |
|--------|---------|--------|-------|
| Total Vulns | [X] | -50% | ↓ |
| Critical Vulns | [X] | 0 | ↓ |
| Avg Fix Time | [X] days | <30 days | → |
| Vuln Recurrence | [X]% | <5% | → |
| Test Coverage | [X]% | 100% | ↑ |

### 6. Recommended Actions

#### 6.1 Immediate (0-7 days)

1. 🔴 **[Urgent] Isolate affected system** - Isolate [system name] immediately to prevent spread
2. 🔴 **[Urgent] Activate incident response** - Convene security team, analyze root cause
3. 🔴 **[Urgent] Notify stakeholders** - Follow protocol to notify management/legal/PR

#### 6.2 Short-term (7-30 days)

1. 🟡 **[Important] Create remediation plan** - Schedule specific fix plan for each high vuln
2. 🟡 **[Important] Code audit** - Deep code audit on [system name] for similar vulns
3. 🟡 **[Important] Security training** - Secure coding training for dev team

#### 6.3 Mid/long-term (30+ days)

1. 🟢 **[Routine] Establish security process** - Integrate security testing into CI/CD
2. 🟢 **[Routine] Regular pentesting** - Quarterly comprehensive pentest
3. 🟢 **[Routine] Security monitoring upgrade** - Deploy/upgrade SIEM

### 7. Vulnerability Overview

| Category | Critical | Medium | Low | Total |
|----------|----------|--------|-----|-------|
| Web Application | [X] | [X] | [X] | [X] |
| Network Security | [X] | [X] | [X] | [X] |
| System Security | [X] | [X] | [X] | [X] |
| Information Disclosure | [X] | [X] | [X] | [X] |
| Authentication & AuthZ | [X] | [X] | [X] | [X] |
| Configuration Issues | [X] | [X] | [X] | [X] |

### 8. Next Steps

- [ ] Confirm remediation timeline with [owner]
- [ ] Schedule next security meeting: [date]
- [ ] Set remediation progress update frequency: [frequency]
- [ ] Schedule retest date: [date]

---
*Executive Summary report template - for decision-maker security posture reporting*
"""

    def _get_template_checklist(self, templates):
        """Checklist style - tickable items for audit/compliance"""
        if self.language == 'zh':
            return """## 安全检查清单 / Security Checklist

> **使用说明**: 请根据实际情况勾选每个项目，填写证据和备注。为每个检查项评估CVSS评分和严重程度，便于优先级排序。

### 一、信息收集 / Information Gathering

| # | 检查项 | CVSS | 严重程度 | 测试方法 | 状态 | 证据 | 复查日期 | 备注 |
|---|--------|------|---------|---------|------|------|---------|------|
| 1 | 目标资产识别 | - | - | 使用 nslookup/Dig/Whois 收集目标基础信息 | ☐ 已完成 ☐ 未完成 ☐ 不适用 | | | |
| 2 | 端口扫描 | - | - | `nmap -sV -sC -Pn -p- TARGET`，发现开放端口和服务版本 | ☐ 已完成 ☐ 未完成 ☐ 不适用 | | | |
| 3 | 子域名枚举 | - | - | `amass enum -passive -d domain.com`，使用在线工具(VirusTotal, Certificate Transparency) | ☐ 已完成 ☐ 未完成 ☐ 不适用 | | | |
| 4 | 技术栈识别 | - | - | 使用 WhatWeb/Wappalyzer 识别Web服务器、框架、语言版本 | ☐ 已完成 ☐ 未完成 ☐ 不适用 | | | |
| 5 | 敏感文件检测 | 5.3 | Medium | 使用 ffuf/dirb 扫描 /.git, /.env, /config, /backup 等敏感路径 | ☐ 已完成 ☐ 未完成 ☐ 不适用 | | | |

### 二、Web应用安全 / Web Application Security

| # | 检查项 | CVSS | 严重程度 | 测试方法 | 状态 | 证据 | 复查日期 | 备注 |
|---|--------|------|---------|---------|------|------|---------|------|
| 6 | SQL注入测试 | 9.8 | Critical | `sqlmap -u TARGET --batch --level=3`，手工测试 ' " \\ ; -- or 1=1 | ☐ 已修复 ☐ 存在 ☐ 不适用 | | | |
| 7 | XSS跨站脚本 | 7.3 | Medium | 测试 <script>, <img onerror>, <svg onload>，检查 HttpOnly/Secure Cookie 标记 | ☐ 已修复 ☐ 存在 ☐ 不适用 | | | |
| 8 | CSRF跨站请求伪造 | 6.5 | Medium | 检查Token存在性和验证，检查 Referer/Origin 头 | ☐ 已修复 ☐ 存在 ☐ 不适用 | | | |
| 9 | 文件上传漏洞 | 8.1 | High | 上传测试 .php/.asp/.jsp/.exe，绕过 Content-Type 和文件内容检测 | ☐ 已修复 ☐ 存在 ☐ 不适用 | | | |
| 10 | API安全测试 | 9.8 | Critical | 测试 /api/* 端点，检查认证、授权、速率限制、参数篡改 | ☐ 已修复 ☐ 存在 ☐ 不适用 | | | |
| 11 | 身份认证测试 | 8.1 | High | 测试暴力破解保护、会话超时、密码强度、多因素认证 | ☐ 已修复 ☐ 存在 ☐ 不适用 | | | |
| 12 | 会话管理测试 | 7.5 | High | 检查会话ID复杂度、固定会话ID、会话Cookie属性 | ☐ 已修复 ☐ 存在 ☐ 不适用 | | | |
| 13 | 访问控制测试 | 8.1 | High | 测试 IDOR、水平越权、垂直越权、强制浏览 | ☐ 已修复 ☐ 存在 ☐ 不适用 | | | |
| 14 | SSRF服务器端请求伪造 | 9.1 | Critical | 测试 ?url=, ?uri=, ?path= 参数，尝试访问内网地址 | ☐ 已修复 ☐ 存在 ☐ 不适用 | | | |
| 15 | 命令注入 | 9.8 | Critical | 测试 |ls, whoami, cat, ping| 管道符，检测系统命令执行 | ☐ 已修复 ☐ 存在 ☐ 不适用 | | | |

### 三、网络安全 / Network Security

| # | 检查项 | CVSS | 严重程度 | 测试方法 | 状态 | 证据 | 复查日期 | 备注 |
|---|--------|------|---------|---------|------|------|---------|------|
| 16 | 端口服务识别 | - | - | `nmap -sV TARGET`，识别服务版本与已知漏洞(CVE)对应 | ☐ 已完成 ☐ 未完成 ☐ 不适用 | | | |
| 17 | 防火墙规则审查 | - | - | 使用 nmap --traceroute 检测网络路径，测试 ACL 规则是否正确 | ☐ 已完成 ☐ 未完成 ☐ 不适用 | | | |
| 18 | SSL/TLS配置 | 7.5 | High | `testssl.sh TARGET`，检测 SSLv2/v3、弱加密套件、证书有效性 | ☐ 已完成 ☐ 未完成 ☐ 不适用 | | | |
| 19 | 中间人攻击测试 | 7.6 | High | 使用 arpspoof/driftnet 测试同一网络中流量劫持可能性 | ☐ 已完成 ☐ 未完成 ☐ 不适用 | | | |
| 20 | DNS安全测试 | 8.1 | High | 测试 DNS 区域传送、DNSSEC 配置、DNS重绑定 | ☐ 已完成 ☐ 未完成 ☐ 不适用 | | | |
| 21 | SMTP/邮件安全 | 7.5 | High | 测试开放中继、SPF/DKIM/DMARC 配置、邮件伪造 | ☐ 已完成 ☐ 未完成 ☐ 不适用 | | | |

### 四、主机安全 / Host Security

| # | 检查项 | CVSS | 严重程度 | 测试方法 | 状态 | 证据 | 复查日期 | 备注 |
|---|--------|------|---------|---------|------|------|---------|------|
| 22 | 操作系统版本识别 | - | - | 使用 nmap -O 或 xprobe2 识别远程OS类型和版本 | ☐ 已完成 ☐ 未完成 ☐ 不适用 | | | |
| 23 | 弱口令检测 | 8.1 | High | 使用 hydra/medusa 进行常见服务(SSH/SMB/MySQL)弱口令测试 | ☐ 已完成 ☐ 未完成 ☐ 不适用 | | | |
| 24 | 默认凭据检测 | 8.0 | High | 使用 searchsploit 和数据库查询默认口令 (admin/admin, root/root) | ☐ 已完成 ☐ 未完成 ☐ 不适用 | | | |
| 25 | 权限配置审查 | 7.8 | High | 检查 SUID/SGID 文件、不必要的服务、过度权限配置 | ☐ 已完成 ☐ 未完成 ☐ 不适用 | | | |
| 26 | 安全更新检查 | 6.5 | Medium | 查询系统版本对应的 CVE，使用 `apt list --upgradable` 或 Windows Update | ☐ 已完成 ☐ 未完成 ☐ 不适用 | | | |
| 27 | 缓冲区溢出测试 | 9.0 | Critical | 使用 metasploit 检测已知溢出漏洞，测试输入长度验证 | ☐ 已完成 ☐ 未完成 ☐ 不适用 | | | |

### 五、安全配置 / Security Configuration

| # | 检查项 | CVSS | 严重程度 | 测试方法 | 状态 | 证据 | 复查日期 | 备注 |
|---|--------|------|---------|---------|------|------|---------|------|
| 28 | 安全头检查 | 3.0 | Low | 使用 curl -I 检查 X-Frame-Options/X-XSS-Protection/ CSP/ HSTS 等头 | ☐ 已配置 ☐ 未配置 ☐ 不适用 | | | |
| 29 | CORS配置检查 | 6.5 | Medium | 检查 Access-Control-Allow-Origin 是否配置为 * 或过度宽松 | ☐ 已配置 ☐ 未配置 ☐ 不适用 | | | |
| 30 | HTTP方法限制 | 5.3 | Medium | 测试 PUT/DELETE/TRACE 等不必要的 HTTP 方法是否被禁用 | ☐ 已配置 ☐ 未配置 ☐ 不适用 | | | |
| 31 | 错误处理配置 | 4.0 | Low | 触发错误检查是否泄漏敏感信息(堆栈跟踪、路径、版本) | ☐ 已配置 ☐ 未配置 ☐ 不适用 | | | |
| 32 | 日志记录配置 | 3.0 | Low | 检查日志是否记录认证尝试、错误、关键操作，保留周期 | ☐ 已配置 ☐ 未配置 ☐ 不适用 | | | |
| 33 | 目录浏览禁止 | 5.3 | Medium | 测试是否可通过 /images/ 等路径列目录，查看敏感文件 | ☐ 已配置 ☐ 未配置 ☐ 不适用 | | | |

### 六、漏洞风险矩阵 / Risk Matrix

> **使用方法**: 在下表中填入已发现漏洞的CVSS评分，评估风险等级和修复优先级

| 漏洞ID | 漏洞名称 | CVSS | 可利用性 | 影响程度 | 风险等级 | 修复优先级 | 修复计划 |
|--------|---------|------|---------|---------|---------|-----------|---------|
| V001 | [名称] | [X.X] | 高/中/低 | 高/中/低 | 🔴严重/🟡高/🟢中/🔵低 | P1/P2/P3/P4 | [计划日期] |
| V002 | [名称] | [X.X] | 高/中/低 | 高/中/低 | 🔴严重/🟡高/🟢中/🔵低 | P1/P2/P3/P4 | [计划日期] |

**风险等级计算**: 🔴严重 = CVSS≥9.0 | 🟡高 = CVSS 7.0-8.9 | 🟢中 = CVSS 4.0-6.9 | 🔵低 = CVSS<4.0

### 七、检查结果汇总 / Checklist Summary

| 类别 | 已完成 | 未完成 | 不适用 | 完成率 | 高危数 | 中危数 | 低危数 |
|------|--------|--------|--------|--------|--------|--------|--------|
| 信息收集 | | | | | | | | |
| Web安全 | | | | | | | | |
| 网络安全 | | | | | | | | |
| 主机安全 | | | | | | | | |
| 安全配置 | | | | | | | | |
| **总计** | | | | | | | | | |

### 八、签字确认 / Sign-off

| 角色 | 姓名 | 日期 | 签字 | 意见 |
|------|------|------|------|------|
| 测试工程师 | [姓名] | [日期] | | |
| 审核人员 | [姓名] | [日期] | | |
| 安全负责人 | [姓名] | [日期] | | |

---
*安全检查清单模板 - 适用于审计、合规检查和整改跟踪*
"""
        else:
            return """## Security Checklist

> **Usage**: Check each item based on actual findings. Fill in CVSS scores and severity for prioritization. Complete evidence and review dates for each item.

### 1. Information Gathering

| # | Check Item | CVSS | Severity | Test Method | Status | Evidence | Review Date | Notes |
|---|-----------|------|----------|-------------|--------|----------|-------------|-------|
| 1 | Target Asset Identification | - | - | Use nslookup/Dig/Whois to collect target info | ☐ Done ☐ Undone ☐ N/A | | | |
| 2 | Port Scanning | - | - | `nmap -sV -sC -Pn -p- TARGET` to find open ports and services | ☐ Done ☐ Undone ☐ N/A | | | |
| 3 | Subdomain Enumeration | - | - | `amass enum -passive -d domain.com`, online tools(VirusTotal, Cert Transparency) | ☐ Done ☐ Undone ☐ N/A | | | |
| 4 | Technology Fingerprinting | - | - | Use WhatWeb/Wappalyzer to identify server, framework, language versions | ☐ Done ☐ Undone ☐ N/A | | | |
| 5 | Sensitive File Detection | 5.3 | Medium | Use ffuf/dirb to scan /.git, /.env, /config, /backup paths | ☐ Done ☐ Undone ☐ N/A | | | |

### 2. Web Application Security

| # | Check Item | CVSS | Severity | Test Method | Status | Evidence | Review Date | Notes |
|---|-----------|------|----------|-------------|--------|----------|-------------|-------|
| 6 | SQL Injection Testing | 9.8 | Critical | `sqlmap -u TARGET --batch --level=3`, manual test ' " \\ ; -- or 1=1 | ☐ Fixed ☐ Found ☐ N/A | | | |
| 7 | XSS Testing | 7.3 | Medium | Test <script>, <img onerror>, <svg onload>, check HttpOnly/Secure Cookie | ☐ Fixed ☐ Found ☐ N/A | | | |
| 8 | CSRF Testing | 6.5 | Medium | Check token existence and validation, Referer/Origin headers | ☐ Fixed ☐ Found ☐ N/A | | | |
| 9 | File Upload Testing | 8.1 | High | Upload test .php/.asp/.jsp/.exe, bypass Content-Type and content detection | ☐ Fixed ☐ Found ☐ N/A | | | |
| 10 | API Security Testing | 9.8 | Critical | Test /api/* endpoints, check auth, authZ, rate limiting, param tampering | ☐ Fixed ☐ Found ☐ N/A | | | |
| 11 | Authentication Testing | 8.1 | High | Test brute force protection, session timeout, password strength, MFA | ☐ Fixed ☐ Found ☐ N/A | | | |
| 12 | Session Management Testing | 7.5 | High | Check session ID complexity, fixed session IDs, Cookie attributes | ☐ Fixed ☐ Found ☐ N/A | | | |
| 13 | Access Control Testing | 8.1 | High | Test IDOR, horizontal/vertical privilege escalation, forced browsing | ☐ Fixed ☐ Found ☐ N/A | | | |
| 14 | SSRF Testing | 9.1 | Critical | Test ?url=, ?uri=, ?path= params, try accessing internal addresses | ☐ Fixed ☐ Found ☐ N/A | | | |
| 15 | Command Injection | 9.8 | Critical | Test |ls, whoami, cat, ping| pipe operators, check system command execution | ☐ Fixed ☐ Found ☐ N/A | | | |

### 3. Network Security

| # | Check Item | CVSS | Severity | Test Method | Status | Evidence | Review Date | Notes |
|---|-----------|------|----------|-------------|--------|----------|-------------|-------|
| 16 | Port & Service Identification | - | - | `nmap -sV TARGET` to map services to known CVEs | ☐ Done ☐ Undone ☐ N/A | | | |
| 17 | Firewall Rule Review | - | - | Use nmap --traceroute to detect network path, test ACL correctness | ☐ Done ☐ Undone ☐ N/A | | | |
| 18 | SSL/TLS Configuration | 7.5 | High | `testssl.sh TARGET`, check SSLv2/v3, weak cipher suites, cert validity | ☐ Done ☐ Undone ☐ N/A | | | |
| 19 | MITM Testing | 7.6 | High | Use arpspoof/driftnet to test traffic hijacking in same network | ☐ Done ☐ Undone ☐ N/A | | | |
| 20 | DNS Security Testing | 8.1 | High | Test DNS zone transfer, DNSSEC config, DNS rebinding | ☐ Done ☐ Undone ☐ N/A | | | |
| 21 | SMTP/Email Security | 7.5 | High | Test open relay, SPF/DKIM/DMARC config, email spoofing | ☐ Done ☐ Undone ☐ N/A | | | |

### 4. Host Security

| # | Check Item | CVSS | Severity | Test Method | Status | Evidence | Review Date | Notes |
|---|-----------|------|----------|-------------|--------|----------|-------------|-------|
| 22 | OS Version Detection | - | - | Use nmap -O or xprobe2 to identify remote OS type and version | ☐ Done ☐ Undone ☐ N/A | | | |
| 23 | Weak Password Detection | 8.1 | High | Use hydra/medusa to test common services (SSH/SMB/MySQL) weak passwords | ☐ Done ☐ Undone ☐ N/A | | | |
| 24 | Default Credentials Detection | 8.0 | High | Use searchsploit and DB queries for default creds (admin/admin, root/root) | ☐ Done ☐ Undone ☐ N/A | | | |
| 25 | Privilege Configuration Review | 7.8 | High | Check SUID/SGID files, unnecessary services, excessive permissions | ☐ Done ☐ Undone ☐ N/A | | | |
| 26 | Security Update Check | 6.5 | Medium | Query CVE for system version, use `apt list --upgradable` or Windows Update | ☐ Done ☐ Undone ☐ N/A | | | |
| 27 | Buffer Overflow Testing | 9.0 | Critical | Use metasploit to detect known overflow vulns, test input length validation | ☐ Done ☐ Undone ☐ N/A | | | |

### 5. Security Configuration

| # | Check Item | CVSS | Severity | Test Method | Status | Evidence | Review Date | Notes |
|---|-----------|------|----------|-------------|--------|----------|-------------|-------|
| 28 | Security Headers Check | 3.0 | Low | Use curl -I to check X-Frame-Options/X-XSS-Protection/CSP/HSTS headers | ☐ Configured ☐ Not Configured ☐ N/A | | | |
| 29 | CORS Configuration Check | 6.5 | Medium | Check if Access-Control-Allow-Origin is * or overly permissive | ☐ Configured ☐ Not Configured ☐ N/A | | | |
| 30 | HTTP Method Restrictions | 5.3 | Medium | Test if PUT/DELETE/TRACE and other unnecessary methods are disabled | ☐ Configured ☐ Not Configured ☐ N/A | | | |
| 31 | Error Handling Configuration | 4.0 | Low | Trigger errors to check if sensitive info is leaked (stack trace, path, version) | ☐ Configured ☐ Not Configured ☐ N/A | | | |
| 32 | Logging Configuration | 3.0 | Low | Check if logs record auth attempts, errors, critical operations, retention period | ☐ Configured ☐ Not Configured ☐ N/A | | | |
| 33 | Directory Listing Disable | 5.3 | Medium | Test if /images/ etc paths allow directory listing, exposing sensitive files | ☐ Configured ☐ Not Configured ☐ N/A | | | |

### 6. Vulnerability Risk Matrix

> **Usage**: Fill in discovered vulns with CVSS scores to evaluate risk level and remediation priority

| Vuln ID | Vuln Name | CVSS | Exploitability | Impact | Risk Level | Priority | Remediation Plan |
|---------|-----------|------|----------------|--------|------------|----------|------------------|
| V001 | [Name] | [X.X] | High/Med/Low | High/Med/Low | 🔴Critical/🟡High/🟢Med/🔵Low | P1/P2/P3/P4 | [Date] |
| V002 | [Name] | [X.X] | High/Med/Low | High/Med/Low | 🔴Critical/🟡High/🟢Med/🔵Low | P1/P2/P3/P4 | [Date] |

**Risk Calculation**: 🔴Critical = CVSS≥9.0 | 🟡High = CVSS 7.0-8.9 | 🟢Medium = CVSS 4.0-6.9 | 🔵Low = CVSS<4.0

### 7. Checklist Summary

| Category | Done | Undone | N/A | Completion | Critical | Medium | Low |
|----------|------|--------|-----|------------|----------|--------|-----|
| Information Gathering | | | | | | | | |
| Web Security | | | | | | | | |
| Network Security | | | | | | | | |
| Host Security | | | | | | | | |
| Security Configuration | | | | | | | |
| **Total** | | | | | | | | |

### 8. Sign-off

| Role | Name | Date | Signature | Comments |
|------|------|------|-----------|----------|
| Test Engineer | [Name] | [Date] | | |
| Reviewer | [Name] | [Date] | | |
| Security Lead | [Name] | [Date] | | |

---
*Security checklist template - for audit, compliance check and remediation tracking*
"""

    def _get_template_ctf(self, templates):
        """CTF Writeup style - detailed exploitation steps"""
        if self.language == 'zh':
            return """## CTF漏洞报告 / CTF Vulnerability Writeup

> 📝 **使用说明**: 按照下方模板详细记录每个漏洞的发现和利用过程。

### 漏洞发现模板 / Vulnerability Writeup Template

#### 1. 信息收集 / Information Gathering

```
目标 Target:     [URL/IP]
端口 Port:        [端口]
服务 Service:     [服务名+版本]
操作系统 OS:      [操作系统]
```

**发现的线索 / Clues Found:**
```
[记录所有蛛丝马迹]
```

#### 2. 漏洞识别 / Vulnerability Identification

| 项目 Item | 内容 Content |
|----------|-------------|
| 漏洞名称 Vuln Name | [名称] |
| 漏洞类型 Vuln Type | [类型] |
| CVSS评分 | [分数] |
| 发现日期 Date | [日期] |
| 影响范围 Scope | [影响范围] |

#### 3. 漏洞利用 / Exploitation

**Payload Used:**
```python
[你的payload代码]
```

**利用过程 / Exploitation Process:**
```
Step 1: [第一步操作]
       [命令/请求]

Step 2: [第二步操作]
       [命令/请求]

Step 3: [第三步操作]
       [命令/请求]
```

**成功截图 / Success Screenshot:**
```
[图片链接或描述]
```

#### 4. 权限维持 / Persistence (可选)

```
[如果获取了shell，记录维持权限的方法]
```

#### 5. 修复建议 / Remediation

| 优先级 Priority | 修复方法 Method | 负责人 Owner |
|---------------|----------------|-------------|
| 高 High | [修复方案] | [负责人] |
| 中 Medium | [修复方案] | [负责人] |
| 低 Low | [修复方案] | [负责人] |

---

### 示例: SQL注入漏洞 / Example: SQL Injection

#### 1. 信息收集
```
目标: http://target.com/login
端口: 80
服务: Apache 2.4.29 + PHP 7.3.11
```

**线索:**
```
- 登录表单存在username和password参数
- 错误回显: "Invalid credentials" (可枚举用户)
- 页面标题: "Admin Panel"
```

#### 2. 漏洞识别
| 项目 | 内容 |
|------|------|
| 漏洞类型 | SQL Injection (Boolean-based Blind) |
| CVSS | 9.8 |
| 影响参数 | username |

#### 3. 漏洞利用
**Payload:**
```python
username: admin' AND 1=1-- -
password: [任意]
```

**过程:**
```
Step 1: 测试注入点
       username: admin' AND 1=1-- -
       Result: 登录成功 ✓

Step 2: 确认漏洞
       username: admin' AND 1=2-- -
       Result: 登录失败 ✓

Step 3: 枚举数据库
       username: admin' AND ASCII(SUBSTRING((SELECT database()),1,1))>64-- -
       Result: 登录成功 → 数据库名第一个字符ASCII>64
```

#### 4. 修复建议
| 优先级 | 修复方法 |
|--------|----------|
| 高 | 使用参数化查询 |

---
*CTF漏洞报告模板 - 详细记录发现与利用过程*
"""
        else:
            return """## CTF Vulnerability Writeup

> 📝 **Instructions**: Record each vulnerability's discovery and exploitation in detail using the template below.

### Vulnerability Writeup Template

#### 1. Information Gathering

```
Target:     [URL/IP]
Port:       [Port]
Service:    [Service+Version]
OS:         [OS]
```

**Clues Found:**
```
[Record all findings]
```

#### 2. Vulnerability Identification

| Item | Content |
|------|---------|
| Vuln Name | [Name] |
| Vuln Type | [Type] |
| CVSS Score | [Score] |
| Date Found | [Date] |
| Scope | [Scope] |

#### 3. Exploitation

**Payload Used:**
```python
[Your payload code]
```

**Exploitation Process:**
```
Step 1: [First action]
       [Command/Request]

Step 2: [Second action]
       [Command/Request]

Step 3: [Third action]
       [Command/Request]
```

**Success Screenshot:**
```
[Image link or description]
```

#### 4. Persistence (Optional)

```
[If shell obtained, record persistence method]
```

#### 5. Remediation

| Priority | Method | Owner |
|----------|--------|-------|
| High | [Fix method] | [Owner] |
| Medium | [Fix method] | [Owner] |
| Low | [Fix method] | [Owner] |

---

### Example: SQL Injection

#### 1. Information Gathering
```
Target: http://target.com/login
Port: 80
Service: Apache 2.4.29 + PHP 7.3.11
```

**Clues:**
```
- Login form with username and password parameters
- Error response: "Invalid credentials" (user enumeration possible)
- Page title: "Admin Panel"
```

#### 2. Vulnerability Identification
| Item | Content |
|------|---------|
| Vuln Type | SQL Injection (Boolean-based Blind) |
| CVSS | 9.8 |
| Affected Parameter | username |

#### 3. Exploitation
**Payload:**
```python
username: admin' AND 1=1-- -
password: [any]
```

**Process:**
```
Step 1: Test injection point
       username: admin' AND 1=1-- -
       Result: Login success ✓

Step 2: Confirm vuln
       username: admin' AND 1=2-- -
       Result: Login failed ✓

Step 3: Enumerate DB
       username: admin' AND ASCII(SUBSTRING((SELECT database()),1,1))>64-- -
       Result: Login success → First char of DB name ASCII>64
```

#### 4. Remediation
| Priority | Method |
|----------|--------|
| High | Use parameterized queries |

---
*CTF writeup template - detailed exploitation documentation*
"""

    def _get_template_full(self, templates):
        """Full template - all placeholder categories combined"""
        if self.language == 'zh':
            sections = ["## 漏洞模板区域 / Vulnerability Template Area\n"]
            sections.append("*以下区域需手动填写，仅供模板参考。包含5大类别共31个漏洞模板*\n\n")
            for t in templates:
                sections.append(self._get_template_zh(t))
            sections.append("\n## 附录A - 漏洞快速参考手册 / Quick Reference Guide\n\n")
            sections.append("> **使用方法**: 根据发现的漏洞类型，参照下方手册快速定位测试方法和修复建议\n\n")
            sections.append("### A.1 Web应用漏洞快速手册\n\n")
            sections.append("| 漏洞类型 | CVSS范围 | 快速检测方法 | 关键修复 |\n")
            sections.append("|---------|---------|-------------|----------|\n")
            sections.append("| SQL注入 | 9.0-9.8 | `sqlmap -u URL --batch` | 参数化查询，禁止拼接用户输入 |\n")
            sections.append("| XSS存储型 | 6.1-8.2 | 提交 `<script>alert(1)</script>` | 输出编码，HTML转义 |\n")
            sections.append("| XSS反射型 | 6.1-7.3 | URL参数中测试特殊字符 | 同上，配置CSP安全头 |\n")
            sections.append("| CSRF | 6.5-8.1 | 检查Token存在性，测试无Token请求 | 启用Anti-CSRF Token，验证Referer |\n")
            sections.append("| 文件上传 | 6.0-9.8 | 上传.php/.jsp，测试绕过MIME | 文件类型白名单，内容检测 |\n")
            sections.append("| SSRF | 8.6-9.1 | 测试?url=/file/, /etc/passwd | 禁用不允许的协议，URL白名单验证 |\n")
            sections.append("| 命令注入 | 9.1-10.0 | `;whoami`, `|ls`, `&&id` | 避免调用系统命令，使用API替代 |\n")
            sections.append("| SSTI | 9.0-9.8 | 测试 `{{7*7}}`, `${IFS}` | 不使用用户输入拼接模板引擎 |\n")
            sections.append("| XXE | 8.1-9.8 | 测试XML中 `<!ENTITY>` | 禁用DTD，XML解析器安全配置 |\n")
            sections.append("\n### A.2 系统漏洞快速手册\n\n")
            sections.append("| 漏洞类型 | CVSS范围 | 快速检测方法 | 关键修复 |\n")
            sections.append("|---------|---------|-------------|----------|\n")
            sections.append("| 缓冲区溢出 | 7.0-10.0 | `msfconsole`，search CVE | 输入长度验证，升级版本 |\n")
            sections.append("| 权限提升 | 6.0-8.2 | 检查SUID文件，`sudo -l` | 最小权限原则，修复配置 |\n")
            sections.append("| 本地文件包含 | 6.0-8.1 | `../../etc/passwd` 测试路径遍历 | 路径规范，过滤../等字符 |\n")
            sections.append("| 远程代码执行 | 8.1-10.0 | 测试反序列化，远程文件包含 | 禁止不信任的反序列化输入 |\n")
            sections.append("\n### A.3 网络漏洞快速手册\n\n")
            sections.append("| 漏洞类型 | CVSS范围 | 快速检测方法 | 关键修复 |\n")
            sections.append("|---------|---------|-------------|----------|\n")
            sections.append("| 中间人攻击 | 7.0-7.6 | `ettercap -T`, arpspoof | 启用ARP绑定，802.1X认证 |\n")
            sections.append("| DNS劫持 | 7.0-8.1 | 检查DNS解析是否被篡改 | DNSSEC配置，安全DNS服务 |\n")
            sections.append("| ARP欺骗 | 6.0-7.5 | `arpspoof -i eth0 -t target` | 静态ARP表，交换机组播隔离 |\n")
            sections.append("| 网络钓鱼 | 5.0-7.0 | 伪造页面检测，社会工程学 | 安全意识培训，邮件验证 |\n")
            sections.append("\n### A.4 信息泄露快速手册\n\n")
            sections.append("| 漏洞类型 | CVSS范围 | 快速检测方法 | 关键修复 |\n")
            sections.append("|---------|---------|-------------|----------|\n")
            sections.append("| 敏感文件泄露 | 4.0-7.5 | `ffuf -w wordlist -u target/FUZZ` 扫敏感路径 | 禁止目录浏览，移除敏感文件 |\n")
            sections.append("| 调试信息泄露 | 3.0-6.0 | 触发错误页面，检查堆栈跟踪 | 生产环境关闭调试模式 |\n")
            sections.append("| 路径遍历 | 6.0-8.1 | `../../etc/passwd`, `%2e%2e%2f` | 路径规范化，白名单限制 |\n")
            sections.append("| 源码泄露 | 5.0-8.0 | Git/SVN信息收集，`.git/config` | 禁止.git目录在Web根目录 |\n")
            sections.append("\n### A.5 认证授权漏洞快速手册\n\n")
            sections.append("| 漏洞类型 | CVSS范围 | 快速检测方法 | 关键修复 |\n")
            sections.append("|---------|---------|-------------|----------|\n")
            sections.append("| 弱口令 | 7.0-9.0 | `hydra -L users.txt -P passwords.txt ssh://target` | 强密码策略，账户锁定 |\n")
            sections.append("| 暴力破解 | 6.0-8.0 | 测试登录5次失败是否锁定 | 账户锁定，验证码，限速 |\n")
            sections.append("| 越权访问 | 6.0-9.0 | 测试A用户访问B用户资源 | 基于会话授权，用户ID校验 |\n")
            sections.append("| 认证绕过 | 7.0-9.0 | 空密码，空Session，Cookie伪造 | 安全Session，强制认证 |\n")
            sections.append("\n### A.6 配置缺陷快速手册\n\n")
            sections.append("| 漏洞类型 | CVSS范围 | 快速检测方法 | 关键修复 |\n")
            sections.append("|---------|---------|-------------|----------|\n")
            sections.append("| 默认凭据 | 7.0-9.0 | `searchsploit service`, 手动尝试 admin/admin | 首次部署必须修改默认密码 |\n")
            sections.append("| 安全头缺失 | 2.0-5.0 | `curl -I headers` | 配置 X-Frame-Options/CSP/HSTS |\n")
            sections.append("| CORS配置错误 | 5.0-8.0 | 检查 ACAO:* 或过度宽松 | 限制来源域名，禁止 Credentials |\n")
            sections.append("\n## 附录B - 完整漏洞索引 / Complete Vulnerability Index\n\n")
            sections.append("| # | 类别 | 漏洞名称 | CVSS | CWE | OWASP分类 | 检测工具 |\n")
            sections.append("|---|------|---------|------|-----|-----------|----------|\n")
            sections.append("| 1 | Web | SQL注入 / SQL Injection | 9.8 | CWE-89 | A03:2021 | sqlmap, manual |\n")
            sections.append("| 2 | Web | XSS跨站脚本 / Cross-Site Scripting | 7.3 | CWE-79 | A03:2021 | BurpSuite, xsstrike |\n")
            sections.append("| 3 | Web | CSRF跨站请求伪造 / CSRF | 6.5 | CWE-352 | A01:2021 | BurpSuite CSRF Scanner |\n")
            sections.append("| 4 | Web | 文件上传漏洞 / File Upload | 8.1 | CWE-434 | A03:2021 | manual, ffuf |\n")
            sections.append("| 5 | Web | SSRF服务器端请求伪造 / SSRF | 8.6 | CWE-918 | A10:2021 | manual |\n")
            sections.append("| 6 | Web | SSTI服务器端模板注入 / SSTI | 9.8 | CWE-1336 | A03:2021 | manual |\n")
            sections.append("| 7 | Web | XXE XML外部实体注入 / XXE | 9.1 | CWE-611 | A03:2021 | BurpSuite, digi.awk |\n")
            sections.append("| 8 | Web | 命令注入 / Command Injection | 9.8 | CWE-77 | A03:2021 | manual, commix |\n")
            sections.append("| 9 | System | 缓冲区溢出 / Buffer Overflow | 9.0 | CWE-119 | - | metasploit, gdb |\n")
            sections.append("| 10 | System | 权限提升 / Privilege Escalation | 8.2 | CWE-269 | - | linpeas, winpeas |\n")
            sections.append("| 11 | System | 本地文件包含 / Local File Inclusion | 7.8 | CWE-22 | A01:2021 | manual, ffuf |\n")
            sections.append("| 12 | System | 远程代码执行 / RCE | 10.0 | CWE-94 | A03:2021 | metasploit, manual |\n")
            sections.append("| 13 | System | 整数溢出 / Integer Overflow | 6.5 | CWE-190 | - | metasploit |\n")
            sections.append("| 14 | Network | 中间人攻击 / MITM | 7.6 | CWE-300 | - | ettercap, wireshark |\n")
            sections.append("| 15 | Network | DNS劫持 / DNS Hijacking | 8.1 | CWE-327 | - | dig, nslookup |\n")
            sections.append("| 16 | Network | ARP欺骗 / ARP Spoofing | 6.5 | CWE-322 | - | arpspoof, ettercap |\n")
            sections.append("| 17 | Network | 网络钓鱼 / Phishing | 6.5 | CWE-601 | A01:2021 | SET, social engineering |\n")
            sections.append("| 18 | Info | 敏感文件泄露 / Sensitive File Disclosure | 5.3 | CWE-200 | A01:2021 | ffuf, dirb, metasploit |\n")
            sections.append("| 19 | Info | 调试信息泄露 / Debug Info Disclosure | 4.0 | CWE-11 | - | manual |\n")
            sections.append("| 20 | Info | 路径遍历 / Path Traversal | 7.5 | CWE-22 | A01:2021 | manual, ffuf |\n")
            sections.append("| 21 | Info | 源码泄露 / Source Code Disclosure | 7.5 | CWE-541 | A01:2021 | .git/, .svn/ scanner |\n")
            sections.append("| 22 | Auth | 弱口令 / Weak Password | 8.1 | CWE-521 | A07:2021 | hydra, medusa |\n")
            sections.append("| 23 | Auth | 暴力破解 / Brute Force | 7.5 | CWE-307 | A07:2021 | hydra, BurpSuite |\n")
            sections.append("| 24 | Auth | 越权访问 / Unauthorized Access | 7.5 | CWE-639 | A01:2021 | BurpSuite, manual |\n")
            sections.append("| 25 | Auth | 身份认证绕过 / Authentication Bypass | 8.0 | CWE-287 | A07:2021 | manual |\n")
            sections.append("| 26 | Config | 默认凭据 / Default Credentials | 8.0 | CWE-798 | A07:2021 | searchsploit, manual |\n")
            sections.append("| 27 | Config | 安全头缺失 / Missing Security Headers | 3.0 | CWE-693 | A05:2021 | securityheaders.com |\n")
            sections.append("| 28 | Config | CORS配置错误 / CORS Misconfiguration | 6.5 | CWE-942 | A05:2021 | manual, corsy |\n")
            sections.append("| 29 | Config | HTTP明文传输 / Cleartext Transmission | 7.5 | CWE-319 | A02:2021 | Wireshark, sslscan |\n")
            sections.append("| 30 | Config | 敏感信息URL明文传输 / Sensitive Data in URL | 5.3 | CWE-598 | A02:2021 | BurpSuite Proxy |\n")
            sections.append("| 31 | Config | 错误信息泄露 / Verbose Error Messages | 4.0 | CWE-209 | A05:2021 | manual |\n")
            return "".join(sections)
        else:
            sections = ["## Vulnerability Template Area\n"]
            sections.append("*Manual completion required. For reference only. Contains 31 vulnerability templates across 5 categories.*\n\n")
            for t in templates:
                sections.append(self._get_template_en(t))
            sections.append("\n## Appendix A - Quick Reference Guide\n\n")
            sections.append("> **Usage**: Match discovered vuln type to find test methods and remediation quickly\n\n")
            sections.append("### A.1 Web Vulnerability Quick Reference\n\n")
            sections.append("| Vuln Type | CVSS Range | Quick Test | Key Fix |\n")
            sections.append("|-----------|-----------|------------|----------|\n")
            sections.append("| SQL Injection | 9.0-9.8 | `sqlmap -u URL --batch` | Parameterized queries, no string concat |\n")
            sections.append("| Stored XSS | 6.1-8.2 | Submit `<script>alert(1)</script>` | Output encoding, HTML escape |\n")
            sections.append("| Reflected XSS | 6.1-7.3 | Test special chars in URL params | Same as above, configure CSP header |\n")
            sections.append("| CSRF | 6.5-8.1 | Check Token presence, test w/o Token | Anti-CSRF Token, Referer validation |\n")
            sections.append("| File Upload | 6.0-9.8 | Upload .php/.jsp, bypass MIME checks | Whitelist file types, content validation |\n")
            sections.append("| SSRF | 8.6-9.1 | Test ?url=/file/, /etc/passwd | Disable disallowed protocols, URL whitelist |\n")
            sections.append("| Command Injection | 9.1-10.0 | `;whoami`, `|ls`, `&&id` | Avoid system calls, use API instead |\n")
            sections.append("| SSTI | 9.0-9.8 | Test `{{7*7}}`, `${IFS}` | Don't concatenate user input to template engine |\n")
            sections.append("| XXE | 8.1-9.8 | Test `<!ENTITY>` in XML | Disable DTD, secure XML parser config |\n")
            sections.append("\n### A.2 System Vulnerability Quick Reference\n\n")
            sections.append("| Vuln Type | CVSS Range | Quick Test | Key Fix |\n")
            sections.append("|-----------|-----------|------------|----------|\n")
            sections.append("| Buffer Overflow | 7.0-10.0 | `msfconsole`, search CVE | Input length validation, upgrade version |\n")
            sections.append("| Privilege Escalation | 6.0-8.2 | Check SUID files, `sudo -l` | Least privilege principle, fix config |\n")
            sections.append("| LFI | 6.0-8.1 | `../../etc/passwd` path traversal test | Path canonicalization, filter ../ chars |\n")
            sections.append("| RCE | 8.1-10.0 | Test deserialization, remote file include | Disable untrusted deserialization input |\n")
            sections.append("\n### A.3 Network Vulnerability Quick Reference\n\n")
            sections.append("| Vuln Type | CVSS Range | Quick Test | Key Fix |\n")
            sections.append("|-----------|-----------|------------|----------|\n")
            sections.append("| MITM | 7.0-7.6 | `ettercap -T`, arpspoof | ARP binding, 802.1X authentication |\n")
            sections.append("| DNS Hijacking | 7.0-8.1 | Check if DNS resolution is tampered | DNSSEC config, secure DNS service |\n")
            sections.append("| ARP Spoofing | 6.0-7.5 | `arpspoof -i eth0 -t target` | Static ARP table, switch MC隔离 |\n")
            sections.append("| Phishing | 5.0-7.0 | Fake page detection, social engineering | Security awareness training, email validation |\n")
            sections.append("\n### A.4 Info Disclosure Quick Reference\n\n")
            sections.append("| Vuln Type | CVSS Range | Quick Test | Key Fix |\n")
            sections.append("|-----------|-----------|------------|----------|\n")
            sections.append("| Sensitive File Disclosure | 4.0-7.5 | `ffuf -w wordlist -u target/FUZZ` scan sensitive paths | Disable directory browsing, remove sensitive files |\n")
            sections.append("| Debug Info Disclosure | 3.0-6.0 | Trigger error page, check stack trace | Disable debug mode in production |\n")
            sections.append("| Path Traversal | 6.0-8.1 | `../../etc/passwd`, `%2e%2e%2f` | Path normalization, whitelist restriction |\n")
            sections.append("| Source Code Disclosure | 5.0-8.0 | Git/SVN info gathering, `.git/config` | Block .git in web root |\n")
            sections.append("\n### A.5 Auth Vulnerability Quick Reference\n\n")
            sections.append("| Vuln Type | CVSS Range | Quick Test | Key Fix |\n")
            sections.append("|-----------|-----------|------------|----------|\n")
            sections.append("| Weak Password | 7.0-9.0 | `hydra -L users.txt -P passwords.txt ssh://target` | Strong password policy, account lockout |\n")
            sections.append("| Brute Force | 6.0-8.0 | Test if 5 failed logins lock account | Account lockout, CAPTCHA, rate limiting |\n")
            sections.append("| IDOR | 6.0-9.0 | Test if User A can access User B resources | Session-based auth, user ID validation |\n")
            sections.append("| Auth Bypass | 7.0-9.0 | Empty password, empty Session, Cookie forgery | Secure session, mandatory auth |\n")
            sections.append("\n### A.6 Config Vulnerability Quick Reference\n\n")
            sections.append("| Vuln Type | CVSS Range | Quick Test | Key Fix |\n")
            sections.append("|-----------|-----------|------------|----------|\n")
            sections.append("| Default Credentials | 7.0-9.0 | `searchsploit service`, manually try admin/admin | Must change default password on first deploy |\n")
            sections.append("| Missing Security Headers | 2.0-5.0 | `curl -I headers` | Configure X-Frame-Options/CSP/HSTS |\n")
            sections.append("| CORS Misconfiguration | 5.0-8.0 | Check if ACAO:* or overly permissive | Restrict origin domain, deny Credentials |\n")
            sections.append("\n## Appendix B - Complete Vulnerability Index\n\n")
            sections.append("| # | Category | Vuln Name | CVSS | CWE | OWASP | Test Tools |\n")
            sections.append("|---|----------|----------|------|-----|------|------------|\n")
            sections.append("| 1 | Web | SQL Injection | 9.8 | CWE-89 | A03:2021 | sqlmap, manual |\n")
            sections.append("| 2 | Web | Cross-Site Scripting (XSS) | 7.3 | CWE-79 | A03:2021 | BurpSuite, xsstrike |\n")
            sections.append("| 3 | Web | CSRF | 6.5 | CWE-352 | A01:2021 | BurpSuite CSRF Scanner |\n")
            sections.append("| 4 | Web | File Upload | 8.1 | CWE-434 | A03:2021 | manual, ffuf |\n")
            sections.append("| 5 | Web | SSRF | 8.6 | CWE-918 | A10:2021 | manual |\n")
            sections.append("| 6 | Web | SSTI | 9.8 | CWE-1336 | A03:2021 | manual |\n")
            sections.append("| 7 | Web | XXE | 9.1 | CWE-611 | A03:2021 | BurpSuite, digi.awk |\n")
            sections.append("| 8 | Web | Command Injection | 9.8 | CWE-77 | A03:2021 | manual, commix |\n")
            sections.append("| 9 | System | Buffer Overflow | 9.0 | CWE-119 | - | metasploit, gdb |\n")
            sections.append("| 10 | System | Privilege Escalation | 8.2 | CWE-269 | - | linpeas, winpeas |\n")
            sections.append("| 11 | System | Local File Inclusion | 7.8 | CWE-22 | A01:2021 | manual, ffuf |\n")
            sections.append("| 12 | System | Remote Code Execution | 10.0 | CWE-94 | A03:2021 | metasploit, manual |\n")
            sections.append("| 13 | System | Integer Overflow | 6.5 | CWE-190 | - | metasploit |\n")
            sections.append("| 14 | Network | MITM | 7.6 | CWE-300 | - | ettercap, wireshark |\n")
            sections.append("| 15 | Network | DNS Hijacking | 8.1 | CWE-327 | - | dig, nslookup |\n")
            sections.append("| 16 | Network | ARP Spoofing | 6.5 | CWE-322 | - | arpspoof, ettercap |\n")
            sections.append("| 17 | Network | Phishing | 6.5 | CWE-601 | A01:2021 | SET, social engineering |\n")
            sections.append("| 18 | Info | Sensitive File Disclosure | 5.3 | CWE-200 | A01:2021 | ffuf, dirb, metasploit |\n")
            sections.append("| 19 | Info | Debug Info Disclosure | 4.0 | CWE-11 | - | manual |\n")
            sections.append("| 20 | Info | Path Traversal | 7.5 | CWE-22 | A01:2021 | manual, ffuf |\n")
            sections.append("| 21 | Info | Source Code Disclosure | 7.5 | CWE-541 | A01:2021 | .git/, .svn/ scanner |\n")
            sections.append("| 22 | Auth | Weak Password | 8.1 | CWE-521 | A07:2021 | hydra, medusa |\n")
            sections.append("| 23 | Auth | Brute Force | 7.5 | CWE-307 | A07:2021 | hydra, BurpSuite |\n")
            sections.append("| 24 | Auth | Unauthorized Access (IDOR) | 7.5 | CWE-639 | A01:2021 | BurpSuite, manual |\n")
            sections.append("| 25 | Auth | Authentication Bypass | 8.0 | CWE-287 | A07:2021 | manual |\n")
            sections.append("| 26 | Config | Default Credentials | 8.0 | CWE-798 | A07:2021 | searchsploit, manual |\n")
            sections.append("| 27 | Config | Missing Security Headers | 3.0 | CWE-693 | A05:2021 | securityheaders.com |\n")
            sections.append("| 28 | Config | CORS Misconfiguration | 6.5 | CWE-942 | A05:2021 | manual, corsy |\n")
            sections.append("| 29 | Config | Cleartext Transmission | 7.5 | CWE-319 | A02:2021 | Wireshark, sslscan |\n")
            sections.append("| 30 | Config | Sensitive Data in URL | 5.3 | CWE-598 | A02:2021 | BurpSuite Proxy |\n")
            sections.append("| 31 | Config | Verbose Error Messages | 4.0 | CWE-209 | A05:2021 | manual |\n")
            return "".join(sections)

    def _get_results_summary(self, results):
        """Calculate summary statistics from results"""
        summary = {'total': len(results), 'high': 0, 'medium': 0, 'low': 0, 'info': 0}
        for r in results:
            sev = r.get('severity', 'info')
            if sev in summary:
                summary[sev] += 1
        return summary

    def generate(self, project_info, scan_results=None, authorized=True, templates=None, report_style='standard'):
        """
        Generate complete report

        Args:
            project_info: Project information dict
            scan_results: List of confirmed vulnerability results
            authorized: True for authorized report, False for template
            templates: List of template types to include for unauthorized mode
            report_style: Template style for unauthorized mode:
                          'standard' | 'executive' | 'checklist' | 'ctf' | 'full'

        Returns:
            Complete report as string (Markdown format)
        """
        parts = []

        # Header
        parts.append(self._generate_header(project_info, authorized, report_style))

        # Authorization page
        parts.append(self.add_authorization_page(project_info, authorized))
        parts.append("\n---\n")

        # Project info
        parts.append(self.add_project_info(project_info))
        parts.append("\n---\n")

        # Scan results or template sections
        if authorized:
            if scan_results:
                parts.append(self.add_scan_results(scan_results))
            else:
                parts.append(self._add_no_findings())
        else:
            # Unauthorized mode: template placeholders with style
            parts.append(self._get_template_style(report_style, templates))

        # Conclusion
        parts.append(self._generate_conclusion(project_info, scan_results, authorized, report_style))

        # Appendices
        parts.append(self._generate_appendix())

        return "\n".join(parts)

    def _generate_header(self, project_info, authorized, report_style='standard'):
        """Generate report header"""
        report_type_map = {
            'zh': {
                True: '渗透测试报告',
                False: {'standard': '渗透测试报告 - 模板版', 'executive': '执行摘要报告 - 模板版',
                        'checklist': '安全检查清单 - 模板版', 'ctf': 'CTF漏洞报告 - 模板版',
                        'full': '渗透测试报告 - 全模板版'}
            },
            'en': {
                True: 'Penetration Test Report',
                False: {'standard': 'Penetration Test Report - TEMPLATE', 'executive': 'Executive Summary Report - TEMPLATE',
                        'checklist': 'Security Checklist - TEMPLATE', 'ctf': 'CTF Vulnerability Report - TEMPLATE',
                        'full': 'Penetration Test Report - FULL TEMPLATE'}
            }
        }

        is_zh = self.language == 'zh'
        if authorized:
            report_type = report_type_map['zh'][True] if is_zh else report_type_map['en'][True]
        else:
            report_type = report_type_map['zh'][False].get(report_style, report_type_map['zh'][False]['standard'])
            if not is_zh:
                report_type = report_type_map['en'][False].get(report_style, report_type_map['en'][False]['standard'])

        emoji_map = {'standard': '', 'executive': '', 'checklist': '', 'ctf': '', 'full': ''}
        title = f"# {report_type}\n\n"
        title += f"**{project_info.get('name', 'N/A')}**\n\n"
        title += f"- {project_info.get('target', 'N/A')}\n"
        title += f"- {datetime.now().strftime('%Y-%m-%d')}\n\n"
        title += "---\n\n"

        return title

    def _generate_conclusion(self, project_info, results, authorized, report_style='standard'):
        """Generate conclusion section"""
        if self.language == 'zh':
            if authorized:
                return """## 结论 / Conclusion

### 安全评估总结

基于本次渗透测试结果，对目标系统的安全性评估如下：

{summary}

### 建议

1. 立即修复高危漏洞
2. 安排中危漏洞的修复计划
3. 持续监控系统安全状态
4. 定期进行安全评估

### 后续工作

- 漏洞修复后的复测
- 安全加固效果验证
- 定期巡检计划

---
*报告生成时间: {timestamp}*
*测试工程师: {engineer}*
""".format(
                    summary=self._generate_summary_text_zh(results),
                    timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    engineer=project_info.get('engineer', 'N/A')
                )
            else:
                return """## 结论 / Conclusion

### 安全评估总结

[在此填写安全评估总结]

### 建议

1. [建议1]
2. [建议2]
3. [建议3]

### 后续工作

- [ ] 漏洞修复后的复测
- [ ] 安全加固效果验证
- [ ] 定期巡检计划

---
*报告生成时间: {timestamp}*
*测试工程师: [工程师姓名]*
""".format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            if authorized:
                return """## Conclusion

### Security Assessment Summary

Based on the penetration test results, the security assessment of the target system is as follows:

{summary}

### Recommendations

1. Immediately remediate high-severity vulnerabilities
2. Schedule remediation for medium-severity vulnerabilities
3. Continuously monitor system security status
4. Conduct regular security assessments

### Follow-up Actions

- Retesting after vulnerability remediation
- Security hardening verification
- Regular inspection schedule

---
*Report generated: {timestamp}*
*Test Engineer: {engineer}*
""".format(
                    summary=self._generate_summary_text_en(results),
                    timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    engineer=project_info.get('engineer', 'N/A')
                )
            else:
                return """## Conclusion

### Security Assessment Summary

[Enter security assessment summary here]

### Recommendations

1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

### Follow-up Actions

- [ ] Retesting after vulnerability remediation
- [ ] Security hardening verification
- [ ] Regular inspection schedule

---
*Report generated: {timestamp}*
*Test Engineer: [Engineer Name]*
""".format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def _generate_summary_text_zh(self, results):
        """Generate Chinese summary text"""
        if not results:
            return "本次扫描未发现明显漏洞，系统基本安全。"

        high = sum(1 for r in results if r.get('severity') == 'high')
        medium = sum(1 for r in results if r.get('severity') == 'medium')
        low = sum(1 for r in results if r.get('severity') == 'low')

        summary = f"共发现 {len(results)} 个问题，其中高危 {high} 个，中危 {medium} 个，低危 {low} 个。"
        if high > 0:
            summary += "建议优先修复高危漏洞。"
        return summary

    def _generate_summary_text_en(self, results):
        """Generate English summary text"""
        if not results:
            return "No obvious vulnerabilities were found in this scan. The system is basically secure."

        high = sum(1 for r in results if r.get('severity') == 'high')
        medium = sum(1 for r in results if r.get('severity') == 'medium')
        low = sum(1 for r in results if r.get('severity') == 'low')

        summary = f"A total of {len(results)} issues were found, including {high} high, {medium} medium, and {low} low severity."
        if high > 0:
            summary += " High-severity vulnerabilities should be prioritized for remediation."
        return summary

    def _generate_appendix(self):
        """Generate appendix section"""
        if self.language == 'zh':
            return """## 附录 / Appendix

### A. 工具列表

| 工具 | 版本 | 用途 |
|------|------|------|
| Nmap | - | 端口扫描 |
| Nikto | - | Web漏洞扫描 |
| SQLMap | - | SQL注入检测 |

### B. 术语表

| 术语 | 英文 | 解释 |
|------|------|------|
| CVSS | Common Vulnerability Scoring System | 通用漏洞评分系统 |
| CVE | Common Vulnerabilities and Exposures | 通用漏洞披露 |
| POC | Proof of Concept | 概念验证 |

### C. 参考资料

1. OWASP Top 10
2. NIST Cybersecurity Framework
3. CVSS v3.1 Specification

---
*本报告结束 / End of Report*
"""
        else:
            return """## Appendix

### A. Tool List

| Tool | Version | Purpose |
|------|---------|---------|
| Nmap | - | Port Scanning |
| Nikto | - | Web Vulnerability Scanning |
| SQLMap | - | SQL Injection Detection |

### B. Glossary

| Term | Explanation |
|------|-------------|
| CVSS | Common Vulnerability Scoring System |
| CVE | Common Vulnerabilities and Exposures |
| POC | Proof of Concept |

### C. References

1. OWASP Top 10
2. NIST Cybersecurity Framework
3. CVSS v3.1 Specification

---
*End of Report*
"""

    def generate_markdown(self, project_info, scan_results=None, authorized=True, templates=None):
        """
        Generate Markdown format report (alias for generate)
        """
        return self.generate(project_info, scan_results, authorized, templates)

    def save_to_file(self, content, output_path):
        """Save report content to file"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(content, encoding='utf-8')
        return output_path


# Alias for backward compatibility
ReportGen = ReportBuilder
