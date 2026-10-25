with open('admin.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

# 1. Add EmailJS script in <head>
if 'email.min.js' not in admin_html:
    admin_html = admin_html.replace('</head>', '  <script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>\n</head>')
    print("Added EmailJS to admin.html head")

# 2. Add Email Settings Card in Tab 5
old_tab5_header = """        <div id="tabContentNotifs" style="display: none;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <div>
              <h2 class="heading-serif" style="color: #fff; font-size: 1.35rem;">Simulated Email Dispatch Log</h2>
              <p style="color: var(--cht-text-muted); font-size: 0.85rem;">Audit all outgoing transactional emails: verification codes, reset links, approval updates, and claims.</p>
            </div>
            <button type="button" class="cht-btn cht-btn-outline cht-btn-sm" onclick="renderAdminNotifs()">
              Refresh Log
            </button>
          </div>"""

new_tab5_header = """        <div id="tabContentNotifs" style="display: none;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <div>
              <h2 class="heading-serif" style="color: #fff; font-size: 1.35rem;">Email Dispatch & Notification Log</h2>
              <p style="color: var(--cht-text-muted); font-size: 0.85rem;">Manage real-time transactional email delivery and audit all outgoing verification codes, reset links, and approval notifications.</p>
            </div>
            <button type="button" class="cht-btn cht-btn-outline cht-btn-sm" onclick="renderAdminNotifs()">
              Refresh Log
            </button>
          </div>

          <!-- EMAIL SERVICE CONFIGURATION CARD -->
          <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--cht-border); border-radius: var(--cht-radius-md); padding: 18px 20px; margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
              <div>
                <h3 style="font-size: 1.05rem; color: #fff; margin-bottom: 4px;">Live Email Dispatch Settings (EmailJS)</h3>
                <p style="font-size: 0.82rem; color: var(--cht-text-muted); margin: 0;">Connect your free EmailJS account (200 free emails/mo) so students receive verification codes and password reset emails in their inboxes.</p>
              </div>
              <span id="emailStatusBadge" class="status-pill pending">Setup Pending</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 12px;">
              <div>
                <label style="font-size: 0.75rem; color: var(--cht-text-muted); display: block; margin-bottom: 4px;">Public Key (User ID)</label>
                <input type="text" id="cfgEmailPublicKey" class="cht-input" style="padding: 8px 12px; font-size: 0.85rem;" placeholder="e.g. pub_xxx">
              </div>
              <div>
                <label style="font-size: 0.75rem; color: var(--cht-text-muted); display: block; margin-bottom: 4px;">Service ID</label>
                <input type="text" id="cfgEmailServiceId" class="cht-input" style="padding: 8px 12px; font-size: 0.85rem;" placeholder="e.g. service_cht">
              </div>
              <div>
                <label style="font-size: 0.75rem; color: var(--cht-text-muted); display: block; margin-bottom: 4px;">Template ID</label>
                <input type="text" id="cfgEmailTemplateId" class="cht-input" style="padding: 8px 12px; font-size: 0.85rem;" placeholder="e.g. template_verify">
              </div>
            </div>
            <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
              <button type="button" class="cht-btn cht-btn-primary cht-btn-sm" onclick="saveEmailSettingsFromAdmin()">Save Email Settings</button>
              <button type="button" class="cht-btn cht-btn-outline cht-btn-sm" onclick="testEmailDispatch()">Send Test Email</button>
              <span id="emailSaveFeedback" style="font-size: 0.82rem; color: #86EFAC;"></span>
            </div>
          </div>"""

if old_tab5_header in admin_html:
    admin_html = admin_html.replace(old_tab5_header, new_tab5_header)
    print("Replaced tab 5 header in admin.html")
else:
    print("Warning: old_tab5_header not found in admin.html")

# 3. Add helper JS in admin.html
js_helpers = """
    // EMAIL CONFIGURATION HANDLERS
    function initEmailSettings() {
      if (!window.CHT || !CHT.getEmailConfig) return;
      const cfg = CHT.getEmailConfig();
      const pubInput = document.getElementById('cfgEmailPublicKey');
      const srvInput = document.getElementById('cfgEmailServiceId');
      const tplInput = document.getElementById('cfgEmailTemplateId');
      const badge = document.getElementById('emailStatusBadge');
      if (pubInput) pubInput.value = cfg.publicKey || '';
      if (srvInput) srvInput.value = cfg.serviceId || '';
      if (tplInput) tplInput.value = cfg.templateId || '';
      if (badge) {
        if (cfg.publicKey && cfg.serviceId && cfg.templateId) {
          badge.className = 'status-pill approved';
          badge.textContent = 'Active & Connected';
        } else {
          badge.className = 'status-pill pending';
          badge.textContent = 'Setup Pending';
        }
      }
    }

    function saveEmailSettingsFromAdmin() {
      const pub = document.getElementById('cfgEmailPublicKey').value.trim();
      const srv = document.getElementById('cfgEmailServiceId').value.trim();
      const tpl = document.getElementById('cfgEmailTemplateId').value.trim();
      CHT.saveEmailConfig({ publicKey: pub, serviceId: srv, templateId: tpl });
      initEmailSettings();
      const feedback = document.getElementById('emailSaveFeedback');
      if (feedback) {
        feedback.textContent = 'Email configuration saved!';
        setTimeout(() => { feedback.textContent = ''; }, 3000);
      }
    }

    async function testEmailDispatch() {
      const testEmail = prompt('Enter destination email for live test:', 'eljosh1170@gmail.com');
      if (!testEmail) return;
      const res = await CHT.sendLiveEmail(testEmail, 'Coach Hyela Admin', '123456', 'VERIFICATION');
      if (res && res.success && res.mode === 'live') {
        alert('Test email successfully dispatched to ' + testEmail + ' via EmailJS!');
      } else if (res && res.mode === 'audit_logged') {
        alert('EmailJS credentials are not configured yet. The message has been logged in the audit log below.');
      } else {
        alert('Email delivery error: ' + (res.error || 'Please check your EmailJS Service, Template, or Public Key.'));
      }
      renderAdminNotifs();
    }
"""

# Call initEmailSettings inside switchTab or init
if "initEmailSettings();" not in admin_html:
    admin_html = admin_html.replace("renderAdminNotifs();", "renderAdminNotifs();\n        initEmailSettings();")
    print("Added initEmailSettings call on tab switch")

# Insert JS helpers right before </script> in admin.html
last_script = admin_html.rfind('</script>')
if last_script != -1 and 'saveEmailSettingsFromAdmin' not in admin_html:
    admin_html = admin_html[:last_script] + js_helpers + '\n' + admin_html[last_script:]
    print("Appended email JS handlers to admin.html")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_html)

print("admin.html update complete!")
