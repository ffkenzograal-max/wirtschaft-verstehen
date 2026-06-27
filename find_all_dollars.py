import glob

with open("all_dollars.txt", "w", encoding="utf-8") as out:
    for fn in glob.glob("chapter_*.md"):
        with open(fn, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for i, l in enumerate(lines):
            if "$" in l:
                out.write(f"{fn}:L{i+1}: {l.strip()}\n")

print("[OK] Dumped to all_dollars.txt")
