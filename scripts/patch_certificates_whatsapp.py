with open('certificates.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Firestore SDK to head
if 'firebase-firestore-compat.js' not in html:
    html = html.replace('firebase-auth-compat.js"></script>', 'firebase-auth-compat.js"></script>\n  <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore-compat.js"></script>')
    print("Added Firestore SDK to certificates.html")

# 2. Add WhatsApp Reminder Modal to HTML (before </main>)
whatsapp_modal_html = """
  <!-- Student Application Success & WhatsApp Reminder Modal -->
  <div id="modalAppSuccess" class="cht-modal-overlay">
    <div class="cht-modal-card" style="max-width: 520px; text-align: center;">
      <div style="font-size: 3rem; margin-bottom: 12px;">🎉</div>
      <h3 class="heading-serif" style="color: #fff; font-size: 1.5rem; margin-bottom: 8px;">Application Submitted Successfully!</h3>
      <p style="color: var(--cht-text-muted); font-size: 0.9rem; line-height: 1.6; margin-bottom: 20px;">
        Your certificate eligibility request has been recorded in the central database and is now <span class="status-badge pending" style="vertical-align: middle;">Pending Approval</span> by Coach Hyela.
      </p>

      <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--cht-border-subtle); border-radius: var(--cht-radius-md); padding: 16px; margin-bottom: 24px; text-align: left; font-size: 0.88rem;">
        <div style="margin-bottom: 6px;"><strong>Application Reference:</strong> <span id="appSuccessRef" style="color: var(--cht-gold-light); font-family: monospace; font-weight: 700;"></span></div>
        <div style="margin-bottom: 6px;"><strong>Course Programme:</strong> <span id="appSuccessCourse" style="color: #fff;"></span></div>
        <div><strong>Applicant Email:</strong> <span id="appSuccessEmail" style="color: var(--cht-text-secondary);"></span></div>
      </div>

      <div style="display: flex; flex-direction: column; gap: 10px;">
        <a id="btnWhatsAppReminder" href="#" target="_blank" rel="noopener noreferrer" class="cht-btn cht-btn-primary" style="background: #25D366; color: #000; border-color: #25D366; font-weight: 700; display: flex; align-items: center; justify-content: center; gap: 8px;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217l.332.007c.106.005.249-.04.39.298.144.347.491 1.2.534 1.287.043.087.072.188.014.304-.058.116-.087.188-.173.289l-.26.304c-.087.086-.177.18-.076.354.101.174.449.741.964 1.201.662.591 1.221.774 1.394.86.173.086.275.072.376-.044.101-.116.433-.506.549-.68.116-.173.231-.145.39-.087s1.011.477 1.184.564.289.13.332.202c.043.073.043.42-.101.825z"/></svg>
          Send WhatsApp Reminder to Coach Hyela 💬
        </a>
        <button type="button" class="cht-btn cht-btn-outline" onclick="closeAppSuccessModal()">
          Close &amp; View Status on Dashboard
        </button>
      </div>
    </div>
  </div>
"""

if 'modalAppSuccess' not in html:
    html = html.replace('</main>', whatsapp_modal_html + '\n</main>')
    print("Added WhatsApp success modal")

# 3. Update handleEligibilitySubmit to call submitEligibilityRequestCloud and open modal
old_submit_func = """    function handleEligibilitySubmit(e) {
      e.preventDefault();
      const authUser = CHT.getAuthLearner();
      const rawCourse = document.getElementById('reqCourseSelect').value;
      if (!rawCourse) return;

      const [courseId, courseTitle] = rawCourse.split('|');
      const res = CHT.submitEligibilityRequest(
        authUser.id,
        authUser.fullName,
        authUser.email,
        courseId,
        courseTitle
      );

      closeEligibilityModal();
      alert(res.message);
      renderStudentEligibility(authUser.email);
    }"""

new_submit_func = """    function closeAppSuccessModal() {
      const modal = document.getElementById('modalAppSuccess');
      if (modal) modal.classList.remove('active');
    }

    async function handleEligibilitySubmit(e) {
      e.preventDefault();
      const authUser = CHT.getAuthLearner();
      const rawCourse = document.getElementById('reqCourseSelect').value;
      if (!rawCourse) return;

      const [courseId, courseTitle] = rawCourse.split('|');
      
      // Submit with Cloud Firestore Real-time Sync
      const res = await CHT.submitEligibilityRequestCloud(
        authUser.id,
        authUser.fullName,
        authUser.email,
        courseId,
        courseTitle
      );

      closeEligibilityModal();

      if (!res.success) {
        alert(res.message);
        return;
      }

      // Populate Success Modal & WhatsApp Reminder
      const req = res.request;
      document.getElementById('appSuccessRef').textContent = req.id;
      document.getElementById('appSuccessCourse').textContent = courseTitle;
      document.getElementById('appSuccessEmail').textContent = authUser.email;

      const waMsg = encodeURIComponent(`Hello Coach Hyela,\\n\\nI have submitted my Certificate Eligibility Application on your website:\\n- Student Name: ${authUser.fullName}\\n- Email: ${authUser.email}\\n- Course: ${courseTitle}\\n- Reference: ${req.id}\\n\\nPlease review and approve my official certificate.`);
      document.getElementById('btnWhatsAppReminder').href = `https://wa.me/2349159637287?text=${waMsg}`;

      document.getElementById('modalAppSuccess').classList.add('active');
      renderStudentEligibility(authUser.email);
    }"""

if old_submit_func in html:
    html = html.replace(old_submit_func, new_submit_func)
    print("Upgraded handleEligibilitySubmit with cloud sync & WhatsApp modal")
else:
    print("Warning: old_submit_func not matched")

# 4. Add visitor activity track on load
if 'CHT.trackVisitorActivity' not in html:
    html = html.replace("document.addEventListener('DOMContentLoaded', () => {", "document.addEventListener('DOMContentLoaded', () => {\n      if (window.CHT && CHT.trackVisitorActivity) CHT.trackVisitorActivity('Student Portal');")
    print("Added visitor tracking on DOMContentLoaded")

with open('certificates.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("certificates.html updated successfully!")
