# scripts/patch_admin_js_full.py
with open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update showAdminConsole
old_show_console = """    function showAdminConsole() {
      document.getElementById('adminLoginBox').style.display = 'none';
      document.getElementById('adminConsole').style.display = 'block';
      renderAdminEligibility();
      renderAdminStudents();
      renderAdminCertificates();
      renderAdminCAC();
      renderAdminNotifs();
        initEmailSettings();
    }"""

new_show_console = """    function showAdminConsole() {
      document.getElementById('adminLoginBox').style.display = 'none';
      document.getElementById('adminConsole').style.display = 'block';

      // 1. Initial renders
      renderAdminEligibility();
      renderAdminStudents();
      renderAdminCertificates();
      renderAdminCAC();
      renderAdminNotifs();
      initEmailSettings();

      // 2. Real-time Cloud Firestore Listeners (Live across any device in Nigeria)
      if (window.CHT) {
        // Real-time Student Eligibility Applications
        if (CHT.subscribeCloudRequests) {
          CHT.subscribeCloudRequests(reqs => {
            renderAdminEligibility(reqs);
          });
        }
        // Real-time Registered Students Directory
        if (CHT.subscribeCloudStudents) {
          CHT.subscribeCloudStudents(students => {
            renderAdminStudents(students);
          });
        }
        // Real-time CAC Inquiries Inbox
        if (CHT.subscribeCloudCAC) {
          CHT.subscribeCloudCAC(subs => {
            renderAdminCAC(subs);
          });
        }
        // Real-time Visitor Stats Counter
        if (CHT.subscribeVisitorStats) {
          CHT.subscribeVisitorStats(stats => {
            updateAdminMetricCards(stats);
          });
        }
        // Real-time Activity Stream Feed
        if (CHT.subscribeActivityLogs) {
          CHT.subscribeActivityLogs(logs => {
            renderAdminActivityStream(logs);
          });
        }
      }
    }

    function updateAdminMetricCards(stats) {
      if (!stats) return;
      const elViews = document.getElementById('metricPageViews');
      const elVisitors = document.getElementById('metricUniqueVisitors');
      const elLastSync = document.getElementById('metricLastSync');
      if (elViews && stats.pageViews !== undefined) elViews.textContent = Number(stats.pageViews).toLocaleString();
      if (elVisitors && stats.visitors !== undefined) elVisitors.textContent = Number(stats.visitors).toLocaleString();
      if (elLastSync && stats.lastActive) {
        elLastSync.textContent = 'Active: ' + new Date(stats.lastActive).toLocaleTimeString();
      }
    }

    let latestActivityLogs = [];
    function renderAdminActivityStream(logs) {
      if (logs) latestActivityLogs = logs;
      const tbody = document.getElementById('tableBodyActivityStream');
      if (!tbody) return;
      if (!latestActivityLogs || latestActivityLogs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:24px; color:var(--cht-text-muted);">No activity recorded yet. Browse the public website to see live events appear here.</td></tr>`;
        return;
      }

      tbody.innerHTML = latestActivityLogs.map(log => {
        let pillColor = 'approved';
        if (log.type === 'STUDENT_APPLICATION' || log.type === 'MANUAL_APP_SYNC') pillColor = 'pending';
        if (log.type === 'ADMIN_DECISION') pillColor = 'more_info';
        if (log.type === 'CAC_REGISTRATION') pillColor = 'approved';

        const timeStr = log.timestamp ? new Date(log.timestamp).toLocaleTimeString() : 'Just now';

        return `
          <tr>
            <td style="font-size:0.78rem; font-family:monospace; color:var(--cht-text-muted);">${timeStr}</td>
            <td><span class="status-pill ${pillColor}" style="font-size:0.7rem;">${log.type}</span></td>
            <td style="color:#fff; font-weight:600;">${log.page || 'Website'}</td>
            <td><span style="font-size:0.8rem; color:var(--cht-gold-light);">${log.device || 'Web'}</span></td>
            <td style="font-size:0.82rem; color:var(--cht-text-secondary);">${log.details || 'Visited page'}</td>
          </tr>
        `;
      }).join('');
    }"""

if old_show_console in html:
    html = html.replace(old_show_console, new_show_console)
    print("Upgraded showAdminConsole with real-time listeners and metric card updates")

