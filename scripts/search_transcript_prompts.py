import json

transcript_path = r'C:\Users\USER\.gemini\antigravity\brain\fbf7f6a7-9a4a-4d42-b6dd-dd251192ac6d\.system_generated\logs\transcript_full.jsonl'

keywords = ['drive', 'prompt', 'folder', 'canva', 'vip', 'link']

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            obj = json.loads(line)
            if obj.get('source') in ['USER', 'USER_EXPLICIT'] or obj.get('type') == 'USER_INPUT':
                txt = str(obj.get('content', ''))
                lower = txt.lower()
                if any(k in lower for k in ['drive', 'canva', 'prompt', 'folder']):
                    print(f"=== STEP {obj.get('step_index')} ===")
                    print(txt)
                    print("-" * 50)
        except Exception as e:
            pass
