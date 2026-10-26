with open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Course TD to include packageTier badge
target_td = """            <td>${r.courseTitle || r.courseId || '-'}</td>"""
new_td = """            <td>
              <div style="font-weight:600; color:#fff;">${r.courseTitle || r.courseId || '-'}</div>
              <div style="margin-top:4px;">
                ${r.packageTier === 'CERT_ONLY'
                  ? '<span style="background:rgba(255,255,255,0.1); color:#fff; padding:2px 8px; border-radius:4px; font-size:0.75rem;">🎓 Cert Only (₦500)</span>'
                  : '<span style="background:rgba(212,175,55,0.2); color:var(--cht-gold-light); padding:2px 8px; border-radius:4px; font-size:0.75rem; font-weight:700;">⭐ VIP (₦2,500)</span>'}
              </div>
            </td>"""

assert target_td in html, "Could not find target_td in admin.html"
html = html.replace(target_td, new_td, 1)

# 2. Add Tier row and Grant VIP access checkbox to modalReviewEligibility
target_modal_info = """        <div style="display:flex; justify-content:space-between;">
          <span style="color:var(--cht-text-muted);">Course Claimed:</span>
          <strong style="color:#fff;" id="reviewCourseTitle">Course</strong>
        </div>
      </div>"""

new_modal_info = """        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
          <span style="color:var(--cht-text-muted);">Course Claimed:</span>
          <strong style="color:#fff;" id="reviewCourseTitle">Course</strong>
        </div>
        <div style="display:flex; justify-content:space-between; padding-top:6px; border-top:1px solid rgba(255,255,255,0.06);">
          <span style="color:var(--cht-text-muted);">Enrolled Tier:</span>
          <span id="reviewPackageTierBadge" style="font-weight:700;">VIP Package (₦2,500)</span>
        </div>
      </div>"""

assert target_modal_info in html, "Could not find target_modal_info in admin.html"
html = html.replace(target_modal_info, new_modal_info, 1)

target_notes = """        <div class="cht-form-group">
          <label class="cht-label" for="reviewAdminNotes">Instructor / Evaluation Notes</label>
          <textarea id="reviewAdminNotes" class="cht-textarea" style="min-height: 80px;" placeholder="Feedback or reason sent tostudent in email notification..."></textarea>
        </div>"""

new_notes = target_notes + """

        <div class="cht-form-group" id="groupGrantVipAccess" style="background: rgba(212,175,55,0.08); border: 1px solid rgba(212,175,55,0.25); border-radius: 6px; padding: 12px; margin-top: 12px;">
          <label style="display:flex; align-items:center; gap:8px; cursor:pointer; font-size:0.88rem; color:#fff; font-weight: 600;">
            <input type="checkbox" id="reviewGrantDriveAccess" checked>
            <span>Grant Google Drive Vault &amp; VIP Access to this student</span>
          </label>
          <div style="font-size:0.75rem; color:var(--cht-text-muted); margin-left:24px; margin-top:3px;">
            Uncheck if student only paid ₦500 for Certificate Only (keeps Drive &amp; Canva vault locked).
          </div>
        </div>"""

assert target_notes in html, "Could not find target_notes in admin.html"
html = html.replace(target_notes, new_notes, 1)

# 3. Update openReviewModal and handleReviewSubmit
target_open_modal = """      document.getElementById('reviewCourseTitle').textContent = req.courseTitle;
      document.getElementById('reviewStatusSelect').value = req.status;
      document.getElementById('reviewAdminNotes').value = req.adminNotes || '';

      document.getElementById('modalReviewEligibility').classList.add('active');"""

new_open_modal = """      document.getElementById('reviewCourseTitle').textContent = req.courseTitle;
      document.getElementById('reviewStatusSelect').value = req.status;
      document.getElementById('reviewAdminNotes').value = req.adminNotes || '';

      const isCertOnly = req.packageTier === 'CERT_ONLY';
      const tierBadge = document.getElementById('reviewPackageTierBadge');
      if (tierBadge) {
        tierBadge.innerHTML = isCertOnly
          ? '<span style="background:rgba(255,255,255,0.1); color:#fff; padding:2px 8px; border-radius:4px; font-size:0.8rem;">🎓 Certificate Only (₦500 Tier)</span>'
          : '<span style="background:rgba(212,175,55,0.2); color:var(--cht-gold-light); padding:2px 8px; border-radius:4px; font-size:0.8rem; font-weight:700;">⭐ Complete VIP Package (₦2,500 Tier)</span>';
      }
      const chk = document.getElementById('reviewGrantDriveAccess');
      if (chk) {
        chk.checked = !isCertOnly;
      }

      document.getElementById('modalReviewEligibility').classList.add('active');"""

assert target_open_modal in html, "Could not find target_open_modal in admin.html"
html = html.replace(target_open_modal, new_open_modal, 1)

target_submit_review = """      const res = await CHT.updateEligibilityStatusCloud(reqId, status, notes);
      closeReviewModal();"""

new_submit_review = """      const res = await CHT.updateEligibilityStatusCloud(reqId, status, notes);
      if (status === 'APPROVED') {
        const grantDrive = document.getElementById('reviewGrantDriveAccess') ? document.getElementById('reviewGrantDriveAccess').checked : true;
        const studentEmail = document.getElementById('reviewStudentEmail').textContent.trim();
        await CHT.toggleDriveAccess(studentEmail, grantDrive);
      }
      closeReviewModal();"""

assert target_submit_review in html, "Could not find target_submit_review in admin.html"
html = html.replace(target_submit_review, new_submit_review, 1)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Successfully patched admin.html")