# 2. Update switchAdminTab
old_switch_tab = """    function switchAdminTab(tab) {
      const tabs = ['eligibility', 'students', 'certs', 'cac', 'notifs', 'liveContent'];
      tabs.forEach(t => {
        const btn = document.getElementById('tabBtn' + capitalize(t));
        const content = document.getElementById('tabContent' + capitalize(t));
        if (btn) btn.classList.toggle('active', t === tab);
        if (content) content.style.display = (t === tab) ? 'block' : 'none';
      });

      if (tab === 'eligibility') renderAdminEligibility();
      if (tab === 'students') renderAdminStudents();
      if (tab === 'certs') renderAdminCertificates();
      if (tab === 'cac') renderAdminCAC();
      if (tab === 'notifs') renderAdminNotifs();
        initEmailSettings();

      if (tab === 'liveContent') renderLiveContentEditor();
    }"""

new_switch_tab = """    function switchAdminTab(tab) {
      const tabs = ['eligibility', 'students', 'certs', 'cac', 'notifs', 'liveContent', 'analytics'];
      tabs.forEach(t => {
        const btn = document.getElementById('tabBtn' + capitalize(t));
        const content = document.getElementById('tabContent' + capitalize(t));
        if (btn) btn.classList.toggle('active', t === tab);
        if (content) content.style.display = (t === tab) ? 'block' : 'none';
      });

      if (tab === 'eligibility') renderAdminEligibility();
      if (tab === 'students') renderAdminStudents();
      if (tab === 'certs') renderAdminCertificates();
      if (tab === 'cac') renderAdminCAC();
      if (tab === 'notifs') renderAdminNotifs();
      if (tab === 'analytics') renderAdminActivityStream();
      initEmailSettings();

      if (tab === 'liveContent') renderLiveContentEditor();
    }"""

if old_switch_tab in html:
    html = html.replace(old_switch_tab, new_switch_tab)
    print("Upgraded switchAdminTab to include analytics tab")

# 3. Update renderAdminEligibility
old_render_eligibility = """    // 1. RENDER ELIGIBILITY
    function renderAdminEligibility() {
      const reqs = CHT.getEligibilityRequests();
      const tbody= document.getElementById('tableBodyEligibility');
      
      const pendingCount = reqs.filter(r => r.status === 'PENDING').length;
      document.getElementById('badgePendingCount').textContent = pendingCount;

      if (reqs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding:24px; color:var(--cht-text-muted);">Noeligibility requests recorded.</td></tr>`;
        return;
      }

      tbody.innerHTML = reqs.map(r => {
        let pillClass = 'pending';
        if (r.status === 'APPROVED') pillClass = 'approved';
        else if (r.status === 'REJECTED') pillClass = 'rejected';
        else if (r.status === 'MORE_INFo') pillClass = 'more_info';

        return `
          <tr>
            <td><strong style="font-family:monospace; color:var(--cht-gold-light);">${r.id}</strong></td>
            <td style="color:#fff; font-weight:600;">${r.fullName}</td>
            <td><span style="color:var(--cht-text-muted);">${r.email}</span></td>
            <td>${r.courseTitle}</td>
            <td style="font-size:0.8rem;">${new Date(r.submissionDate).toLocaleDateString()}</td>
            <td><span class="status-pill ${pillClass}">${r.status}</span></td>
            <td style="font-size:0.8rem; max-width:200px;">${r.adminNotes || '—'}</td>
            <td>
              <div style="display:flex; gap:6px;">
                <button type="button" class="cht-btn cht-btn-primary cht-btn-sm" style="padding:4px 10px; font-size:0.75rem;" onclick="openReviewModal('${r.id}')">
                  Review / Update
                </button>
                ${r.certificateCode ? `
                  <a href="verify.html?code=${r.certificateCode}" target="_blank" class="cht-btn cht-btn-outline cht-btn-sm" style="padding:4px 8px; font-size:0.75rem;">
                    Cert
                  </a>
                ` : ''}
              </div>
            </td>
          </tr>
        `;
      }).join('');
    }"""

