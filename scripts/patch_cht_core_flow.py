# Patch cht-core.js to add setFlowStatus and update setMuseAiStatus and updateStudentDetails

with open('js/cht-core.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update updateStudentDetails
old_update_details = """    if (updatedData.fullName) user.fullName = updatedData.fullName.trim();
    if (updatedData.driveAccess !== undefined) user.driveAccess = !!updatedData.driveAccess;
    if (updatedData.assignedCourses) user.assignedCourses = updatedData.assignedCourses;

    saveUsers(users);"""

new_update_details = """    if (updatedData.fullName) user.fullName = updatedData.fullName.trim();
    if (updatedData.driveAccess !== undefined) user.driveAccess = !!updatedData.driveAccess;
    if (updatedData.assignedCourses) user.assignedCourses = updatedData.assignedCourses;
    if (updatedData.flowAccessed !== undefined) {
      user.flowAccessed = !!updatedData.flowAccessed;
      user.googleAiProAccessed = !!updatedData.flowAccessed;
    }
    if (updatedData.museAiPaid !== undefined) {
      user.museAiPaid = !!updatedData.museAiPaid;
    }

    saveUsers(users);

    const db = getFirestore();
    if (db && userId) {
      try {
        const firestoreUpdate = {
          fullName: user.fullName,
          driveAccess: !!user.driveAccess
        };
        if (updatedData.flowAccessed !== undefined) {
          firestoreUpdate.flowAccessed = !!updatedData.flowAccessed;
          firestoreUpdate.googleAiProAccessed = !!updatedData.flowAccessed;
        }
        if (updatedData.museAiPaid !== undefined) {
          firestoreUpdate.museAiPaid = !!updatedData.museAiPaid;
        }
        db.collection('students').doc(userId).set(firestoreUpdate, { merge: true });
      } catch(e) {
        console.error('Failed to sync student update to Firestore:', e);
      }
    }"""

if old_update_details in code:
    code = code.replace(old_update_details, new_update_details, 1)
    print("[OK] Patched updateStudentDetails")
else:
    print("Could not find old_update_details")

# 2. Add setFlowStatus and update setMuseAiStatus
old_muse_fn = """  async function setMuseAiStatus(userId, accessed, whatsappNum = '') {
    const db = getFirestore();
    if (db && userId) {
      try {
        const updateData = {
          museAiAccessed: !!accessed
        };
        if (whatsappNum) {
          updateData.museAiWhatsApp = whatsappNum.trim();
        }
        await db.collection('students').doc(userId).set(updateData, { merge: true });
        return { success: true };
      } catch(e) {
        return { success: false, message: e.message };
      }
    }
    return { success: false };
  }
  const setGoogleAiProStatus = setMuseAiStatus;"""

new_muse_fn = """  async function setFlowStatus(userId, accessed) {
    const db = getFirestore();
    const updateData = {
      flowAccessed: !!accessed,
      googleAiProAccessed: !!accessed
    };
    if (db && userId) {
      try {
        await db.collection('students').doc(userId).set(updateData, { merge: true });
      } catch(e) {
        console.error('Error updating flow status in Firestore:', e);
      }
    }
    const users = getUsers();
    const user = users.find(u => u.id === userId);
    if (user) {
      user.flowAccessed = !!accessed;
      user.googleAiProAccessed = !!accessed;
      saveUsers(users);
    }
    return { success: true };
  }

  async function setMuseAiStatus(userId, accessed, isPaid = false) {
    const db = getFirestore();
    const updateData = {
      museAiAccessed: !!accessed,
      museAiPaid: !!isPaid
    };
    if (db && userId) {
      try {
        await db.collection('students').doc(userId).set(updateData, { merge: true });
      } catch(e) {
        console.error('Error updating museAi status in Firestore:', e);
      }
    }
    const users = getUsers();
    const user = users.find(u => u.id === userId);
    if (user) {
      user.museAiAccessed = !!accessed;
      user.museAiPaid = !!isPaid;
      saveUsers(users);
    }
    return { success: true };
  }
  const setGoogleAiProStatus = setFlowStatus;"""

if old_muse_fn in code:
    code = code.replace(old_muse_fn, new_muse_fn, 1)
    print("[OK] Patched setFlowStatus and setMuseAiStatus")
else:
    print("Could not find old_muse_fn")

# 3. Export setFlowStatus
if 'setMuseAiStatus,' in code and 'setFlowStatus,' not in code:
    code = code.replace('setMuseAiStatus,', 'setFlowStatus,\n    setMuseAiStatus,', 1)
    print("[OK] Exported setFlowStatus in window.CHT")

with open('js/cht-core.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Done patching js/cht-core.js")
