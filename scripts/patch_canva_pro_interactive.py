# scripts/patch_canva_pro_interactive.py

# 1. Update js/cht-core.js
with open('js/cht-core.js', 'r', encoding='utf-8') as f:
    core_js = f.read()

canva_helpers = """
  // Canva Pro Claim & Dispatch Helpers
  async function submitCanvaClaim(userId, canvaEmail) {
    const db = getFirestore();
    if (db && userId) {
      try {
        await db.collection('students').doc(userId).set({
          canvaStatus: 'REQUESTED',
          canvaEmail: canvaEmail.trim().toLowerCase(),
          canvaRequestedAt: new Date().toISOString()
        }, { merge: true });

        await db.collection('activity_logs').add({
          type: 'CANVA_CLAIM_REQUEST',
          page: 'Student Portal',
          device: window.innerWidth <= 768 ? 'Mobile' : 'Desktop',
          details: `Canva Pro team invite requested for email: ${canvaEmail}`,
          timestamp: new Date().toISOString()
        });
        return { success: true, message: "Canva Pro invite request submitted to Coach Hyela!" };
      } catch (e) {
        return { success: false, message: e.message };
      }
    }
    return { success: false, message: "Cloud connection unavailable." };
  }

  async function confirmCanvaAccepted(userId) {
    const db = getFirestore();
    if (db && userId) {
      try {
        await db.collection('students').doc(userId).set({
          canvaStatus: 'CLAIMED',
          canvaClaimedAt: new Date().toISOString()
        }, { merge: true });
        return { success: true, message: "Canva Pro status marked as Claimed & Active!" };
      } catch(e) {
        return { success: false, message: e.message };
      }
    }
    return { success: false, message: "Cloud connection unavailable." };
  }

  async function dispatchCanvaInvite(userId, studentEmail) {
    const db = getFirestore();
    if (db && userId) {
      try {
        await db.collection('students').doc(userId).set({
          canvaStatus: 'INVITE_SENT',
          canvaInviteSentAt: new Date().toISOString()
        }, { merge: true });

        await db.collection('activity_logs').add({
          type: 'CANVA_INVITE_DISPATCHED',
          page: 'Operations Hub',
          device: window.innerWidth <= 768 ? 'Mobile' : 'Desktop',
          details: `Coach Hyela dispatched Canva Pro team invite to ${studentEmail}`,
          timestamp: new Date().toISOString()
        });

        logNotification(
          studentEmail,
          "Canva Pro Team Invite Sent - Coach Hyela Tech",
          "An email invitation has been sent to your inbox from Coach Hyela Tech Canva Team. Please accept the invitation to activate your 1-Year Pro access.",
          "CANVA_VIP"
        );
        return { success: true, message: `Canva Pro invite notification sent to student dashboard for ${studentEmail}!` };
      } catch(e) {
        return { success: false, message: e.message };
      }
    }
    return { success: false, message: "Cloud connection unavailable." };
  }

  async function setGoogleAiProStatus(userId, accessed) {
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
  }
"""

if 'submitCanvaClaim' not in core_js:
    target_pos = "// Initial boot\n  initStorage();"
    core_js = core_js.replace(target_pos, canva_helpers + "\n  " + target_pos)
    print("Added Canva Pro & Google AI Pro helper functions to cht-core.js")

# Expose in return object
if 'submitCanvaClaim,' not in core_js:
    core_js = core_js.replace(
        'getMasterDriveUrl,',
        'getMasterDriveUrl,\n    submitCanvaClaim,\n    confirmCanvaAccepted,\n    dispatchCanvaInvite,\n    setGoogleAiProStatus,'
    )
    print("Exposed Canva & AI Pro methods in cht-core.js return block")

with open('js/cht-core.js', 'w', encoding='utf-8') as f:
    f.write(core_js)

# 2. Update certificates.html
with open('certificates.html', 'r', encoding='utf-8') as f:
    cert_html = f.read()

