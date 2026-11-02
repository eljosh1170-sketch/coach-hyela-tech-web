# -*- coding: utf-8 -*-
with open('certificates.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace text mentions
text = text.replace(
    'grant your VIP bonuses (Canva Pro invite, Google Drive Vault, and Muse AI 1 Billion Credits delivered via WhatsApp).',
    'grant your VIP bonuses (Canva Pro invite, In-Portal Master Prompts Vault, and Flow Creative Access).'
)

text = text.replace(
    '<span><strong>Muse AI (1 Billion Credits)</strong> (Delivered directly to your WhatsApp number)</span>',
    '<span><strong>Flow Creative AI Access</strong> (AI generation models &amp; video workflow suite)</span>'
)

text = text.replace(
    '<span>Muse AI (1 Billion Credits) <em>(Locked)</em></span>',
    '<span>Flow Creative AI Access <em>(Locked)</em></span>'
)

text = text.replace(
    '<option value="VIP_BUNDLE">⭐ Complete VIP Access Bundle (₦2,500 / Full Paid — Includes Canva Pro + Drive Vault + Muse AI 1B Credits)</option>',
    '<option value="VIP_BUNDLE">⭐ Complete VIP Access Bundle (₦2,500 / Full Paid — Includes Canva Pro + Master Prompts Vault + Flow Access)</option>'
)

text = text.replace(
    '<li>✨ <strong>Muse AI (1 Billion Credits - Delivered via WhatsApp)</strong></li>',
    '<li>⚡ <strong>Flow Creative AI Access</strong></li>'
)

# 2. In renderDriveAccess, update variables
old_vars = """      const canvaStatus = freshUser.canvaStatus || user.canvaStatus || 'NOT_CLAIMED';
      const canvaEmail = freshUser.canvaEmail || user.canvaEmail || user.email;
      const museAiAccessed = !!freshUser.museAiAccessed || !!user.museAiAccessed || !!freshUser.googleAiProAccessed || !!user.googleAiProAccessed;
      const studentName = freshUser.fullName || user.fullName || 'Verified VIP Candidate';"""

new_vars = """      const canvaStatus = freshUser.canvaStatus || user.canvaStatus || 'NOT_CLAIMED';
      const canvaEmail = freshUser.canvaEmail || user.canvaEmail || user.email;
      const flowAccessed = !!freshUser.flowAccessed || !!user.flowAccessed || !!freshUser.googleAiProAccessed || !!user.googleAiProAccessed;
      const museAiPaid = !!freshUser.museAiPaid || !!user.museAiPaid;
      const museAiAccessed = !!freshUser.museAiAccessed || !!user.museAiAccessed;
      const studentName = freshUser.fullName || user.fullName || 'Verified VIP Candidate';"""

if old_vars in text:
    text = text.replace(old_vars, new_vars, 1)
    print("[OK] Replaced variables in renderDriveAccess")
else:
    print("Could not find old_vars in certificates.html")

# 3. Replace Muse AI box with Flow + Standalone Muse AI
old_muse_box = """              <!-- 3. Muse AI (1 Billion Credits) -->
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
                    <a href="https://wa.me/2349159637287?text=Hello%20Coach%20Hyela%2C%20I%20am%20a%20verified%20VIP%20student%20(${encodeURIComponent(studentName)}%20-%20${encodeURIComponent(studentEmail)}).%20Please%20deliver%20my%20Muse%20AI%20(1%20Billion%20Credits)%20to%20my%20WhatsApp." target="_blank" rel="noopener noreferrer" class="cht-btn cht-btn-primary cht-btn-sm" style="font-size: 0.78rem; padding: 5px 12px; display: inline-flex; align-items: center; gap: 6px; font-weight: 700;">
                      <span>📲 Receive / Claim Muse AI on WhatsApp →</span>
                    </a>
                  </div>
                </div>
              </div>"""

new_flow_muse_box = """              <!-- 3. Flow Creative AI Access (Included in VIP) -->
              <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 8px; padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 6px;">
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.1rem;">⚡</span>
                    <strong style="color: #fff; font-size: 0.95rem;">Flow Creative AI Suite</strong>
                  </div>
                  <span class="status-pill approved" style="font-size: 0.7rem; background: ${flowAccessed ? '#22C55E' : '#EAB308'}; color: #000; font-weight: 700;">
                    ${flowAccessed ? '✓ Verified Active' : 'Pending Confirmation'}
                  </span>
                </div>
                <p style="color: var(--cht-text-muted); font-size: 0.82rem; line-height: 1.5; margin-bottom: 10px;">
                  Access Flow creative tools, generative prompt engines, and video workflow models included with your verified enrollment.
                </p>
                
                <div style="background: rgba(0,0,0,0.25); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 12px;">
                  <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 8px;">
                    <div style="font-size: 0.88rem; color: #fff; font-weight: 600;">
                      Have you accessed your Flow Creative Suite?
                    </div>
                    <div style="display: flex; gap: 16px;">
                      <label style="display: flex; align-items: center; gap: 6px; cursor: pointer; color: var(--cht-text-secondary); font-size: 0.85rem;">
                        <input type="radio" name="flowCheck" value="yes" ${flowAccessed ? 'checked' : ''} onchange="handleFlowCheck(true, '${user.id}')">
                        <span>Yes, I have Flow</span>
                      </label>
                      <label style="display: flex; align-items: center; gap: 6px; cursor: pointer; color: var(--cht-text-secondary); font-size: 0.85rem;">
                        <input type="radio" name="flowCheck" value="no" ${!flowAccessed ? 'checked' : ''} onchange="handleFlowCheck(false, '${user.id}')">
                        <span>No, not yet</span>
                      </label>
                    </div>
                  </div>
                  ${!flowAccessed ? `
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 10px;">
                      <span style="font-size: 0.78rem; color: var(--cht-text-muted);">Official Dispatch WhatsApp: <strong>0915-963-7287</strong></span>
                      <a href="https://wa.me/2349159637287?text=Hello%20Coach%20Hyela%2C%20I%20am%20a%20verified%20VIP%20student%20(${encodeURIComponent(studentName)}%20-%20${encodeURIComponent(studentEmail)}).%20Please%20guide%20me%20on%20accessing%20my%20Flow%20creative%20suite." target="_blank" rel="noopener noreferrer" class="cht-btn cht-btn-primary cht-btn-sm" style="font-size: 0.78rem; padding: 5px 12px; display: inline-flex; align-items: center; gap: 6px; font-weight: 700;">
                        <span>📲 Request Flow Onboarding Guide →</span>
                      </a>
                    </div>
                  ` : `
                    <div style="font-size: 0.8rem; color: #86EFAC; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 8px;">
                      ✓ Flow suite receipt confirmed on your account. Ready for use with your 23 Master Prompts above.
                    </div>
                  `}
                </div>
              </div>

              <!-- 4. Optional Standalone Upgrade: Muse AI (1 Billion Credits) -->
              <div style="background: rgba(0,0,0,0.35); border: 1px solid rgba(212, 175, 55, 0.35); border-radius: 8px; padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 6px;">
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.1rem;">✨</span>
                    <strong style="color: var(--cht-gold-light); font-size: 0.95rem;">Do you want Muse AI? (1 Billion Credits)</strong>
                  </div>
                  <span style="background: rgba(212, 175, 55, 0.15); color: var(--cht-gold-light); border: 1px solid rgba(212, 175, 55, 0.4); font-size: 0.72rem; padding: 2px 8px; border-radius: 4px; font-weight: 700;">
                    ${museAiPaid ? '✓ Purchased Standalone' : 'Optional Paid Add-On • ₦3,000'}
                  </span>
                </div>
                <p style="color: var(--cht-text-muted); font-size: 0.82rem; line-height: 1.5; margin-bottom: 10px;">
                  <strong style="color: #F87171;">Important Notice:</strong> Muse AI is a massive 1,000,000,000 generation credit tool. It is <strong>NOT</strong> an automatic right included in your student training package. If you want Muse AI for your video avatars and generation workflows, you can purchase it as a separate standalone add-on for <strong>₦3,000</strong>.
                </p>
                
                ${museAiPaid ? `
                  <div style="background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 6px; padding: 10px 14px; font-size: 0.84rem; color: #86EFAC;">
                    ✓ You have purchased standalone Muse AI. Credentials dispatched to your registered WhatsApp.
                  </div>
                ` : `
                  <div style="background: rgba(0,0,0,0.25); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 10px;">
                      <div style="font-size: 0.82rem; color: var(--cht-text-secondary);">
                        Official PalmPay: <strong style="color: #fff;">7011706511</strong> &bull; <span style="color: var(--cht-gold-light);">EL JOSHUA HYELAKURI EMMANUEL</span>
                      </div>
                      <div style="font-size: 0.9rem; font-weight: 800; color: #fff;">₦3,000</div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 10px;">
                      <span style="font-size: 0.78rem; color: var(--cht-text-muted);">After transfer, submit payment receipt for instant activation.</span>
                      <a href="https://wa.me/2349159637287?text=Hello%20Coach%20Hyela%2C%20I%20want%20to%20buy%20Muse%20AI%20(1%20Billion%20Credits)%20separately%20for%20%E2%82%A63%2C000.%20My%20name%20is%20${encodeURIComponent(studentName)}%20(${encodeURIComponent(studentEmail)}).%20Here%20is%20my%20payment%20receipt." target="_blank" rel="noopener noreferrer" class="cht-btn cht-btn-primary cht-btn-sm" style="font-size: 0.78rem; padding: 6px 14px; display: inline-flex; align-items: center; gap: 6px; font-weight: 700;">
                        <span>🛒 Buy Muse AI Separately (₦3,000) →</span>
                      </a>
                    </div>
                  </div>
                `}
              </div>"""

if old_muse_box in text:
    text = text.replace(old_muse_box, new_flow_muse_box, 1)
    print("[OK] Replaced Muse AI box with Flow + Standalone Muse AI")
else:
    print("Could not find old_muse_box")

# 4. Add handleFlowCheck function
old_handlers = """    async function handleMuseAiCheck(accessed, userId) {
      if (window.CHT && CHT.setMuseAiStatus) {
        await CHT.setMuseAiStatus(userId, accessed);
      }
    }
    const handleAiProCheck = handleMuseAiCheck;"""

new_handlers = """    async function handleFlowCheck(accessed, userId) {
      if (window.CHT && CHT.setFlowStatus) {
        await CHT.setFlowStatus(userId, accessed);
        // Refresh local student record
        const updated = await CHT.getStudentById(userId);
        if (updated) renderDriveAccess(updated);
      }
    }

    async function handleMuseAiCheck(accessed, userId) {
      if (window.CHT && CHT.setMuseAiStatus) {
        await CHT.setMuseAiStatus(userId, accessed);
      }
    }
    const handleAiProCheck = handleFlowCheck;"""

if old_handlers in text:
    text = text.replace(old_handlers, new_handlers, 1)
    print("[OK] Added handleFlowCheck in certificates.html")
else:
    print("Could not find old_handlers")

with open('certificates.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done patching certificates.html")
