# PTReport
Penetration Testing Report Generator
Title:


v2.1 - PTReport | Penetration Test Report Generator
Release Note:


## PTReport v2.1

Penetration Testing Report Generator - Simple, Fast, Bilingual (Chinese/English)

---

### Features
- 5 Report Templates: Standard, Executive, Security Checklist, CTF Writeup, Full
- Bilingual Interface: Chinese / English (`--lang en`)
- PDF Export via pandoc
- No database required - single Python script

---

### Quick Start

**1. Install**
```bash
pip install -r requirements.txt
# or just: pip install jinja2
2. Run


python ptr.py
3. Select Options

Enter project name, target, scope
Choose report template (1-5)
For English: type en when asked for language
4. Output

Generated report saved to output/ folder as .md file
Report Templates
#	Template	Use Case
1	Standard	General penetration test
2	Executive	Management summary / overview
3	Security Checklist	Compliance checklist
4	CTF Writeup	CTF competition writeup
5	Full	Complete report with all sections
PDF Export
Install pandoc first:

Windows: winget install pandoc
Linux/Mac: sudo apt install pandoc
Then export from menu when prompted.

Project Structure

PTReport/
├── ptr.py              # Main program
├── report_builder.py   # Template engine
├── scanner.py          # Scan tools
├── i18n.py             # Language support
├── README.md           # Documentation
└── CHANGELOG.md        # Version history
System Requirements
Python 3.6+
jinja2
pandoc (optional, for PDF export)
License
MIT License

Contributing
Issues and pull requests welcome!
