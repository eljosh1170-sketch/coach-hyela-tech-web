# scripts/patch_vip_drive_vault.py
import re

DRIVE_LINK = "https://drive.google.com/drive/folders/1_0uldj8-IFcWQxRa4PuFRFVgCRDeSNDJ?usp=drive_link"

# 1. Update js/cht-core.js
with open('js/cht-core.js', 'r', encoding='utf-8') as f:
    core_js = f.read()

# Add CHT_MASTER_DRIVE_URL
drive_const = f'  const CHT_MASTER_DRIVE_URL = "{DRIVE_LINK}";'
if 'CHT_MASTER_DRIVE_URL' not in core_js:
    core_js = core_js.replace("const CHT_FIREBASE_CONFIG = {", drive_const + "\n  const CHT_FIREBASE_CONFIG = {")
    print("Added CHT_MASTER_DRIVE_URL constant to cht-core.js")

# Upgrade toggleDriveAccess to sync to Firestore
old_toggle_drive = """  function toggleDriveAccess(email, hasAccess) {
    if (!isAdminLoggedIn()) return { success: false, message: "Unauthorized." };
    const users = getUsers();
    const user = users.find(u => u.email.toLowerCase() === email.toLowerCase());
    if (user) {
      user.driveAccess = hasAccess;
      saveUsers(users);

      logNotification(
        email,
        `Course Resource Access Updated`,
        `Your access to the restricted Coach Hyela Student Google Drive repository has been ${hasAccess ? 'ACTIVATED' : 'REVOKED'}.`,
        'PERMISSIoNS'
      );
      return { success: true, message: `Drive access ${hasAccess ? 'granted' : 'revoked'}.` };
    }
    return { success: false, message: "Student not found." };
  }"""

new_toggle_drive = """  async function toggleDriveAccess(email, hasAccess) {
    if (!isAdminLoggedIn()) return { success: false, message: "Unauthorized." };
    const users = getUsers();
    const user = users.find(u => u.email.toLowerCase() === email.toLowerCase());
    if (user) {
      user.driveAccess = hasAccess;
      user.vipAccess = hasAccess;
      saveUsers(users);

      const db = getFirestore();
      if (db) {
        try {
          await db.collection('students').doc(user.id).set({
            driveAccess: hasAccess,
            vipAccess: hasAccess,
            email: user.email,
            fullName: user.fullName
          }, { merge: true });
          await db.collection('activity_logs').add({
            type: 'VIP_ACCESS_TOGGLE',
            page: 'Operations Hub',
            device: window.innerWidth <= 768 ? 'Mobile' : 'Desktop',
            details: `Admin set VIP Google Drive access to ${hasAccess ? 'GRANTED' : 'REVOKED'} for ${email}`,
            timestamp: new Date().toISOString()
          });
        } catch(e) {
          console.warn('[CHT Cloud] Firestore drive toggle error:', e);
        }
      }

      logNotification(
        email,
        `VIP Resource & Google Drive Access Updated`,
        `Your access to the restricted Coach Hyela VIP Google Drive Master Prompts repository has been ${hasAccess ? 'ACTIVATED' : 'REVOKED'}.`,
        'PERMISSIONS'
      );
      return { success: true, message: `VIP Drive access ${hasAccess ? 'granted' : 'revoked'} and synced to Google Cloud!` };
    }
    return { success: false, message: "Student not found." };
  }

  function getMasterDriveUrl() {
    const content = getLiveContent();
    return (content && content.masterDriveUrl) ? content.masterDriveUrl : CHT_MASTER_DRIVE_URL;
  }"""

if old_toggle_drive in core_js:
    core_js = core_js.replace(old_toggle_drive, new_toggle_drive)
    print("Upgraded toggleDriveAccess to cloud Firestore sync")

# Expose getMasterDriveUrl in return block
if 'getMasterDriveUrl,' not in core_js:
    core_js = core_js.replace('toggleDriveAccess,', 'toggleDriveAccess,\n    getMasterDriveUrl,')
    print("Exposed getMasterDriveUrl in cht-core.js return block")

