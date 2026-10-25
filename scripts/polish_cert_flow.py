with open('certificates.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update help text under email in Register form
old_help = '<div class="cht-help-text">A 6-digit verification code will be sent tothis email.</div>'
new_help = '<div class="cht-help-text">A secure email verification link from Coach Hyela Tech will be sent to this email.</div>'
if old_help in html:
    html = html.replace(old_help, new_help)
    print("Updated register help text")

# 2. Update forgot password handler to use Firebase sendPasswordResetEmail directly
old_forgot_handler = """    // 4. FORGOT & RESET PASSWORD HANDLERS
    function handleForgotRequestSubmit(e) {
      e.preventDefault();
      const email = document.getElementById('forgotEmailInput').value.trim();
      const res = CHT.requestPasswordReset(email);
      showAuthAlert(res.success ? `If an account exists for ${email}, a 6-digit password reset code has been dispatched to your email address. Please check your inbox.` : res.message, !res.success);
      if (res.success) {
        document.getElementById('formForgotRequest').style.display = 'none';
        document.getElementById('formResetSubmit').style.display = 'block';
      }
    }"""

new_forgot_handler = """    // 4. FORGOT & RESET PASSWORD HANDLERS (Automated via Google Firebase)
    async function handleForgotRequestSubmit(e) {
      e.preventDefault();
      const email = document.getElementById('forgotEmailInput').value.trim();

      if (fbAuth) {
        try {
          await fbAuth.sendPasswordResetEmail(email);
          showAuthAlert(`Password reset link dispatched! Please check your email inbox (${email}) and follow the instructions to securely reset your password.`, false);
          setTimeout(() => {
            switchAuthTab('login');
            document.getElementById('loginEmail').value = email;
          }, 3500);
          return;
        } catch (err) {
          console.warn('[CHT Auth] Reset error:', err);
          if (err.code === 'auth/user-not-found') {
            showAuthAlert("No account found with this email. Please verify the email or register a new account.", true);
            return;
          } else if (err.code === 'auth/invalid-email') {
            showAuthAlert("Please enter a valid email address.", true);
            return;
          }
        }
      }

      const res = CHT.requestPasswordReset(email);
      showAuthAlert(res.success ? `If an account exists for ${email}, password reset instructions have been dispatched to your email address. Please check your inbox.` : res.message, !res.success);
      if (res.success) {
        document.getElementById('formForgotRequest').style.display = 'none';
        document.getElementById('formResetSubmit').style.display = 'block';
      }
    }"""

if old_forgot_handler in html:
    html = html.replace(old_forgot_handler, new_forgot_handler)
    print("Updated forgot password handler to Firebase automated reset")

with open('certificates.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("certificates.html polished!")
