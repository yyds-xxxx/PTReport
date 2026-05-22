#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PTReport v2 - 渗透测试报告生成器
Pentest Report Generator v2.0

用法：
  python ptr.py --interactive          交互式向导模式
  python ptr.py --scan TARGET          快速扫描指定目标
  python ptr.py --template             生成模板报告（无扫描）
  python ptr.py --list                 列出所有漏洞模板
  python ptr.py --config               显示工具配置状态
  python ptr.py --lang zh|en           设置语言
"""

import sys
import os
import argparse
from datetime import datetime
from pathlib import Path

# 导入v2模块
from i18n import I18n
from scanner import VulnerabilityScanner
from report_builder import ReportBuilder
from vuln_templates import VULN_TEMPLATES, get_templates_by_category
from tools.checker import ToolChecker


class PTReport:
    """PTReport v2 主控制器"""

    TOTAL_STEPS = 6

    def __init__(self, lang='zh'):
        self.i18n = I18n(lang)
        self.lang = lang
        self.project_info = {}
        self.authorized = None
        self.scan_results = []
        self.selected_vulns = []
        self.tool_checker = ToolChecker(self.i18n)
        self.scanner = VulnerabilityScanner(self.i18n, self.tool_checker)
        self.report_builder = ReportBuilder(self.i18n, self.lang)

    # ========== 通用交互函数 ==========

    def _print_step(self, step, title=None):
        """打印步骤标题"""
        print("\n" + "=" * 60)
        if title:
            print(f"  {self.i18n.t(f'step_{step}')} - {title}")
        else:
            print(f"  {self.i18n.t(f'step_{step}')}")
        print("=" * 60)

    def _print_banner(self):
        """打印横幅"""
        print("\n" + "=" * 60)
        print(f"  {self.i18n.t('banner_title')}")
        print(f"  {self.i18n.t('banner_version')}")
        print("=" * 60)
        print(f"  {self.i18n.t('welcome')}")
        print()

    def _input_with_default(self, prompt, default, back_ok=True):
        """带默认值的输入"""
        if back_ok:
            prompt_str = f"  {prompt} [{default}] (b: {self.i18n.t('back')}): "
        else:
            prompt_str = f"  {prompt} [{default}]: "
        val = input(prompt_str).strip()
        if val.lower() in ('b', '0'):
            return '__BACK__'
        return val if val else default

    def _yes_no(self, prompt, default='no', back_ok=True):
        """是/否问题"""
        default_lower = default.lower()
        default_str = default_lower if default_lower in ('yes', 'no') else 'no'
        if back_ok:
            prompt_str = f"  {prompt} (yes/no，默认: {default_str}) (b: {self.i18n.t('back')}): "
        else:
            prompt_str = f"  {prompt} (yes/no，默认: {default_str}): "
        while True:
            val = input(prompt_str).strip().lower()
            if val in ('b', '0') and back_ok:
                return '__BACK__'
            if val in ('yes', 'y', 'no', 'n', ''):
                if val == '':
                    return default_lower == 'yes'
                return val in ('yes', 'y')
            print(f"  {self.i18n.t('invalid_input')}")

    def _select_from_list(self, prompt, items, default_idx=0, back_ok=True):
        """从列表选择，支持多选"""
        if back_ok:
            prompt_str = f"  {prompt} (多选用逗号分隔，b: {self.i18n.t('back')}): "
        else:
            prompt_str = f"  {prompt} (多选用逗号分隔): "

        while True:
            val = input(prompt_str).strip()
            if val.lower() in ('b', '0') and back_ok:
                return '__BACK__'

            if not val:
                return [default_idx]

            try:
                indices = []
                for v in val.split(','):
                    v = v.strip()
                    if v:
                        idx = int(v) - 1
                        if 0 <= idx < len(items):
                            indices.append(idx)
                if indices:
                    return indices
                print(f"  {self.i18n.t('invalid_input')}")
            except ValueError:
                print(f"  {self.i18n.t('invalid_input')}")

    def _confirm_yes_no(self, prompt, back_ok=True):
        """确认是/否问题"""
        if back_ok:
            prompt_str = f"  {prompt} (yes/no) (b: {self.i18n.t('back')}): "
        else:
            prompt_str = f"  {prompt} (yes/no): "

        while True:
            val = input(prompt_str).strip().lower()
            if val in ('b', '0') and back_ok:
                return '__BACK__'
            if val == 'yes' or val == 'y':
                return True
            if val == 'no' or val == 'n':
                return False
            print(f"  {self.i18n.t('invalid_input')}")

    # ========== 步骤1：项目信息 ==========

    def step_project_info(self):
        """收集项目基本信息"""
        self._print_step(1, self.i18n.t('project_info'))

        name = self._input_with_default(
            self.i18n.t('project_name'),
            self.i18n.t('default_project')
        )
        if name == '__BACK__':
            return False, 'back'

        target = self._input_with_default(
            self.i18n.t('target_asset'),
            'example.com'
        )
        if target == '__BACK__':
            return False, 'back'

        scope = self._input_with_default(
            self.i18n.t('test_scope'),
            self.i18n.t('all_ports')
        )
        if scope == '__BACK__':
            return False, 'back'

        engineer = self._input_with_default(
            self.i18n.t('engineer_name'),
            self.i18n.t('default_author')
        )
        if engineer == '__BACK__':
            return False, 'back'

        self.project_info = {
            'name': name,
            'target': target,
            'scope': scope,
            'engineer': engineer,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'version': '2.0'
        }

        return True, self.project_info

    # ========== 步骤2：授权状态 ==========

    def step_authorization(self):
        """收集授权状态"""
        self._print_step(2, self.i18n.t('auth_status'))

        print(f"\n  {'已获得授权' if self.lang=='zh' else 'Authorized'}: ", end='')
        print(f"{self.i18n.t('has_auth')}")
        print(f"  {'未获得授权' if self.lang=='zh' else 'Not Authorized'}: ", end='')
        print(f"{self.i18n.t('no_auth')}")
        print()

        result = self._yes_no(
            self.i18n.t('auth_status'),
            default='no'
        )

        if result == '__BACK__':
            return False, 'back'

        self.authorized = result

        if not self.authorized:
            print(f"\n  {self.i18n.t('template_only')}")

            # 选择报告风格
            print(f"\n  {'选择报告风格 / Select Report Style:' if self.lang=='zh' else 'Select Report Style:'}")
            print(f"  1 - Standard ({self.i18n.t('standard') if 'standard' in self.i18n.strings else '标准模板'})")
            print(f"  2 - Executive Summary ({self.i18n.t('executive') if 'executive' in self.i18n.strings else '执行摘要'})")
            print(f"  3 - Checklist ({self.i18n.t('checklist') if 'checklist' in self.i18n.strings else '检查清单'})")
            print(f"  4 - CTF Writeup ({self.i18n.t('ctf') if 'ctf' in self.i18n.strings else 'CTF报告'})")
            print(f"  5 - Full ({self.i18n.t('full') if 'full' in self.i18n.strings else '全模板'})")
            print()

            style_map = {'1': 'standard', '2': 'executive', '3': 'checklist', '4': 'ctf', '5': 'full'}
            while True:
                val = input(f"  {self.i18n.t('select_style')} (1-5, default 1): ").strip()
                if val == '':
                    style = 1
                    break
                if val in style_map:
                    style = int(val)
                    break
                print(f"  {self.i18n.t('invalid_input')}")
            self.report_style = style_map.get(str(style), 'standard')
            self.report_builder.report_style = self.report_style
        else:
            self.report_style = 'standard'
            self.report_builder.report_style = 'standard'

        return True, self.authorized

    # ========== 步骤3：自动化扫描选择 ==========

    def step_scan_choice(self):
        """是否进行自动化扫描"""
        self._print_step(3, self.i18n.t('auto_scan_prompt'))

        result = self._yes_no(
            self.i18n.t('auto_scan_prompt'),
            default='no'
        )

        if result == '__BACK__':
            return False, 'back'

        do_scan = result

        if do_scan:
            # 检查工具
            print(f"\n  {self.i18n.t('tool_check')}...")
            results = self.tool_checker.check_all_tools()

            available_tools = [(name, r) for name, r in results.items() if r['installed']]
            missing_tools = [(name, r) for name, r in results.items() if not r['installed']]

            print(f"\n  {self.i18n.t('detected_tools')}:")
            if available_tools:
                for name, r in available_tools:
                    ver = f"v{r['version']}" if r['version'] else ''
                    print(f"    [OK] {r['info']['name']} {ver}")
            else:
                print(f"    {'无可用工具' if self.lang=='zh' else 'No tools available'}")

            if missing_tools:
                print(f"\n  {self.i18n.t('missing_tools')}:")
                for name, r in missing_tools:
                    print(f"    [--] {r['info']['name']}")

            if not available_tools:
                print(f"\n  {'警告：没有可用扫描工具，将生成模板报告' if self.lang=='zh' else 'Warning: No scanning tools available, will generate template report'}")
                return True, {'do_scan': False, 'tools': [], 'selected_tools': []}

            # 选择工具
            print(f"\n  {'可用的扫描工具，请选择使用的工具（多选）:' if self.lang=='zh' else 'Available tools, select which to use (multi-select):'}")
            for i, (name, r) in enumerate(available_tools, 1):
                ver = f"v{r['version']}" if r['version'] else ''
                print(f"    {i}. {r['info']['name']} {ver}")

            selected_indices = self._select_from_list(
                self.i18n.t('enter_number'),
                available_tools,
                default_idx=list(range(len(available_tools)))
            )

            if selected_indices == '__BACK__':
                return False, 'back'

            selected_tools = [available_tools[i][0] for i in selected_indices]
            print(f"\n  {'已选择工具:' if self.lang=='zh' else 'Selected tools'}: {', '.join(selected_tools)}")

            return True, {'do_scan': True, 'tools': available_tools, 'selected_tools': selected_tools}
        else:
            return True, {'do_scan': False, 'tools': [], 'selected_tools': []}

    # ========== 步骤4：执行扫描 ==========

    def step_scan_execution(self, scan_choice):
        """执行扫描"""
        self._print_step(4, self.i18n.t('generating_report').replace('生成报告中', '扫描执行中'))

        if not scan_choice.get('do_scan'):
            print(f"\n  {'跳过扫描（未选择）' if self.lang=='zh' else 'Scan skipped (not selected)'}")
            return True, []

        selected_tools = scan_choice.get('selected_tools', [])
        if not selected_tools:
            print(f"\n  {'没有选择任何工具，跳过扫描' if self.lang=='zh' else 'No tools selected, skipping scan'}")
            return True, []

        target = self.project_info.get('target', '')

        print(f"\n  {'目标:' if self.lang=='zh' else 'Target'}: {target}")
        print(f"  {'工具:' if self.lang=='zh' else 'Tools'}: {', '.join(selected_tools)}")
        print(f"\n  {'正在扫描，请稍候...' if self.lang=='zh' else 'Scanning, please wait...'}")
        print()

        results = []
        for tool in selected_tools:
            print(f"  {'运行' if self.lang=='zh' else 'Running'} {tool}...", end=' ', flush=True)
            try:
                if tool == 'nmap':
                    tool_results = self.scanner.run_nmap_scan(target)
                elif tool == 'nikto':
                    tool_results = self.scanner.run_nikto_scan(target)
                elif tool == 'sqlmap':
                    tool_results = self.scanner.run_sqlmap_check(target)
                else:
                    tool_results = []
                results.extend(tool_results)
                print(f"OK ({len(tool_results)} {'结果' if self.lang=='zh' else 'results'})")
            except Exception as e:
                print(f"Error: {e}")

        self.scan_results = results

        # 显示摘要
        summary = self.scanner.get_summary(results)
        print(f"\n  {'扫描摘要:' if self.lang=='zh' else 'Scan summary'}:")
        print(f"    {'总计:' if self.lang=='zh' else 'Total'}: {summary['total']}")
        print(f"    {'高危:' if self.lang=='zh' else 'High'}: {summary['high']} | "
              f"{'中危:' if self.lang=='zh' else 'Medium'}: {summary['medium']} | "
              f"{'低危:' if self.lang=='zh' else 'Low'}: {summary['low']} | "
              f"{'信息:' if self.lang=='zh' else 'Info'}: {summary['info']}")

        return True, results

    # ========== 步骤5：确认结果 ==========

    def step_confirm_results(self, scan_results):
        """确认扫描结果"""
        self._print_step(5, self.i18n.t('review_results'))

        if not scan_results:
            print(f"\n  {'无扫描结果' if self.lang=='zh' else 'No scan results'}")
            return True, []

        # 按严重性分组显示
        by_severity = {'high': [], 'medium': [], 'low': [], 'info': []}
        for r in scan_results:
            sev = r.get('severity', 'info')
            if sev not in by_severity:
                sev = 'info'
            by_severity[sev].append(r)

        total_count = len(scan_results)
        print(f"\n  {'发现' if self.lang=='zh' else 'Found'} {total_count} {'个问题' if self.lang=='zh' else 'issues'}:")
        print(f"    {'高危' if self.lang=='zh' else 'High'}: {len(by_severity['high'])} | "
              f"{'中危' if self.lang=='zh' else 'Medium'}: {len(by_severity['medium'])} | "
              f"{'低危' if self.lang=='zh' else 'Low'}: {len(by_severity['low'])} | "
              f"{'信息' if self.lang=='zh' else 'Info'}: {len(by_severity['info'])}")

        print(f"\n  {self.i18n.t('select_to_report')}")
        print()

        confirmed = []

        for sev in ['high', 'medium', 'low', 'info']:
            items = by_severity[sev]
            if not items:
                continue

            sev_label = {'high': '高危', 'medium': '中危', 'low': '低危', 'info': '信息'}[sev]
            print(f"  --- {sev_label} ({len(items)}) ---")

            for i, item in enumerate(items, 1):
                title = item.get('title', item.get('name', 'Unknown'))
                tool = item.get('tool', 'unknown').upper()
                target = item.get('target', self.project_info.get('target', 'N/A'))

                desc = item.get('description', '')[:50]
                if desc:
                    desc = f" - {desc}"

                print(f"    {len(confirmed)+1}. [{tool}] {title}{desc}")

                # 询问是否包含
                include = self._confirm_yes_no(
                    f"{'包含此漏洞到报告' if self.lang=='zh' else 'Include in report'}",
                    back_ok=False
                )
                if include:
                    confirmed.append(item)

        self.selected_vulns = confirmed
        print(f"\n  {'已选择' if self.lang=='zh' else 'Selected'}: {len(confirmed)} {'个漏洞' if self.lang=='zh' else 'vulnerabilities'}")

        return True, confirmed

    # ========== 步骤6：生成报告 ==========

    def step_generate_report(self, scan_results):
        """生成最终报告"""
        self._print_step(6, self.i18n.t('generating_report'))

        print(f"\n  {'正在生成报告...' if self.lang=='zh' else 'Generating report...'}")
        print(f"  {'项目:' if self.lang=='zh' else 'Project'}: {self.project_info.get('name', 'N/A')}")
        print(f"  {'目标:' if self.lang=='zh' else 'Target'}: {self.project_info.get('target', 'N/A')}")
        print(f"  {'授权:' if self.lang=='zh' else 'Authorized'}: {'是' if self.authorized else '否（模板）' if self.lang=='zh' else 'No (template)'}")
        print(f"  {'漏洞数:' if self.lang=='zh' else 'Vulnerabilities'}: {len(scan_results)}")

        # 生成报告
        report_content = self.report_builder.generate(
            project_info=self.project_info,
            scan_results=scan_results,
            authorized=self.authorized,
            report_style=self.report_style
        )

        # 保存
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = self.project_info.get('name', 'project').replace(' ', '_')
        filename = f'渗透测试报告_{safe_name}_{timestamp}.md'
        output_path = output_dir / filename

        self.report_builder.save_to_file(report_content, str(output_path))

        print(f"\n  {'='*40}")
        print(f"  {self.i18n.t('report_generated')}")
        print(f"  {'文件:' if self.lang=='zh' else 'File'}: {output_path}")
        print(f"  {'='*40}")

        # 询问是否导出PDF
        export_pdf = self._confirm_yes_no(
            self.i18n.t('export_pdf'),
            back_ok=False
        )

        if export_pdf:
            try:
                import subprocess, shutil
                pdf_path = str(output_path).replace('.md', '.pdf')

                # 检测pandoc是否存在
                if not shutil.which('pandoc'):
                    print(f"  pandoc {self.i18n.t('pdf_error').split('（')[1]}")
                    install = self._confirm_yes_no(
                        self.i18n.t('install_now') if 'install_now' in self.i18n.strings else '是否自动安装',
                        back_ok=False
                    )
                    if install:
                        print(f"  {'安装中...' if self.lang=='zh' else 'Installing...'}")
                        subprocess.run(['winget', 'install', 'pandoc', '--accept-source-agreements', '--accept-package-agreements'], capture_output=True)
                    else:
                        print(f"  {self.i18n.t('pdf_skipped')}")
                        return True, output_path

                result = subprocess.run(
                    ['pandoc', str(output_path), '-o', pdf_path],
                    capture_output=True, text=True, timeout=60
                )
                if result.returncode == 0 and Path(pdf_path).exists():
                    print(f"  {self.i18n.t('pdf_generated')}: {pdf_path}")
                else:
                    print(f"  {self.i18n.t('pdf_error')}")
            except Exception as e:
                print(f"  {self.i18n.t('pdf_error')}")
        else:
            print(f"  {self.i18n.t('pdf_skipped')}")

        # 询问是否打开
        open_now = self._confirm_yes_no(
            self.i18n.t('open_report'),
            back_ok=False
        )

        if open_now:
            try:
                if sys.platform == 'win32':
                    os.startfile(output_path)
                elif sys.platform == 'darwin':
                    subprocess.run(['open', output_path])
                else:
                    subprocess.run(['xdg-open', output_path])
            except Exception:
                pass

        return True, output_path

    # ========== 交互式向导 ==========

    def run_interactive(self):
        """运行交互式向导"""
        self._print_banner()

        # 步骤1：项目信息
        success, result = self.step_project_info()
        if not success:
            print(f"\n  {'已退出' if self.lang=='zh' else 'Exited'}")
            return

        # 步骤2：授权状态
        success, result = self.step_authorization()
        if not success:
            print(f"\n  {'已退出' if self.lang=='zh' else 'Exited'}")
            return

        # 步骤3：扫描选择
        success, scan_choice = self.step_scan_choice()
        if not success:
            print(f"\n  {'已退出' if self.lang=='zh' else 'Exited'}")
            return

        # 步骤4：执行扫描
        success, scan_results = self.step_scan_execution(scan_choice)
        if not success:
            print(f"\n  {'已退出' if self.lang=='zh' else 'Exited'}")
            return

        # 步骤5：确认结果
        success, confirmed_vulns = self.step_confirm_results(scan_results)
        if not success:
            print(f"\n  {'已退出' if self.lang=='zh' else 'Exited'}")
            return

        # 步骤6：生成报告
        success, report_path = self.step_generate_report(confirmed_vulns if confirmed_vulns else scan_results)

        # 询问是否继续
        if success:
            again = self._confirm_yes_no(
                self.i18n.t('continue'),
                back_ok=False
            )
            if again:
                self.run_interactive()

    # ========== CLI命令 ==========

    def cmd_scan(self, target):
        """快速扫描命令"""
        print(f"\n  {'目标:' if self.lang=='zh' else 'Target'}: {target}")
        print(f"  {'检查可用工具...' if self.lang=='zh' else 'Checking available tools...'}")
        print()

        results = self.tool_checker.check_all_tools()
        available = [(name, r) for name, r in results.items() if r['installed']]

        if not available:
            print(f"  {'错误：没有可用扫描工具' if self.lang=='zh' else 'Error: No scanning tools available'}")
            return

        print(f"  {'可用工具:' if self.lang=='zh' else 'Available tools'}: ", end='')
        print(', '.join([r['info']['name'] for _, r in available]))
        print()

        scan_results = self.scanner.scan(target)

        summary = self.scanner.get_summary(scan_results)
        print(f"\n  {'扫描完成!' if self.lang=='zh' else 'Scan complete!'}")
        print(f"  {'总计:' if self.lang=='zh' else 'Total'}: {summary['total']}")
        print(f"  {'高危:' if self.lang=='zh' else 'High'}: {summary['high']} | "
              f"{'中危:' if self.lang=='zh' else 'Medium'}: {summary['medium']} | "
              f"{'低危:' if self.lang=='zh' else 'Low'}: {summary['low']}")

        return scan_results

    def cmd_template(self):
        """生成模板报告"""
        print(f"\n  {'生成模板报告...' if self.lang=='zh' else 'Generating template report...'}")

        self.project_info = {
            'name': self.i18n.t('default_project'),
            'target': 'example.com',
            'scope': self.i18n.t('all_ports'),
            'engineer': self.i18n.t('default_author'),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'version': '2.0'
        }
        self.authorized = False
        self.report_style = 'standard'
        self.report_builder.report_style = 'standard'

        report_content = self.report_builder.generate(
            project_info=self.project_info,
            scan_results=[],
            authorized=False,
            report_style=self.report_style
        )

        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = output_dir / f'渗透测试报告_模板_{timestamp}.md'

        self.report_builder.save_to_file(report_content, str(output_path))

        print(f"\n  {'模板报告已生成:' if self.lang=='zh' else 'Template report generated'}: {output_path}")

    def cmd_list_templates(self):
        """列出所有漏洞模板"""
        print(f"\n  {'漏洞模板库' if self.lang=='zh' else 'Vulnerability Templates'}")
        print(f"  {'总计:' if self.lang=='zh' else 'Total'}: {len(VULN_TEMPLATES)} {'个模板' if self.lang=='zh' else 'templates'}")
        print()

        categories = {}
        for t in VULN_TEMPLATES:
            cat = t.get('category', 'Other')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(t)

        for cat, templates in categories.items():
            print(f"  [{cat}] {len(templates)} {'个' if self.lang=='zh' else ''}")
            for t in templates[:5]:
                name = t.get('name_zh', t.get('name_en', 'Unknown'))
                sev = t.get('severity', 'N/A')
                print(f"    - {name} ({sev})")
            if len(templates) > 5:
                print(f"    ... {'等' if self.lang=='zh' else 'etc'} {len(templates)} {'个' if self.lang=='zh' else ''}")
            print()

    def cmd_config(self):
        """显示工具配置"""
        self.tool_checker.print_status()


# ========== CLI入口 ==========

def main():
    parser = argparse.ArgumentParser(
        description='PTReport - 渗透测试报告生成器 v2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python ptr.py --interactive          交互式向导模式
  python ptr.py --scan example.com    快速扫描目标
  python ptr.py --template             生成模板报告
  python ptr.py --list                列出漏洞模板
  python ptr.py --config              显示工具状态
  python ptr.py --lang zh             设置中文
  python ptr.py --lang en            设置英文
        """
    )

    parser.add_argument('--interactive', '-i', action='store_true',
                        help='交互式向导模式')
    parser.add_argument('--scan', '-s', metavar='TARGET',
                        help='扫描指定目标')
    parser.add_argument('--template', '-t', action='store_true',
                        help='生成模板报告（无扫描）')
    parser.add_argument('--list', '-l', action='store_true',
                        help='列出所有漏洞模板')
    parser.add_argument('--config', '-c', action='store_true',
                        help='显示工具配置状态')
    parser.add_argument('--lang', default='zh', choices=['zh', 'en'],
                        help='设置语言 (默认: zh)')

    args = parser.parse_args()

    app = PTReport(lang=args.lang)

    # CLI命令优先级
    if args.list:
        app.cmd_list_templates()
    elif args.config:
        app.cmd_config()
    elif args.scan:
        app.cmd_scan(args.scan)
    elif args.template:
        app.cmd_template()
    elif args.interactive:
        app.run_interactive()
    else:
        # 默认启动交互模式
        app.run_interactive()


if __name__ == '__main__':
    main()
