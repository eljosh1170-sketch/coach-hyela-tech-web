# scripts/patch_render_drive_vault.py
import re

DRIVE_LINK = "https://drive.google.com/drive/folders/1_0uldj8-IFcWQxRa4PuFRFVgCRDeSNDJ?usp=drive_link"

with open('certificates.html', 'r', encoding='utf-8') as f:
    cert_html = f.read()

new_vault_code = f"""    // 7. RENDER RESTRICTED VIP GOOGLE DRIVE VAULT & MASTER PROMPTS
    function renderDriveVault(user) {{
      const users = CHT.getUsers();
      const freshUser = users.find(u => (u.id === user.id || u.email.toLowerCase() === user.email.toLowerCase())) || user;
      const isEligible = !!freshUser.driveAccess || !!user.driveAccess;
      const driveUrl = (window.CHT && CHT.getMasterDriveUrl) ? CHT.getMasterDriveUrl() : "{DRIVE_LINK}";

      const badge = document.getElementById('drivePermissionBadge');
      const container = document.getElementById('driveAccessContainer');

      if (isEligible) {{
        badge.innerHTML = `<span class="status-badge approved" style="background:#22C55E; color:#000; font-weight:800; padding:4px 10px;">✓ VIP ACCESS ACTIVE</span>`;
        container.innerHTML = `
          <div style="background: rgba(34, 197, 94, 0.08); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: var(--cht-radius-md); padding: 18px; margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 14px; color: #86EFAC; font-weight: 700; font-size: 0.92rem;">
              <span>🌟 Exclusive VIP Candidate Access Granted for ${{user.email}}</span>
            </div>
            
            <div style="display: flex; flex-direction: column; gap: 12px;">
              <!-- 1. Master AI Prompts & E-Books Google Drive -->
              <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 6px;">
                  <strong style="color: #fff; font-size: 0.95rem;">📁 Master AI Prompts &amp; E-Books Library</strong>
                  <span class="status-pill approved" style="font-size: 0.7rem;">Google Drive Live</span>
                </div>
                <p style="color: var(--cht-text-muted); font-size: 0.82rem; line-height: 1.5; margin-bottom: 12px;">
                  Includes commercial master prompts for ChatGPT, Midjourney, Claude, AI Avatar Lip-Sync workflows, CapCut post-production templates &amp; UGC advertising scripts.
                </p>
                <a href="${{driveUrl}}" target="_blank" rel="noopener noreferrer" class="cht-btn cht-btn-primary cht-btn-sm" style="font-weight: 700; display: inline-flex; align-items: center; gap: 6px;">
                  Open Master Prompts Drive Folder ↗
                </a>
              </div>

              <!-- 2. Canva Pro 1-Year Access -->
              <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 6px;">
                  <strong style="color: #fff; font-size: 0.95rem;">🎨 Canva Pro (1-Year VIP Access)</strong>
                  <span class="status-pill approved" style="font-size: 0.7rem;">Active</span>
                </div>
                <p style="color: var(--cht-text-muted); font-size: 0.82rem; line-height: 1.5; margin-bottom: 12px;">
                  1-Year premium Canva Pro creative suite license. To claim your direct team invite, tap below to notify Coach Hyela directly on WhatsApp with your verified email (${{user.email}}).
                </p>
                <a href="https://wa.me/2349159637287?text=Hello%20Coach%20Hyela%2C%20my%20VIP%20student%20access%20is%20active%20on%20the%20website.%20Please%20grant%20my%20email%20(${{encodeURIComponent(user.email)}})%20direct%20access%20to%20the%201-Year%20Canva%20Pro%20Team%20workspace." target="_blank" rel="noopener noreferrer" class="cht-btn cht-btn-outline cht-btn-sm" style="display: inline-flex; align-items: center; gap: 6px; border-color: #25D366; color: #86EFAC;">
                  Claim Canva Pro Access on WhatsApp 💬
                </a>
              </div>

              <!-- 3. Google AI Pro Package -->
              <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 4px;">
                  <strong style="color: #fff; font-size: 0.95rem;">⚡ Google AI Pro (18-Month Package)</strong>
                  <span class="status-pill approved" style="font-size: 0.7rem;">Included</span>
                </div>
                <p style="color: var(--cht-text-muted); font-size: 0.82rem; line-height: 1.5; margin: 0;">
                  Complete 18-month curriculum and practical enterprise AI automation blueprints, accessible directly inside your Master Google Drive folder above.
                </p>
              </div>

              <!-- 4. Certified Credential -->
              <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 4px;">
                  <strong style="color: #fff; font-size: 0.95rem;">🎓 Coach Hyela Tech Industries Limited Official Certificate</strong>
                  <span class="status-pill approved" style="font-size: 0.7rem;">Official</span>
                </div>
                <p style="color: var(--cht-text-muted); font-size: 0.82rem; line-height: 1.5; margin: 0;">
                  Official verified digital credential with public QR code validation and permanent verification link.
                </p>
              </div>
            </div>
          </div>
        `;
      }} else {{
        badge.innerHTML = `<span class="status-badge pending">🔒 VIP Verification Required</span>`;
        container.innerHTML = `
          <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: var(--cht-radius-md); padding: 16px;">
            <div style="display: flex; align-items: center; gap: 8px; color: #FCD34D; font-weight: 700; font-size: 0.9rem; margin-bottom: 8px;">
              <span>🔒 Restricted VIP Resource Suite</span>
            </div>
            <p style="color: var(--cht-text-muted); font-size: 0.84rem; line-height: 1.6; margin-bottom: 12px;">
              Your account (${{user.email}}) is currently pending VIP verification. Once Coach Hyela verifies your course enrollment or fee payment, this vault will unlock automatically with:
            </p>
            <ul style="color: var(--cht-text-secondary); font-size: 0.82rem; line-height: 1.8; margin-left: 20px; margin-bottom: 14px;">
              <li>🎨 <strong>Canva Pro (1-Year Access)</strong></li>
              <li>📁 <strong>Master AI Prompts &amp; E-Books Google Drive Vault</strong></li>
              <li>⚡ <strong>Google AI Pro 18-Month Workflow Package</strong></li>
              <li>🎓 <strong>Official Verified Coach Hyela Tech Certificate</strong></li>
            </ul>
            <a href="https://wa.me/2349159637287?text=Hello%20Coach%20Hyela%2C%20I%20have%20registered%20on%20your%20website%20with%20email%3A%20${{encodeURIComponent(user.email)}}.%20Please%20verify%20my%20VIP%20Student%20Access." target="_blank" rel="noopener noreferrer" class="cht-btn cht-btn-outline cht-btn-sm" style="display: inline-flex; align-items: center; gap: 6px;">
              Contact Coach Hyela to Confirm VIP Access 💬
            </a>
          </div>
        `;
      }}
    }}"""

# Regex match renderDriveVault function
pattern = r"// 7\.\s*RENDER RESTRICTED GooGLE DRIVE VAULT\s*\r?\n\s*function renderDriveVault\(user\) \{[\s\S]*?\}\r?\n\s*\r?\n\s*// 8\."
match = re.search(pattern, cert_html)
if match:
    cert_html = cert_html[:match.start()] + new_vault_code + "\n\n    // 8." + cert_html[match.end():]
    print("Successfully replaced renderDriveVault using regex!")
else:
    print("Failed to match renderDriveVault with regex")

# Also bump cache buster to v=20261025_06
cert_html = re.sub(r'src="js/cht-core\.js(\?v=[^"]*)?"', 'src="js/cht-core.js?v=20261025_06"', cert_html)

with open('certificates.html', 'w', encoding='utf-8') as f:
    f.write(cert_html)

print("certificates.html patched!")
