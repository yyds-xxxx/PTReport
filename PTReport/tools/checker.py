#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PTReport tools/checker.py - 工具检测与安装提示
"""

import subprocess
import sys
import re

TOOLS = {
    'nmap': {'name': 'Nmap', 'desc_zh': '端口扫描', 'desc_en': 'Port scanner', 'check_args': ['--version']},
    'nikto': {'name': 'Nikto', 'desc_zh': 'Web漏洞扫描', 'desc_en': 'Web vulnerability scanner', 'check_args': ['-Version']},
    'sqlmap': {'name': 'SQLMap', 'desc_zh': 'SQL注入检测', 'desc_en': 'SQL injection scanner', 'check_args': ['--version']},
    'whatweb': {'name': 'WhatWeb', 'desc_zh': 'Web技术识别', 'desc_en': 'Web technology fingerprinting', 'check_args': ['--version']},
    'dirb': {'name': 'DIRB', 'desc_zh': 'Web目录扫描', 'desc_en': 'Web directory scanner', 'check_args': ['-v']},
}

def check_tool(tool_name):
    try:
        result = subprocess.run([tool_name, '--version'], capture_output=True, text=True, timeout=10, shell=True)
        if result.returncode == 0:
            output = result.stdout + result.stderr
            version = re.search(r'[0-9]+\.[0-9]+', output)
            return True, version.group(0) if version else 'unknown'
    except:
        pass
    return False, ''

class ToolChecker:
    def __init__(self, i18n=None):
        self.i18n = i18n
        self.tools = TOOLS

    def check_all_tools(self):
        results = {}
        for name, info in self.tools.items():
            installed, version = check_tool(name)
            results[name] = {'installed': installed, 'version': version, 'info': info}
        return results

    def print_status(self):
        results = self.check_all_tools()
        lang = self.i18n.lang if self.i18n else 'zh'
        print()
        print('=' * 60)
        print(f"{'工具检测' if lang=='zh' else 'Tool Check':^60}")
        print('=' * 60)
        for name, result in results.items():
            icon = '[OK]' if result['installed'] else '[--]'
            ver = f"v{result['version']}" if result['version'] else ''
            print(f"  {icon} {result['info']['name']} {ver}")
        missing = [n for n,r in results.items() if not r['installed']]
        if missing: print(f"Missing: {', '.join(missing)}")
        else: print('All installed')
