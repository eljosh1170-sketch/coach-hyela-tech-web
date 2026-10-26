# Patch certificates.html to add Payment & Enrollment Verification Gate
with open('certificates.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Insert Payment Gate HTML before <div class="cht-grid cht-grid-2 no-print"
target_grid = """        <!-- Grid of Statuses and Resources -->
        <div class="cht-grid cht-grid-2 no-print" style="margin-bottom: 40px;">"""

payment_gate_html = """        <!-- Interactive Enrollment & Payment Verification Gate -->
        <div id="paymentEnrollmentGate" class="cht-card no-print" style="padding: 26px; margin-bottom: 34px; border: 1px solid rgba(212, 175, 55, 0.45); background: linear-gradient(135deg, rgba(20, 24, 33, 0.98), rgba(15, 18, 25, 0.95)); border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 14px; margin-bottom: 20px;">
            <div>
              <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(212, 175, 55, 0.15); border: 1px solid rgba(212, 175, 55, 0.3); padding: 4px 12px; border-radius: 99px; margin-bottom: 8px;">
                <span style="color: var(--cht-gold-light); font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Student Enrollment Verification</span>
              </div>
              <h3 class="heading-serif" style="color: #fff; font-size: 1.4rem; margin-top: 4px;">
                Have You Already Made Payment for Your Course or Certificate?
              </h3>
              <p style="color: var(--cht-text-secondary); font-size: 0.9rem; margin-top: 4px; max-width: 720px;">
                Select your payment status below to submit your certificate verification claim or lock in the special October promo discount.
              </p>
            </div>
          </div>

          <!-- Toggle Buttons -->
          <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 24px;">
            <button type="button" id="btnPaidYes" class="cht-btn cht-btn-primary" onclick="setPaymentGateChoice('YES')" style="padding: 10px 20px; font-weight: 700; font-size: 0.92rem; display: inline-flex; align-items: center; gap: 8px;">
              <span>✓ Yes, I Already Paid</span>
            </button>
            <button type="button" id="btnPaidNo" class="cht-btn cht-btn-outline" onclick="setPaymentGateChoice('NO')" style="padding: 10px 20px; font-weight: 700; font-size: 0.92rem; display: inline-flex; align-items: center; gap: 8px; border-color: var(--cht-gold-500); color: var(--cht-gold-light);">
              <span>⚡ No, I Have Not Paid Yet / Pay Now</span>
            </button>
          </div>

          <!-- PANEL A: YES, ALREADY PAID -->
          <div id="panelPaidYes" style="display: block;">
            <div style="background: rgba(34, 197, 94, 0.08); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 8px; padding: 18px; margin-bottom: 10px;">
              <div style="display: flex; align-items: flex-start; gap: 12px;">
                <div style="font-size: 1.5rem; line-height: 1;">🎓</div>
                <div style="flex: 1;">
                  <h4 style="color: #86EFAC; font-size: 1.05rem; margin-bottom: 4px; font-weight: 700;">
                    Existing Paid Student Access
                  </h4>
                  <p style="color: var(--cht-text-secondary); font-size: 0.88rem; line-height: 1.5; margin-bottom: 14px;">
                    If you already made payment for your training, submit your completion claim below. Coach Hyela will evaluate your coursework, issue your official certificate, and grant your VIP bonuses (Canva Pro invite, Google Drive Vault, and Google AI Pro).
                  </p>
                  <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                    <button type="button" class="cht-btn cht-btn-primary cht-btn-sm" onclick="openEligibilityModal()">
                      + Submit Certificate &amp; VIP Claim
                    </button>
                    <a id="btnWhatsAppPaymentProof" href="https://wa.me/2349159637287" target="_blank" rel="noopener noreferrer" class="cht-btn cht-btn-outline cht-btn-sm" style="display: inline-flex; align-items: center; gap: 6px; border-color: #22C55E; color: #86EFAC;">
                      <span>💬 Send Verification Reminder on WhatsApp</span>
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- PANEL B: NO, NOT PAID YET (SPECIAL OCTOBER PROMO) -->
          <div id="panelPaidNo" style="display: none;">
            <!-- Urgency Countdown & Alert -->
            <div style="background: linear-gradient(135deg, rgba(212, 175, 55, 0.15), rgba(239, 68, 68, 0.1)); border: 1px solid var(--cht-gold-500); border-radius: 8px; padding: 16px; margin-bottom: 24px;">
              <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                  <span style="font-size: 1.4rem;">🔥</span>
                  <div>
                    <strong style="color: var(--cht-gold-light); font-size: 1rem; text-transform: uppercase; letter-spacing: 0.5px;">Special Limited-Time Discount Offer</strong>
                    <div style="font-size: 0.85rem; color: #fff; margin-top: 2px;">
                      Offer valid strictly until <strong>31st of October 2026</strong>. Lock in your preferred option before tuition returns to normal pricing.
                    </div>
                  </div>
                </div>
                <div style="background: rgba(0,0,0,0.5); border: 1px solid rgba(212,175,55,0.4); padding: 6px 14px; border-radius: 6px; text-align: center;">
                  <div style="font-size: 0.72rem; text-transform: uppercase; color: var(--cht-text-muted); letter-spacing: 1px;">Offer Ends</div>
                  <div style="font-size: 0.95rem; font-weight: 800; color: #EF4444;">31 OCT 2026</div>
                </div>
              </div>
            </div>

            <!-- The 2 Side-by-Side Pricing Cards -->
            <div class="cht-grid cht-grid-2" style="gap: 20px; margin-bottom: 24px;">
              
              <!-- CARD 1: COMPLETE VIP ACCESS BUNDLE -->
              <div class="cht-card" style="padding: 24px; border: 2px solid var(--cht-gold-500); background: rgba(0,0,0,0.35); position: relative; display: flex; flex-direction: column; justify-content: space-between;">
                <div style="position: absolute; top: -12px; right: 20px; background: linear-gradient(135deg, var(--cht-gold-400), var(--cht-gold-600)); color: #000; font-size: 0.75rem; font-weight: 800; padding: 3px 12px; border-radius: 99px; text-transform: uppercase; letter-spacing: 0.5px;">
                  ⭐ Best Value • Complete Bundle
                </div>

                <div>
                  <h4 style="color: #fff; font-size: 1.25rem; margin-top: 4px; margin-bottom: 6px;">
                    Complete VIP Access Bundle
                  </h4>
                  <p style="color: var(--cht-text-muted); font-size: 0.85rem; margin-bottom: 16px;">
                    Full practical career package with official certificate and complete suite of premium AI assets.
                  </p>

                  <div style="display: flex; align-items: baseline; gap: 8px; margin-bottom: 18px; border-bottom: 1px solid var(--cht-border-subtle); padding-bottom: 14px;">
                    <span style="font-size: 2.2rem; font-weight: 800; color: var(--cht-gold-light);">₦2,500</span>
                    <span style="text-decoration: line-through; color: var(--cht-text-muted); font-size: 1.1rem;">₦4,000</span>
                    <span style="background: rgba(34, 197, 94, 0.2); color: #86EFAC; font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 4px;">Save ₦1,500</span>
                  </div>

                  <ul style="list-style: none; padding: 0; margin: 0 0 20px 0; font-size: 0.88rem; color: var(--cht-text-secondary); line-height: 1.8;">
                    <li style="display: flex; align-items: flex-start; gap: 8px;">
                      <span style="color: #22C55E; font-weight: bold;">✓</span>
                      <span><strong>Official Certificate of Completion</strong> (with Verifiable QR Code &amp; Direct Link)</span>
                    </li>
                    <li style="display: flex; align-items: flex-start; gap: 8px;">
                      <span style="color: #22C55E; font-weight: bold;">✓</span>
                      <span><strong>1-Year Canva Pro Team Access</strong> (Brand kits, magic AI tools, premium assets)</span>
                    </li>
                    <li style="display: flex; align-items: flex-start; gap: 8px;">
                      <span style="color: #22C55E; font-weight: bold;">✓</span>
                      <span><strong>Google Drive Master Prompts &amp; E-Books Vault</strong> (Photorealistic prompts, reel workflows)</span>
                    </li>
                    <li style="display: flex; align-items: flex-start; gap: 8px;">
                      <span style="color: #22C55E; font-weight: bold;">✓</span>
                      <span><strong>Google AI Pro 18-Month Package</strong> (Extended reasoning &amp; models suite)</span>
                    </li>
                  </ul>
                </div>

                <button type="button" class="cht-btn cht-btn-primary" onclick="selectPaymentTier('VIP_BUNDLE', 2500)" style="width: 100%; font-weight: 700; padding: 12px; font-size: 0.95rem;">
                  Select VIP Bundle — Pay ₦2,500 →
                </button>
              </div>

              <!-- CARD 2: OFFICIAL CERTIFICATE ONLY -->
              <div class="cht-card" style="padding: 24px; border: 1px solid var(--cht-border-subtle); background: rgba(0,0,0,0.25); position: relative; display: flex; flex-direction: column; justify-content: space-between;">
                <div style="position: absolute; top: -12px; right: 20px; background: rgba(255,255,255,0.1); color: var(--cht-text-muted); font-size: 0.75rem; font-weight: 700; padding: 3px 12px; border-radius: 99px; text-transform: uppercase; letter-spacing: 0.5px;">
                  🎓 Certificate Only
                </div>

                <div>
                  <h4 style="color: #fff; font-size: 1.25rem; margin-top: 4px; margin-bottom: 6px;">
                    Official Certificate Only
                  </h4>
                  <p style="color: var(--cht-text-muted); font-size: 0.85rem; margin-bottom: 16px;">
                    First-time special offer for students who only require the verifiable graduation credential.
                  </p>

                  <div style="display: flex; align-items: baseline; gap: 8px; margin-bottom: 18px; border-bottom: 1px solid var(--cht-border-subtle); padding-bottom: 14px;">
                    <span style="font-size: 2.2rem; font-weight: 800; color: #FFFFFF;">₦500</span>
                    <span style="text-decoration: line-through; color: var(--cht-text-muted); font-size: 1.1rem;">₦5,000</span>
                    <span style="background: rgba(212, 175, 55, 0.2); color: var(--cht-gold-light); font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 4px;">Save ₦4,500</span>
                  </div>

                  <ul style="list-style: none; padding: 0; margin: 0 0 20px 0; font-size: 0.88rem; color: var(--cht-text-secondary); line-height: 1.8;">
                    <li style="display: flex; align-items: flex-start; gap: 8px;">
                      <span style="color: #22C55E; font-weight: bold;">✓</span>
                      <span><strong>Official Certificate of Completion</strong> (with Verifiable QR Code &amp; Direct Link)</span>
                    </li>
                    <li style="display: flex; align-items: flex-start; gap: 8px; color: var(--cht-text-muted);">
                      <span style="color: #EF4444; font-weight: bold;">✕</span>
                      <span>1-Year Canva Pro Team Access <em>(Locked)</em></span>
                    </li>
                    <li style="display: flex; align-items: flex-start; gap: 8px; color: var(--cht-text-muted);">
                      <span style="color: #EF4444; font-weight: bold;">✕</span>
                      <span>Google Drive Master Prompts Vault <em>(Locked)</em></span>
                    </li>
                    <li style="display: flex; align-items: flex-start; gap: 8px; color: var(--cht-text-muted);">
                      <span style="color: #EF4444; font-weight: bold;">✕</span>
                      <span>Google AI Pro Package <em>(Locked)</em></span>
                    </li>
                  </ul>
                </div>

                <button type="button" class="cht-btn cht-btn-outline" onclick="selectPaymentTier('CERT_ONLY', 500)" style="width: 100%; font-weight: 700; padding: 12px; font-size: 0.95rem; border-color: rgba(255,255,255,0.3);">
                  Select Certificate Only — Pay ₦500 →
                </button>
              </div>

            </div>

            <!-- Official PalmPay Transfer Box -->
            <div id="paymentInstructionsBox" style="background: rgba(0,0,0,0.35); border: 1px solid rgba(212, 175, 55, 0.35); border-radius: 10px; padding: 20px;">
              <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 14px; margin-bottom: 16px;">
                <div>
                  <span class="cht-section-tag" style="background: rgba(212, 175, 55, 0.2); font-size: 0.75rem;">Official PalmPay Payment Gateway</span>
                  <h4 style="color: #fff; font-size: 1.15rem; margin-top: 4px;">
                    Transfer Tuition Directly to Coach Hyela
                  </h4>
                  <p style="color: var(--cht-text-secondary); font-size: 0.85rem; margin-top: 2px;">
                    Use the official PalmPay credentials below to transfer via PalmPay or any mobile banking app.
                  </p>
                </div>
                <div id="selectedTierBanner" style="background: rgba(212,175,55,0.15); border: 1px solid var(--cht-gold-500); padding: 6px 14px; border-radius: 6px; font-size: 0.85rem; font-weight: 700; color: var(--cht-gold-light);">
                  Selected: Complete VIP Bundle (₦2,500)
                </div>
              </div>

              <div class="cht-grid cht-grid-2" style="gap: 16px; margin-bottom: 18px;">
                <div class="cht-account-number-box">
                  <div>
                    <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: var(--cht-text-muted);">PalmPay Account Number</div>
                    <div class="cht-acc-num" id="payGateAccNum">7011706511</div>
                    <div style="font-size: 0.75rem; color: var(--cht-text-muted); margin-top: 2px;">(Also accepts phone: 09159637287)</div>
                  </div>
                  <button type="button" class="cht-copy-btn" onclick="copyAccountNumber('7011706511', this)">Copy 7011706511</button>
                </div>

                <div class="cht-account-number-box">
                  <div>
                    <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: var(--cht-text-muted);">Account Beneficiary Name</div>
                    <div style="font-size: 1.1rem; font-weight: 800; color: #FFFFFF;" id="payGateAccName">EL JOSHUA HYELAKURI EMMANUEL</div>
                    <div style="font-size: 0.75rem; color: var(--cht-gold-light); margin-top: 2px;">Bank: PalmPay • Always verify name before sending</div>
                  </div>
                  <span style="font-size: 0.8rem; color: var(--cht-gold-light); font-weight: 700;">Verified ✓</span>
                </div>
              </div>

              <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 16px;">
                <div style="font-size: 0.85rem; color: var(--cht-text-muted);">
                  After transfer, click below to forward your payment receipt to Coach Hyela on WhatsApp for instant confirmation.
                </div>
                <a id="btnSubmitPaymentReceiptWa" href="https://wa.me/2349159637287" target="_blank" rel="noopener noreferrer" class="cht-btn cht-btn-primary" style="display: inline-flex; align-items: center; gap: 8px; font-weight: 700; padding: 10px 18px;">
                  <span>📲 Submit Payment Receipt on WhatsApp (0915-963-7287) →</span>
                </a>
              </div>
            </div>

          </div>
        </div>

"""

assert target_grid in html, "Could not find target_grid in certificates.html"
html = html.replace(target_grid, payment_gate_html + target_grid, 1)

# 2. Add Package Tier select in modalEligibility
target_modal_course = """        <div class="cht-form-group">
          <label class="cht-label" for="reqCourseSelect">Completed Course Programme <span class="req">*</span></label>"""

modal_tier_html = """        <div class="cht-form-group">
          <label class="cht-label" for="reqPackageTier">Package / Enrollment Tier <span class="req">*</span></label>
          <select id="reqPackageTier" class="cht-select" required>
            <option value="VIP_BUNDLE">⭐ Complete VIP Access Bundle (₦2,500 / Full Paid — Includes Canva Pro + Drive Vault + AI Pro)</option>
            <option value="CERT_ONLY">🎓 Official Certificate Only (₦500 Promo Tier — Verifiable QR Certificate Only)</option>
          </select>
        </div>

"""

assert target_modal_course in html, "Could not find target_modal_course in certificates.html"
html = html.replace(target_modal_course, modal_tier_html + target_modal_course, 1)

# 3. Add client JS functions for Payment Gate
target_show_dash = """    function showStudentDashboard(user) {
      document.getElementById('authSectionWrapper').style.display = 'none';
      document.getElementById('studentDashboardSection').style.display = 'block';

      document.getElementById('dashUserId').textContent = user.id;
      document.getElementById('dashStudentName').textContent = user.fullName;
      document.getElementById('dashStudentEmail').textContent = user.email;

      renderStudentEligibility(user.email);
      renderDriveVault(user);"""

new_show_dash = """    function showStudentDashboard(user) {
      document.getElementById('authSectionWrapper').style.display = 'none';
      document.getElementById('studentDashboardSection').style.display = 'block';

      document.getElementById('dashUserId').textContent = user.id;
      document.getElementById('dashStudentName').textContent = user.fullName;
      document.getElementById('dashStudentEmail').textContent = user.email;

      initPaymentGate(user);
      renderStudentEligibility(user.email);
      renderDriveVault(user);"""

assert target_show_dash in html, "Could not find target_show_dash in certificates.html"
html = html.replace(target_show_dash, new_show_dash, 1)

# 4. Update handleEligibilitySubmit
target_submit = """      // Submit with Cloud Firestore Real-time Sync
      const res = await CHT.submitEligibilityRequestCloud(
        authUser.id,
        authUser.fullName,
        authUser.email,
        courseId,
        courseTitle
      );"""

new_submit = """      const packageTier = document.getElementById('reqPackageTier') ? document.getElementById('reqPackageTier').value : 'VIP_BUNDLE';
      const tierLabel = packageTier === 'CERT_ONLY' ? 'Official Certificate Only (₦500 Promo Tier)' : 'Complete VIP Access Bundle (₦2,500)';

      // Submit with Cloud Firestore Real-time Sync
      const res = await CHT.submitEligibilityRequestCloud(
        authUser.id,
        authUser.fullName,
        authUser.email,
        courseId,
        courseTitle,
        packageTier
      );"""

assert target_submit in html, "Could not find target_submit in certificates.html"
html = html.replace(target_submit, new_submit, 1)

# 5. Update waMsg in handleEligibilitySubmit
target_wamsg = """      const waMsg = encodeURIComponent(`Hello Coach Hyela,\\n\\nI have submitted my Certificate Eligibility Application on your website:\\n- Student Name: ${authUser.fullName}\\n- Email: ${authUser.email}\\n- Course: ${courseTitle}\\n- Reference: ${req.id}\\n\\nPlease review and approve my official certificate.`);"""
new_wamsg = """      const waMsg = encodeURIComponent(`Hello Coach Hyela,\\n\\nI have submitted my Certificate Eligibility Application on your website:\\n- Student Name: ${authUser.fullName}\\n- Email: ${authUser.email}\\n- Course: ${courseTitle}\\n- Selected Tier: ${tierLabel}\\n- Reference: ${req.id}\\n\\nPlease review and approve my official credentials.`);"""

assert target_wamsg in html, "Could not find target_wamsg in certificates.html"
html = html.replace(target_wamsg, new_wamsg, 1)

# 6. Add JS helper functions before closing script
js_helpers = """
    // ============================================================
    // PAYMENT GATE & ENROLLMENT LOGIC
    // ============================================================
    function initPaymentGate(user) {
      if (!user) return;
      const waProofMsg = encodeURIComponent(`Hello Coach Hyela,\\n\\nI have registered on your website and already paid for my course:\\n- Student Name: ${user.fullName}\\n- Registered Email: ${user.email}\\n\\nPlease verify my payment and approve my Certificate and VIP Access.`);
      const proofBtn = document.getElementById('btnWhatsAppPaymentProof');
      if (proofBtn) proofBtn.href = `https://wa.me/2349159637287?text=${waProofMsg}`;

      setPaymentGateChoice('YES');
    }

    function setPaymentGateChoice(choice) {
      const panelYes = document.getElementById('panelPaidYes');
      const panelNo = document.getElementById('panelPaidNo');
      const btnYes = document.getElementById('btnPaidYes');
      const btnNo = document.getElementById('btnPaidNo');
      if (!panelYes || !panelNo) return;

      if (choice === 'YES') {
        panelYes.style.display = 'block';
        panelNo.style.display = 'none';
        btnYes.className = 'cht-btn cht-btn-primary';
        btnNo.className = 'cht-btn cht-btn-outline';
        btnNo.style.borderColor = 'var(--cht-gold-500)';
        btnNo.style.color = 'var(--cht-gold-light)';
      } else {
        panelYes.style.display = 'none';
        panelNo.style.display = 'block';
        btnYes.className = 'cht-btn cht-btn-outline';
        btnNo.className = 'cht-btn cht-btn-primary';
        btnNo.style.borderColor = '';
        btnNo.style.color = '';
        selectPaymentTier('VIP_BUNDLE', 2500);
      }
    }

    function selectPaymentTier(tier, amount) {
      const authUser = CHT.getAuthLearner();
      const banner = document.getElementById('selectedTierBanner');
      const btnWa = document.getElementById('btnSubmitPaymentReceiptWa');
      const tierName = tier === 'VIP_BUNDLE' ? 'Complete VIP Access Bundle (₦2,500)' : 'Official Certificate Only (₦500)';

      if (banner) {
        banner.innerHTML = `<span style="color:var(--cht-gold-light);">Selected:</span> <strong>${tierName}</strong>`;
      }

      if (btnWa) {
        const studentInfo = authUser ? `${authUser.fullName} (${authUser.email})` : 'Student';
        const msg = encodeURIComponent(`Hello Coach Hyela,\\n\\nI am transferring payment for my course package:\\n- Selected Package: ${tierName}\\n- Amount: ₦${amount.toLocaleString()}\\n- Student: ${studentInfo}\\n- Beneficiary Name: EL JOSHUA HYELAKURI EMMANUEL\\n- Bank: PalmPay\\n\\nAttached is my payment proof screenshot for immediate activation.`);
        btnWa.href = `https://wa.me/2349159637287?text=${msg}`;
      }

      const modalTierSelect = document.getElementById('reqPackageTier');
      if (modalTierSelect) {
        modalTierSelect.value = tier;
      }

      const box = document.getElementById('paymentInstructionsBox');
      if (box) {
        box.scrollIntoView({ behavior: 'smooth' });
      }
    }

    function copyAccountNumber(accNum, btn) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(accNum).then(() => {
          const orig = btn.textContent;
          btn.textContent = 'Copied ✓';
          btn.style.background = 'var(--cht-success)';
          btn.style.color = '#000';
          setTimeout(() => {
            btn.textContent = orig;
            btn.style.background = '';
            btn.style.color = '';
          }, 2000);
        });
      } else {
        const ta = document.createElement('textarea');
        ta.value = accNum;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        btn.textContent = 'Copied ✓';
        setTimeout(() => { btn.textContent = 'Copy'; }, 2000);
      }
    }
"""

target_end_script = "  </script>\n</body>"
assert target_end_script in html, "Could not find target_end_script in certificates.html"
html = html.replace(target_end_script, js_helpers + target_end_script, 1)

# 7. Update renderStudentEligibility to display package tier badge
target_card_course = """            <h4 style="color: #fff; font-size: 1.15rem; margin-bottom: 4px;">${req.courseTitle}</h4>"""
new_card_course = """            <h4 style="color: #fff; font-size: 1.15rem; margin-bottom: 4px;">${req.courseTitle}</h4>
            <div style="margin-bottom: 8px;">
              ${req.packageTier === 'CERT_ONLY'
                ? '<span style="background:rgba(255,255,255,0.1); color:#fff; padding:2px 8px; border-radius:4px; font-size:0.75rem; font-weight:600;">🎓 Official Certificate Only (₦500)</span>'
                : '<span style="background:rgba(212,175,55,0.2); color:var(--cht-gold-light); padding:2px 8px; border-radius:4px; font-size:0.75rem; font-weight:700;">⭐ Complete VIP Package (₦2,500)</span>'}
            </div>"""

assert target_card_course in html, "Could not find target_card_course in certificates.html"
html = html.replace(target_card_course, new_card_course, 1)

with open('certificates.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Successfully patched certificates.html")
