import re

with open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

live_content_html = '''          </div>
        </div>

        <!-- ========================================== -->
        <!-- TAB 6: LIVE WEBSITE CONTENT EDITOR & UNDO  -->
        <!-- ========================================== -->
        <div id="tabContentLiveContent" style="display: none;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 14px;">
            <div>
              <span class="status-pill approved" style="margin-bottom: 6px;">Live In-Browser Visual CMS</span>
              <h2 class="heading-serif" style="color: #fff; font-size: 1.35rem; margin-top: 4px;">Live Website Content Editor</h2>
              <p style="color: var(--cht-text-muted); font-size: 0.85rem;">Modify slogans, contact info, PalmPay details, pricing, and curriculum text with instant Undo &amp; Redo capability.</p>
            </div>
            
            <!-- UNDO / REDO / ACTION TOOLBAR -->
            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
              <button type="button" id="btnUndoLive" class="cht-btn cht-btn-outline cht-btn-sm" onclick="handleUndoLiveContent()" disabled style="opacity: 0.4; cursor: not-allowed; display: inline-flex; align-items: center; gap: 6px;" title="Undo previous edit (Ctrl+Z)">
                <span>↺</span> <strong>Undo</strong> <span id="undoCountBadge" style="font-size: 0.75rem; color: var(--cht-gold-light);">(0)</span>
              </button>
              <button type="button" id="btnRedoLive" class="cht-btn cht-btn-outline cht-btn-sm" onclick="handleRedoLiveContent()" disabled style="opacity: 0.4; cursor: not-allowed; display: inline-flex; align-items: center; gap: 6px;" title="Redo undone edit (Ctrl+Y)">
                <span>↻</span> <strong>Redo</strong> <span id="redoCountBadge" style="font-size: 0.75rem; color: var(--cht-gold-light);">(0)</span>
              </button>
              <button type="button" class="cht-btn cht-btn-primary cht-btn-sm" onclick="handleSaveLiveContent()">
                ✓ Save Live Changes
              </button>
              <button type="button" class="cht-btn cht-btn-outline cht-btn-sm" onclick="exportContentJSON()" title="Export updated content as a JSON file">
                ⤓ Export JSON
              </button>
              <button type="button" class="cht-btn cht-btn-outline cht-btn-sm" style="border-color: #EF4444; color: #FCA5A5;" onclick="handleResetLiveContent()">
                Reset Defaults
              </button>
            </div>
          </div>

          <!-- Alert Banner -->
          <div id="liveAlertBanner" style="display: none; padding: 12px 16px; border-radius: var(--cht-radius-md); font-size: 0.88rem; margin-bottom: 20px; font-weight: 500;"></div>

          <div style="background: #081B11; border: 1px solid var(--cht-border-subtle); border-radius: var(--cht-radius-md); padding: 24px; margin-bottom: 30px;">
            <div class="cht-grid cht-grid-2" style="gap: 20px;">
              
              <!-- Section 1: Brand & Slogan -->
              <div style="background: rgba(0,0,0,0.25); padding: 20px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
                <h3 class="heading-serif" style="color: var(--cht-gold-light); font-size: 1.05rem; margin-bottom: 14px; border-bottom: 1px solid var(--cht-border-subtle); padding-bottom: 8px;">
                  1. Brand Header &amp; Contact Info
                </h3>
                <div class="cht-form-group">
                  <label class="cht-label" for="liveEditorSlogan">Brand Slogan / Tagline</label>
                  <input type="text" id="liveEditorSlogan" class="cht-input live-trackable" oninput="onLiveFieldInput()">
                </div>
                <div class="cht-form-group">
                  <label class="cht-label" for="liveEditorPhone">Official Phone Number</label>
                  <input type="text" id="liveEditorPhone" class="cht-input live-trackable" oninput="onLiveFieldInput()">
                </div>
                <div class="cht-form-group">
                  <label class="cht-label" for="liveEditorEmail">Official Contact Email</label>
                  <input type="email" id="liveEditorEmail" class="cht-input live-trackable" oninput="onLiveFieldInput()">
                </div>
              </div>

              <!-- Section 2: PalmPay Account Details -->
              <div style="background: rgba(0,0,0,0.25); padding: 20px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
                <h3 class="heading-serif" style="color: var(--cht-gold-light); font-size: 1.05rem; margin-bottom: 14px; border-bottom: 1px solid var(--cht-border-subtle); padding-bottom: 8px;">
                  2. Official Payment Details (PalmPay)
                </h3>
                <div class="cht-form-group">
                  <label class="cht-label" for="liveEditorBankName">Bank / Financial Institution</label>
                  <input type="text" id="liveEditorBankName" class="cht-input live-trackable" oninput="onLiveFieldInput()">
                </div>
                <div class="cht-form-group">
                  <label class="cht-label" for="liveEditorAccNum">PalmPay Account Number</label>
                  <input type="text" id="liveEditorAccNum" class="cht-input live-trackable" oninput="onLiveFieldInput()">
                </div>
                <div class="cht-form-group">
                  <label class="cht-label" for="liveEditorAccName">Beneficiary Account Name</label>
                  <input type="text" id="liveEditorAccName" class="cht-input live-trackable" oninput="onLiveFieldInput()">
                </div>
              </div>

              <!-- Section 3: Training Cohort & Announcement -->
              <div style="background: rgba(0,0,0,0.25); padding: 20px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
                <h3 class="heading-serif" style="color: var(--cht-gold-light); font-size: 1.05rem; margin-bottom: 14px; border-bottom: 1px solid var(--cht-border-subtle); padding-bottom: 8px;">
                  3. Cohort Schedule &amp; Announcements
                </h3>
                <div class="cht-form-group">
                  <label class="cht-label" for="liveEditorCohortMonth">Upcoming Cohort Month</label>
                  <input type="text" id="liveEditorCohortMonth" class="cht-input live-trackable" oninput="onLiveFieldInput()">
                </div>
                <div class="cht-form-group">
                  <label class="cht-label" for="liveEditorTickerText">Marquee Announcement Bar Text</label>
                  <input type="text" id="liveEditorTickerText" class="cht-input live-trackable" oninput="onLiveFieldInput()">
                </div>
                <div class="cht-form-group">
                  <label class="cht-label" for="liveEditorPricingNotice">General Admission Notice</label>
                  <input type="text" id="liveEditorPricingNotice" class="cht-input live-trackable" oninput="onLiveFieldInput()">
                </div>
              </div>

              <!-- Section 4: AI Website Track (Zero Coding) -->
              <div style="background: rgba(0,0,0,0.25); padding: 20px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
                <h3 class="heading-serif" style="color: var(--cht-gold-light); font-size: 1.05rem; margin-bottom: 14px; border-bottom: 1px solid var(--cht-border-subtle); padding-bottom: 8px;">
                  4. Website Building Programme (100% AI &amp; Zero Coding)
                </h3>
                <div class="cht-form-group">
                  <label class="cht-label" for="liveEditorC3Title">Course Track Headline</label>
                  <input type="text" id="liveEditorC3Title" class="cht-input live-trackable" oninput="onLiveFieldInput()">
                </div>
                <div class="cht-form-group">
                  <label class="cht-label" for="liveEditorC3Desc">Curriculum Syllabus Description</label>
                  <textarea id="liveEditorC3Desc" class="cht-textarea live-trackable" style="min-height: 100px;" oninput="onLiveFieldInput()"></textarea>
                </div>
              </div>

            </div>
          </div>
        </div>'''

