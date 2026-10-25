with open('certificates.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace handleRegisterSubmit with Firebase-powered automated version
old_reg_handler = """    // 1. REGISTRATION HANDLER
    async function handleRegisterSubmit(e) {
      e.preventDefault();
      const name = document.getElementById('regFullName').value.trim();
      const email = document.getElementById('regEmail').value.trim();
      const pass = document.getElementById('regPassword').value;

      const res = await CHT.registerStudent(name, email, pass);
      if (!res.success) {
        showAuthAlert(res.message, true);
        return;
      }

      pendingVerificationEmail = res.email;
      document.getElementById('verifyTargetEmail').textContent = res.email;
      document.getElementById('viewRegister').style.display = 'none';
      document.getElementById('viewVerifyEmail').style.display = 'block';
      showAuthAlert(`Account created! A 6-digit verification code has been dispatched to your email (${res.email}). Please check your inbox and spam folder, then enter the code below to complete verification.`, false);
      const codeField = document.getElementById('verificationCodeInput');
      if (codeField) {
        codeField.value = '';
        codeField.focus();
      }
    }"""

new_reg_handler = """    // 1. REGISTRATION HANDLER (Automated via Google Firebase with fallback)
    async function handleRegisterSubmit(e) {
      e.preventDefault();
      const name = document.getElementById('regFullName').value.trim();
      const email = document.getElementById('regEmail').value.trim();
      const pass = document.getElementById('regPassword').value;

      if (fbAuth) {
        try {
          const userCred = await fbAuth.createUserWithEmailAndPassword(email, pass);
          if (userCred.user) {
            await userCred.user.updateProfile({ displayName: name });
            await userCred.user.sendEmailVerification();
            
            showAuthAlert(`Account created successfully! Google has dispatched a secure verification link to ${email}. Please check your email inbox (and spam folder) and click the link to verify.`, false);
            setTimeout(() => {
              switchAuthTab('login');
              document.getElementById('loginEmail').value = email;
            }, 3500);
            return;
          }
        } catch (fbErr) {
          console.warn('[CHT Auth] Firebase register error:', fbErr.code, fbErr.message);
          if (fbErr.code === 'auth/email-already-in-use') {
            showAuthAlert("An account with this email already exists. Please sign in or reset your password.", true);
            return;
          } else if (fbErr.code === 'auth/invalid-email') {
            showAuthAlert("Google validation error: Please enter a valid email address.", true);
            return;
          } else if (fbErr.code === 'auth/weak-password') {
            showAuthAlert("Password must be at least 6 characters.", true);
            return;
          }
          // If project Auth is not yet toggled in console, proceed seamlessly with internal engine
        }
      }

      // Internal verification engine
      const res = await CHT.registerStudent(name, email, pass);
      if (!res.success) {
        showAuthAlert(res.message, true);
        return;
      }

      pendingVerificationEmail = res.email;
      document.getElementById('verifyTargetEmail').textContent = res.email;
      document.getElementById('viewRegister').style.display = 'none';
      document.getElementById('viewVerifyEmail').style.display = 'block';
      showAuthAlert(`Account created! A 6-digit verification code has been dispatched to your email (${res.email}). Please check your inbox and spam folder, then enter the code below to complete verification.`, false);
      const codeField = document.getElementById('verificationCodeInput');
      if (codeField) {
        codeField.value = '';
        codeField.focus();
      }
    }"""

if old_reg_handler in html:
    html = html.replace(old_reg_handler, new_reg_handler)
    print("Replaced handleRegisterSubmit with Firebase automated version")
else:
    print("Warning: old_reg_handler not matched")

# Replace handleLoginSubmit with Firebase-powered automated version
old_login_handler = """    // 3. LOGIN HANDLER
    async function handleLoginSubmit(e) {
      e.preventDefault();
      const email = document.getElementById('loginEmail').value.trim();
      const pass = document.getElementById('loginPassword').value;

      const res = await CHT.loginStudent(email, pass);
      if (!res.success) {
        if (res.requiresVerification) {
          pendingVerificationEmail = res.email;
          document.getElementById('verifyTargetEmail').textContent = res.email;
          document.getElementById('viewLogin').style.display = 'none';
          document.getElementById('viewVerifyEmail').style.display = 'block';
          showAuthAlert(res.message, true);
        } else {
          showAuthAlert(res.message, true);
        }
        return;
      }

      showStudentDashboard(res.user);
    }"""

new_login_handler = """    // 3. LOGIN HANDLER (Automated via Google Firebase with fallback)
    async function handleLoginSubmit(e) {
      e.preventDefault();
      const email = document.getElementById('loginEmail').value.trim();
      const pass = document.getElementById('loginPassword').value;

      if (fbAuth) {
        try {
          const userCred = await fbAuth.signInWithEmailAndPassword(email, pass);
          if (userCred.user) {
            if (!userCred.user.emailVerified) {
              showAuthAlert("Your email address is not verified yet. Google has sent a verification email to " + email + ". Please check your inbox and click the verification link before signing in.", true);
              return;
            }
            const studentUser = {
              id: "USR-" + userCred.user.uid.substring(0, 8).toUpperCase(),
              fullName: userCred.user.displayName || email.split('@')[0],
              email: userCred.user.email.toLowerCase(),
              emailVerified: true,
              registeredAt: new Date().toISOString(),
              driveAccess: false
            };
            CHT.setAuthLearner(studentUser);
            showAuthAlert("Welcome back, " + studentUser.fullName + "!", false);
            setTimeout(() => {
              showStudentDashboard(studentUser);
            }, 600);
            return;
          }
        } catch (fbErr) {
          console.warn('[CHT Auth] Firebase login error:', fbErr.code);
          if (fbErr.code === 'auth/wrong-password' || fbErr.code === 'auth/invalid-credential') {
            showAuthAlert("Invalid email or password. Please try again.", true);
            return;
          } else if (fbErr.code === 'auth/user-not-found') {
            showAuthAlert("No account found with this email. Please click Create Account.", true);
            return;
          }
        }
      }

      // Internal auth engine
      const res = await CHT.loginStudent(email, pass);
      if (!res.success) {
        if (res.requiresVerification) {
          pendingVerificationEmail = res.email;
          document.getElementById('verifyTargetEmail').textContent = res.email;
          document.getElementById('viewLogin').style.display = 'none';
          document.getElementById('viewVerifyEmail').style.display = 'block';
          showAuthAlert(res.message, true);
        } else {
          showAuthAlert(res.message, true);
        }
        return;
      }

      showStudentDashboard(res.user);
    }"""

if old_login_handler in html:
    html = html.replace(old_login_handler, new_login_handler)
    print("Replaced handleLoginSubmit with Firebase automated version")
else:
    print("Warning: old_login_handler not matched")

with open('certificates.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("certificates.html handlers successfully upgraded!")
