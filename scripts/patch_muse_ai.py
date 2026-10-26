# Patch script to replace Google AI Pro with Muse AI (1 Billion Credits)

# 1. Update js/cht-core.js
with open('js/cht-core.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

old_ai_fn = """  async function setGoogleAiProStatus(userId, accessed) {
    const db = getFirestore();
    if (db && userId) {
      try {
        await db.collection('students').doc(userId).set({
          googleAiProAccessed: !!accessed
        }, { merge: true });
        return { success: true };
      } catch(e) {
        return { success: false, message: e.message };
      }
    }
    return { success: false };
  }"""

new_ai_fn = """  async function setMuseAiStatus(userId, accessed, whatsappNum = '') {
    const db = getFirestore();
    if (db && userId) {
      try {
        const updateData = {
          museAiAccessed: !!accessed
        };
        if (whatsappNum) {
          updateData.museAiWhatsApp = whatsappNum.trim();
        }
        await db.collection('students').doc(userId).set(updateData, { merge: true });
        return { success: true };
      } catch(e) {
        return { success: false, message: e.message };
      }
    }
    return { success: false };
  }
  const setGoogleAiProStatus = setMuseAiStatus;"""

if old_ai_fn in js_text:
    js_text = js_text.replace(old_ai_fn, new_ai_fn, 1)
    print("Updated setMuseAiStatus in js/cht-core.js")
else:
    print("Could not find old_ai_fn in js/cht-core.js")

if 'setGoogleAiProStatus,' in js_text:
    js_text = js_text.replace('setGoogleAiProStatus,', 'setMuseAiStatus,\n    setGoogleAiProStatus,', 1)
    print("Exported setMuseAiStatus in window.CHT")

with open('js/cht-core.js', 'w', encoding='utf-8') as f:
    f.write(js_text)

# 2. Update certificates.html
with open('certificates.html', 'r', encoding='utf-8') as f:
    cert_html = f.read()

# Replace mentions in certificates.html
cert_html = cert_html.replace(
    'grant your VIP bonuses (Canva Pro invite, Google Drive Vault, and Google AI Pro).',
    'grant your VIP bonuses (Canva Pro invite, Google Drive Vault, and Muse AI 1 Billion Credits delivered via WhatsApp).'
)

cert_html = cert_html.replace(
    '<span><strong>Google AI Pro 18-Month Package</strong> (Extended reasoning &amp; models suite)</span>',
    '<span><strong>Muse AI (1 Billion Credits)</strong> (Delivered directly to your WhatsApp number)</span>'
)

cert_html = cert_html.replace(
    '<span>Google AI Pro Package <em>(Locked)</em></span>',
    '<span>Muse AI (1 Billion Credits) <em>(Locked)</em></span>'
)

cert_html = cert_html.replace(
    '<option value="VIP_BUNDLE">⭐ Complete VIP Access Bundle (₦2,500 / Full Paid — Includes Canva Pro + Drive Vault + AI Pro)</option>',
    '<option value="VIP_BUNDLE">⭐ Complete VIP Access Bundle (₦2,500 / Full Paid — Includes Canva Pro + Drive Vault + Muse AI 1B Credits)</option>'
)

cert_html = cert_html.replace(
    'const aiProAccessed = !!freshUser.googleAiProAccessed || !!user.googleAiProAccessed;',
    'const museAiAccessed = !!freshUser.museAiAccessed || !!user.museAiAccessed || !!freshUser.googleAiProAccessed || !!user.googleAiProAccessed;'
)

old_google_box = """              <!-- 3. Google AI Pro Package -->
              <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 6px;">
                  <strong style="color: #fff; font-size: 0.95rem;">⚡ Google AI Pro (18-Month Package)</strong>
                  <span class="status-pill approved" style="font-size: 0.7rem;">Included</span>
                </div>
                <p style="color: var(--cht-text-muted); font-size: 0.82rem; line-height: 1.5; margin-bottom: 10px;">
                  Complete 18-month curriculum and practical enterprise AI automation blueprints, accessible directly inside your Master Google Drive folder.
                </p>
                
                <div style="background: rgba(0,0,0,0.25); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 12px;">
                  <div style="font-size: 0.88rem; color: #fff; font-weight: 600; margin-bottom: 6px;">
                    Have you accessed your Google AI Pro 18-Month Package?
                  </div>
                  <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                    <div style="display: flex; gap: 16px;">
                      <label style="display: flex; align-items: center; gap: 6px; cursor: pointer; color: var(--cht-text-secondary); font-size: 0.85rem;">
                        <input type="radio" name="aiProCheck" value="yes" ${aiProAccessed ? 'checked' : ''} onchange="handleAiProCheck(true, '${user.id}')">
                        <span>Yes</span>
                      </label>
                      <label style="display: flex; align-items: center; gap: 6px; cursor: pointer; color: var(--cht-text-secondary); font-size: 0.85rem;">
                        <input type="radio" name="aiProCheck" value="no" ${!aiProAccessed ? 'checked' : ''} onchange="handleAiProCheck(false, '${user.id}')">
                        <span>No</span>
                      </label>
                    </div>
                    <a href="${driveUrl}" target="_blank" rel="noopener noreferrer" class="cht-btn cht-btn-outline cht-btn-sm" style="font-size: 0.75rem; padding: 4px 10px;">
                      Open in Master Drive ↗
                    </a>
                  </div>
                </div>
              </div>"""

new_muse_box = """              <!-- 3. Muse AI (1 Billion Credits) -->
              <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 8px; padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 6px;">
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.1rem;">✨</span>
                    <strong style="color: var(--cht-gold-light); font-size: 0.95rem;">Muse AI (1 Billion Credits)</strong>
                  </div>
                  <span class="status-pill approved" style="font-size: 0.7rem; background: #22C55E; color: #000; font-weight: 700;">Delivered via WhatsApp</span>
                </div>
                <p style="color: var(--cht-text-muted); font-size: 0.82rem; line-height: 1.5; margin-bottom: 10px;">
                  Enjoy 1,000,000,000 generation credits on Muse AI for premium creative and AI workflows. Your access package and credentials are dispatched directly to your WhatsApp number by Coach Hyela upon VIP verification.
                </p>
                
                <div style="background: rgba(0,0,0,0.25); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 12px;">
                  <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 8px;">
                    <div style="font-size: 0.88rem; color: #fff; font-weight: 600;">
                      Have you received your Muse AI (1 Billion Credits) on WhatsApp?
                    </div>
                    <div style="display: flex; gap: 16px;">
                      <label style="display: flex; align-items: center; gap: 6px; cursor: pointer; color: var(--cht-text-secondary); font-size: 0.85rem;">
                        <input type="radio" name="museAiCheck" value="yes" ${museAiAccessed ? 'checked' : ''} onchange="handleMuseAiCheck(true, '${user.id}')">
                        <span>Yes</span>
                      </label>
                      <label style="display: flex; align-items: center; gap: 6px; cursor: pointer; color: var(--cht-text-secondary); font-size: 0.85rem;">
                        <input type="radio" name="museAiCheck" value="no" ${!museAiAccessed ? 'checked' : ''} onchange="handleMuseAiCheck(false, '${user.id}')">
                        <span>No</span>
                      </label>
                    </div>
                  </div>
                  <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 10px;">
                    <span style="font-size: 0.78rem; color: var(--cht-text-muted);">Official Dispatch WhatsApp: <strong>0915-963-7287</strong></span>
                    <a href="https://wa.me/2349159637287?text=Hello%20Coach%20Hyela%2C%20I%20am%20a%20verified%20VIP%20student%20(${encodeURIComponent(user.fullName)}%20-%20${encodeURIComponent(user.email)}).%20Please%20deliver%20my%20Muse%20AI%20(1%20Billion%20Credits)%20to%20my%20WhatsApp." target="_blank" rel="noopener noreferrer" class="cht-btn cht-btn-primary cht-btn-sm" style="font-size: 0.78rem; padding: 5px 12px; display: inline-flex; align-items: center; gap: 6px; font-weight: 700;">
                      <span>📲 Receive / Claim Muse AI on WhatsApp →</span>
                    </a>
                  </div>
                </div>
              </div>"""

if old_google_box in cert_html:
    cert_html = cert_html.replace(old_google_box, new_muse_box, 1)
    print("Replaced Google AI Pro box with Muse AI box in certificates.html")
else:
    print("Could not find old_google_box in certificates.html")

cert_html = cert_html.replace(
    '<li>⚡ <strong>Google AI Pro 18-Month Workflow Package</strong></li>',
    '<li>✨ <strong>Muse AI (1 Billion Credits - Delivered via WhatsApp)</strong></li>'
)

old_check_handler = """    async function handleAiProCheck(accessed, userId) {
      await CHT.setGoogleAiProStatus(userId, accessed);
    }"""

new_check_handler = """    async function handleMuseAiCheck(accessed, userId) {
      if (window.CHT && CHT.setMuseAiStatus) {
        await CHT.setMuseAiStatus(userId, accessed);
      }
    }
    const handleAiProCheck = handleMuseAiCheck;"""

if old_check_handler in cert_html:
    cert_html = cert_html.replace(old_check_handler, new_check_handler, 1)
    print("Replaced handleAiProCheck with handleMuseAiCheck")
else:
    print("Could not find old_check_handler")

with open('certificates.html', 'w', encoding='utf-8') as f:
    f.write(cert_html)
print("Finished patching certificates.html")
