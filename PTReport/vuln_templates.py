#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PTReport vuln_templates.py - 漏洞模板库 v1.0
包含30+常见渗透测试漏洞模板
"""

VULN_TEMPLATES = [
    # ========== Web 漏洞 ==========
    {
        'id': 'WEB-001',
        'name_zh': 'SQL注入',
        'name_en': 'SQL Injection',
        'severity': '高危',
        'cvss': 9.8,
        'category': 'Web',
        'description_zh': '通过用户输入拼接SQL语句，未使用参数化查询，攻击者可执行任意SQL命令',
        'description_en': 'User input is concatenated into SQL statements without parameterized queries, allowing attackers to execute arbitrary SQL commands',
        'detection_zh': [
            '1. 识别所有用户输入点（GET/POST参数、Cookie、Header）',
            '2. 尝试注入单引号、双引号、括号等特殊字符',
            '3. 观察错误信息或页面响应变化',
            '4. 使用UNION SELECT提取数据库版本和表结构',
            '5. 提取敏感数据或写入Webshell'
        ],
        'detection_en': [
            '1. Identify all user input points (GET/POST params, Cookie, Header)',
            '2. Try injecting single/double quotes, parentheses and special chars',
            '3. Observe error messages or page response changes',
            '4. Use UNION SELECT to extract DB version and table structure',
            '5. Extract sensitive data or write Webshell'
        ],
        'payload': "' OR '1'='1",
        'fix_zh': '使用参数化查询或ORM框架，禁止拼接用户输入到SQL语句',
        'fix_en': 'Use parameterized queries or ORM framework, never concatenate user input into SQL',
        'reference_url': 'https://owasp.org/www-community/attacks/SQL_Injection'
    },
    {
        'id': 'WEB-002',
        'name_zh': '跨站脚本攻击',
        'name_en': 'Cross-Site Scripting (XSS)',
        'severity': '中危',
        'cvss': 6.1,
        'category': 'Web',
        'description_zh': 'Web应用未对用户输入进行过滤，注入恶意JavaScript代码，可窃取Cookie、会话劫持',
        'description_en': 'Web application does not filter user input, allowing injection of malicious JavaScript to steal cookies or hijack sessions',
        'detection_zh': [
            '1. 识别所有输入点和输出点',
            '2. 尝试注入<script>alert(1)</script>',
            '3. 测试事件处理器如onerror、onload',
            '4. 验证Cookie的HttpOnly标记',
            '5. 编写POC验证会话劫持'
        ],
        'detection_en': [
            '1. Identify all input and output points',
            '2. Try injecting <script>alert(1)</script>',
            '3. Test event handlers like onerror, onload',
            '4. Verify Cookie HttpOnly flag',
            '5. Write POC to verify session hijacking'
        ],
        'payload': '<script>alert(document.cookie)</script>',
        'fix_zh': '对HTML特殊字符进行转义，使用Content-Security-Policy头',
        'fix_en': 'Escape HTML special characters, use Content-Security-Policy header',
        'reference_url': 'https://owasp.org/www-community/attacks/xss/'
    },
    {
        'id': 'WEB-003',
        'name_zh': '跨站请求伪造',
        'name_en': 'Cross-Site Request Forgery (CSRF)',
        'severity': '中危',
        'cvss': 6.8,
        'category': 'Web',
        'description_zh': '攻击者诱导已登录用户访问恶意页面，以受害者身份执行非预期操作',
        'description_en': 'Attacker induces logged-in user to visit malicious page, executing unintended actions on behalf of victim',
        'detection_zh': [
            '1. 检查关键操作是否验证CSRF Token',
            '2. 验证Token的随机性和唯一性',
            '3. 检查Referer/Origin头的有效性',
            '4. 构造恶意页面测试功能',
            '5. 检查是否使用SameSite Cookie'
        ],
        'detection_en': [
            '1. Check if critical operations validate CSRF Token',
            '2. Verify Token randomness and uniqueness',
            '3. Check有效性 of Referer/Origin headers',
            '4. Construct malicious page to test functionality',
            '5. Check if SameSite Cookie is used'
        ],
        'payload': '<img src="http://target.com/change_email?email=attacker@evil.com">',
        'fix_zh': '添加CSRF Token，验证Referer/Origin，使用SameSite=Strict Cookie',
        'fix_en': 'Add CSRF Token, validate Referer/Origin, use SameSite=Strict Cookie',
        'reference_url': 'https://owasp.org/www-community/attacks/csrf'
    },
    {
        'id': 'WEB-004',
        'name_zh': '服务器端请求伪造',
        'name_en': 'Server-Side Request Forgery (SSRF)',
        'severity': '高危',
        'cvss': 8.6,
        'category': 'Web',
        'description_zh': '服务端接受用户控制的URL参数，访问内部系统或云元数据服务',
        'description_en': 'Server accepts user-controlled URL parameter, allowing access to internal systems or cloud metadata services',
        'detection_zh': [
            '1. 识别接受URL作为参数的接口',
            '2. 测试访问内网IP（127.0.0.1、10.0.0.0/8）',
            '3. 尝试访问云元数据服务（169.254.169.254）',
            '4. 测试file://、dict://等协议',
            '5. 探测内部服务端口和路径'
        ],
        'detection_en': [
            '1. Identify endpoints accepting URL parameters',
            '2. Test access to internal IPs (127.0.0.1, 10.0.0.0/8)',
            '3. Try accessing cloud metadata service (169.254.169.254)',
            '4. Test protocols like file://, dict://',
            '5. Probe internal service ports and paths'
        ],
        'payload': 'http://127.0.0.1:80/admin',
        'fix_zh': '限制允许访问的域名/IP，使用URL解析库验证，避免用户输入进入URL构造',
        'fix_en': 'Restrict allowed domains/IPs, use URL parsing library for validation, avoid user input in URL construction',
        'reference_url': 'https://owasp.org/www-community/attacks/Server_Side_Request_Forgery'
    },
    {
        'id': 'WEB-005',
        'name_zh': 'XML外部实体注入',
        'name_en': 'XML External Entity (XXE)',
        'severity': '高危',
        'cvss': 7.5,
        'category': 'Web',
        'description_zh': 'XML解析器允许加载外部实体，攻击者可读取本地文件或发起SSRF攻击',
        'description_en': 'XML parser allows loading external entities, attacker can read local files or launch SSRF attacks',
        'detection_zh': [
            '1. 识别接受XML格式数据的接口',
            '2. 注入<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>',
            '3. 使用XXE读取敏感文件',
            '4. 尝试利用XXE进行端口探测',
            '5. 检查WAF是否拦截明显XXE payload'
        ],
        'detection_en': [
            '1. Identify endpoints accepting XML format data',
            '2. Inject <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>',
            '3. Use XXE to read sensitive files',
            '4. Try using XXE for port scanning',
            '5. Check if WAF blocks obvious XXE payloads'
        ],
        'payload': '<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>',
        'fix_zh': '禁用XML外部实体解析，使用安全的XML解析器配置',
        'fix_en': 'Disable XML external entity resolution, use secure XML parser configuration',
        'reference_url': 'https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing'
    },
    {
        'id': 'WEB-006',
        'name_zh': '服务端模板注入',
        'name_en': 'Server-Side Template Injection (SSTI)',
        'severity': '高危',
        'cvss': 8.5,
        'category': 'Web',
        'description_zh': '用户输入被直接拼接到模板中，攻击者可执行模板引擎任意代码',
        'description_en': 'User input is directly concatenated into templates, attacker can execute arbitrary template engine code',
        'detection_zh': [
            '1. 识别使用模板引擎的页面',
            '2. 注入{{7*7}}测试是否执行',
            '3. 使用Twig或Jinja2的调试语法',
            '4. 尝试{{constructor}}或__subclasses__',
            '5. 写入Webshell或读取文件'
        ],
        'detection_en': [
            '1. Identify pages using template engines',
            '2. Inject {{7*7}} to test execution',
            '3. Use Twig or Jinja2 debug syntax',
            '4. Try {{constructor}} or __subclasses__',
            '5. Write Webshell or read files'
        ],
        'payload': '{{7*7}}',
        'fix_zh': '不将用户输入直接拼入模板，使用模板沙箱',
        'fix_en': 'Never concatenate user input directly into templates, use template sandbox',
        'reference_url': 'https://portswigger.net/web-security/server-side-template-injection'
    },
    {
        'id': 'WEB-007',
        'name_zh': '任意文件上传',
        'name_en': 'Unrestricted File Upload',
        'severity': '高危',
        'cvss': 8.1,
        'category': 'Web',
        'description_zh': '文件上传功能未验证文件类型和内容，攻击者可上传恶意脚本获得服务器权限',
        'description_en': 'File upload function does not validate file type and content, attacker can upload malicious scripts to gain server access',
        'detection_zh': [
            '1. 识别所有文件上传点',
            '2. 尝试上传合法图片马',
            '3. 绕过Content-Type验证',
            '4. 尝试上传.php/.jsp/.asp webshell',
            '5. 访问上传文件执行命令'
        ],
        'detection_en': [
            '1. Identify all file upload points',
            '2. Try uploading legitimate image with malware',
            '3. Bypass Content-Type validation',
            '4. Try uploading .php/.jsp/.asp webshell',
            '5. Access uploaded file to execute commands'
        ],
        'payload': '<?php system($_GET["cmd"]); ?>',
        'fix_zh': '验证文件扩展名、MIME类型、内容头，重命名上传文件，限制上传目录执行权限',
        'fix_en': 'Validate file extension, MIME type, content headers, rename uploaded files, restrict upload directory execution',
        'reference_url': 'https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload'
    },
    {
        'id': 'WEB-008',
        'name_zh': '不安全的直接对象引用',
        'name_en': 'Insecure Direct Object Reference (IDOR)',
        'severity': '中危',
        'cvss': 6.5,
        'category': 'Web',
        'description_zh': '应用直接使用用户输入访问对象，未验证用户是否有权访问该对象',
        'description_en': 'Application directly uses user input to access objects without verifying user permission',
        'detection_zh': [
            '1. 识别使用ID（如user_id、file_id）访问资源的接口',
            '2. 抓包修改ID参数值为其他用户ID',
            '3. 检查是否返回了他人的敏感数据',
            '4. 测试ID遍历访问',
            '5. 验证是否有权限验证逻辑'
        ],
        'detection_en': [
            '1. Identify endpoints using IDs (user_id, file_id) to access resources',
            '2. Capture and modify ID parameter to other user IDs',
            '3. Check if sensitive data of others is returned',
            '4. Test ID traversal access',
            '5. Verify if there is permission validation logic'
        ],
        'payload': '/profile/user_id=123 -> /profile/user_id=124',
        'fix_zh': '实现对象级访问控制，使用间接引用映射，避免直接暴露内部ID',
        'fix_en': 'Implement object-level access control, use indirect reference mapping, avoid exposing internal IDs',
        'reference_url': 'https://owasp.org/www-community/attacks/Insecure_Direct_Object_Reference'
    },
    {
        'id': 'WEB-009',
        'name_zh': '本地文件包含',
        'name_en': 'Local File Inclusion (LFI)',
        'severity': '高危',
        'cvss': 7.5,
        'category': 'Web',
        'description_zh': '应用使用用户输入构建文件路径，未进行严格验证，可读取任意本地文件',
        'description_en': 'Application uses user input to construct file paths without strict validation, can read arbitrary local files',
        'detection_zh': [
            '1. 识别路径遍历参数（如?page=, ?file=, ?include=）',
            '2. 尝试使用../遍历读取/etc/passwd',
            '3. 测试NULL字节截断（%00）',
            '4. 利用日志文件注入PHP代码',
            '5. 尝试远程文件包含'
        ],
        'detection_en': [
            '1. Identify path traversal parameters (?page=, ?file=, ?include=)',
            '2. Try using ../ to traverse and read /etc/passwd',
            '3. Test NULL byte truncation (%00)',
            '4. Inject PHP code via log files',
            '5. Try remote file inclusion'
        ],
        'payload': '../../../etc/passwd',
        'fix_zh': '严格验证文件路径，禁止../，使用白名单，禁用远程文件包含',
        'fix_en': 'Strictly validate file paths, block ../, use whitelist, disable remote file inclusion',
        'reference_url': 'https://owasp.org/www-community/vulnerabilities/Path_Traversal'
    },
    {
        'id': 'WEB-010',
        'name_zh': '远程代码执行',
        'name_en': 'Remote Code Execution (RCE)',
        'severity': '严重',
        'cvss': 9.8,
        'category': 'Web',
        'description_zh': '应用存在命令注入或代码注入漏洞，攻击者可在服务器上执行任意命令',
        'description_en': 'Application has command injection or code injection vulnerability, attacker can execute arbitrary commands on server',
        'detection_zh': [
            '1. 识别命令执行函数（system, exec, shell_exec）',
            '2. 测试管道符（|,&,;,`$()`）注入',
            '3. 尝试Sleep命令验证注入',
            '4. 使用Wget或Curl下载并执行后门',
            '5. 反弹Shell获得持久访问'
        ],
        'detection_en': [
            '1. Identify command execution functions (system, exec, shell_exec)',
            '2. Test pipe operator (|,&,;,`$()`) injection',
            '3. Try Sleep command to verify injection',
            '4. Use Wget or Curl to download and execute backdoor',
            '5. Reverse Shell for persistent access'
        ],
        'payload': '; cat /etc/passwd',
        'fix_zh': '避免使用命令执行函数，对用户输入严格过滤和验证',
        'fix_en': 'Avoid using command execution functions, strictly filter and validate user input',
        'reference_url': 'https://owasp.org/www-community/attacks/Command_Injection'
    },
    # ========== Network 漏洞 ==========
    {
        'id': 'NET-001',
        'name_zh': '开放端口服务',
        'name_en': 'Open Port Service',
        'severity': '信息',
        'cvss': 0.0,
        'category': 'Network',
        'description_zh': '主机开放了不必要的端口和服务，增加了攻击面',
        'description_en': 'Host has unnecessary ports and services open, increasing attack surface',
        'detection_zh': [
            '1. 使用Nmap进行端口扫描（-p-全端口）',
            '2. 识别开放端口对应的服务',
            '3. 探测服务版本信息',
            '4. 检查是否为必要服务',
            '5. 检查是否有老旧或漏洞版本'
        ],
        'detection_en': [
            '1. Use Nmap for port scanning (-p- full port)',
            '2. Identify services corresponding to open ports',
            '3. Probe service version information',
            '4. Check if it is a necessary service',
            '5. Check for old or vulnerable versions'
        ],
        'payload': 'nmap -sV -p- 192.168.1.1',
        'fix_zh': '关闭不必要的端口和服务，使用防火墙限制访问',
        'fix_en': 'Close unnecessary ports and services, use firewall to restrict access',
        'reference_url': 'https://nmap.org/'
    },
    {
        'id': 'NET-002',
        'name_zh': '弱SSL/TLS配置',
        'name_en': 'Weak SSL/TLS Configuration',
        'severity': '中危',
        'cvss': 5.3,
        'category': 'Network',
        'description_zh': 'SSL/TLS配置允许使用弱加密算法或过时的协议版本，存在中间人攻击风险',
        'description_en': 'SSL/TLS configuration allows weak encryption algorithms or outdated protocol versions, MITM attack risk',
        'detection_zh': [
            '1. 使用SSLyze或testssl.sh扫描SSL配置',
            '2. 检查支持的协议版本（SSLv2/SSLv3）',
            '3. 检查弱加密算法（MD5, RC4）',
            '4. 检查证书有效性',
            '5. 测试是否存在填充漏洞'
        ],
        'detection_en': [
            '1. Use SSLyze or testssl.sh to scan SSL configuration',
            '2. Check supported protocol versions (SSLv2/SSLv3)',
            '3. Check weak encryption algorithms (MD5, RC4)',
            '4. Check certificate validity',
            '5. Test for padding vulnerabilities'
        ],
        'payload': 'testssl.sh https://target.com',
        'fix_zh': '禁用SSLv2/SSLv3，使用TLS 1.2+，启用强加密套件',
        'fix_en': 'Disable SSLv2/SSLv3, use TLS 1.2+, enable strong cipher suites',
        'reference_url': 'https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/09-Testing_for_Weak_Cryptography/01-Testing_for_Weak_SSL_TLS_Ciphers'
    },
    {
        'id': 'NET-003',
        'name_zh': 'DNS区域传送',
        'name_en': 'DNS Zone Transfer',
        'severity': '中危',
        'cvss': 5.3,
        'category': 'Network',
        'description_zh': 'DNS服务器允许任意AXFR请求，攻击者可获取整个域名的完整记录',
        'description_en': 'DNS server allows arbitrary AXFR requests, attacker can obtain complete records of entire domain',
        'detection_zh': [
            '1. 识别DNS服务器地址',
            '2. 使用dig axfr @dns_server target.com',
            '3. 检查是否返回完整zone数据',
            '4. 枚举所有子域名和内网IP',
            '5. 分析获取的信息用于进一步攻击'
        ],
        'detection_en': [
            '1. Identify DNS server addresses',
            '2. Use dig axfr @dns_server target.com',
            '3. Check if complete zone data is returned',
            '4. Enumerate all subdomains and internal IPs',
            '5. Analyze obtained information for further attacks'
        ],
        'payload': 'dig axfr @10.0.0.1 target.com',
        'fix_zh': '限制DNS区域传送来源IP，使用TSIG密钥验证',
        'fix_en': 'Restrict DNS zone transfer source IPs, use TSIG key authentication',
        'reference_url': 'https://owasp.org/www-community/attacks/DNS_Hijacking'
    },
    {
        'id': 'NET-004',
        'name_zh': 'SMTP开放转发',
        'name_en': 'SMTP Open Relay',
        'severity': '中危',
        'cvss': 5.3,
        'category': 'Network',
        'description_zh': '邮件服务器允许开放转发，可被用于发送垃圾邮件或钓鱼邮件',
        'description_en': 'Mail server allows open relay, can be used to send spam or phishing emails',
        'detection_zh': [
            '1. 扫描25/465/587端口识别SMTP服务',
            '2. 使用telnet测试邮件发送',
            '3. 尝试匿名发送邮件测试',
            '4. 检查是否需要认证',
            '5. 验证转发限制策略'
        ],
        'detection_en': [
            '1. Scan port 25/465/587 to identify SMTP service',
            '2. Use telnet to test email sending',
            '3. Try anonymous email sending test',
            '4. Check if authentication is required',
            '5. Verify relay restriction policy'
        ],
        'payload': 'telnet smtp.target.com 25\nMAIL FROM:<test@target.com>\nRCPT TO:<victim@external.com>',
        'fix_zh': '配置SMTP认证，限制转发来源IP，使用SPF/DKIM/DMARC',
        'fix_en': 'Configure SMTP authentication, restrict relay source IPs, use SPF/DKIM/DMARC',
        'reference_url': 'https://tools.ietf.org/html/rfcRFC-2821'
    },
    # ========== System 漏洞 ==========
    {
        'id': 'SYS-001',
        'name_zh': '弱口令',
        'name_en': 'Weak Password',
        'severity': '高危',
        'cvss': 7.5,
        'category': 'System',
        'description_zh': '系统或服务使用弱口令或默认口令，可被暴力破解或猜测',
        'description_en': 'System or service uses weak or default passwords, can be brute forced or guessed',
        'detection_zh': [
            '1. 识别所有需要认证的服务',
            '2. 使用常见弱口令字典尝试登录',
            '3. 尝试默认口令',
            '4. 使用Hydra进行暴力破解',
            '5. 检查密码策略复杂度要求'
        ],
        'detection_en': [
            '1. Identify all services requiring authentication',
            '2. Try common weak passwords dictionary',
            '3. Try default passwords',
            '4. Use Hydra for brute force attacks',
            '5. Check password policy complexity requirements'
        ],
        'payload': 'hydra -l admin -p password 192.168.1.1 ssh',
        'fix_zh': '强制使用强密码策略，限制登录失败次数，使用多因素认证',
        'fix_en': 'Enforce strong password policy, limit login failures, use multi-factor authentication',
        'reference_url': 'https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/02-Testing_for_Weak_Lock_Out_Mechanism'
    },
    {
        'id': 'SYS-002',
        'name_zh': '默认凭证',
        'name_en': 'Default Credential',
        'severity': '高危',
        'cvss': 8.0,
        'category': 'System',
        'description_zh': '系统或应用使用出厂默认用户名密码，未修改',
        'description_en': 'System or application uses factory default username/password, not changed',
        'detection_zh': [
            '1. 识别应用类型和版本',
            '2. 查找该应用的默认凭证列表',
            '3. 尝试常见默认口令组合',
            '4. 检查是否有强制首次登录修改',
            '5. 测试是否允许重复使用默认口令'
        ],
        'detection_en': [
            '1. Identify application type and version',
            '2. Find default credential list for this application',
            '3. Try common default password combinations',
            '4. Check if forced to change on first login',
            '5. Test if default passwords can be reused'
        ],
        'payload': 'admin/admin, admin/password, root/root',
        'fix_zh': '首次部署强制修改默认密码，建立密码管理流程',
        'fix_en': 'Force default password change on first deployment, establish password management process',
        'reference_url': 'https://www.cvedetails.com/google-web-site/Global-Device-Default-Credentials.html'
    },
    {
        'id': 'SYS-003',
        'name_zh': '权限提升',
        'name_en': 'Privilege Escalation',
        'severity': '高危',
        'cvss': 7.8,
        'category': 'System',
        'description_zh': '攻击者利用漏洞或配置缺陷获得比原账号更高的系统权限',
        'description_en': 'Attacker exploits vulnerability or misconfiguration to gain higher system privileges than original account',
        'detection_zh': [
            '1. 收集系统信息（OS版本、内核版本）',
            '2. 检查Sudo配置（sudo -l）',
            '3. 查找具有SUID权限的文件',
            '4. 检查计划任务和启动服务',
            '5. 使用LinPEAS或WinPEAS自动化检测'
        ],
        'detection_en': [
            '1. Collect system info (OS version, kernel version)',
            '2. Check Sudo configuration (sudo -l)',
            '3. Find files with SUID permission',
            '4. Check scheduled tasks and startup services',
            '5. Use LinPEAS or WinPEAS for automated detection'
        ],
        'payload': 'sudo -l\nfind / -perm -4000 2>/dev/null',
        'fix_zh': '及时打补丁，遵循最小权限原则，限制SUID文件，定期安全审计',
        'fix_en': 'Keep patches updated, follow least privilege principle, restrict SUID files, regular security audits',
        'reference_url': 'https://blog.pentestgreets.com/p/privesc.html'
    },
    {
        'id': 'SYS-004',
        'name_zh': 'Sudo劫持',
        'name_en': 'Sudo Hijacking',
        'severity': '高危',
        'cvss': 7.5,
        'category': 'System',
        'description_zh': '攻击者通过修改Sudo相关环境变量或配置文件，窃取其他用户sudo权限',
        'description_en': 'Attacker steals other users sudo privileges by modifying sudo-related environment variables or config files',
        'detection_zh': [
            '1. 检查sudoers文件权限和内容',
            '2. 检查恶意alias或环境变量',
            '3. 检查PATH劫持（ls, cd等命令重写）',
            '4. 分析/etc/sudoers.d/目录',
            '5. 验证LD_PRELOAD劫持'
        ],
        'detection_en': [
            '1. Check sudoers file permissions and content',
            '2. Check for malicious aliases or environment variables',
            '3. Check PATH hijacking (ls, cd command rewriting)',
            '4. Analyze /etc/sudoers.d/ directory',
            '5. Verify LD_PRELOAD hijacking'
        ],
        'payload': 'export PATH=/tmp:$PATH\nalias sudo=/tmp/sudo',
        'fix_zh': '使用secure_path，锁定sudoers文件，禁用LD_PRELOAD',
        'fix_en': 'Use secure_path, lock sudoers file, disable LD_PRELOAD',
        'reference_url': 'https://www.sudo.ws/security/advisories/'
    },
    # ========== Information Disclosure ==========
    {
        'id': 'INFO-001',
        'name_zh': '信息泄露',
        'name_en': 'Information Disclosure',
        'severity': '低危',
        'cvss': 4.0,
        'category': 'Info',
        'description_zh': '系统或应用通过错误信息、注释、调试功能等途径泄露敏感信息',
        'description_en': 'System or application leaks sensitive information through error messages, comments, debug features, etc.',
        'detection_zh': [
            '1. 触发应用错误观察错误信息',
            '2. 检查HTML/JS源码中的敏感注释',
            '3. 扫描敏感文件（.git, .env, config.*）',
            '4. 使用爬虫遍历所有页面',
            '5. 检查HTTP头泄露的版本信息'
        ],
        'detection_en': [
            '1. Trigger application errors to observe error messages',
            '2. Check sensitive comments in HTML/JS source',
            '3. Scan sensitive files (.git, .env, config.*)',
            '4. Use crawler to traverse all pages',
            '5. Check version info leaked in HTTP headers'
        ],
        'payload': 'dirb http://target.com -r\nnikto -h target.com',
        'fix_zh': '生产环境关闭调试模式，统一错误处理，删除敏感注释和文件',
        'fix_en': 'Disable debug mode in production, unified error handling, remove sensitive comments and files',
        'reference_url': 'https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/01-Conduct_Search_Engine_Discovery_Reconnaissance_for_Web_Application_Content'
    },
    {
        'id': 'INFO-002',
        'name_zh': '调试模式开启',
        'name_en': 'Debug Mode Enabled',
        'severity': '中危',
        'cvss': 5.0,
        'category': 'Info',
        'description_zh': '生产环境开启了调试模式，泄露详细错误信息和代码路径',
        'description_en': 'Debug mode enabled in production environment, leaking detailed error information and code paths',
        'detection_zh': [
            '1. 检查?debug=true或?debug=1参数',
            '2. 检查X-Debug或X-Audit-Trail头',
            '3. 观察错误页面是否显示堆栈跟踪',
            '4. 检查.env文件DEBUG=true',
            '5. 查找debug.log或trace.log文件'
        ],
        'detection_en': [
            '1. Check ?debug=true or ?debug=1 parameters',
            '2. Check X-Debug or X-Audit-Trail headers',
            '3. Observe if error pages show stack trace',
            '4. Check .env file DEBUG=true',
            '5. Find debug.log or trace.log files'
        ],
        'payload': '?debug=true\nX-Debug: 1',
        'fix_zh': '生产环境关闭所有调试功能，使用生产配置文件',
        'fix_en': 'Disable all debug features in production, use production config files',
        'reference_url': 'https://owasp.org/www-community/vulnerabilities/Information_exposure_through_query_strings_in_url'
    },
    {
        'id': 'INFO-003',
        'name_zh': '备份文件泄露',
        'name_en': 'Backup Files Exposure',
        'severity': '中危',
        'cvss': 5.0,
        'category': 'Info',
        'description_zh': 'Web服务器配置不当，泄露了.bak、.old、.zip等备份文件',
        'description_en': 'Web server misconfigured, exposing .bak, .old, .zip and other backup files',
        'detection_zh': [
            '1. 使用DirBuster或ffuf枚举备份文件',
            '2. 尝试常见备份文件扩展名',
            '3. 识别整站备份文件',
            '4. 下载并分析备份文件内容',
            '5. 查找数据库备份文件'
        ],
        'detection_en': [
            '1. Use DirBuster or ffuf to enumerate backup files',
            '2. Try common backup file extensions',
            '3. Identify full site backup files',
            '4. Download and analyze backup file contents',
            '5. Find database backup files'
        ],
        'payload': 'ffuf -w wordlist.txt -u http://target.com/FUZZ.bak',
        'fix_zh': '禁止Web服务器索引备份文件目录，及时清理备份文件',
        'fix_en': 'Prevent web server from indexing backup file directories, clean up backup files promptly',
        'reference_url': 'https://owasp.org/www-community/attacks/Path_Traversal'
    },
    {
        'id': 'INFO-004',
        'name_zh': 'Git/SVN源码泄露',
        'name_en': 'Git/SVN Source Exposure',
        'severity': '高危',
        'cvss': 6.5,
        'category': 'Info',
        'description_zh': '.git或.svn目录可通过Web访问，泄露完整源码和提交历史',
        'description_en': '.git or .svn directory accessible via web, leaking complete source code and commit history',
        'detection_zh': [
            '1. 访问http://target.com/.git/config',
            '2. 使用GitHacker或svn-extractor工具',
            '3. 还原完整源码和历史版本',
            '4. 分析源码寻找其他漏洞',
            '5. 查找数据库连接密码等敏感信息'
        ],
        'detection_en': [
            '1. Access http://target.com/.git/config',
            '2. Use GitHacker or svn-extractor tools',
            '3. Restore complete source code and historical versions',
            '4. Analyze source code for other vulnerabilities',
            '5. Find sensitive info like database connection passwords'
        ],
        'payload': 'python GitHacker.py http://target.com/.git/',
        'fix_zh': '配置Web服务器禁止访问.git和.svn目录，使用.gitignore排除',
        'fix_en': 'Configure web server to deny access to .git and .svn directories, use .gitignore to exclude',
        'reference_url': 'https://github.com/WangWenQian123/PentestSuite/tree/master/GitHacker'
    },
    {
        'id': 'INFO-005',
        'name_zh': 'robots.txt泄露',
        'name_en': 'robots.txt Information Disclosure',
        'severity': '信息',
        'cvss': 0.0,
        'category': 'Info',
        'description_zh': 'robots.txt文件暴露了敏感目录和文件路径',
        'description_en': 'robots.txt file exposes sensitive directory and file paths',
        'detection_zh': [
            '1. 获取http://target.com/robots.txt',
            '2. 分析Disallow列表识别敏感路径',
            '3. 访问所有Disallow的路径',
            '4. 查找管理后台、API端点等',
            '5. 结合其他漏洞进行利用'
        ],
        'detection_en': [
            '1. Fetch http://target.com/robots.txt',
            '2. Analyze Disallow list to identify sensitive paths',
            '3. Visit all disallowed paths',
            '4. Find admin panels, API endpoints, etc.',
            '5. Combine with other vulnerabilities for exploitation'
        ],
        'payload': 'curl http://target.com/robots.txt',
        'fix_zh': 'robots.txt不要列出真正的敏感路径，或使用meta robots标签保护',
        'fix_en': 'Do not list truly sensitive paths in robots.txt, or use meta robots tag for protection',
        'reference_url': 'https://developers.google.com/search/docs/crawling/indexing-data'
    },
    # ========== Authentication Issues ==========
    {
        'id': 'AUTH-001',
        'name_zh': '会话固定',
        'name_en': 'Session Fixation',
        'severity': '中危',
        'cvss': 6.0,
        'category': 'Auth',
        'description_zh': '应用在登录前后使用相同的会话ID，攻击者可劫持用户会话',
        'description_en': 'Application uses same session ID before and after login, attacker can hijack user session',
        'detection_zh': [
            '1. 登录前获取会话ID',
            '2. 完成登录操作',
            '3. 检查会话ID是否改变',
            '4. 如ID未变则存在会话固定漏洞',
            '5. 使用固定会话ID测试访问'
        ],
        'detection_en': [
            '1. Get session ID before login',
            '2. Complete login operation',
            '3. Check if session ID changed',
            '4. If ID unchanged, session fixation vulnerability exists',
            '5. Use fixed session ID to test access'
        ],
        'payload': '登录前: Cookie: SESSIONID=attacker_set\n登录后: 同一SESSIONID仍有效',
        'fix_zh': '用户登录成功后重新生成会话ID，限制会话ID长度和随机性',
        'fix_en': 'Regenerate session ID after user login, limit session ID length and randomness',
        'reference_url': 'https://owasp.org/www-community/attacks/Session_fixation'
    },
    {
        'id': 'AUTH-002',
        'name_zh': 'JWT弱密钥',
        'name_en': 'JWT Weak Secret',
        'severity': '高危',
        'cvss': 7.4,
        'category': 'Auth',
        'description_zh': 'JWT使用弱密钥或空密钥，攻击者可伪造任意用户身份',
        'description_en': 'JWT uses weak or empty secret key, attacker can forge arbitrary user identities',
        'detection_zh': [
            '1. 获取JWT token',
            '2. 分析JWT结构（header.payload.signature）',
            '3. 提取alg字段检查算法类型',
            '4. 使用hashcat或jwt_tool尝试破解密钥',
            '5. 伪造admin权限的token'
        ],
        'detection_en': [
            '1. Get JWT token',
            '2. Analyze JWT structure (header.payload.signature)',
            '3. Extract alg field to check algorithm type',
            '4. Use hashcat or jwt_tool to try cracking secret',
            '5. Forge token with admin privileges'
        ],
        'payload': 'python jwt_tool.py <JWT_TOKEN> -C -d dict.txt',
        'fix_zh': '使用强密钥（256位），避免使用none算法，定期轮换密钥',
        'fix_en': 'Use strong secret (256 bits), avoid none algorithm, rotate keys regularly',
        'reference_url': 'https://owasp.org/www-community/vulnerabilities/Using_a_broken_or_risky_cryptographic_algorithm'
    },
    {
        'id': 'AUTH-003',
        'name_zh': 'OAuth配置错误',
        'name_en': 'OAuth Misconfiguration',
        'severity': '高危',
        'cvss': 7.5,
        'category': 'Auth',
        'description_zh': 'OAuth实现存在配置错误，可导致账户接管或敏感信息泄露',
        'description_en': 'OAuth implementation has configuration errors, can lead to account takeover or sensitive info disclosure',
        'detection_zh': [
            '1. 检查redirect_uri是否被验证',
            '2. 测试Scope权限范围',
            '3. 尝试劫持授权码',
            '4. 检查state参数是否随机',
            '5. 测试CSRF攻击OAuth绑定'
        ],
        'detection_en': [
            '1. Check if redirect_uri is validated',
            '2. Test Scope permission range',
            '3. Try hijacking authorization code',
            '4. Check if state parameter is random',
            '5. Test CSRF attack on OAuth binding'
        ],
        'payload': 'redirect_uri=https://attacker.com/callback',
        'fix_zh': '严格验证redirect_uri，使用随机state参数，限制scope权限',
        'fix_en': 'Strictly validate redirect_uri, use random state parameter, restrict scope permissions',
        'reference_url': 'https://oauth.net/2/cross-site-request-forgery/'
    },
    {
        'id': 'AUTH-004',
        'name_zh': '双因素认证绕过',
        'name_en': '2FA Bypass',
        'severity': '高危',
        'cvss': 7.2,
        'category': 'Auth',
        'description_zh': '双因素认证存在逻辑漏洞，可被绕过或劫持',
        'description_en': 'Two-factor authentication has logic vulnerabilities, can be bypassed or hijacked',
        'detection_zh': [
            '1. 测试2FA码是否可暴力破解',
            '2. 检查是否存在备用验证通道',
            '3. 测试Session覆盖攻击',
            '4. 检查验证失败后的处理逻辑',
            '5. 尝试钓鱼绕过2FA'
        ],
        'detection_en': [
            '1. Test if 2FA code can be brute forced',
            '2. Check for alternative verification channels',
            '3. Test session override attack',
            '4. Check validation failure handling logic',
            '5. Try phishing to bypass 2FA'
        ],
        'payload': '使用Responder拦截NTLMv2哈希\n或尝试暴力破解6位验证码',
        'fix_zh': '限制验证尝试次数，绑定设备指纹，启用异常登录提醒',
        'fix_en': 'Limit verification attempts, bind device fingerprint, enable abnormal login alerts',
        'reference_url': 'https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/04-Testing_for_Weakness_in_Two-Factor_Authentication'
    },
    # ========== Configuration Issues ==========
    {
        'id': 'CFG-001',
        'name_zh': 'CORS配置错误',
        'name_en': 'CORS Misconfiguration',
        'severity': '中危',
        'cvss': 6.5,
        'category': 'Config',
        'description_zh': 'CORS配置允许任意域名访问，可导致敏感数据被跨域窃取',
        'description_en': 'CORS configuration allows arbitrary domains to access, can lead to cross-domain theft of sensitive data',
        'detection_zh': [
            '1. 检查Access-Control-Allow-Origin头',
            '2. 测试是否设置为*或null',
            '3. 检查是否信任子域名',
            '4. 检查Access-Control-Allow-Credentials',
            '5. 构造恶意页面测试数据窃取'
        ],
        'detection_en': [
            '1. Check Access-Control-Allow-Origin header',
            '2. Test if set to * or null',
            '3. Check if subdomains are trusted',
            '4. Check Access-Control-Allow-Credentials',
            '5. Construct malicious page to test data theft'
        ],
        'payload': 'Origin: https://attacker.com\n检查是否返回Access-Control-Allow-Origin: https://attacker.com',
        'fix_zh': '明确指定允许的Origin名单，避免使用*，验证Origin头',
        'fix_en': 'Explicitly specify allowed Origin list, avoid using *, validate Origin header',
        'reference_url': 'https://owasp.org/www-community/attacks/CORS_OriginHeaderScrutiny'
    },
    {
        'id': 'CFG-002',
        'name_zh': '安全头缺失',
        'name_en': 'Missing Security Headers',
        'severity': '低危',
        'cvss': 4.0,
        'category': 'Config',
        'description_zh': 'HTTP响应缺少安全相关响应头，降低了防御XSS、点击劫持等攻击的能力',
        'description_en': 'HTTP response missing security-related headers, reducing defense against XSS, clickjacking attacks',
        'detection_zh': [
            '1. 检查是否设置Content-Security-Policy',
            '2. 检查X-Frame-Options防止点击劫持',
            '3. 检查X-Content-Type-Options',
            '4. 检查Strict-Transport-Security',
            '5. 使用securityheaders.com分析'
        ],
        'detection_en': [
            '1. Check if Content-Security-Policy is set',
            '2. Check X-Frame-Options to prevent clickjacking',
            '3. Check X-Content-Type-Options',
            '4. Check Strict-Transport-Security',
            '5. Use securityheaders.com to analyze'
        ],
        'payload': 'curl -I http://target.com\n检查响应头中是否包含安全头',
        'fix_zh': '配置完整的安全响应头，包括CSP、X-Frame-Options、HSTS等',
        'fix_en': 'Configure complete security response headers including CSP, X-Frame-Options, HSTS, etc.',
        'reference_url': 'https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/03-Review_Webpage_Content_and_Configuration'
    },
    {
        'id': 'CFG-003',
        'name_zh': 'HTTP Banner泄露',
        'name_en': 'HTTP Banner Disclosure',
        'severity': '信息',
        'cvss': 0.0,
        'category': 'Config',
        'description_zh': 'HTTP响应头泄露服务器类型和版本信息',
        'description_en': 'HTTP response headers leak server type and version information',
        'detection_zh': [
            '1. 发送HEAD请求获取响应头',
            '2. 检查Server、X-Powered-By头',
            '3. 识别Web服务器和版本',
            '4. 检查其他泄露信息的头',
            '5. 查找已知漏洞利用'
        ],
        'detection_en': [
            '1. Send HEAD request to get response headers',
            '2. Check Server, X-Powered-By headers',
            '3. Identify web server and version',
            '4. Check other headers leaking information',
            '5. Search for known vulnerabilities to exploit'
        ],
        'payload': 'curl -I http://target.com\ncurl -v http://target.com',
        'fix_zh': '配置服务器隐藏版本信息，禁用X-Powered-By头',
        'fix_en': 'Configure server to hide version info, disable X-Powered-By header',
        'reference_url': 'https://owasp.org/www-community/attacks/Information_exposure_through_query_strings_in_url'
    },
]

def get_template_by_id(template_id):
    for template in VULN_TEMPLATES:
        if template['id'] == template_id:
            return template
    return None

def get_templates_by_category(category):
    return [t for t in VULN_TEMPLATES if t['category'] == category]

def get_templates_by_severity(severity):
    return [t for t in VULN_TEMPLATES if t['severity'] == severity]

if __name__ == '__main__':
    print(f"Loaded {len(VULN_TEMPLATES)} vulnerability templates")
    print("\nCategories:")
    categories = set(t['category'] for t in VULN_TEMPLATES)
    for cat in categories:
        count = len(get_templates_by_category(cat))
        print(f"  {cat}: {count}")