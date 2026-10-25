# scripts/add_firebase_to_all_pages.py
import glob

fb_scripts = """  <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore-compat.js"></script>
  <script src="js/cht-core.js"></script>"""

pages = ['about.html', 'cac.html', 'contact.html', 'index.html', 'privacy.html', 'services.html', 'training.html', 'verify.html']

for page in pages:
    with open(page, 'r', encoding='utf-8') as f:
        html = f.read()

    if 'firebase-firestore-compat.js' not in html and '<script src="js/cht-core.js"></script>' in html:
        html = html.replace('<script src="js/cht-core.js"></script>', fb_scripts)
        with open(page, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Added Firebase SDKs to {page}")

# Now enhance verify.html executeLookup to use findCertificateByIdCloud
with open('verify.html', 'r', encoding='utf-8') as f:
    verify_html = f.read()

old_lookup = """    function executeLookup(code) {
      const resultBox = document.getElementById('verifyResultContainer');
      const notFoundBox = document.getElementById('verifyNotFound');

      resultBox.style.display = 'none';
      notFoundBox.style.display = 'none';

      if (!code) return;

      const cert = CHT.findCertificateById(code);"""

new_lookup = """    async function executeLookup(code) {
      const resultBox = document.getElementById('verifyResultContainer');
      const notFoundBox = document.getElementById('verifyNotFound');

      resultBox.style.display = 'none';
      notFoundBox.style.display = 'none';

      if (!code) return;

      let cert = CHT.findCertificateById(code);
      if (!cert && CHT.findCertificateByIdCloud) {
        cert = await CHT.findCertificateByIdCloud(code);
      }"""

if old_lookup in verify_html:
    verify_html = verify_html.replace(old_lookup, new_lookup)
    with open('verify.html', 'w', encoding='utf-8') as f:
        f.write(verify_html)
    print("Enhanced verify.html with cloud lookup")

print("All pages successfully updated with Firebase Cloud SDKs!")
