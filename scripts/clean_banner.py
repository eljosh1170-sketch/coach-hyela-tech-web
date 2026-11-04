with open('certificates.html', 'r', encoding='utf-8') as f:
    text = f.read()

bad = """                <div style="background: rgba(0,0,0,0.5); border: 1px solid rgba(212,175,55,0.4); padding: 6px 14px; border-radius: 6px; text-align: center;">
                  <div style="font-size: 0.72rem; text-transform: uppercase; color: var(--cht-text-muted); letter-spacing: 1px;">Offer Ends</div>
                  <div style="font-size: 0.95rem; font-weight: 800; color: #EF4444;">31 OCT 2026</div>
                </div>
              </div>
            </div>"""

if bad in text:
    text = text.replace(bad, '', 1)
    print('Cleaned orphaned banner')
    with open('certificates.html', 'w', encoding='utf-8') as f:
        f.write(text)
else:
    print('Bad string not found')
