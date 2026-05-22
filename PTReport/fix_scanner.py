
import shutil
shutil.copy("scanner_backup.py", "scanner.py")
with open("scanner.py", "r", encoding="utf-8", errors="replace") as f:
    content = f.read()
# Replace all occurrences of the corruption
content = content.replace("text_output.split('
'):
'):
'):
''):", "text_output.split('\n'):")
with open("scanner.py", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