# Add Canva claim & AI Pro interactive client functions
client_canva_js = """
    function toggleCanvaInput(hasClaimed, userId) {
      const box = document.getElementById('canvaEmailBox');
      if (box) box.style.display = hasClaimed ? 'none' : 'block';
      if (hasClaimed) {
        CHT.confirmCanvaAccepted(userId);
      }
    }

    async function handleSubmitCanvaClaim(userId) {
      const emailInput = document.getElementById('inputCanvaEmail');
      if (!emailInput || !emailInput.value.trim()) {
        alert("Please enter a valid email address.");
        return;
      }
      const email = emailInput.value.trim();
      const res = await CHT.submitCanvaClaim(userId, email);
      alert(res.message);
    }

    async function handleConfirmCanvaAccepted(userId) {
      const res = await CHT.confirmCanvaAccepted(userId);
      alert(res.message);
    }

    async function handleAiProCheck(accessed, userId) {
      await CHT.setGoogleAiProStatus(userId, accessed);
    }
"""

if 'handleSubmitCanvaClaim' not in cert_html:
    cert_html = cert_html.replace('// 8. CLAIM CERTIFICATE ACTIoN', client_canva_js + '\n    // 8. CLAIM CERTIFICATE ACTIoN')
    print("Added client Canva & AI Pro handlers to certificates.html")

# Update renderDriveVault in certificates.html with interactive Canva & AI Pro widgets
old_render_vault_header = """    // 7. RENDER RESTRICTED VIP GOOGLE DRIVE VAULT & MASTER PROMPTS
    function renderDriveVault(user) {"""

