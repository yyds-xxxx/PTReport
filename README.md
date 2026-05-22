Title:


v2.1 - PTReport | Penetration Test Report Generator
Description:


## PTReport v2.1

Penetration Testing Report Generator - Simple, Fast, Bilingual (Chinese/English)

---

### Features
- 5 Report Templates: Standard, Executive, Security Checklist, CTF Writeup, Full
- Bilingual Interface: Chinese / English switch
- PDF Export via pandoc
- No database required - single Python script

---

### Quick Start

**1. Install dependencies**
```bash
pip install jinja2
2. Run the program


python ptr.py
3. Follow the prompts

Enter project name, target, scope
Select report template (1-5)
Select language (cn/en)
4. Output

Report saved to output/ folder as .md file
Commands
Command	Description
python ptr.py	Start program (default Chinese)
python ptr.py --lang en	Start in English mode
Interactive Options:

1 - Standard template
2 - Executive summary
3 - Security checklist
4 - CTF writeup
5 - Full report
Report Templates
#	Template	Use Case
1	Standard	General penetration test
2	Executive	Management summary
3	Security Checklist	Compliance audit
4	CTF Writeup	CTF competition writeup
5	Full	Complete all-in-one report
PDF Export
Install pandoc:

Windows: winget install pandoc
Linux: sudo apt install pandoc
Mac: brew install pandoc
Export: When prompted in program, select PDF export option.

Project Structure

PTReport/
├── ptr.py              # Main program
├── report_builder.py   # Template engine
├── scanner.py          # Scan tools integration
├── i18n.py             # Language support
├── README.md           # Full documentation
└── CHANGELOG.md        # Version history
Requirements
Python 3.6+
jinja2
License
MIT License
