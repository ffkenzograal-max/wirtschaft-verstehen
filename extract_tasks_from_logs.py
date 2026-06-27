import json
import re

log_file = r"C:\Users\Gemat\.gemini\antigravity\brain\487f15fb-59b9-47ce-9e9c-b5dafe97e344\.system_generated\logs\transcript.jsonl"

tasks_found = []

try:
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                content = data.get("content", "")
                # Look for mentions of exam questions
                if "Aufgabe" in content or "задач" in content:
                    # Let's see if we can extract blocks of tasks
                    # We print a snippet
                    tasks_found.append(content)
            except Exception:
                pass
except Exception as e:
    print(f"Error opening logs: {e}")

print(f"[+] Found {len(tasks_found)} mentions in logs.")

# Let's save the extracted text to a text file for inspection
with open("extracted_logs.txt", "w", encoding="utf-8") as out:
    for i, t in enumerate(tasks_found):
        out.write(f"=== MENTION {i+1} ===\n")
        out.write(t)
        out.write("\n\n")

print("[OK] Dumped to extracted_logs.txt")