# We'll create the upgraded renderDriveVault function
upgraded_render_vault = """    // 7. RENDER RESTRICTED VIP GOOGLE DRIVE VAULT & MASTER PROMPTS
    function renderDriveVault(user) {
      const users = CHT.getUsers();
      const freshUser = users.find(u => (u.id === user.id || u.email.toLowerCase() === user.email.toLowerCase())) || user;
      const isEligible = !!freshUser.driveAccess || !!user.driveAccess;
      const driveUrl = (window.CHT && CHT.getMasterDriveUrl) ? CHT.getMasterDriveUrl() : "https://drive.google.com/drive/folders/1_0uldj8-IFcWQxRa4PuFRFVgCRDeSNDJ?usp=drive_link";
      const canvaStatus = freshUser.canvaStatus || user.canvaStatus || 'NOT_CLAIMED';
      const canvaEmail = freshUser.canvaEmail || user.canvaEmail || user.email;
      const aiProAccessed = !!freshUser.googleAiProAccessed || !!user.googleAiProAccessed;

      const badge = document.getElementById('drivePermissionBadge');
      const container = document.getElementById('driveAccessContainer');

      if (isEligible) {
        badge.innerHTML = `<span class="status-badge approved" style="background:#22C55E; color:#000; font-weight:800; padding:4px 10px;">✓ VIP ACCESS ACTIVE</span>`;

        let canvaSectionHtml = '';
        if (canvaStatus === 'INVITE_SENT') {
          canvaSectionHtml = `
            <div style="background: rgba(212, 175, 55, 0.15); border: 2px solid var(--cht-gold-500); border-radius: 8px; padding: 14px; margin-top: 10px;">
              <div style="display: flex; align-items: center; gap: 8px; color: var(--cht-gold-light); font-weight: 700; font-size: 0.95rem; margin-bottom: 4px;">
                <span>📩 Canva Team Invite Sent!</span>
              </div>
              <p style="color: #fff; font-size: 0.85rem; line-height: 1.5; margin-bottom: 10px;">
                An invitation has been sent to <strong>${canvaEmail}</strong> from <strong>Coach Hyela Tech Canva Team</strong>. Please check your email inbox and spam folder, and accept it to activate your 1-Year Pro access!
              </p>
              <button type="button" class="cht-btn cht-btn-primary cht-btn-sm" onclick="handleConfirmCanvaAccepted('${user.id}')" style="font-size: 0.8rem; font-weight: 700;">
                ✓ I Have Accepted the Canva Invite
              </button>
            </div>
          `;
        } else if (canvaStatus === 'CLAIMED') {
          canvaSectionHtml = `
            <div style="background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.4); border-radius: 8px; padding: 12px; margin-top: 10px;">
              <span style="color: #86EFAC; font-weight: 700; font-size: 0.88rem;">✓ 1-Year Canva Pro Access Active on Team Workspace</span>
              <div style="font-size: 0.8rem; color: var(--cht-text-muted); margin-top: 2px;">Registered Email: ${canvaEmail}</div>
            </div>
          `;
        } else if (canvaStatus === 'REQUESTED') {
          canvaSectionHtml = `
            <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 8px; padding: 12px; margin-top: 10px;">
              <span style="color: #FCD34D; font-weight: 700; font-size: 0.88rem;">⏳ Canva Team Invite Request Pending</span>
              <p style="color: var(--cht-text-secondary); font-size: 0.82rem; margin: 4px 0 0 0;">
                Your request for <strong>${canvaEmail}</strong> has been received by Coach Hyela. An invite will be dispatched to your inbox shortly.
              </p>
            </div>
          `;
        } else {
          canvaSectionHtml = `
            <div style="background: rgba(0,0,0,0.25); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 12px; margin-top: 10px;">
              <div style="font-size: 0.88rem; color: #fff; font-weight: 600; margin-bottom: 8px;">
                Have you already claimed your Canva Pro?
              </div>
              <div style="display: flex; gap: 16px; margin-bottom: 10px;">
                <label style="display: flex; align-items: center; gap: 6px; cursor: pointer; color: var(--cht-text-secondary); font-size: 0.85rem;">
                  <input type="radio" name="canvaClaimCheck" value="yes" onchange="toggleCanvaInput(true, '${user.id}')">
                  <span>Yes, I have it</span>
                </label>
                <label style="display: flex; align-items: center; gap: 6px; cursor: pointer; color: var(--cht-text-secondary); font-size: 0.85rem;">
                  <input type="radio" name="canvaClaimCheck" value="no" checked onchange="toggleCanvaInput(false, '${user.id}')">
                  <span>No, I need access</span>
                </label>
              </div>
              <div id="canvaEmailBox">
                <label class="cht-label" style="font-size: 0.8rem; margin-bottom: 4px;">Enter your email for Canva Team Invite:</label>
                <div style="display: flex; gap: 8px;">
                  <input type="email" id="inputCanvaEmail" class="cht-input" value="${user.email}" style="padding: 6px 12px; font-size: 0.85rem;" required>
                  <button type="button" class="cht-btn cht-btn-primary cht-btn-sm" style="white-space: nowrap; padding: 6px 14px; font-weight: 700;" onclick="handleSubmitCanvaClaim('${user.id}')">
                    Request Invite →
                  </button>
                </div>
                <div class="cht-help-text" style="font-size: 0.75rem; margin-top: 4px;">Coach Hyela will dispatch your invite from the Coach Hyela Tech Canva Team.</div>
              </div>
            </div>
          `;
        }

        container.innerHTML = `
          <div style="background: rgba(34, 197, 94, 0.08); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: var(--cht-radius-md); padding: 18px; margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 14px; color: #86EFAC; font-weight: 700; font-size: 0.92rem;">
              <span>🌟 Exclusive VIP Candidate Access Granted for ${user.email}</span>
            </div>
            
            <div style="display: flex; flex-direction: column; gap: 14px;">
              <!-- 1. Master AI Prompts & E-Books Google Drive -->
              <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 6px;">
                  <strong style="color: #fff; font-size: 0.95rem;">📁 Master AI Prompts &amp; E-Books Library</strong>
                  <span class="status-pill approved" style="font-size: 0.7rem;">Google Drive Live</span>
                </div>
                <p style="color: var(--cht-text-muted); font-size: 0.82rem; line-height: 1.5; margin-bottom: 12px;">
                  Includes commercial master prompts for ChatGPT, Midjourney, Claude, AI Avatar Lip-Sync workflows, CapCut post-production templates &amp; UGC advertising scripts.
                </p>
                <a href="${driveUrl}" target="_blank" rel="noopener noreferrer" class="cht-btn cht-btn-primary cht-btn-sm" style="font-weight: 700; display: inline-flex; align-items: center; gap: 6px;">
                  Open Master Prompts Drive Folder ↗
                </a>
              </div>

              <!-- 2. Canva Pro 1-Year Access -->
              <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 4px;">
                  <strong style="color: #fff; font-size: 0.95rem;">🎨 Canva Pro (1-Year VIP Access)</strong>
                  <span class="status-pill approved" style="font-size: 0.7rem;">Active</span>
                </div>
                <p style="color: var(--cht-text-muted); font-size: 0.82rem; line-height: 1.5; margin-bottom: 8px;">
                  1-Year full Canva Pro creative suite license managed by Coach Hyela Tech.
                </p>
                ${canvaSectionHtml}
              </div>

              <!-- 3. Google AI Pro Package -->
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
      } else {
        badge.innerHTML = `<span class="status-badge pending">🔒 VIP Verification Required</span>`;
        container.innerHTML = `
          <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: var(--cht-radius-md); padding: 16px;">
            <div style="display: flex; align-items: center; gap: 8px; color: #FCD34D; font-weight: 700; font-size: 0.9rem; margin-bottom: 8px;">
              <span>🔒 Restricted VIP Resource Suite</span>
            </div>
            <p style="color: var(--cht-text-muted); font-size: 0.84rem; line-height: 1.6; margin-bottom: 12px;">
              Your account (${user.email}) is currently pending VIP verification. Once Coach Hyela verifies your course enrollment or fee payment, this vault will unlock automatically with:
            </p>
            <ul style="color: var(--cht-text-secondary); font-size: 0.82rem; line-height: 1.8; margin-left: 20px; margin-bottom: 14px;">
              <li>🎨 <strong>Canva Pro (1-Year Access)</strong></li>
              <li>📁 <strong>Master AI Prompts &amp; E-Books Google Drive Vault</strong></li>
              <li>⚡ <strong>Google AI Pro 18-Month Workflow Package</strong></li>
              <li>🎓 <strong>Official Verified Coach Hyela Tech Certificate</strong></li>
            </ul>
            <a href="https://wa.me/2349159637287?text=Hello%20Coach%20Hyela%2C%20I%20have%20registered%20on%20your%20website%20with%20email%3A%20${encodeURIComponent(user.email)}.%20Please%20verify%20my%20VIP%20Student%20Access." target="_blank" rel="noopener noreferrer" class="cht-btn cht-btn-outline cht-btn-sm" style="display: inline-flex; align-items: center; gap: 6px;">
              Contact Coach Hyela to Confirm VIP Access 💬
            </a>
          </div>
        `;
      }
    }"""

