# scripts/patch_admin_full_analytics.py
with open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Firebase SDKs in head
head_firebase = """  <!-- Firebase SDKs for Real-time Cloud Synchronization -->
  <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore-compat.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>"""

if 'firebase-firestore-compat.js' not in html:
    html = html.replace('<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>', head_firebase)
    print("Added Firebase SDKs to admin.html head")

# 2. Add Executive KPI Metrics Cards Bar
metrics_bar_html = """        <!-- EXECUTIVE KPI METRICS BAR -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; margin-bottom: 24px;">
          <!-- Metric 1: Total Page Views -->
          <div style="background: #081B11; border: 1px solid var(--cht-border-subtle); border-radius: var(--cht-radius-md); padding: 18px 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--cht-text-muted); font-weight: 700;">Total Website Views</span>
              <span style="font-size: 1.2rem;">👁️</span>
            </div>
            <div id="metricPageViews" style="font-size: 2rem; font-weight: 800; color: #fff; font-family: 'Cinzel', serif;">0</div>
            <div style="font-size: 0.75rem; color: #86EFAC; margin-top: 4px; display: flex; align-items: center; gap: 4px;">
              <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #22C55E;"></span>
              Live visitor tracking active
            </div>
          </div>

          <!-- Metric 2: Unique Visitors -->
          <div style="background: #081B11; border: 1px solid var(--cht-border-subtle); border-radius: var(--cht-radius-md); padding: 18px 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--cht-text-muted); font-weight: 700;">Unique Visitors</span>
              <span style="font-size: 1.2rem;">👥</span>
            </div>
            <div id="metricUniqueVisitors" style="font-size: 2rem; font-weight: 800; color: var(--cht-gold-light); font-family: 'Cinzel', serif;">0</div>
            <div style="font-size: 0.75rem; color: var(--cht-text-muted); margin-top: 4px;">Across mobile &amp; desktop</div>
          </div>

          <!-- Metric 3: Student Applications -->
          <div style="background: #081B11; border: 1px solid var(--cht-border-subtle); border-radius: var(--cht-radius-md); padding: 18px 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--cht-text-muted); font-weight: 700;">Student Applications</span>
              <span style="font-size: 1.2rem;">🎓</span>
            </div>
            <div style="display: flex; align-items: baseline; gap: 8px;">
              <div id="metricTotalApps" style="font-size: 2rem; font-weight: 800; color: #fff; font-family: 'Cinzel', serif;">0</div>
              <span id="metricPendingPill" class="status-pill pending" style="font-size: 0.7rem;">0 Pending</span>
            </div>
            <div style="font-size: 0.75rem; color: var(--cht-text-muted); margin-top: 4px;">Certificate claims submitted</div>
          </div>

          <!-- Metric 4: CAC Registrations -->
          <div style="background: #081B11; border: 1px solid var(--cht-border-subtle); border-radius: var(--cht-radius-md); padding: 18px 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--cht-text-muted); font-weight: 700;">CAC Registrations</span>
              <span style="font-size: 1.2rem;">🏛️</span>
            </div>
            <div id="metricTotalCAC" style="font-size: 2rem; font-weight: 800; color: #fff; font-family: 'Cinzel', serif;">0</div>
            <div style="font-size: 0.75rem; color: var(--cht-text-muted); margin-top: 4px;">Corporate filings submitted</div>
          </div>

          <!-- Metric 5: Cloud Status -->
          <div style="background: #081B11; border: 1px solid var(--cht-border-subtle); border-radius: var(--cht-radius-md); padding: 18px 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--cht-text-muted); font-weight: 700;">Sync Network</span>
              <span style="font-size: 1.2rem;">⚡</span>
            </div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #86EFAC; margin-top: 4px; display: flex; align-items: center; gap: 8px;">
              <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #22C55E; box-shadow: 0 0 10px #22C55E;"></span>
              Cloud Live
            </div>
            <div id="metricLastSync" style="font-size: 0.75rem; color: var(--cht-text-muted); margin-top: 6px;">Real-time Firestore active</div>
          </div>
        </div>
"""

