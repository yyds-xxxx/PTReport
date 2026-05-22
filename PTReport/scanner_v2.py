#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PTReport scanner.py - Low-impact automated vulnerability scanning engine
Tool detection -> User selection yes/no -> Execute low-pressure scan
"""

import subprocess
import time
import socket
import re
import os
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path


class VulnerabilityScanner:
    """Low-impact vulnerability scanner with rate limiting and user confirmation"""

    def __init__(self, i18n=None, tool_checker=None):
        self.i18n = i18n
        self.tool_checker = tool_checker
        self.scan_results = []
        self.rate_limit_delay = 2  # seconds between scans
        self.timeout = 120  # seconds per scan

    def check_tool_installed(self, tool_name):
        """Check if a tool is installed and get its version"""
        try:
            if tool_name == 'nmap':
                result = subprocess.run(
                    ['nmap', '--version'], capture_output=True, text=True,
                    timeout=10, shell=True
                )
            elif tool_name == 'nikto':
                result = subprocess.run(
                    ['nikto', '-Version'], capture_output=True, text=True,
                    timeout=10, shell=True
                )
            elif tool_name == 'sqlmap':
                result = subprocess.run(
                    ['sqlmap', '--version'], capture_output=True, text=True,
                    timeout=10, shell=True
                )
            elif tool_name == 'whatweb':
                result = subprocess.run(
                    ['whatweb', '--version'], capture_output=True, text=True,
                    timeout=10, shell=True
                )
            elif tool_name == 'dirb':
                result = subprocess.run(
                    ['dirb', '-v'], capture_output=True, text=True,
                    timeout=10, shell=True
                )
            else:
                return False

            if result.returncode == 0:
                output = result.stdout + result.stderr
                version = re.search(r'[0-9]+\.[0-9]+(?:\.[0-9]+)?', output)
                return True, version.group(0) if version else 'unknown'
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            pass
        return False, None

    def is_valid_target(self, target):
        """Validate target is valid IP or hostname"""
        # Check if it's a valid IP address
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(ip_pattern, target):
            try:
                socket.inet_aton(target)
                return True
            except socket.error:
                return False

        # Check if it's a valid hostname
        hostname_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        if re.match(hostname_pattern, target):
            return True

        return False

    def resolve_hostname(self, hostname):
        """Resolve hostname to IP address"""
        try:
            ip = socket.gethostbyname(hostname)
            return ip
        except socket.gaierror:
            return None

    def run_nmap_scan(self, target, port_range='1-1000'):
        """
        Run Nmap port scan (low-impact: TCP connect only, no aggressive options)
        Uses -sT (TCP connect scan - no root required), -sV (version detection)
        Avoids: -sS (SYN scan requires root), -A (aggressive), -T5 (fast)
        """
        results = []

        # Resolve hostname if needed
        if not self.is_valid_target(target):
            resolved = self.resolve_hostname(target)
            if resolved:
                target = resolved
            else:
                return [{'tool': 'nmap', 'error': f'Cannot resolve target: {target}'}]

        # Low-impact scan: TCP connect scan with version detection, top ports only
        cmd = [
            'nmap',
            '-sT',           # TCP connect scan (no root needed)
            '-sV',           # Version detection
            '--top-ports', '100',  # Only scan top 100 ports
            '-oX', '-',      # Output XML to stdout
            '--open',        # Only show open ports
            '-Pn',           # Skip ping discovery
            '--max-retries', '1',  # Reduce retries for lower impact
            '--host-timeout', '60s',  # Per-host timeout
            target
        ]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=self.timeout, shell=True
            )

            if result.returncode == 0:
                parsed = self.parse_nmap_results(result.stdout)
                for port_info in parsed:
                    port_info['tool'] = 'nmap'
                    port_info['target'] = target
                    port_info['timestamp'] = datetime.now().isoformat()
                    results.append(port_info)
            else:
                results.append({
                    'tool': 'nmap',
                    'error': result.stderr or 'Scan failed',
                    'target': target
                })

        except subprocess.TimeoutExpired:
            results.append({'tool': 'nmap', 'error': 'Scan timeout', 'target': target})
        except Exception as e:
            results.append({'tool': 'nmap', 'error': str(e), 'target': target})

        return results

    def run_nikto_scan(self, target):
        """
        Run Nikto web vulnerability scan (low-impact settings)
        Uses minimal options, -T (timing) set to 1 (slow), limited port check
        """
        results = []

        # Ensure target has scheme for Nikto
        if not target.startswith('http://') and not target.startswith('https://'):
            target = f'http://{target}'

        # Resolve to IP for consistency
        if not self.is_valid_target(target.replace('http://', '').replace('https://', '')):
            host = target.replace('http://', '').replace('https://', '')
            resolved = self.resolve_hostname(host)
            if resolved:
                target = target.replace(host, resolved)

        output_file = Path(tempfile.gettempdir()) / 'ptreport_nikto_output.xml'

        cmd = [
            'nikto',
            '-h', target,
            '-o', str(output_file),
            '-Format', 'xml',
            '-T', '1',      # Timing: 1 = slow (stealthy)
            '-port', '80,443',  # Only common ports
            '-nointeractive',  # Non-interactive mode
        ]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=self.timeout, shell=True
            )

            if result.returncode == 0 and output_file.exists():
                parsed = self.parse_nikto_results(output_file.read_text())
                for finding in parsed:
                    finding['tool'] = 'nikto'
                    finding['target'] = target
                    finding['timestamp'] = datetime.now().isoformat()
                    results.append(finding)
                # Clean up
                output_file.unlink(missing_ok=True)
            else:
                results.append({
                    'tool': 'nikto',
                    'error': result.stderr or 'Scan failed',
                    'target': target
                })

        except subprocess.TimeoutExpired:
            results.append({'tool': 'nikto', 'error': 'Scan timeout', 'target': target})
        except FileNotFoundError:
            results.append({'tool': 'nikto', 'error': 'Nikto not installed', 'target': target})
        except Exception as e:
            results.append({'tool': 'nikto', 'error': str(e), 'target': target})

        return results

    def run_sqlmap_check(self, target):
        """
        Run SQLMap basic detection (lowest impact settings)
        Uses --batch (non-interactive), --banner (get version), --level=1 (minimal testing)
        """
        results = []

        # Ensure target has URL scheme
        if not target.startswith('http://') and not target.startswith('https://'):
            target = f'http://{target}'

        output_dir = Path(tempfile.gettempdir()) / 'ptreport_sqlmap'
        output_dir.mkdir(exist_ok=True)

        cmd = [
            'sqlmap',
            '-u', target,
            '--batch',         # Non-interactive mode
            '--banner',       # Get database banner
            '--level', '1',   # Minimal test level
            '--risk', '1',    # Minimal risk
            '--threads', '1', # Single thread
            '--timeout', '30', # 30 second timeout per request
            '--crawl', '1',   # Minimal crawl depth
            '--output-dir', str(output_dir),
        ]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=self.timeout, shell=True
            )

            # SQLMap outputs to stderr typically
            output = result.stderr + result.stdout

            # Parse SQLMap results for vulnerabilities
            if 'vulnerable' in output.lower() or 'parameter is vulnerable' in output.lower():
                results.append({
                    'tool': 'sqlmap',
                    'severity': 'high',
                    'title': 'SQL Injection Vulnerability Detected',
                    'description': 'SQLMap detected potential SQL injection vulnerability',
                    'target': target,
                    'timestamp': datetime.now().isoformat()
                })
            elif 'error' in output.lower() and 'syntax' in output.lower():
                results.append({
                    'tool': 'sqlmap',
                    'severity': 'medium',
                    'title': 'Potential SQL Error Detected',
                    'description': 'Potential SQL error detected, manual verification recommended',
                    'target': target,
                    'timestamp': datetime.now().isoformat()
                })

            # Always add scan info even if no vuln found
            if not any(r.get('tool') == 'sqlmap' for r in results):
                results.append({
                    'tool': 'sqlmap',
                    'severity': 'info',
                    'title': 'SQLMap Scan Completed',
                    'description': 'Basic SQL injection checks completed, no obvious vulnerabilities found',
                    'target': target,
                    'timestamp': datetime.now().isoformat()
                })

        except subprocess.TimeoutExpired:
            results.append({'tool': 'sqlmap', 'error': 'Scan timeout', 'target': target})
        except FileNotFoundError:
            results.append({'tool': 'sqlmap', 'error': 'SQLMap not installed', 'target': target})
        except Exception as e:
            results.append({'tool': 'sqlmap', 'error': str(e), 'target': target})

        return results

    def parse_nmap_results(self, xml_output):
        """Parse Nmap XML output to extract port information"""
        results = []

        if not xml_output or not xml_output.strip():
            return results

        try:
            # Handle namespace issues by removing namespace prefixes
            xml_clean = re.sub(r'\sxmlns="[^"]*"', '', xml_output)
            xml_clean = re.sub(r'\sxmlns:[a-z]+="[^"]*"', '', xml_clean)

            root = ET.fromstring(xml_clean)

            for host in root.findall('.//host'):
                addresses = []
                for addr in host.findall('addresses/addr'):
                    addresses.append(addr.get('addr'))

                hostnames = []
                for hostname in host.findall('hostnames/hostname'):
                    hostnames.append(hostname.get('name'))

                for port in host.findall('.//port'):
                    port_id = port.get('portid')
                    protocol = port.get('protocol')
                    state = port.find('state')
                    service = port.find('service')

                    port_info = {
                        'port': port_id,
                        'protocol': protocol,
                        'state': state.get('state') if state is not None else 'unknown',
                        'service': service.get('name') if service is not None else 'unknown',
                        'version': service.get('version') if service is not None else '',
                        'product': service.get('product') if service is not None else '',
                    }

                    # Determine severity based on port and service
                    severity = 'info'
                    if port_info['state'] == 'open':
                        # High risk services
                        high_risk = ['http', 'https', 'ssh', 'ftp', 'telnet', 'mysql', 'postgresql', 'mongodb', 'redis']
                        if any(svc in port_info['service'].lower() for svc in high_risk):
                            severity = 'medium'

                        # Critical ports always get attention
                        critical_ports = ['21', '22', '23', '25', '110', '143', '3306', '3389', '5432', '6379', '27017']
                        if port_id in critical_ports:
                            severity = 'medium'

                        port_info['severity'] = severity
                        port_info['title'] = f"Open Port: {port_id}/{protocol} ({port_info['service']})"
                        port_info['description'] = f"Port {port_id}/{protocol} is open. Service: {port_info['service']} {port_info['version']}".strip()

                    results.append(port_info)

        except ET.ParseError as e:
            results.append({'error': f'XML parse error: {str(e)}'})

        return results

    def parse_nikto_results(self, xml_output):
        """Parse Nikto XML output to extract vulnerabilities"""
        results = []

        if not xml_output or not xml_output.strip():
            return results

        try:
            # Nikto XML parsing
            root = ET.fromstring(xml_output)

            for item in root.findall('.//item'):
                title = item.find('name')
                description = item.find('description')
                severity = item.find('severity')
                method = item.find('method')

                finding = {
                    'title': title.text if title is not None else 'Unknown',
                    'description': description.text if description is not None else '',
                    'severity': severity.text if severity is not None else 'info',
                    'method': method.text if method is not None else '',
                }

                # Map severity
                sev = finding['severity'].lower()
                if 'high' in sev or 'critical' in sev:
                    finding['severity'] = 'high'
                elif 'medium' in sev or 'moderate' in sev:
                    finding['severity'] = 'medium'
                elif 'low' in sev:
                    finding['severity'] = 'low'
                else:
                    finding['severity'] = 'info'

                results.append(finding)

        except ET.ParseError:
            # Try parsing as text if XML fails
            for line in xml_output.split('\n'):
                if '?' in line and ('+' in line or '!' in line):
                    results.append({
                        'title': 'Web Vulnerability',
                        'description': line.strip(),
                        'severity': 'medium'
                    })

        return results

    def run_whatweb_scan(self, target):
        results = []
        if not target.startswith('http://') and not target.startswith('https://'):
            target = f'http://{target}'
        cmd = ['whatweb', '--color=never', '--log-xml=-', target]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout, shell=True)
            if result.returncode == 0:
                parsed = self.parse_whatweb_results(result.stdout)
                for item in parsed:
                    item['tool'] = 'whatweb'
                    item['target'] = target
                    item['timestamp'] = datetime.now().isoformat()
                    results.append(item)
        except subprocess.TimeoutExpired:
            results.append({'tool': 'whatweb', 'error': 'Scan timeout', 'target': target})
        except Exception as e:
            results.append({'tool': 'whatweb', 'error': str(e), 'target': target})
        return results

    def parse_whatweb_results(self, xml_output):
        results = []
        if not xml_output or not xml_output.strip():
            return results
        try:
            root = ET.fromstring(xml_output)
            for target_elem in root.findall('.//target'):
                plugins = target_elem.findall('.//plugin')
                for plugin in plugins:
                    name = plugin.find('name')
                    version = plugin.find('version')
                    desc = plugin.find('description')
                    certainty = plugin.get('certainty', '0')
                    finding = {
                        'title': name.text if name is not None else 'Unknown',
                        'version': version.text if version is not None else '',
                        'description': desc.text if desc is not None else '',
                        'certainty': certainty,
                        'severity': 'info'
                    }
                    try:
                        c = int(certainty)
                        finding['severity'] = 'low' if c < 70 else 'info'
                    except:
                        finding['severity'] = 'info'
                    results.append(finding)
        except ET.ParseError:
            pass
        return results

    def run_dirb_scan(self, target):
        results = []
        if not target.startswith('http://') and not target.startswith('https://'):
            target = f'http://{target}'
        cmd = ['dirb', target, '/usr/share/dirb/wordlists/common.txt', '-o', '/tmp/dirb_result.txt', '-w']
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout, shell=True)
            try:
                with open('/tmp/dirb_result.txt', 'r', encoding='utf-8') as f:
                    parsed = self.parse_dirb_results(f.read())
                    for item in parsed:
                        item['tool'] = 'dirb'
                        item['target'] = target
                        item['timestamp'] = datetime.now().isoformat()
                        results.append(item)
            except FileNotFoundError:
                pass
        except subprocess.TimeoutExpired:
            results.append({'tool': 'dirb', 'error': 'Scan timeout', 'target': target})
        except Exception as e:
            results.append({'tool': 'dirb', 'error': str(e), 'target': target})
        return results

    def parse_dirb_results(self, text_output):
        results = []
        for line in text_output.split('
'):
            if line.startswith('+ '):
                try:
'):
''):
            if line.startswith('+ '):
                try:
                    parts = line[2:].split(' (CODE:')
                    if len(parts) >= 1:
                        url = parts[0].strip()
                        code = ''
                        if len(parts) > 1:
                            code = parts[1].split('|')[0].replace(')', '')
                        if code and code != '404':
                            results.append({
                                'title': f'Discovered: {url}',
                                'description': f'HTTP {code}',
                                'severity': 'low' if code == '403' else 'info'
                            })
                except:
                    pass
        return results

    def scan(self, target, port_range='1-1000', categories=None):
        """
        Main scan method with low-impact scanning strategy

        Workflow:
        1. Validate target
        2. Check available tools
        3. Execute low-impact scans with rate limiting
        4. Return results for user confirmation

        Args:
            target: Target IP or hostname
            port_range: Port range to scan (default 1-1000)
            categories: List of tool categories to use ['nmap', 'nikto', 'sqlmap']

        Returns:
            List of scan results
        """
        results = []

        # Validate target
        if not target:
            return [{'error': 'No target specified'}]

        # Normalize target
        target = target.strip()

        # Default categories if not specified
        if categories is None:
            categories = ['nmap', 'nikto', 'sqlmap']

        # Check which tools are available
        available_tools = []
        for tool in categories:
            installed, version = self.check_tool_installed(tool)
            if installed:
                available_tools.append((tool, version))

        if not available_tools:
            return [{'error': 'No scanning tools available', 'target': target}]

        # Execute scans with rate limiting
        for tool, version in available_tools:
            tool_results = []

            if tool == 'nmap':
                tool_results = self.run_nmap_scan(target, port_range)
            elif tool == 'nikto':
                tool_results = self.run_nikto_scan(target)
            elif tool == 'sqlmap':
                tool_results = self.run_sqlmap_check(target)
            elif tool == 'whatweb':
                tool_results = self.run_whatweb_scan(target)
            elif tool == 'dirb':
                tool_results = self.run_dirb_scan(target)

            for result in tool_results:
                result['tool_version'] = version
                results.append(result)

            # Rate limiting between tools
            time.sleep(self.rate_limit_delay)

        self.scan_results = results
        return results

    def get_summary(self, results=None):
        """Get a summary of scan results"""
        if results is None:
            results = self.scan_results

        summary = {
            'total': len(results),
            'high': 0,
            'medium': 0,
            'low': 0,
            'info': 0,
            'errors': 0,
            'by_tool': {}
        }

        for result in results:
            if 'error' in result:
                summary['errors'] += 1
                continue

            severity = result.get('severity', 'info')
            tool = result.get('tool', 'unknown')

            if severity == 'high':
                summary['high'] += 1
            elif severity == 'medium':
                summary['medium'] += 1
            elif severity == 'low':
                summary['low'] += 1
            else:
                summary['info'] += 1

            if tool not in summary['by_tool']:
                summary['by_tool'][tool] = 0
            summary['by_tool'][tool] += 1

        return summary


# Alias for backward compatibility
Scanner = VulnerabilityScanner