import re
pattern = r"// 7\.\s*RENDER RESTRICTED VIP GOOGLE DRIVE VAULT & MASTER PROMPTS\s*\r?\n\s*function renderDriveVault\(user\) \{[\s\S]*?\}\r?\n\s*\r?\n\s*function toggleCanvaInput"
m = re.search(pattern, cert_html)
if m:
    cert_html = cert_html[:m.start()] + upgraded_render_vault + "\n\n    function toggleCanvaInput" + cert_html[m.end():]
    print("Replaced renderDriveVault with interactive Canva & AI Pro suite")
else:
    # Match till // 8.
    pattern2 = r"// 7\.\s*RENDER RESTRICTED VIP GOOGLE DRIVE VAULT & MASTER PROMPTS\s*\r?\n\s*function renderDriveVault\(user\) \{[\s\S]*?\}\r?\n\s*\r?\n\s*// 8\."
    m2 = re.search(pattern2, cert_html)
    if m2:
        cert_html = cert_html[:m2.start()] + upgraded_render_vault + "\n\n    // 8." + cert_html[m2.end():]
        print("Replaced renderDriveVault (pattern 2)")

with open('certificates.html', 'w', encoding='utf-8') as f:
    f.write(cert_html)

# 3. Update admin.html with Canva Pro Management column in Registered Students Table
with open('admin.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

# Update table headers: add Canva Pro Status
old_th = """                  <th>Assigned Courses</th>
                  <th>Drive Access</th>
                  <th>Actions</th>"""

new_th = """                  <th>Assigned Courses</th>
                  <th>Drive Access</th>
                  <th>Canva Pro VIP Status</th>
                  <th>Actions</th>"""

if old_th in admin_html and 'Canva Pro VIP Status' not in admin_html:
    admin_html = admin_html.replace(old_th, new_th)
    print("Added Canva Pro VIP Status column header to admin.html")

# Update renderAdminStudents rows
old_td_drive = """          <td>
            <button type="button" class="cht-btn cht-btn-sm ${u.driveAccess ? 'cht-btn-primary' : 'cht-btn-outline'}" style="padding:2px 8px; font-size:0.75rem;" onclick="handleToggleDrive('${u.email}', ${!u.driveAccess})">
              ${u.driveAccess ? '✓ Granted' : 'Locked (Click to Grant)'}
            </button>
          </td>
          <td>
            <button type="button" class="cht-btn cht-btn-outline cht-btn-sm" style="padding:4px 8px; font-size:0.75rem;" onclick="openEditStudentModal('${u.id}')">
              Edit Details
            </button>
          </td>"""

new_td_drive = """          <td>
            <button type="button" class="cht-btn cht-btn-sm ${u.driveAccess ? 'cht-btn-primary' : 'cht-btn-outline'}" style="padding:2px 8px; font-size:0.75rem;" onclick="handleToggleDrive('${u.email}', ${!u.driveAccess})">
              ${u.driveAccess ? '✓ Granted' : 'Locked (Click to Grant)'}
            </button>
          </td>
          <td>
            ${(() => {
              const status = u.canvaStatus || 'NOT_CLAIMED';
              const email = u.canvaEmail || u.email;
              if (status === 'REQUESTED') {
                return `
                  <div>
                    <span class="status-pill pending" style="font-size:0.7rem;">Invite Requested</span>
                    <div style="font-size:0.8rem; color:#fff; font-weight:600; margin:4px 0;">${email}</div>
                    <div style="display:flex; gap:4px; margin-top:4px;">
                      <button type="button" class="cht-btn cht-btn-outline cht-btn-sm" style="padding:2px 6px; font-size:0.7rem;" onclick="copyStudentEmail('${email}')">📋 Copy</button>
                      <button type="button" class="cht-btn cht-btn-primary cht-btn-sm" style="padding:2px 8px; font-size:0.7rem; font-weight:700;" onclick="handleMarkCanvaSent('${u.id}', '${email}')">✉️ Mark Invite Sent</button>
                    </div>
                  </div>
                `;
              } else if (status === 'INVITE_SENT') {
                return `
                  <div>
                    <span class="status-pill approved" style="font-size:0.7rem;">✓ Invite Sent</span>
                    <div style="font-size:0.75rem; color:var(--cht-text-muted); margin-top:2px;">${email}</div>
                    <button type="button" class="cht-btn cht-btn-outline cht-btn-sm" style="padding:1px 6px; font-size:0.68rem; margin-top:4px;" onclick="handleMarkCanvaSent('${u.id}', '${email}')">Re-notify</button>
                  </div>
                `;
              } else if (status === 'CLAIMED') {
                return `
                  <div>
                    <span class="status-pill approved" style="font-size:0.7rem;">✓ Claimed & Active</span>
                    <div style="font-size:0.75rem; color:var(--cht-text-muted); margin-top:2px;">${email}</div>
                  </div>
                `;
              } else {
                return `<span class="status-pill" style="opacity:0.6; font-size:0.7rem;">Not Claimed Yet</span>`;
              }
            })()}
          </td>
          <td>
            <button type="button" class="cht-btn cht-btn-outline cht-btn-sm" style="padding:4px 8px; font-size:0.75rem;" onclick="openEditStudentModal('${u.id}')">
              Edit Details
            </button>
          </td>"""

if old_td_drive in admin_html:
    admin_html = admin_html.replace(old_td_drive, new_td_drive)
    print("Added Canva Pro actions to student rows in admin.html")

# Add copyStudentEmail and handleMarkCanvaSent handlers to admin.html
admin_canva_handlers = """
    function copyStudentEmail(email) {
      if (!email) return;
      navigator.clipboard.writeText(email).then(() => {
        alert("Copied " + email + " to clipboard! You can now paste it into Canva to add the student.");
      }).catch(() => {
        prompt("Copy student email:", email);
      });
    }

    async function handleMarkCanvaSent(userId, email) {
      const confirmDispatch = confirm(`Mark Canva Pro invite as SENT to ${email}?\\n\\nThis will immediately update the student's dashboard with a notice instructing them to check their inbox and accept the team invitation.`);
      if (!confirmDispatch) return;

      const res = await CHT.dispatchCanvaInvite(userId, email);
      alert(res.message);
      renderAdminStudents();
      renderAdminNotifs();
    }
"""

if 'copyStudentEmail' not in admin_html:
    admin_html = admin_html.replace('async function handleToggleDrive', admin_canva_handlers + '\n    async function handleToggleDrive')
    print("Added copyStudentEmail and handleMarkCanvaSent to admin.html")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_html)

print("All Canva Pro & Google AI Pro interactive files patched successfully!")
