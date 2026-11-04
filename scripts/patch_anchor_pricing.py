import re

# 1. Update certificates.html
with open('certificates.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace Urgency Alert Banner in certificates.html
old_banner_regex = r'<div style="background: linear-gradient\(135deg, rgba\(212, 175, 55, 0\.15\), rgba\(239, 68, 68, 0\.1\)\); border: 1px solid var\(--cht-gold-500\); border-radius: 8px; padding: 16px; margin-bottom: 24px;">[\s\S]*?</div>\s*</div>\s*</div>'

new_banner_html = """<div style="background: linear-gradient(135deg, rgba(212, 175, 55, 0.18), rgba(239, 68, 68, 0.12)); border: 1px solid var(--cht-gold-500); border-radius: 8px; padding: 16px; margin-bottom: 24px;">
              <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                  <span style="font-size: 1.5rem;">🔥</span>
                  <div>
                    <strong style="color: var(--cht-gold-light); font-size: 1.05rem; text-transform: uppercase; letter-spacing: 0.5px;">Special Allocation Offer — Open While Stock Lasts!</strong>
                    <div style="font-size: 0.88rem; color: #fff; margin-top: 3px;">
                      Complete VIP Access is discounted to <strong>₦5,000</strong> with <strong>Muse AI (1 Billion Credits)</strong> included. Official Certificate Only is <strong>₦10,000</strong>.
                    </div>
                  </div>
                </div>
                <div style="background: rgba(0,0,0,0.6); border: 1px solid rgba(212,175,55,0.5); padding: 6px 14px; border-radius: 6px; text-align: center;">
                  <div style="font-size: 0.72rem; text-transform: uppercase; color: var(--cht-gold-light); letter-spacing: 1px; font-weight: 700;">Status</div>
                  <div style="font-size: 0.92rem; font-weight: 800; color: #86EFAC;">WHILE STOCK LASTS</div>
                </div>
              </div>
            </div>"""

text = re.sub(old_banner_regex, new_banner_html, text, count=1)

# Replace VIP Bundle card price and button
old_vip_card_regex = r'<span style="font-size: 2\.2rem; font-weight: 800; color: var\(--cht-gold-light\);">₦2,500</span>[\s\S]*?Select VIP Bundle — Pay ₦2,500 →\s*</button>'

new_vip_card_html = """<span style="font-size: 2.2rem; font-weight: 800; color: var(--cht-gold-light);">₦5,000</span>
                    <span style="text-decoration: line-through; color: var(--cht-text-muted); font-size: 1.1rem;">₦15,000</span>
                    <span style="background: rgba(34, 197, 94, 0.2); color: #86EFAC; font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 4px;">Save ₦10,000 (50% Off Certificate Solo!)</span>
                  </div>

                  <ul style="list-style: none; padding: 0; margin: 0 0 20px 0; font-size: 0.88rem; color: var(--cht-text-secondary); line-height: 1.8;">
                    <li style="display: flex; align-items: flex-start; gap: 8px;">
                      <span style="color: #22C55E; font-weight: bold;">✓</span>
                      <span><strong>Official Certificate of Completion</strong> (with Verifiable QR Code &amp; Direct Link)</span>
                    </li>
                    <li style="display: flex; align-items: flex-start; gap: 8px;">
                      <span style="color: #22C55E; font-weight: bold;">✓</span>
                      <span><strong>1-Year Canva Pro Team Access</strong> (Brand kits, magic AI tools, premium assets)</span>
                    </li>
                    <li style="display: flex; align-items: flex-start; gap: 8px;">
                      <span style="color: #22C55E; font-weight: bold;">✓</span>
                      <span><strong>Complete Master Prompts Suite &amp; Drive Vault</strong> (All 23 AI Production Engines)</span>
                    </li>
                    <li style="display: flex; align-items: flex-start; gap: 8px;">
                      <span style="color: #22C55E; font-weight: bold;">✓</span>
                      <span><strong>Muse AI (1 Billion Generation Credits)</strong> — <em>Delivered to your WhatsApp while stock lasts!</em></span>
                    </li>
                  </ul>
                </div>

                <button type="button" class="cht-btn cht-btn-primary" onclick="selectPaymentTier('VIP_BUNDLE', 5000)" style="width: 100%; font-weight: 700; padding: 12px; font-size: 0.95rem;">
                  Select VIP Bundle — Pay ₦5,000 →
                </button>"""

text = re.sub(old_vip_card_regex, new_vip_card_html, text, count=1)

# Replace Certificate Only card price and button
old_cert_card_regex = r'<span style="font-size: 2\.2rem; font-weight: 800; color: #FFFFFF;">₦500</span>[\s\S]*?Select Certificate Only — Pay ₦500 →\s*</button>'

new_cert_card_html = """<span style="font-size: 2.2rem; font-weight: 800; color: #FFFFFF;">₦10,000</span>
                    <span style="color: var(--cht-text-muted); font-size: 0.88rem; font-weight: 500;">Official Standalone Price</span>
                  </div>

                  <div style="background: rgba(212,175,55,0.1); border: 1px solid rgba(212,175,55,0.25); border-radius: 6px; padding: 10px; margin-bottom: 14px; font-size: 0.82rem; color: var(--cht-gold-light);">
                    💡 <strong>Smart Move:</strong> Get the <strong>Complete VIP Package for only ₦5,000</strong> — includes this certificate PLUS Canva Pro, Master Prompts &amp; Muse AI!
                  </div>

                  <ul style="list-style: none; padding: 0; margin: 0 0 20px 0; font-size: 0.88rem; color: var(--cht-text-secondary); line-height: 1.8;">
                    <li style="display: flex; align-items: flex-start; gap: 8px;">
                      <span style="color: #22C55E; font-weight: bold;">✓</span>
                      <span><strong>Official Certificate of Completion</strong> (with Verifiable QR Code &amp; Direct Link)</span>
                    </li>
                    <li style="display: flex; align-items: flex-start; gap: 8px; color: var(--cht-text-muted);">
                      <span style="color: #EF4444; font-weight: bold;">✕</span>
                      <span>1-Year Canva Pro Team Access <em>(Locked)</em></span>
                    </li>
                    <li style="display: flex; align-items: flex-start; gap: 8px; color: var(--cht-text-muted);">
                      <span style="color: #EF4444; font-weight: bold;">✕</span>
                      <span>Master Prompts Suite &amp; Drive Vault <em>(Locked)</em></span>
                    </li>
                    <li style="display: flex; align-items: flex-start; gap: 8px; color: var(--cht-text-muted);">
                      <span style="color: #EF4444; font-weight: bold;">✕</span>
                      <span>Muse AI 1 Billion Credits <em>(Locked)</em></span>
                    </li>
                  </ul>
                </div>

                <button type="button" class="cht-btn cht-btn-outline" onclick="selectPaymentTier('CERT_ONLY', 10000)" style="width: 100%; font-weight: 700; padding: 12px; font-size: 0.95rem; border-color: rgba(255,255,255,0.3);">
                  Select Certificate Only — Pay ₦10,000 →
                </button>"""

text = re.sub(old_cert_card_regex, new_cert_card_html, text, count=1)

# Replace select dropdown options
text = text.replace(
    '<option value="VIP_BUNDLE">⭐ Complete VIP Access Bundle (₦2,500 / Full Paid — Includes Canva Pro + Master Prompts Vault + Flow Access)</option>',
    '<option value="VIP_BUNDLE">⭐ Complete VIP Access Bundle (₦5,000 — Includes Certificate + Canva Pro + Master Prompts + Muse AI 1B Credits)</option>'
)
text = text.replace(
    '<option value="VIP_BUNDLE">⭐ Complete VIP Access Bundle (₦2,500 / Full Paid — Includes Canva Pro + Drive Vault + Muse AI 1B Credits)</option>',
    '<option value="VIP_BUNDLE">⭐ Complete VIP Access Bundle (₦5,000 — Includes Certificate + Canva Pro + Master Prompts + Muse AI 1B Credits)</option>'
)
text = text.replace(
    '<option value="CERT_ONLY">🎓 Official Certificate Only (₦500 Promo Tier — Verifiable QR Certificate Only)</option>',
    '<option value="CERT_ONLY">🎓 Official Certificate Only (₦10,000 — Verifiable QR Certificate Only)</option>'
)

# Replace JS tier defaults and labels
text = text.replace(
    "const tierLabel = packageTier === 'CERT_ONLY' ? 'Official Certificate Only (₦500 Promo Tier)' : 'Complete VIP Access Bundle (₦2,500)';",
    "const tierLabel = packageTier === 'CERT_ONLY' ? 'Official Certificate Only (₦10,000)' : 'Complete VIP Access Bundle (₦5,000)';",
)
text = text.replace(
    "selectPaymentTier('VIP_BUNDLE', 2500);",
    "selectPaymentTier('VIP_BUNDLE', 5000);",
)
text = text.replace(
    "const tierName = tier === 'VIP_BUNDLE' ? 'Complete VIP Access Bundle (₦2,500)' : 'Official Certificate Only (₦500)';",
    "const tierName = tier === 'VIP_BUNDLE' ? 'Complete VIP Access Bundle (₦5,000)' : 'Official Certificate Only (₦10,000)';",
)
text = text.replace(
    "Complete VIP Package (₦2,500)",
    "Complete VIP Package (₦5,000)",
)
text = text.replace(
    "Official Certificate Only (₦500)",
    "Official Certificate Only (₦10,000)",
)
text = text.replace(
    "Selected: Complete VIP Bundle (₦2,500)",
    "Selected: Complete VIP Bundle (₦5,000)",
)
text = text.replace(
    "enrollment (₦2,500 package)",
    "enrollment (₦5,000 package)",
)

with open('certificates.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated certificates.html successfully")

# 2. Update admin.html
with open('admin.html', 'r', encoding='utf-8') as f:
    admin_text = f.read()

admin_text = admin_text.replace(
    '<span id="reviewPackageTierBadge" style="font-weight:700;">VIP Package (₦2,500)</span>',
    '<span id="reviewPackageTierBadge" style="font-weight:700;">VIP Package (₦5,000)</span>'
)
admin_text = admin_text.replace(
    'Uncheck if student only paid ₦500 for Certificate Only (keeps Drive &amp; Canva vault locked).',
    'Uncheck if student only paid ₦10,000 for Certificate Only solo (keeps Drive &amp; Canva vault locked).'
)
admin_text = admin_text.replace(
    "? '<span style=\"background:rgba(255,255,255,0.1); color:#fff; padding:2px 8px; border-radius:4px; font-size:0.75rem;\">🎓 Cert Only (₦500)</span>'\n                  : '<span style=\"background:rgba(212,175,55,0.2); color:var(--cht-gold-light); padding:2px 8px; border-radius:4px; font-size:0.75rem; font-weight:700;\">⭐ VIP (₦2,500)</span>'",
    "? '<span style=\"background:rgba(255,255,255,0.1); color:#fff; padding:2px 8px; border-radius:4px; font-size:0.75rem;\">🎓 Cert Only (₦10,000)</span>'\n                  : '<span style=\"background:rgba(212,175,55,0.2); color:var(--cht-gold-light); padding:2px 8px; border-radius:4px; font-size:0.75rem; font-weight:700;\">⭐ VIP (₦5,000)</span>'"
)
admin_text = admin_text.replace(
    "? '<span style=\"background:rgba(255,255,255,0.1); color:#fff; padding:2px 8px; border-radius:4px; font-size:0.8rem;\">🎓 Certificate Only (₦500 Tier)</span>'\n          : '<span style=\"background:rgba(212,175,55,0.2); color:var(--cht-gold-light); padding:2px 8px; border-radius:4px; font-size:0.8rem; font-weight:700;\">⭐ Complete VIP Package (₦2,500 Tier)</span>'",
    "? '<span style=\"background:rgba(255,255,255,0.1); color:#fff; padding:2px 8px; border-radius:4px; font-size:0.8rem;\">🎓 Certificate Only (₦10,000 Solo Tier)</span>'\n          : '<span style=\"background:rgba(212,175,55,0.2); color:var(--cht-gold-light); padding:2px 8px; border-radius:4px; font-size:0.8rem; font-weight:700;\">⭐ Complete VIP Package (₦5,000 Tier)</span>'"
)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_text)
print("Updated admin.html successfully")

# 3. Update GEMINI.md
with open('GEMINI.md', 'r', encoding='utf-8') as f:
    gemini_text = f.read()

gemini_old_section = """## 2. Pricing & Enrollment Down-Sell Structure (Promo valid till October 31st, 2026)
- **Complete VIP Access Package**:
  - **Promo Price**: `₦2,500` (Discounted from `₦4,000`)
  - **Includes**: Official Certificate of Completion (with QR code) + 1-Year Canva Pro Team Access + Google Drive Master Prompts & E-Books Vault + Muse AI (1 Billion Credits - delivered to student's WhatsApp).
- **Official Certificate Only (Strategic Down-Sell)**:
  - **Promo Price**: `₦500` (Discounted from `₦5,000`)
  - **Strategic Purpose**: First time ever offered separately. Serves as a low-barrier down-sell so students who cannot afford ₦2,500 still contribute revenue. Zero lost leads.
  - **Includes**: Official Certificate of Completion (with QR code). Canva Pro, Master Prompts, and Muse AI remain locked until upgraded.
- **Promo Expiry**: **31st of October 2026**."""

gemini_new_section = """## 2. Pricing & Enrollment Psychological Anchor Structure (Offer open while Muse AI stock lasts)
- **Complete VIP Access Package**:
  - **Current Price**: `₦5,000`
  - **Strategic Role**: The irresistible no-brainer bundle. Costing half the price of the certificate alone, students naturally choose VIP.
  - **Includes**: Official Certificate of Completion (with QR code) + 1-Year Canva Pro Team Access + Complete 23 Master Prompts Suite & Google Drive Vault + Muse AI (1 Billion Credits - delivered to student's WhatsApp while stock lasts).
- **Official Certificate Only (High Anchor Bait)**:
  - **Price**: `₦10,000`
  - **Strategic Purpose**: Acts as the anchor price so students recognize that getting the Complete VIP Package at ₦5,000 is an immense bargain.
  - **Includes**: Official Certificate of Completion (with QR code). Canva Pro, Master Prompts, and Muse AI remain locked until upgraded.
- **Offer Condition**: **Open while Muse AI stock lasts**."""

if gemini_old_section in gemini_text:
    gemini_text = gemini_text.replace(gemini_old_section, gemini_new_section)
    print("Replaced pricing section in GEMINI.md")
else:
    print("Could not find exact pricing section in GEMINI.md, will search for partial")

gemini_text = gemini_text.replace("₦2,500 (Full VIP) or ₦500 (Certificate Only)", "₦5,000 (Full VIP) or ₦10,000 (Certificate Only)")

with open('GEMINI.md', 'w', encoding='utf-8') as f:
    f.write(gemini_text)
print("Updated GEMINI.md successfully")
