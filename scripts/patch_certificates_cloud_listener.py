# scripts/patch_certificates_cloud_listener.py
with open('certificates.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Sync student to Firestore on register
target_reg = """            await userCred.user.updateProfile({ displayName: name });
            await userCred.user.sendEmailVerification();"""

new_reg = """            await userCred.user.updateProfile({ displayName: name });
            await userCred.user.sendEmailVerification();
            if (window.CHT && CHT.saveStudentCloud) {
              CHT.saveStudentCloud({
                id: "USR-" + userCred.user.uid.substring(0, 8).toUpperCase(),
                fullName: name,
                email: email.toLowerCase(),
                emailVerified: false,
                registeredAt: new Date().toISOString(),
                driveAccess: false,
                assignedCourses: []
              });
            }"""

if target_reg in html and 'CHT.saveStudentCloud' not in html:
    html = html.replace(target_reg, new_reg)
    print("Added student cloud sync on register")

# 2. Sync student to Firestore on login
target_login = """            CHT.setAuthLearner(studentUser);
            showAuthAlert("Welcome back, " + studentUser.fullName + "!", false);"""

new_login = """            CHT.setAuthLearner(studentUser);
            if (window.CHT && CHT.saveStudentCloud) {
              CHT.saveStudentCloud(studentUser);
            }
            showAuthAlert("Welcome back, " + studentUser.fullName + "!", false);"""

if target_login in html:
    html = html.replace(target_login, new_login)
    print("Added student cloud sync on login")

# 3. Update showStudentDashboard to subscribe to real-time cloud updates
target_dash = """    function showStudentDashboard(user) {
      document.getElementById('authSectionWrapper').style.display = 'none';
      document.getElementById('studentDashboardSection').style.display = 'block';

      document.getElementById('dashUserId').textContent = user.id;
      document.getElementById('dashStudentName').textContent = user.fullName;
      document.getElementById('dashStudentEmail').textContent = user.email;

      renderStudentEligibility(user.email);
      renderDriveVault(user);
    }"""

new_dash = """    function showStudentDashboard(user) {
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

if target_dash in html:
    html = html.replace(target_dash, new_dash)
    print("Added real-time cloud request listener in student dashboard")

# 4. Update renderStudentEligibility to accept cloudReqs
target_render_elig = """    // 6. RENDER ELIGIBILITY & CLAIMS
    function renderStudentEligibility(email) {
      const allReqs = CHT.getEligibilityRequests();"""

new_render_elig = """    // 6. RENDER ELIGIBILITY & CLAIMS
    function renderStudentEligibility(email, cloudReqs) {
      const allReqs = cloudReqs || CHT.getEligibilityRequests();"""

if target_render_elig in html:
    html = html.replace(target_render_elig, new_render_elig)
    print("Updated renderStudentEligibility to support cloudReqs")

with open('certificates.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("certificates.html real-time updates completed!")
