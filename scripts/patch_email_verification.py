import os

# 1. Update certificates.html
with open('certificates.html', 'r', encoding='utf-8') as f:
    cert_html = f.read()

# Replace registration code display & autofill
old_reg = """      showAuthAlert(`${res.message} (Verification Code: ${res.verificationCode})`, false);
      const codeField = document.getElementById('verificationCodeInput');
      if (codeField) {
        codeField.value = res.verificationCode;
        codeField.focus();
      }"""

new_reg = """      showAuthAlert(`Account created! A 6-digit verification code has been dispatched to your email (${res.email}). Please check your inbox and spam folder, then enter the code below to complete verification.`, false);
      const codeField = document.getElementById('verificationCodeInput');
      if (codeField) {
        codeField.value = '';
        codeField.focus();
      }"""

if old_reg in cert_html:
    cert_html = cert_html.replace(old_reg, new_reg)
    print("Fixed registration alert in certificates.html")
else:
    print("Warning: old_reg not found")

# Replace resend code display
old_resend = """      showAuthAlert(res.message + (res.verificationCode ? ` (Code: ${res.verificationCode})` : ''), !res.success);"""
new_resend = """      showAuthAlert(res.success ? `A new 6-digit verification code has been dispatched to ${pendingVerificationEmail}. Please check your inbox and spam folder.` : res.message, !res.success);
      const resendCodeField = document.getElementById('verificationCodeInput');
      if (resendCodeField) resendCodeField.value = '';"""

if old_resend in cert_html:
    cert_html = cert_html.replace(old_resend, new_resend)
    print("Fixed resend alert in certificates.html")
else:
    print("Warning: old_resend not found")

# Replace forgot password code display
old_forgot = """      showAuthAlert(res.message + (res.resetCode ? ` (Demo Reset Code: ${res.resetCode})` : ''), !res.success);"""
new_forgot = """      showAuthAlert(res.success ? `If an account exists for ${email}, a 6-digit password reset code has been dispatched to your email address. Please check your inbox.` : res.message, !res.success);"""

if old_forgot in cert_html:
    cert_html = cert_html.replace(old_forgot, new_forgot)
    print("Fixed forgot password alert in certificates.html")
else:
    print("Warning: old_forgot not found")

# Add EmailJS CDN in head
if "emailjs" not in cert_html:
    cert_html = cert_html.replace("</head>", '  <script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>\n</head>')
    print("Added EmailJS SDK to certificates.html")

with open('certificates.html', 'w', encoding='utf-8') as f:
    f.write(cert_html)

print("certificates.html update complete!")
