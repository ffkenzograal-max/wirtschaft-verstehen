import glob
import re

with open("broken_report.txt", "w", encoding="utf-8") as out:
    for fn in glob.glob("chapter_*.md"):
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check for inline math
        math_instances = re.findall(r'\$[^\$]+\$', content)
        if math_instances:
            out.write(f"[{fn}] Found inline math:\n")
            for inst in math_instances:
                out.write(f"  {inst}\n")

        # Check for single/double asterisks
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '*' in line:
                if re.match(r'^\s*\*\s', line):
                    continue
                if '**' in line:
                    if line.count('**') % 2 != 0:
                        out.write(f"[{fn}:L{i+1}] Unbalanced bold asterisks: {line}\n")
                    continue
                if line.count('*') % 2 != 0:
                    out.write(f"[{fn}:L{i+1}] Unbalanced single asterisks: {line}\n")

print("[OK] Dumped")
