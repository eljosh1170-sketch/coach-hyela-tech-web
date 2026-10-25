with open('certificates.html', 'r', encoding='utf-8') as f:
    html = f.read()

fb_logic = """
    // ==========================================
    // GOOGLE FIREBASE AUTOMATED AUTHENTICATION
    // ==========================================
    const FIREBASE_CONFIG = {
      projectId: 'coachhyelatech-d3207',
      appId: '1:946569619362:web:d03da6c819375625c034fb',
      storageBucket: 'coachhyelatech-d3207.firebasestorage.app',
      apiKey: 'AIzaSyB4j-litduC2dvVAdMcyJUTVa7sqDmqiPY',
      authDomain: 'coachhyelatech-d3207.firebaseapp.com',
      messagingSenderId: '946569619362',
      measurementId: 'G-5LNNMMX44T'
    };

    let fbAuth = null;
    try {
      if (typeof firebase !== 'undefined') {
        if (!firebase.apps.length) {
          firebase.initializeApp(FIREBASE_CONFIG);
        }
        fbAuth = firebase.auth();
      }
    } catch (e) {
      console.warn('[CHT Auth] Firebase init error:', e);
    }

    // Automated 1-Click Google Sign-In / Sign-Up
    async function handleGoogleSignIn() {
      if (!fbAuth) {
        showAuthAlert('Google authentication service is initializing. Please try again or use email sign-in.', true);
        return;
      }
      try {
        const provider = new firebase.auth.GoogleAuthProvider();
        provider.setCustomParameters({ prompt: 'select_account' });
        const res = await fbAuth.signInWithPopup(provider);
        const gUser = res.user;

        const studentUser = {
          id: 'USR-' + gUser.uid.substring(0, 8).toUpperCase(),
          fullName: gUser.displayName || gUser.email.split('@')[0],
          email: gUser.email.toLowerCase(),
          emailVerified: true,
          registeredAt: new Date().toISOString(),
          driveAccess: false
        };

        CHT.setAuthLearner(studentUser);
        showAuthAlert('Welcome ' + studentUser.fullName + '! Signed in via Google.', false);
        setTimeout(() => {
          showStudentDashboard(studentUser);
        }, 800);
      } catch (err) {
        console.error('Google Sign-in error:', err);
        if (err.code === 'auth/popup-closed-by-user') return;
        if (err.code === 'auth/configuration-not-found' || err.code === 'auth/operation-not-allowed') {
          showAuthAlert('Google Sign-In is being activated on the project. Please sign in with email and password below.', true);
        } else {
          showAuthAlert(err.message, true);
        }
      }
    }
"""

target = "document.addEventListener('DOMContentLoaded', () => {"
if target in html and 'FIREBASE_CONFIG' not in html:
    html = html.replace(target, fb_logic + '\n    ' + target)
    with open('certificates.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Successfully inserted FIREBASE_CONFIG and handleGoogleSignIn!')
else:
    print('Target not found or already inserted')
