#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PTReport scanner.py - Low-impact automated vulnerability scanning engine"""

import subprocess
import time
import socket
import re
import os
import xml.etree.ElementTree as ET
from datetime import datetime


class VulnerabilityScanner:
    def __init__(self, i18n=None, tool_checker=None):
        self.i18n = i18n
        self.tool_checker = tool_checker
        self.scan_results = []
        self.rate_limit_delay = 2
        self.timeout = 120

    def check_tool_installed(self, tool_name):
        try:
            if tool_name == 'nmap':
                result = subprocess.run(['nmap', '--version'], capture_output=True, text=True, timeout=10, shell=True)
            elif tool_name == 'nikto':
                result = subprocess.run(['nikto', '-Version'], capture_output=True, text=True, timeout=10, shell=True)
            elif tool_name == 'sqlmap':
                result = subprocess.run(['sqlmap', '--version'], capture_output=True, text=True, timeout=10, shell=True)
            elif tool_name == 'whatweb':
                result = subprocess.run(['whatweb', '--version'], capture_output=True, text=True, timeout=10, shell=True)
            elif tool_name == 'dirb':
                result = subprocess.run(['dirb', '-v'], capture_output=True, text=True, timeout=10, shell=True)
            else:
                return False, None
            if result.returncode == 0:
                output = result.stdout + result.stderr
                version = re.search(r'[0-9]+\.[0-9]+(?:\.[0-9]+)?', output)
                return True, version.group(0) if version else 'unknown'
        except Exception:
            pass
        return False, None

    def is_valid_target(self, target):
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(ip_pattern, target):
            try:
                socket.inet_aton(target)
                return True
            except socket.error:
                return False
        hostname_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        if re.match(hostname_pattern, target):
            return True
        return False

    def resolve_hostname(self, hostname):
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return None

    def run_nmap_scan(self, target, port_range='1-1000'):
        results = []
        if not self.is_valid_target(target):
            resolved = self.resolve_hostname(target)
            if resolved:
                target = resolved
            else:
                return [{'tool': 'nmap', 'error': f'Cannot resolve: {target}', 'target': target}]
        cmd = ['nmap', '-sT', '-sV', '--top-ports', '100', '-oX', '-', '--open', '-Pn', '--max-retries', '1', '--host-timeout', '60s', target]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout, shell=True)
            if result.returncode == 0:
                for port_info in self.parse_nmap_results(result.stdout):
                    port_info['tool'] = 'nmap'
                    port_info['target'] = target
                    port_info['timestamp'] = datetime.now().isoformat()
                    results.append(port_info)
            else:
                results.append({'tool': 'nmap', 'error': result.stderr or 'Scan failed', 'target': target})
        except subprocess.TimeoutExpired:
            results.append({'tool': 'nmap', 'error': 'Scan timeout', 'target': target})
        except Exception as e:
            results.append({'tool': 'nmap', 'error': str(e), 'target': target})
        return results

    def parse_nmap_results(self, xml_output):
        results = []
        if not xml_output or not xml_output.strip():
            return results
        try:
            root = ET.fromstring(xml_output)
            for port in root.findall('.//port'):
                port_id = port.get('portid', '')
                protocol = port.get('protocol', 'tcp')
                service = port.find('service')
                finding = {'title': f'Open Port: {port_id}/{protocol}', 'description': '', 'severity': 'info', 'port': port_id, 'protocol': protocol}
                if service is not None:
                    finding['description'] = f"Service: {service.get('name', '')} {service.get('version', '')}".strip()
                high_risk = ['21', '22', '23', '25', '110', '143', '445', '3306', '5432', '27017', '6379']
                medium_risk = ['80', '443', '8080', '8443', '3000', '5000']
                if port_id in high_risk:
                    finding['severity'] = 'high'
                elif port_id in medium_risk:
                    finding['severity'] = 'medium'
                results.append(finding)
        except ET.ParseError:
            pass
        return results

    def run_nikto_scan(self, target):
        results = []
        if not target.startswith('http://') and not target.startswith('https://'):
            target = f'http://{target}'
        cmd = ['nikto', '-h', target, '-T', '1', '-o', '/tmp/nikto.xml', '-Format', 'xml']
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout, shell=True)
            try:
                with open('/tmp/nikto.xml', 'r', encoding='utf-8') as f:
                    for finding in self.parse_nikto_results(f.read()):
                        finding['tool'] = 'nikto'
                        finding['target'] = target
                        finding['timestamp'] = datetime.now().isoformat()
                        results.append(finding)
            except FileNotFoundError:
                pass
        except subprocess.TimeoutExpired:
            results.append({'tool': 'nikto', 'error': 'Scan timeout', 'target': target})
        except Exception as e:
            results.append({'tool': 'nikto', 'error': str(e), 'target': target})
        return results

    def parse_nikto_results(self, xml_output):
        results = []
        if not xml_output or not xml_output.strip():
            return results
        try:
            root = ET.fromstring(xml_output)
            for item in root.findall('.//item'):
                title = item.find('name')
                description = item.find('description')
                finding = {'title': title.text if title is not None else 'Unknown', 'description': description.text if description is not None else '', 'severity': 'medium'}
                sev = finding['severity'].lower()
                if 'high' in sev or 'critical' in sev:
                    finding['severity'] = 'high'
                elif 'low' in sev:
                    finding['severity'] = 'low'
                else:
                    finding['severity'] = '
