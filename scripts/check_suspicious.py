import os, sys, re

suspicious_patterns = [
    r'&#[0-9]+;',
    r'â',
    r'ð',
    r'Ã',
    r'Â',
    r'™',
    r'CafAc',
    r'DoMContentLoaded',
    r'JSoN',
    r'toStudent',
    r'toSign',
    r'toRegister',
    r'tothe',
    r'toThis',
    r'VideoCreation',
    r'videoscenes',
    r'videoadvertisements',
    r'videoeditors',
    r'videoassignments',
    r'Demostudent',
    r'Demotest',
    r'DemoReset',
    r'DoYou',
    r'nofalse',
    r'zerofalse',
    r'Toequip',
    r'intomeaningful',
    r'Tohelp',
    r'tocreate',
    r'togive',
    r'tobuild',
    r'toGrant',
    r'toyour'
]

total_found = 0
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith(('.html', '.js', '.css', '.json')) and not f.startswith('_') and not 'scripts' in root:
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                txt = fp.read()
            for pattern in suspicious_patterns:
                matches = list(re.finditer(pattern, txt))
                if matches:
                    # Filter out allowed HTML entities like checkmark &#10003; or &#9662; or &#9888;
                    filtered = []
                    for m in matches:
                        matched_str = m.group(0)
                        if matched_str in ['&#10003;', '&#10005;', '&#9662;', '&#9888;', '&#9998;']:
                            continue
                        filtered.append(matched_str)
                    if filtered:
                        print(f'{p}: found {pattern} -> {filtered[:5]}')
                        total_found += len(filtered)

print(f'Total suspicious items found: {total_found}')