with open('js/cht-core.js', 'w', encoding='utf-8') as f:
    f.write(core_js)

# 2. Update admin.html handleToggleDrive to async
with open('admin.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

old_admin_toggle = """    function handleToggleDrive(email, newAccess) {
      const res = CHT.toggleDriveAccess(email, newAccess);
      alert(res.message);
      renderAdminStudents();
      renderAdminNotifs();
        initEmailSettings();
    }"""

new_admin_toggle = """    async function handleToggleDrive(email, newAccess) {
      const res = await CHT.toggleDriveAccess(email, newAccess);
      alert(res.message);
      renderAdminStudents();
      renderAdminNotifs();
      initEmailSettings();
    }"""

if old_admin_toggle in admin_html:
    admin_html = admin_html.replace(old_admin_toggle, new_admin_toggle)
    with open('admin.html', 'w', encoding='utf-8') as f:
        f.write(admin_html)
    print("Updated handleToggleDrive in admin.html to async")

# 3. Update certificates.html
with open('certificates.html', 'r', encoding='utf-8') as f:
    cert_html = f.read()

# Update showStudentDashboard to listen to student's Firestore doc for real-time driveAccess
old_dash_func = """    function showStudentDashboard(user) {
      document.getElementById('authSectionWrapper').style.display = 'none';
      document.getElementById('studentDashboardSection').style.display = 'block';

      document.getElementById('dashUserId').textContent = user.id;
      document.getElementById('dashStudentName').textContent = user.fullName;
      document.getElementById('dashStudentEmail').textContent = user.email;

      renderStudentEligibility(user.email);
      renderDriveVault(user);

      // Real-time Cloud updates from Coach Hyela
      if (window.CHT && CHT.subscribeCloudRequests) {
        CHT.subscribeCloudRequests(reqs => {
          renderStudentEligibility(user.email, reqs);
        });
      }
    }"""

new_dash_func = """    function showStudentDashboard(user) {
      document.getElementById('authSectionWrapper').style.display = 'none';
      document.getElementById('studentDashboardSection').style.display = 'block';

      document.getElementById('dashUserId').textContent = user.id;
      document.getElementById('dashStudentName').textContent = user.fullName;
      document.getElementById('dashStudentEmail').textContent = user.email;

      renderStudentEligibility(user.email);
      renderDriveVault(user);

      // Real-time Cloud updates for Eligibility Requests
      if (window.CHT && CHT.subscribeCloudRequests) {
        CHT.subscribeCloudRequests(reqs => {
          renderStudentEligibility(user.email, reqs);
        });
      }

      // Real-time Cloud updates for VIP Google Drive Access
      try {
        const db = (typeof firebase !== 'undefined' && firebase.firestore) ? firebase.firestore() : null;
        if (db) {
          // Listen to specific user document
          db.collection('students').doc(user.id).onSnapshot(doc => {
            if (doc.exists) {
              const freshData = doc.data();
              if (freshData.driveAccess !== undefined) {
                user.driveAccess = !!freshData.driveAccess;
                user.vipAccess = !!freshData.vipAccess;
                CHT.setAuthLearner(user);
                renderDriveVault(user);
              }
            }
          }, err => console.warn('[CHT Auth] Student snapshot listener:', err));

          // Fallback query by email if doc ID differs
          db.collection('students').where('email', '==', user.email.toLowerCase()).onSnapshot(snapshot => {
            snapshot.forEach(doc => {
              const freshData = doc.data();
              if (freshData.driveAccess !== undefined) {
                user.driveAccess = !!freshData.driveAccess;
                user.vipAccess = !!freshData.vipAccess;
                CHT.setAuthLearner(user);
                renderDriveVault(user);
              }
            });
          }, err => console.warn('[CHT Auth] Email student snapshot listener:', err));
        }
      } catch(e) {
        console.warn('[CHT Cloud] Student listener error:', e);
      }
    }"""

if old_dash_func in cert_html:
    cert_html = cert_html.replace(old_dash_func, new_dash_func)
    print("Updated showStudentDashboard with real-time student Firestore listener")

# Upgrade renderDriveVault to render the full VIP 4-Part Package
old_render_vault = """    function renderDriveVault(user) {
      const users = CHT.getUsers();
      const freshUser = users.find(u => u.id === user.id) || user;
      const isEligible = freshUser.driveAccess;

      const badge = document.getElementById('drivePermissionBadge');
      const container = document.getElementById('driveAccessContainer');

      if (isEligible) {
        badge.innerHTML = `<span class="status-badge approved">Access Granted</span>`;
        container.innerHTML = `
          <a href="https://drive.google.com" target="_blank" rel="noopener noreferrer" class="cht-btn cht-btn-primary cht-btn-sm" style="display:inline-flex;">
            open Restricted Student Drive Folder ?
          </a>
        `;
      } else {
        badge.innerHTML = `<span class="status-badge rejected">Locked</span>`;
        container.innerHTML = `
          <div style="display: flex; align-items: center; gap: 8px; font-size: 0.82rem; color: #FCA5A5;">
            ?? Access is unlocked automatically when Coach Hyela approves your course eligibility.
          </div>
        `;
      }
    }"""

new_render_vault = f"""    function renderDriveVault(user) {{
      const users = CHT.getUsers();
      const freshUser = users.find(u => (u.id === user.id || u.email.toLowerCase() === user.email.toLowerCase())) || user;
      const isEligible = !!freshUser.driveAccess || !!user.driveAccess;
      const driveUrl = (window.CHT && CHT.getMasterDriveUrl) ? CHT.getMasterDriveUrl() : "{DRIVE_LINK}";

      const badge = document.getElementById('drivePermissionBadge');
      const container = document.getElementById('driveAccessContainer');

      if (isEligible) {{
        badge.innerHTML = `<span class="status-badge approved" style="background:#22C55E; color:#000; font-weight:800;">✓ VIP ACCESS ACTIVE</span>`;
        container.innerHTML = `
          <div style="background: rgba(34, 197, 94, 0.08); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: var(--cht-radius-md); padding: 18px; margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px; color: #86EFAC; font-weight: 700; font-size: 0.92rem;">
              <span>🌟 Exclusive VIP Candidate Access Granted for ${{user.email}}</span>
            </div>
            
            <div style="display: flex; flex-direction: column; gap: 12px;">
              <!-- 1. Master AI Prompts & E-Books Google Drive -->
              <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 6px;">
                  <strong style="color: #fff; font-size: 0.95rem;">📁 Master AI Prompts &amp; E-Books Library</strong>
                  <span class="status-pill approved" style="font-size: 0.7rem;">Google Drive Live</span>
                </div>
                <p style="color: var(--cht-text-muted); font-size: 0.82rem; line-height: 1.5; margin-bottom: 10px;">
                  Includes ChatGPT commercial master prompts, Midjourney image engineering, AI Avatar lip-sync workflow guides, CapCut video templates &amp; UGC advertising scripts.
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
                <p style="color: var(--cht-text-muted); font-size: 0.82rem; line-height: 1.5; margin-bottom: 10px;">
                  1-Year full Canva Pro creative suite license. To claim your direct team invite, tap below to notify Coach Hyela directly on WhatsApp with your verified email (${{user.email}}).
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
                  Complete 18-month curriculum and practical enterprise AI automation blueprints, accessible directly inside your Master Google Drive vault above.
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

if old_render_vault in cert_html:
    cert_html = cert_html.replace(old_render_vault, new_render_vault)
    print("Updated renderDriveVault with rich VIP Package")
else:
    print("Warning: old_render_vault string didn't match directly, searching regex")

# Also bump cache buster to v=20261025_05
cert_html = re.sub(r'src="js/cht-core\.js(\?v=[^"]*)?"', 'src="js/cht-core.js?v=20261025_05"', cert_html)

with open('certificates.html', 'w', encoding='utf-8') as f:
    f.write(cert_html)

print("certificates.html updated successfully!")
