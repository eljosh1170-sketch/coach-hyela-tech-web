# -*- coding: utf-8 -*-
with open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update action buttons in renderAdminStudents
old_action_btn = """              ${(u.vipAccess || u.driveAccess) ? `
                <a href="https://wa.me/?text=${encodeURIComponent(`Hello ${u.fullName}, congratulations on your VIP verification! Here are your activation credentials for Muse AI (1 Billion Credits):\\n\\n[Insert Voucher / Credentials Here]\\n\\nCoach Hyela Tech Industries`)}" target="_blank" class="cht-btn cht-btn-primary cht-btn-sm" style="padding:3px 8px; font-size:0.7rem; font-weight:700; background:#22C55E; color:#000; text-align:center; text-decoration:none;">
                  📲 Send Muse AI on WA
                </a>
              ` : ''}"""

new_action_btn = """              ${(u.vipAccess || u.driveAccess) ? `
                <a href="https://wa.me/?text=${encodeURIComponent(`Hello ${u.fullName}, congratulations on your VIP verification! Here is your access guide for Flow Creative AI workflows and your In-Portal Master Prompts Vault:\\n\\nPortal: https://coachhyelatech.com.ng/certificates.html\\n\\nCoach Hyela Tech Industries`)}" target="_blank" class="cht-btn cht-btn-primary cht-btn-sm" style="padding:3px 8px; font-size:0.7rem; font-weight:700; background:var(--cht-gold-500); color:#000; text-align:center; text-decoration:none;">
                  📲 Send Flow Guide
                </a>
              ` : ''}
              ${u.museAiPaid ? `
                <a href="https://wa.me/?text=${encodeURIComponent(`Hello ${u.fullName}, thank you for purchasing Muse AI (1 Billion Credits)! Here are your activation credentials:\\n\\n[Insert Voucher / Credentials Here]\\n\\nCoach Hyela Tech Industries`)}" target="_blank" class="cht-btn cht-btn-primary cht-btn-sm" style="padding:3px 8px; font-size:0.7rem; font-weight:700; background:#22C55E; color:#000; text-align:center; text-decoration:none;">
                  ✨ Send Muse AI (₦3k Paid)
                </a>
              ` : ''}"""

if old_action_btn in text:
    text = text.replace(old_action_btn, new_action_btn, 1)
    print("[OK] Updated action buttons in admin.html")
else:
    print("Could not find old_action_btn in admin.html")

# 2. Update modalEditStudent form to include Flow and Muse AI checkboxes
old_modal_fields = """        <div class="cht-form-group">
          <label class="cht-label" style="display: flex; align-items: center; gap: 8px; cursor: pointer;">
            <input type="checkbox" id="editStudentDriveAccess" style="width: 18px; height: 18px;">
            <span>Grant Access toRestricted Google Drive Student Vault</span>
          </label>
        </div>"""

new_modal_fields = """        <div class="cht-form-group">
          <label class="cht-label" style="display: flex; align-items: center; gap: 8px; cursor: pointer;">
            <input type="checkbox" id="editStudentDriveAccess" style="width: 18px; height: 18px;">
            <span>Grant Access to Restricted Google Drive Student Vault &amp; VIP Suite</span>
          </label>
        </div>

        <div class="cht-form-group" style="background: rgba(34, 197, 94, 0.08); border: 1px solid rgba(34, 197, 94, 0.25); border-radius: 6px; padding: 10px;">
          <label class="cht-label" style="display: flex; align-items: center; gap: 8px; cursor: pointer; color: #86EFAC; margin: 0;">
            <input type="checkbox" id="editStudentFlowAccess" style="width: 18px; height: 18px;">
            <span>Flow Creative AI Access Verified (Student has Flow)</span>
          </label>
        </div>

        <div class="cht-form-group" style="background: rgba(212, 175, 55, 0.08); border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 6px; padding: 10px;">
          <label class="cht-label" style="display: flex; align-items: center; gap: 8px; cursor: pointer; color: var(--cht-gold-light); margin: 0;">
            <input type="checkbox" id="editStudentMuseAiPaid" style="width: 18px; height: 18px;">
            <span>Muse AI (1 Billion Credits) Purchased as ₦3,000 Standalone</span>
          </label>
        </div>"""

if old_modal_fields in text:
    text = text.replace(old_modal_fields, new_modal_fields, 1)
    print("[OK] Added Flow and Muse AI checkboxes in modalEditStudent")
else:
    print("Could not find old_modal_fields in admin.html")

# 3. Update openEditStudentModal and handleEditStudentSubmit
old_modal_handlers = """    function openEditStudentModal(userId) {
      const users = CHT.getUsers();
      const user = users.find(u => u.id === userId);
      if (!user) return;

      document.getElementById('editStudentUserId').value = user.id;
      document.getElementById('editStudentFullName').value = user.fullName;
      document.getElementById('editStudentEmail').value = user.email;
      document.getElementById('editStudentDriveAccess').checked = !!user.driveAccess;

      document.getElementById('modalEditStudent').classList.add('active');
    }

    function closeEditStudentModal() {
      document.getElementById('modalEditStudent').classList.remove('active');
    }

    function handleEditStudentSubmit(e) {
      e.preventDefault();
      const userId = document.getElementById('editStudentUserId').value;
      const fullName = document.getElementById('editStudentFullName').value.trim();
      const driveAccess = document.getElementById('editStudentDriveAccess').checked;

      const res = CHT.updateStudentDetails(userId, { fullName, driveAccess });
      closeEditStudentModal();
      alert(res.message);
      renderAdminStudents();
      renderAdminEligibility();
    }"""

new_modal_handlers = """    function openEditStudentModal(userId) {
      const users = CHT.getUsers();
      const user = users.find(u => u.id === userId);
      if (!user) return;

      document.getElementById('editStudentUserId').value = user.id;
      document.getElementById('editStudentFullName').value = user.fullName;
      document.getElementById('editStudentEmail').value = user.email;
      document.getElementById('editStudentDriveAccess').checked = !!user.driveAccess;
      document.getElementById('editStudentFlowAccess').checked = !!(user.flowAccessed || user.googleAiProAccessed);
      document.getElementById('editStudentMuseAiPaid').checked = !!user.museAiPaid;

      document.getElementById('modalEditStudent').classList.add('active');
    }

    function closeEditStudentModal() {
      document.getElementById('modalEditStudent').classList.remove('active');
    }

    async function handleEditStudentSubmit(e) {
      e.preventDefault();
      const userId = document.getElementById('editStudentUserId').value;
      const fullName = document.getElementById('editStudentFullName').value.trim();
      const driveAccess = document.getElementById('editStudentDriveAccess').checked;
      const flowAccessed = document.getElementById('editStudentFlowAccess').checked;
      const museAiPaid = document.getElementById('editStudentMuseAiPaid').checked;

      const res = await CHT.updateStudentDetails(userId, {
        fullName,
        driveAccess,
        flowAccessed,
        museAiPaid
      });
      closeEditStudentModal();
      alert(res.message);
      renderAdminStudents();
      renderAdminEligibility();
    }"""

if old_modal_handlers in text:
    text = text.replace(old_modal_handlers, new_modal_handlers, 1)
    print("[OK] Updated openEditStudentModal and handleEditStudentSubmit")
else:
    print("Could not find old_modal_handlers in admin.html")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done patching admin.html")