# Target insertion before the closing </div> of adminConsole
target_str = '          </div>\n        </div>\n\n      </div>'
if target_str not in html:
    target_str = '          </div>\r\n        </div>\r\n\r\n      </div>'

if target_str in html:
    html = html.replace(target_str, live_content_html + '\n\n      </div>')
    print('Successfully inserted live content markup into admin.html')
else:
    print('Target string not found!')

# Now update the JavaScript functions in admin.html
old_js_start = '    function renderLiveContentEditor() {'
old_js_end = '    function capitalize(str) {'

new_js = '''    // ==========================================
    // LIVE CONTENT EDITOR WITH UNDO / REDO ENGINE
    // ==========================================
    let liveHistory = [];
    let liveHistoryIndex = -1;
    let liveInputDebounceTimer = null;

    function getLiveFormSnapshot() {
      return {
        slogan: document.getElementById('liveEditorSlogan') ? document.getElementById('liveEditorSlogan').value : '',
        phone: document.getElementById('liveEditorPhone') ? document.getElementById('liveEditorPhone').value : '',
        email: document.getElementById('liveEditorEmail') ? document.getElementById('liveEditorEmail').value : '',
        bankName: document.getElementById('liveEditorBankName') ? document.getElementById('liveEditorBankName').value : '',
        accountNumber: document.getElementById('liveEditorAccNum') ? document.getElementById('liveEditorAccNum').value : '',
        accountName: document.getElementById('liveEditorAccName') ? document.getElementById('liveEditorAccName').value : '',
        cohortMonth: document.getElementById('liveEditorCohortMonth') ? document.getElementById('liveEditorCohortMonth').value : '',
        tickerText: document.getElementById('liveEditorTickerText') ? document.getElementById('liveEditorTickerText').value : '',
        pricingNotice: document.getElementById('liveEditorPricingNotice') ? document.getElementById('liveEditorPricingNotice').value : '',
        c3Title: document.getElementById('liveEditorC3Title') ? document.getElementById('liveEditorC3Title').value : '',
        c3Desc: document.getElementById('liveEditorC3Desc') ? document.getElementById('liveEditorC3Desc').value : ''
      };
    }

    function applySnapshotToLiveForm(data) {
      if (!data) return;
      if (document.getElementById('liveEditorSlogan')) document.getElementById('liveEditorSlogan').value = data.slogan || '';
      if (document.getElementById('liveEditorPhone')) document.getElementById('liveEditorPhone').value = data.phone || '';
      if (document.getElementById('liveEditorEmail')) document.getElementById('liveEditorEmail').value = data.email || '';
      if (document.getElementById('liveEditorBankName')) document.getElementById('liveEditorBankName').value = data.bankName || '';
      if (document.getElementById('liveEditorAccNum')) document.getElementById('liveEditorAccNum').value = data.accountNumber || '';
      if (document.getElementById('liveEditorAccName')) document.getElementById('liveEditorAccName').value = data.accountName || '';
      if (document.getElementById('liveEditorCohortMonth')) document.getElementById('liveEditorCohortMonth').value = data.cohortMonth || '';
      if (document.getElementById('liveEditorTickerText')) document.getElementById('liveEditorTickerText').value = data.tickerText || '';
      if (document.getElementById('liveEditorPricingNotice')) document.getElementById('liveEditorPricingNotice').value = data.pricingNotice || '';
      if (document.getElementById('liveEditorC3Title')) document.getElementById('liveEditorC3Title').value = data.c3Title || '';
      if (document.getElementById('liveEditorC3Desc')) document.getElementById('liveEditorC3Desc').value = data.c3Desc || '';
    }

    function renderLiveContentEditor() {
      const data = CHT.getLiveContent();
      applySnapshotToLiveForm(data);

      if (liveHistory.length === 0) {
        liveHistory = [JSON.parse(JSON.stringify(data))];
        liveHistoryIndex = 0;
      }
      updateUndoRedoButtons();
    }

    function onLiveFieldInput() {
      clearTimeout(liveInputDebounceTimer);
      liveInputDebounceTimer = setTimeout(() => {
        const currentSnapshot = getLiveFormSnapshot();
        const prevSnapshot = liveHistory[liveHistoryIndex];

        if (!prevSnapshot || JSON.stringify(currentSnapshot) !== JSON.stringify(prevSnapshot)) {
          liveHistory = liveHistory.slice(0, liveHistoryIndex + 1);
          liveHistory.push(currentSnapshot);
          liveHistoryIndex = liveHistory.length - 1;
          updateUndoRedoButtons();
          CHT.saveLiveContent(currentSnapshot);
        }
      }, 350);
    }

    function handleUndoLiveContent() {
      if (liveHistoryIndex > 0) {
        liveHistoryIndex--;
        const snapshot = liveHistory[liveHistoryIndex];
        applySnapshotToLiveForm(snapshot);
        CHT.saveLiveContent(snapshot);
        updateUndoRedoButtons();
        showLiveAlert('↺ Undone: Reverted to step ' + (liveHistoryIndex + 1) + ' of ' + liveHistory.length, false);
      }
    }

    function handleRedoLiveContent() {
      if (liveHistoryIndex < liveHistory.length - 1) {
        liveHistoryIndex++;
        const snapshot = liveHistory[liveHistoryIndex];
        applySnapshotToLiveForm(snapshot);
        CHT.saveLiveContent(snapshot);
        updateUndoRedoButtons();
        showLiveAlert('↻ Redone: Restored step ' + (liveHistoryIndex + 1) + ' of ' + liveHistory.length, false);
      }
    }

    function updateUndoRedoButtons() {
      const btnUndo = document.getElementById('btnUndoLive');
      const btnRedo = document.getElementById('btnRedoLive');
      const undoBadge = document.getElementById('undoCountBadge');
      const redoBadge = document.getElementById('redoCountBadge');

      const canUndo = liveHistoryIndex > 0;
      const canRedo = liveHistoryIndex < liveHistory.length - 1;

      if (btnUndo) {
        btnUndo.disabled = !canUndo;
        btnUndo.style.opacity = canUndo ? '1' : '0.4';
        btnUndo.style.cursor = canUndo ? 'pointer' : 'not-allowed';
      }
      if (btnRedo) {
        btnRedo.disabled = !canRedo;
        btnRedo.style.opacity = canRedo ? '1' : '0.4';
        btnRedo.style.cursor = canRedo ? 'pointer' : 'not-allowed';
      }
      if (undoBadge) undoBadge.textContent = '(' + liveHistoryIndex + ')';
      const remainingRedos = liveHistory.length - 1 - liveHistoryIndex;
      if (redoBadge) redoBadge.textContent = '(' + (remainingRedos > 0 ? remainingRedos : 0) + ')';
    }

    function handleSaveLiveContent() {
      const snapshot = getLiveFormSnapshot();
      const res = CHT.saveLiveContent(snapshot);
      
      // Also register into history if changed
      const prevSnapshot = liveHistory[liveHistoryIndex];
      if (!prevSnapshot || JSON.stringify(snapshot) !== JSON.stringify(prevSnapshot)) {
        liveHistory = liveHistory.slice(0, liveHistoryIndex + 1);
        liveHistory.push(snapshot);
        liveHistoryIndex = liveHistory.length - 1;
        updateUndoRedoButtons();
      }
      showLiveAlert('✓ ' + res.message, false);
    }

    function handleResetLiveContent() {
      if (!confirm('Are you sure you want to reset all live content to system defaults?')) return;
      const res = CHT.resetLiveContent();
      renderLiveContentEditor();
      liveHistory = [JSON.parse(JSON.stringify(res.data))];
      liveHistoryIndex = 0;
      updateUndoRedoButtons();
      showLiveAlert(res.message, false);
    }

    function showLiveAlert(msg, isError) {
      const b = document.getElementById('liveAlertBanner');
      if (!b) return;
      b.style.display = 'block';
      b.style.background = isError ? 'rgba(239, 68, 68, 0.15)' : 'rgba(16, 185, 129, 0.15)';
      b.style.border = isError ? '1px solid #EF4444' : '1px solid #10B981';
      b.style.color = isError ? '#EF4444' : '#10B981';
      b.textContent = msg;
      setTimeout(() => { b.style.display = 'none'; }, 4000);
    }

    function exportContentJSON() {
      const data = CHT.getLiveContent();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'content-live.json';
      a.click();
      URL.revokeObjectURL(url);
    }

    // Keyboard Shortcuts: Ctrl+Z (Undo) and Ctrl+Y / Ctrl+Shift+Z (Redo)
    document.addEventListener('keydown', (e) => {
      const activeTab = document.getElementById('tabContentLiveContent');
      if (!activeTab || activeTab.style.display === 'none') return;

      if ((e.ctrlKey || e.metaKey) && (e.key === 'z' || e.key === 'Z')) {
        if (e.shiftKey) {
          e.preventDefault();
          handleRedoLiveContent();
        } else {
          e.preventDefault();
          handleUndoLiveContent();
        }
      } else if ((e.ctrlKey || e.metaKey) && (e.key === 'y' || e.key === 'Y')) {
        e.preventDefault();
        handleRedoLiveContent();
      }
    });

'''

if old_js_start in html and old_js_end in html:
    start_pos = html.find(old_js_start)
    end_pos = html.find(old_js_end)
    html = html[:start_pos] + new_js + html[end_pos:]
    print('Successfully updated JavaScript in admin.html')
else:
    print('JavaScript markers not found!')

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Finished updating admin.html')
