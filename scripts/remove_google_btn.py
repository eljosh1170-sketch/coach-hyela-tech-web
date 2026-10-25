with open('certificates.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove Google button blocks
old_login_btn = """              <!-- Google 1-Click Automated Sign-In -->
              <button type="button" class="cht-btn" onclick="handleGoogleSignIn()" style="width: 100%; margin-bottom: 16px; background: #ffffff; color: #1f2937; border: 1px solid #e5e7eb; display: flex; align-items: center; justify-content: center; gap: 10px; font-weight: 600; font-size: 0.95rem;">
                <svg width="18" height="18" viewBox="0 0 18 18"><path fill="#4285F4" d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.616z"/><path fill="#34A853" d="M9 18c2.43 0 4.467-.806 5.956-2.184l-2.908-2.258c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 0 0 9 18z"/><path fill="#FBBC05" d="M3.964 10.707c-.18-.54-.282-1.117-.282-1.707s.102-1.167.282-1.707V4.961H.957A8.996 8.996 0 0 0 0 9c0 1.452.348 2.827.957 4.039l3.007-2.332z"/><path fill="#EA4335" d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 0 0 .957 4.961L3.964 7.293C4.672 5.166 6.656 3.58 9 3.58z"/></svg>
                Continue with Google
              </button>

              <div style="display: flex; align-items: center; margin-bottom: 16px;">
                <div style="flex: 1; height: 1px; background: var(--cht-border);"></div>
                <span style="padding: 0 12px; font-size: 0.78rem; color: var(--cht-text-muted); text-transform: uppercase;">or sign in with email</span>
                <div style="flex: 1; height: 1px; background: var(--cht-border);"></div>
              </div>\n"""

old_reg_btn = """              <!-- Google 1-Click Automated Sign-Up -->
              <button type="button" class="cht-btn" onclick="handleGoogleSignIn()" style="width: 100%; margin-bottom: 16px; background: #ffffff; color: #1f2937; border: 1px solid #e5e7eb; display: flex; align-items: center; justify-content: center; gap: 10px; font-weight: 600; font-size: 0.95rem;">
                <svg width="18" height="18" viewBox="0 0 18 18"><path fill="#4285F4" d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.616z"/><path fill="#34A853" d="M9 18c2.43 0 4.467-.806 5.956-2.184l-2.908-2.258c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 0 0 9 18z"/><path fill="#FBBC05" d="M3.964 10.707c-.18-.54-.282-1.117-.282-1.707s.102-1.167.282-1.707V4.961H.957A8.996 8.996 0 0 0 0 9c0 1.452.348 2.827.957 4.039l3.007-2.332z"/><path fill="#EA4335" d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 0 0 .957 4.961L3.964 7.293C4.672 5.166 6.656 3.58 9 3.58z"/></svg>
                Sign Up with Google
              </button>

              <div style="display: flex; align-items: center; margin-bottom: 16px;">
                <div style="flex: 1; height: 1px; background: var(--cht-border);"></div>
                <span style="padding: 0 12px; font-size: 0.78rem; color: var(--cht-text-muted); text-transform: uppercase;">or register with email</span>
                <div style="flex: 1; height: 1px; background: var(--cht-border);"></div>
              </div>\n"""

if old_login_btn in html:
    html = html.replace(old_login_btn, '')
    print("Removed Google button from Login")

if old_reg_btn in html:
    html = html.replace(old_reg_btn, '')
    print("Removed Google button from Register")

with open('certificates.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Google buttons removed.")
