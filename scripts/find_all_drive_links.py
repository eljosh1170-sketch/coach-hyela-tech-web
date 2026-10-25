import json
import re

transcript_path = r'C:\Users\USER\.gemini\antigravity\brain\fbf7f6a7-9a4a-4d42-b6dd-dd251192ac6d\.system_generated\logs\transcript_full.jsonl'

pattern = re.compile(r'https?://[^\s"\'<>]+drive\.google\.com[^\s"\'<>]*', re.IGNORECASE)

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            matches = pattern.findall(line)
            if matches:
                obj = json.loads(line)
                step = obj.get('step_index')
                src = obj.get('source')
                print(f"Step {step} ({src}): {matches}")
        except Exception:
            pass