target_header_end = """            <button type="button" class="cht-btn cht-btn-outline cht-btn-sm" onclick="logoutAdminSession()">
              Sign out
            </button>
          </div>
        </div>"""

if 'EXECUTIVE KPI METRICS BAR' not in html and target_header_end in html:
    html = html.replace(target_header_end, target_header_end + "\n\n" + metrics_bar_html)
    print("Added Executive KPI Metrics Bar")

# 3. Add Analytics Tab Button
target_tab_buttons = """          <button type="button" class="admin-tab-btn" id="tabBtnLiveContent" onclick="switchAdminTab('liveContent')" style="background: rgba(212, 175, 55, 0.12); border-color: var(--cht-gold-500); color: var(--cht-gold-light);">
            <span style="color: var(--cht-gold-light);">&#9998;</span> Live Website Content Editor
          </button>"""

analytics_tab_btn = """          <button type="button" class="admin-tab-btn" id="tabBtnLiveContent" onclick="switchAdminTab('liveContent')" style="background: rgba(212, 175, 55, 0.12); border-color: var(--cht-gold-500); color: var(--cht-gold-light);">
            <span style="color: var(--cht-gold-light);">&#9998;</span> Live Website Content Editor
          </button>
          <button type="button" class="admin-tab-btn" id="tabBtnAnalytics" onclick="switchAdminTab('analytics')">
            📊 Live Visitor Analytics &amp; Activity
          </button>"""

if 'tabBtnAnalytics' not in html and target_tab_buttons in html:
    html = html.replace(target_tab_buttons, analytics_tab_btn)
    print("Added Analytics tab button")

# 4. Add "+ Manually Add Student Application" in Tab 1
target_refresh_btn = """            <button type="button" class="cht-btn cht-btn-outline cht-btn-sm" onclick="renderAdminEligibility()">
              Refresh Requests
            </button>"""

new_refresh_btns = """            <div style="display: flex; gap: 8px;">
              <button type="button" class="cht-btn cht-btn-primary cht-btn-sm" onclick="openManualAddAppModal()">
                + Manually Add Student Application
              </button>
              <button type="button" class="cht-btn cht-btn-outline cht-btn-sm" onclick="renderAdminEligibility()">
                Refresh Requests
              </button>
            </div>"""

if target_refresh_btn in html and 'openManualAddAppModal()' not in html:
    html = html.replace(target_refresh_btn, new_refresh_btns)
    print("Added Manual Add button in Tab 1")

# 5. Add Tab 7 (tabContentAnalytics)
tab_analytics_content = """
        <!-- ========================================== -->
        <!-- TAB 7: VISITOR ANALYTICS & ACTIVITY STREAM -->
        <!-- ========================================== -->
        <div id="tabContentAnalytics" style="display: none;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 12px;">
            <div>
              <h2 class="heading-serif" style="color: #fff; font-size: 1.35rem;">Live Visitor Analytics &amp; Activity Stream</h2>
              <p style="color: var(--cht-text-muted); font-size: 0.85rem;">Real-time feed of visitor interactions, student logins, course applications, and administrative actions.</p>
            </div>
            <button type="button" class="cht-btn cht-btn-outline cht-btn-sm" onclick="renderAdminAnalytics()">
              Refresh Stream
            </button>
          </div>

          <div class="cht-table-responsive">
            <table class="cht-admin-table">
              <thead>
                <tr>
                  <th style="width: 170px;">Timestamp</th>
                  <th style="width: 140px;">Activity Type</th>
                  <th>Page / Source</th>
                  <th style="width: 110px;">Device</th>
                  <th>Action Details</th>
                </tr>
              </thead>
              <tbody id="tableBodyActivityStream">
                <tr><td colspan="5" style="text-align:center; padding:24px; color:var(--cht-text-muted);">Listening for real-time visitor activity...</td></tr>
              </tbody>
            </table>
          </div>
        </div>
"""

target_before_admin_console_close = """              </div>

            </div>
          </div>
        </div>

      </div>"""

