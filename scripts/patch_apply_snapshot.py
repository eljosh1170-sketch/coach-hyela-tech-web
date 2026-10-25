DRIVE_LINK = 'https://drive.google.com/drive/folders/1_0uldj8-IFcWQxRa4PuFRFVgCRDeSNDJ?usp=drive_link'

with open('admin.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = "if (document.getElementById('liveEditorC3Desc')) document.getElementById('liveEditorC3Desc').value = data.c3Desc || '';"
repl = target + f"\n      if (document.getElementById('liveEditorMasterDriveUrl')) document.getElementById('liveEditorMasterDriveUrl').value = data.masterDriveUrl || '{DRIVE_LINK}';"

if target in c:
    c = c.replace(target, repl)
    with open('admin.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print('Updated applySnapshotToLiveForm in admin.html')
