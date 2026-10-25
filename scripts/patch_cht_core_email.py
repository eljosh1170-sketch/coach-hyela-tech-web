import os

# 1. Update js/cht-core.js
with open('js/cht-core.js', 'r', encoding='utf-8') as f:
    core_js = f.read()

# Define the email integration code to insert
email_helper_code = """
  // ==========================================
  // LIVE TRANSACTIONAL EMAIL DISPATCHER (EmailJS)
  // ==========================================
  const EMAILJS_CONFIG_KEY = 'cht_emailjs_config';

  function getEmailConfig() {
    try {
      const cfg = JSON.parse(localStorage.getItem(EMAILJS_CONFIG_KEY) || '{}');
      return {
        serviceId: cfg.serviceId || '',
        templateId: cfg.templateId || '',
        publicKey: cfg.publicKey || ''
      };
    } catch (e) {
      return { serviceId: '', templateId: '', publicKey: '' };
    }
  }

  function saveEmailConfig(cfg) {
    localStorage.setItem(EMAILJS_CONFIG_KEY, JSON.stringify({
      serviceId: (cfg.serviceId || '').trim(),
      templateId: (cfg.templateId || '').trim(),
      publicKey: (cfg.publicKey || '').trim()
    }));
    return { success: true, message: 'Email configuration saved!' };
  }

  async function sendLiveEmail(toEmail, toName, code, type = 'VERIFICATION') {
    const cfg = getEmailConfig();
    const hasKeys = cfg.serviceId && cfg.templateId && cfg.publicKey;

    if (window.emailjs && hasKeys) {
      try {
        emailjs.init(cfg.publicKey);
        const templateParams = {
          to_email: toEmail,
          to_name: toName || 'Student',
          verification_code: code,
          action_type: type === 'RESET' ? 'Password Reset Code' : 'Student Email Verification Code',
          expiry_mins: type === 'RESET' ? '20 minutes' : '30 minutes',
          site_name: 'Coach Hyela Tech Industries Limited',
          site_url: 'https://coachhyelatech.com.ng'
        };

        const resp = await emailjs.send(cfg.serviceId, cfg.templateId, templateParams);
        console.log('[CHT Email] Live email dispatched successfully:', resp.status, resp.text);
        return { success: true, mode: 'live', status: resp.status };
      } catch (err) {
        console.error('[CHT Email] EmailJS send error:', err);
        return { success: false, mode: 'live_failed', error: err.text || err.message };
      }
    } else {
      console.info('[CHT Email] EmailJS not configured yet; code recorded in admin audit log.');
      return { success: true, mode: 'audit_logged' };
    }
  }
"""

if 'LIVE TRANSACTIONAL EMAIL DISPATCHER' not in core_js:
    # Insert right before registerStudent
    core_js = core_js.replace('  // Student Account Registration with Verification Code', email_helper_code + '\n  // Student Account Registration with Verification Code')
    print("Inserted email helper code into js/cht-core.js")

# Now ensure sendLiveEmail is called in registerStudent, resendVerificationCode, requestPasswordReset
# In registerStudent:
old_reg_call = """    // Send simulated email
    logNotification(
      cleanEmail,
      "Verify Your Coach Hyela Tech Student Account",
      `Welcome ${fullName.trim()}! Your 6-digit email verification code is: ${verificationCode}. This code expires in 30 minutes. Note: Creating an account does not automatically certify you; certificate eligibility requires course completion review by Coach Hyela.`,
      "VERIFICATION"
    );"""

new_reg_call = """    // Send live email notification + record in admin audit log
    sendLiveEmail(cleanEmail, fullName.trim(), verificationCode, 'VERIFICATION');
    logNotification(
      cleanEmail,
      "Verify Your Coach Hyela Tech Student Account",
      `Welcome ${fullName.trim()}! Your 6-digit email verification code is: ${verificationCode}. This code expires in 30 minutes. Note: Creating an account does not automatically certify you; certificate eligibility requires course completion review by Coach Hyela.`,
      "VERIFICATION"
    );"""

if old_reg_call in core_js:
    core_js = core_js.replace(old_reg_call, new_reg_call)
    print("Added sendLiveEmail to registerStudent")

# In resendVerificationCode:
old_resend_call = """    logNotification(
      cleanEmail,
      "New Verification Code - Coach Hyela Tech",
      `Your new 6-digit email verification code is: ${newCode}. Valid for 30 minutes.`,
      "VERIFICATION"
    );"""

new_resend_call = """    sendLiveEmail(cleanEmail, user.fullName || cleanEmail, newCode, 'VERIFICATION');
    logNotification(
      cleanEmail,
      "New Verification Code - Coach Hyela Tech",
      `Your new 6-digit email verification code is: ${newCode}. Valid for 30 minutes.`,
      "VERIFICATION"
    );"""

if old_resend_call in core_js:
    core_js = core_js.replace(old_resend_call, new_resend_call)
    print("Added sendLiveEmail to resendVerificationCode")

# In requestPasswordReset:
old_reset_call = """    logNotification(
      cleanEmail,
      "Password Reset Request - Coach Hyela Tech",
      `Hello ${user.fullName}. You requested a password reset. Your temporary reset verification code is: ${resetCode}. It will expire in 20 minutes. If you did not request this, please ignore this email. We never send your existing password by email.`,
      "SECURITY"
    );"""

new_reset_call = """    sendLiveEmail(cleanEmail, user.fullName || cleanEmail, resetCode, 'RESET');
    logNotification(
      cleanEmail,
      "Password Reset Request - Coach Hyela Tech",
      `Hello ${user.fullName}. You requested a password reset. Your temporary reset verification code is: ${resetCode}. It will expire in 20 minutes. If you did not request this, please ignore this email. We never send your existing password by email.`,
      "SECURITY"
    );"""

# Notice in cht-core.js it might be Hello${user.fullName} without space
if old_reset_call in core_js:
    core_js = core_js.replace(old_reset_call, new_reset_call)
    print("Added sendLiveEmail to requestPasswordReset")
else:
    # check without space
    old_reset_call2 = old_reset_call.replace("Hello ", "Hello")
    new_reset_call2 = new_reset_call.replace("Hello ", "Hello")
    if old_reset_call2 in core_js:
        core_js = core_js.replace(old_reset_call2, new_reset_call2)
        print("Added sendLiveEmail to requestPasswordReset (matched variant)")

# Add export in return window.CHT
old_export = "    requestPasswordReset,"
new_export = """    requestPasswordReset,
    getEmailConfig,
    saveEmailConfig,
    sendLiveEmail,"""
if old_export in core_js and "getEmailConfig," not in core_js:
    core_js = core_js.replace(old_export, new_export)
    print("Exported getEmailConfig and saveEmailConfig")

with open('js/cht-core.js', 'w', encoding='utf-8') as f:
    f.write(core_js)

print("cht-core.js update complete!")
