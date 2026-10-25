import json
import re

transcript_path = r'C:\Users\USER\.gemini\antigravity\brain\fbf7f6a7-9a4a-4d42-b6dd-dd251192ac6d\.system_generated\logs\transcript_full.jsonl'

pattern = re.compile(r'(https?://[^\s"\'<>]*drive\.google\.com[^\s"\'<>]*)', re.IGNORECASE)

with open(transcript_path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        m = pattern.findall(line)
        if m:
            # check if any match is NOT generic drive.google.com
            specific = [url for url in m if url != 'https://drive.google.com' and url != 'https://drive.google.com"']
            if specific:
                print(f"Line {i}: {specific}")
