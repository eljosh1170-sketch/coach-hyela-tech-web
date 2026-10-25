import json

transcript_path = r'C:\Users\USER\.gemini\antigravity\brain\fbf7f6a7-9a4a-4d42-b6dd-dd251192ac6d\.system_generated\logs\transcript_full.jsonl'

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            obj = json.loads(line)
            if obj.get('type') == 'USER_INPUT':
                txt = obj.get('content', '')
                if any(w in txt.lower() for w in ['vault', 'drive', 'master', 'prompts', 'canva', 'folder']):
                    print(f"Step {obj.get('step_index')}: {txt}\n{'='*60}")
        except Exception:
            pass
