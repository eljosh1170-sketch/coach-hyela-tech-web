# scripts/patch_admin_drive_editor.py
DRIVE_LINK = "https://drive.google.com/drive/folders/1_0uldj8-IFcWQxRa4PuFRFVgCRDeSNDJ?usp=drive_link"

# 1. Update DEFAULT_LIVE_CONTENT in js/cht-core.js
with open('js/cht-core.js', 'r', encoding='utf-8') as f:
    core_js = f.read()

if 'masterDriveUrl:' not in core_js:
    core_js = core_js.replace(
        'c3Desc: "Comprehensive curriculum covering modern practical workflows for creative professionals."',
        f'c3Desc: "Comprehensive curriculum covering modern practical workflows for creative professionals.",\n    masterDriveUrl: "{DRIVE_LINK}"'
    )
    print("Added masterDriveUrl to DEFAULT_LIVE_CONTENT in cht-core.js")

with open('js/cht-core.js', 'w', encoding='utf-8') as f:
    f.write(core_js)

# 2. Update admin.html form and handlers
with open('admin.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

drive_input_html = """                <div class="cht-form-group">
                  <label class="cht-label" for="liveEditorMasterDriveUrl">VIP Master Prompts Google Drive Folder Link</label>
                  <input type="url" id="liveEditorMasterDriveUrl" class="cht-input live-trackable" oninput="onLiveFieldInput()" placeholder="https://drive.google.com/drive/folders/...">
                  <div class="cht-help-text">Live Google Drive link unlocked automatically for approved VIP candidates.</div>
                </div>"""

target_email_group = """                <div class="cht-form-group">
                  <label class="cht-label" for="liveEditorEmail">Official Contact Email</label>
                  <input type="email" id="liveEditorEmail" class="cht-input live-trackable" oninput="onLiveFieldInput()">
                </div>"""

if target_email_group in admin_html and 'liveEditorMasterDriveUrl' not in admin_html:
    admin_html = admin_html.replace(target_email_group, target_email_group + "\n" + drive_input_html)
    print("Added drive link input to admin.html form")

# In getLiveFormSnapshot:
if 'masterDriveUrl:' not in admin_html:
    admin_html = admin_html.replace(
        "c3Desc: document.getElementById('liveEditorC3Desc') ? document.getElementById('liveEditorC3Desc').value : ''",
        "c3Desc: document.getElementById('liveEditorC3Desc') ? document.getElementById('liveEditorC3Desc').value : '',\n        masterDriveUrl: document.getElementById('liveEditorMasterDriveUrl') ? document.getElementById('liveEditorMasterDriveUrl').value : ''"
    )
    print("Added masterDriveUrl to getLiveFormSnapshot")

# In applySnapshotToLiveForm:
if "document.getElementById('liveEditorMasterDriveUrl')" not in admin_html:
    admin_html = admin_html.replace(
        "if (document.getElementById('liveEditorC3Desc')) document.getElementById('liveEditorC3Desc').value = data.c3Desc || '';",
        "if (document.getElementById('liveEditorC3Desc')) document.getElementById('liveEditorC3Desc').value = data.c3Desc || '';\n      if (document.getElementById('liveEditorMasterDriveUrl')) document.getElementById('liveEditorMasterDriveUrl').value = data.masterDriveUrl || '';"
    )
    print("Added masterDriveUrl to applySnapshotToLiveForm")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_html)

print("Admin Drive editor patched successfully!")