new_render_eligibility = """    // 1. RENDER ELIGIBILITY WITH CLOUD SYNC & EXECUTIVE METRIC UPDATES
    let currentEligibilityReqs = [];
    function renderAdminEligibility(cloudReqs) {
      const reqs = cloudReqs || CHT.getEligibilityRequests();
      currentEligibilityReqs = reqs;
      const tbody = document.getElementById('tableBodyEligibility');
      if (!tbody) return;
      
      const pendingCount = reqs.filter(r => r.status === 'PENDING').length;
      const badge = document.getElementById('badgePendingCount');
      if (badge) badge.textContent = pendingCount;
      const metricPending = document.getElementById('metricPendingPill');
      if (metricPending) metricPending.textContent = `${pendingCount} Pending`;
      const metricTotal = document.getElementById('metricTotalApps');
      if (metricTotal) metricTotal.textContent = reqs.length;

      if (reqs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding:24px; color:var(--cht-text-muted);">No eligibility requests recorded yet. Click "+ Manually Add Student Application" above to record one.</td></tr>`;
        return;
      }

      tbody.innerHTML = reqs.map(r => {
        let pillClass = 'pending';
        if (r.status === 'APPROVED') pillClass = 'approved';
        else if (r.status === 'REJECTED') pillClass = 'rejected';
        else if (r.status === 'MORE_INFO' || r.status === 'MORE_INFo') pillClass = 'more_info';

        return `
          <tr>
            <td><strong style="font-family:monospace; color:var(--cht-gold-light);">${r.id}</strong></td>
            <td style="color:#fff; font-weight:600;">${r.fullName || 'Student'}</td>
            <td><span style="color:var(--cht-text-muted);">${r.email || '-'}</span></td>
            <td>${r.courseTitle || r.courseId || '-'}</td>
            <td style="font-size:0.8rem;">${r.submissionDate ? new Date(r.submissionDate).toLocaleDateString() : 'Recent'}</td>
            <td><span class="status-pill ${pillClass}">${r.status}</span></td>
            <td style="font-size:0.8rem; max-width:200px;">${r.adminNotes || '—'}</td>
            <td>
              <div style="display:flex; gap:6px;">
                <button type="button" class="cht-btn cht-btn-primary cht-btn-sm" style="padding:4px 10px; font-size:0.75rem;" onclick="openReviewModal('${r.id}')">
                  Review / Update
                </button>
                ${r.certificateCode ? `
                  <a href="verify.html?code=${r.certificateCode}" target="_blank" class="cht-btn cht-btn-outline cht-btn-sm" style="padding:4px 8px; font-size:0.75rem;">
                    Cert
                  </a>
                ` : ''}
              </div>
            </td>
          </tr>
        `;
      }).join('');
    }"""

if old_render_eligibility in html:
    html = html.replace(old_render_eligibility, new_render_eligibility)
    print("Upgraded renderAdminEligibility with cloud synchronization")

# 4. Update openReviewModal and handleReviewSubmit
old_review_handlers = """    // 2. REVIEW MoDAL LoGIC
    function openReviewModal(reqId) {
      const reqs = CHT.getEligibilityRequests();
      const req = reqs.find(r => r.id === reqId);
      if (!req) return;

      document.getElementById('reviewReqId').value = req.id;
      document.getElementById('reviewStudentName').textContent = req.fullName;
      document.getElementById('reviewStudentEmail').textContent = req.email;
      document.getElementById('reviewCourseTitle').textContent = req.courseTitle;
      document.getElementById('reviewStatusSelect').value = req.status;
      document.getElementById('reviewAdminNotes').value = req.adminNotes || '';

      document.getElementById('modalReviewEligibility').classList.add('active');
    }

    function closeReviewModal() {
      document.getElementById('modalReviewEligibility').classList.remove('active');
    }

    function handleReviewSubmit(e) {
      e.preventDefault();
      const reqId = document.getElementById('reviewReqId').value;
      const status = document.getElementById('reviewStatusSelect').value;
      const notes = document.getElementById('reviewAdminNotes').value.trim();

      const res = CHT.updateEligibilityStatus(reqId, status, notes);
      closeReviewModal();
      alert(res.message);
      renderAdminEligibility();
      renderAdminStudents();
      renderAdminNotifs();
        initEmailSettings();
    }"""

