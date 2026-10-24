import sys, os, re, subprocess

all_ok = True
for f in os.listdir('.'):
    if f.endswith('.html'):
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            c = fp.read()
        scripts = re.findall(r'<script(?:\s+[^>]*)?>([\s\S]*?)<\/script>', c)
        for i, s in enumerate(scripts):
            if s.strip():
                tmp = f'_check_{f}_{i}.js'
                with open(tmp, 'w', encoding='utf-8') as out:
                    out.write(s)
                res = subprocess.run(['node', '-c', tmp], capture_output=True, text=True)
                if res.returncode != 0:
                    print(f'SYNTAX ERROR in {f} script {i}:')
                    print(res.stderr.strip()[:300])
                    all_ok = False
                os.remove(tmp)

if all_ok:
    print('SUCCESS: ALL inline scripts in all HTML files have VALID JavaScript syntax!')
