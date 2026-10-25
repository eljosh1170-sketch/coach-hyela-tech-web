import glob
import re

for f in glob.glob('*.html'):
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    c2 = re.sub(r'src="js/cht-core\.js(\?v=[^"]*)?"', 'src="js/cht-core.js?v=20261025_08"', c)
    if c2 != c:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(c2)
        print('Updated', f)
