with open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_btn = """          <td>
            <button type="button" class="cht-btn cht-btn-outline cht-btn-sm" style="padding:4px 8px; font-size:0.75rem;" onclick="openEditStudentModal('${u.id}')">
              Edit Details
            </button>
          </td>"""

new_btn = """          <td>
            <div style="display:flex; flex-direction:column; gap:4px;">
              <button type="button" class="cht-btn cht-btn-outline cht-btn-sm" style="padding:4px 8px; font-size:0.75rem;" onclick="openEditStudentModal('${u.id}')">
                Edit Details
              </button>
              ${(u.vipAccess || u.driveAccess) ? `
                <a href="https://wa.me/?text=${encodeURIComponent(`Hello ${u.fullName}, congratulations on your VIP verification! Here are your activation credentials for Muse AI (1 Billion Credits):\\n\\n[Insert Voucher / Credentials Here]\\n\\nCoach Hyela Tech Industries`)}" target="_blank" class="cht-btn cht-btn-primary cht-btn-sm" style="padding:3px 8px; font-size:0.7rem; font-weight:700; background:#22C55E; color:#000; text-align:center; text-decoration:none;">
                  📲 Send Muse AI on WA
                </a>
              ` : ''}
            </div>
          </td>"""

if old_btn in text:
    text = text.replace(old_btn, new_btn, 1)
    print("Replaced button in admin.html")
else:
    print("Could not find old_btn")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Finished patching admin.html")