if 'tabContentAnalytics' not in html and target_before_admin_console_close in html:
    html = html.replace(target_before_admin_console_close, """              </div>

            </div>
          </div>
        </div>""" + tab_analytics_content + "\n      </div>")
    print("Added tabContentAnalytics")

# 6. Add Modal for Manually Adding Student Application
manual_modal_html = """
  <!-- MODAL: MANUALLY ADD STUDENT APPLICATION -->
  <div class="cht-modal-overlay" id="modalManualAddApp">
    <div class="cht-modal-card" style="max-width: 540px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid var(--cht-border-subtle); padding-bottom: 10px;">
        <h3 class="heading-serif" style="color: #fff; font-size: 1.3rem;">Manually Record Student Application</h3>
        <button type="button" onclick="closeManualAddAppModal()" style="background: none; border: none; color: #fff; font-size: 1.4rem; cursor: pointer;">✕</button>
      </div>

      <p style="color: var(--cht-text-muted); font-size: 0.85rem; line-height: 1.5; margin-bottom: 16px;">
        Use this form to immediately record a student application (e.g. from a WhatsApp screenshot or previous session). The record will sync straight to Google Cloud Firestore.
      </p>

      <form onsubmit="handleManualAddAppSubmit(event)">
        <div class="cht-form-group">
          <label class="cht-label" for="manualAppName">Student Full Legal Name <span class="req">*</span></label>
          <input type="text" id="manualAppName" class="cht-input" placeholder="e.g. Bilkisu Danjuma" required>
        </div>

        <div class="cht-form-group">
          <label class="cht-label" for="manualAppEmail">Student Email Address <span class="req">*</span></label>
          <input type="email" id="manualAppEmail" class="cht-input" placeholder="e.g. student@example.com" required>
        </div>

        <div class="cht-form-group">
          <label class="cht-label" for="manualAppCourse">Course Programme <span class="req">*</span></label>
          <select id="manualAppCourse" class="cht-select" required>
            <option value="ai-video-ugc|AI Video Creation & UGC-Style Advertising">AI Video Creation &amp; UGC-Style Advertising</option>
            <option value="website-building|Modern Website Building & Digital Presence">Modern Website Building &amp; Digital Presence</option>
            <option value="ai-digital-skills|Artificial Intelligence & Creative Workflows for Individuals">Artificial Intelligence &amp; Creative Workflows</option>
            <option value="corporate-ict|Executive Corporate Training & Digital Operations">Executive Corporate Training &amp; Digital Operations</option>
            <option value="graphics-branding|Commercial Smartphone Graphic Design & Brand Identity">Commercial Smartphone Graphic Design &amp; Brand Identity</option>
            <option value="social-media-growth|Social Media Strategy & Organic Lead Generation">Social Media Strategy &amp; Organic Lead Generation</option>
          </select>
        </div>

        <div class="cht-form-group">
          <label class="cht-label" for="manualAppStatus">Initial Status <span class="req">*</span></label>
          <select id="manualAppStatus" class="cht-select" required>
            <option value="PENDING">PENDING (Awaiting evaluation)</option>
            <option value="APPROVED">APPROVED (Issue certificate immediately)</option>
          </select>
        </div>

        <div class="cht-form-group">
          <label class="cht-label" for="manualAppNotes">Instructor Evaluation Notes</label>
          <textarea id="manualAppNotes" class="cht-textarea" style="min-height: 70px;" placeholder="e.g. Verified via WhatsApp capstone submission."></textarea>
        </div>

        <div style="display: flex; justify-content: flex-end; gap: 12px; margin-top: 20px;">
          <button type="button" class="cht-btn cht-btn-outline" onclick="closeManualAddAppModal()">Cancel</button>
          <button type="submit" class="cht-btn cht-btn-primary" id="btnSubmitManualApp">Save &amp; Sync to Cloud</button>
        </div>
      </form>
    </div>
  </div>
"""

if 'modalManualAddApp' not in html:
    html = html.replace('<!-- MoDAL: REVIEW ELIGIBILITY REQUEST -->', manual_modal_html + '\n  <!-- MoDAL: REVIEW ELIGIBILITY REQUEST -->')
    print("Added modalManualAddApp")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("admin.html structural patch completed!")