new_review_handlers = """    // 2. REVIEW MODAL LOGIC & CLOUD UPDATE
    function openReviewModal(reqId) {
      const reqs = currentEligibilityReqs.length > 0 ? currentEligibilityReqs : CHT.getEligibilityRequests();
      const req = reqs.find(r => r.id === reqId);
      if (!req) return;

      document.getElementById('reviewReqId').value = req.id;
      document.getElementById('reviewStudentName').textContent = req.fullName;
      document.getElementById('reviewStudentEmail').textContent = req.email;
      document.getElementById('reviewCourseTitle').textContent = req.courseTitle;
      document.getElementById('reviewStatusSelect').value = req.status;
      document.getElementById('reviewAdminNotes').value = req.adminNotes || '';

      document.getElementById('modalReviewEligibility').classList.add('active');
    }

    function closeReviewModal() {
      document.getElementById('modalReviewEligibility').classList.remove('active');
    }

    async function handleReviewSubmit(e) {
      e.preventDefault();
      const reqId = document.getElementById('reviewReqId').value;
      const status = document.getElementById('reviewStatusSelect').value;
      const notes = document.getElementById('reviewAdminNotes').value.trim();

      const res = await CHT.updateEligibilityStatusCloud(reqId, status, notes);
      closeReviewModal();
      alert(res.message);
      renderAdminEligibility();
      renderAdminStudents();
      renderAdminCertificates();
      renderAdminNotifs();
      initEmailSettings();
    }

    // MANUAL APPLICATION ADD MODAL HANDLERS
    function openManualAddAppModal() {
      document.getElementById('modalManualAddApp').classList.add('active');
    }
    function closeManualAddAppModal() {
      document.getElementById('modalManualAddApp').classList.remove('active');
    }
    async function handleManualAddAppSubmit(e) {
      e.preventDefault();
      const name = document.getElementById('manualAppName').value.trim();
      const email = document.getElementById('manualAppEmail').value.trim();
      const rawCourse = document.getElementById('manualAppCourse').value;
      const status = document.getElementById('manualAppStatus').value;
      const notes = document.getElementById('manualAppNotes').value.trim();

      const [courseId, courseTitle] = rawCourse.split('|');

      const btn = document.getElementById('btnSubmitManualApp');
      if (btn) btn.disabled = true;

      const res = await CHT.createEligibilityRequestCloud({
        fullName: name,
        email: email,
        courseId: courseId,
        courseTitle: courseTitle,
        status: status,
        adminNotes: notes || (status === 'APPROVED' ? 'Approved by Coach Hyela administration.' : 'Awaiting evaluation.')
      });

      if (btn) btn.disabled = false;
      closeManualAddAppModal();

      if (res.success) {
        alert(`Application recorded and synced to Cloud Firestore!\\nReference: ${res.request.id}\\nStatus: ${status}`);
        renderAdminEligibility();
        renderAdminCertificates();
      } else {
        alert('Error recording application: ' + res.message);
      }
    }"""

if old_review_handlers in html:
    html = html.replace(old_review_handlers, new_review_handlers)
    print("Upgraded review handlers and added manual application add handlers")

# 5. Update renderAdminCAC to update metric card
old_render_cac = """    // 5. RENDER CAC INBoX
    function renderAdminCAC() {
      const submissions = CHT.getCACSubmissions();
      document.getElementById('cacCountLabel').textContent = `${submissions.length} Total Submissions`;
      const tbody= document.getElementById('adminCACTableBody');"""

new_render_cac = """    // 5. RENDER CAC INBOX WITH METRIC CARD UPDATE
    function renderAdminCAC(cloudSubs) {
      const submissions = cloudSubs || CHT.getCACSubmissions();
      const label = document.getElementById('cacCountLabel');
      if (label) label.textContent = `${submissions.length} Total Submissions`;
      const metricCAC = document.getElementById('metricTotalCAC');
      if (metricCAC) metricCAC.textContent = submissions.length;
      const tbody = document.getElementById('adminCACTableBody');"""

if old_render_cac in html:
    html = html.replace(old_render_cac, new_render_cac)
    print("Upgraded renderAdminCAC with metric update")

# 6. Update renderAdminStudents
old_render_students = """    // 3. RENDER STUDENTS DIRECToRY
    function renderAdminStudents() {
      const users = CHT.getUsers();
      const tbody= document.getElementById('tableBodyStudents');"""

new_render_students = """    // 3. RENDER STUDENTS DIRECTORY WITH CLOUD SYNC
    function renderAdminStudents(cloudStudents) {
      const users = cloudStudents || CHT.getUsers();
      const tbody = document.getElementById('tableBodyStudents');"""

if old_render_students in html:
    html = html.replace(old_render_students, new_render_students)
    print("Upgraded renderAdminStudents with cloud sync parameter")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("admin.html JavaScript block upgraded successfully!")
