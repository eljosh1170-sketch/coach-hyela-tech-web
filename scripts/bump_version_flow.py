import glob
import re

files = glob.glob('*.html')
new_ver = '20261102_01'

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    updated = re.sub(r'cht-core\.js\?v=[a-zA-Z0-9_]+', f'cht-core.js?v={new_ver}', content)
    if updated != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f"Bumped version in {filepath}")

print("Version bump complete.")
