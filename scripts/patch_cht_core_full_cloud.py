# scripts/patch_cht_core_full_cloud.py
import re

with open('js/cht-core.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update subscribeVisitorStats to handle empty metrics doc gracefully
old_sub_stats = """  // Subscribe to Live Visitor Stats
  function subscribeVisitorStats(callback) {
    const db = getFirestore();
    if (db) {
      return db.collection('visitor_stats').doc('metrics')
        .onSnapshot(doc => {
          if (doc.exists) {
            callback(doc.data());
          }
        }, err => console.warn('[CHT Cloud] Stats error:', err));
    }
    return null;
  }"""

new_sub_stats = """  // Subscribe to Live Visitor Stats
  function subscribeVisitorStats(callback) {
    const db = getFirestore();
    if (db) {
      return db.collection('visitor_stats').doc('metrics')
        .onSnapshot(doc => {
          if (doc.exists) {
            callback(doc.data());
          } else {
            callback({ pageViews: 0, visitors: 0, lastActive: new Date().toISOString() });
          }
        }, err => {
          console.warn('[CHT Cloud] Stats error:', err);
          callback({ pageViews: 0, visitors: 0, lastActive: null });
        });
    }
    return null;
  }"""

if old_sub_stats in content:
    content = content.replace(old_sub_stats, new_sub_stats)
    print("Updated subscribeVisitorStats")

# 2. Add subscribeCloudStudents, saveStudentCloud, createEligibilityRequestCloud, subscribeCloudCAC, findCertificateByIdCloud
additional_cloud_helpers = """
  // Subscribe to Registered Students from Cloud Firestore
  function subscribeCloudStudents(callback) {
    const db = getFirestore();
    if (db) {
      return db.collection('students')
        .orderBy('registeredAt', 'desc')
        .onSnapshot(snapshot => {
          const cloudStudents = [];
          snapshot.forEach(doc => {
            const data = doc.data();
            data.id = doc.id;
            cloudStudents.push(data);
          });
          if (cloudStudents.length > 0) {
            const local = getUsers();
            const map = new Map();
            local.forEach(u => map.set(u.id || u.email, u));
            cloudStudents.forEach(u => map.set(u.id || u.email, u));
            saveUsers(Array.from(map.values()));
          }
          if (callback) callback(cloudStudents);
        }, err => {
          console.warn('[CHT Cloud] Students snapshot error:', err);
          if (callback) callback(getUsers());
        });
    } else {
      if (callback) callback(getUsers());
      return null;
    }
  }

  // Save Student directly to Cloud Firestore
  async function saveStudentCloud(studentData) {
    const db = getFirestore();
    if (db && studentData) {
      try {
        const id = studentData.id || ('USR-' + Date.now().toString(36).toUpperCase());
        studentData.id = id;
        await db.collection('students').doc(id).set(studentData, { merge: true });
        await db.collection('activity_logs').add({
          type: 'STUDENT_REGISTER',
          page: 'Student Portal',
          device: window.innerWidth <= 768 ? 'Mobile' : 'Desktop',
          details: `${studentData.fullName} (${studentData.email}) account registered`,
          timestamp: new Date().toISOString()
        });
        return { success: true, student: studentData };
      } catch (e) {
        console.warn('[CHT Cloud] Save student error:', e);
        return { success: false, message: e.message };
      }
    }
    return { success: false, message: 'Firestore unavailable' };
  }

  // Manually Create / Sync Eligibility Request from Admin Console to Cloud
  async function createEligibilityRequestCloud(reqData) {
    const db = getFirestore();
    const id = reqData.id || ('REQ-2026-' + Math.random().toString(36).substring(2, 6).toUpperCase());
    const newReq = {
      id: id,
      userId: reqData.userId || ('USR-' + Date.now().toString(36).substring(2, 7).toUpperCase()),
      fullName: reqData.fullName || 'Student',
      email: reqData.email ? reqData.email.trim().toLowerCase() : '',
      courseId: reqData.courseId || 'general',
      courseTitle: reqData.courseTitle || 'Training Course',
      submissionDate: reqData.submissionDate || new Date().toISOString(),
      status: reqData.status || 'PENDING',
      adminNotes: reqData.adminNotes || 'Manually entered / synced by Coach Hyela administration.',
      reviewedAt: reqData.status === 'APPROVED' ? new Date().toISOString() : null,
      certificateIssued: false,
      certificateCode: null
    };

    if (reqData.status === 'APPROVED') {
      const code = 'CHT-2026-' + Math.random().toString(36).substring(2, 6).toUpperCase();
      newReq.certificateIssued = true;
      newReq.certificateCode = code;

      if (db) {
        await db.collection('certificates').doc(code).set({
          id: code,
          verifyCode: code,
          learnerName: newReq.fullName,
          learnerEmail: newReq.email,
          courseId: newReq.courseId,
          courseTitle: newReq.courseTitle,
          issueDate: new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' }),
          status: 'VALID',
          statusReason: 'Coursework certified by Coach Hyela administration.',
          credentialType: 'Executive Certificate of Practical Completion',
          instructor: 'Coach Hyela',
          instructorTitle: 'Lead Instructor & Director',
          topicsCompleted: ['Practical Capstone Completion', 'Verified Project Workflow']
        });
      }
    }

    if (db) {
      await db.collection('eligibility_requests').doc(id).set(newReq);
      await db.collection('activity_logs').add({
        type: 'MANUAL_APP_SYNC',
        page: 'Operations Hub',
        device: window.innerWidth <= 768 ? 'Mobile' : 'Desktop',
        details: `Application ${id} created for ${newReq.fullName} (${newReq.email})`,
        timestamp: new Date().toISOString()
      });
    }

    // Save locally
    const reqs = getEligibilityRequests();
    reqs.unshift(newReq);
    saveEligibilityRequests(reqs);

    return { success: true, request: newReq };
  }

  // Real-time Cloud CAC Inquiries Listener
  function subscribeCloudCAC(callback) {
    const db = getFirestore();
    if (db) {
      return db.collection('cac_submissions')
        .orderBy('timestamp', 'desc')
        .onSnapshot(snapshot => {
          const subs = [];
          snapshot.forEach(doc => {
            const data = doc.data();
            data.id = doc.id;
            subs.push(data);
          });
          if (subs.length > 0) {
            localStorage.setItem(STORAGE_KEYS.CAC_SUBMISSIONS, JSON.stringify(subs));
          }
          if (callback) callback(subs);
        }, err => {
          console.warn('[CHT Cloud] CAC snapshot error:', err);
          if (callback) callback(getCACSubmissions());
        });
    } else {
      if (callback) callback(getCACSubmissions());
      return null;
    }
  }

  // Find Certificate by ID from Cloud Firestore fallback
  async function findCertificateByIdCloud(code) {
    const local = findCertificateById(code);
    if (local) return local;

    const db = getFirestore();
    if (db && code) {
      try {
        const clean = code.trim().toUpperCase();
        const doc = await db.collection('certificates').doc(clean).get();
        if (doc.exists) {
          const cert = doc.data();
          const certs = getCertificates();
          certs.unshift(cert);
          saveCertificates(certs);
          return cert;
        }
      } catch (e) {
        console.warn('[CHT Cloud] Find cert error:', e);
      }
    }
    return null;
  }
"""

if 'subscribeCloudStudents' not in content:
    target_str = "// Cloud Sync for Submitting Eligibility Request"
    content = content.replace(target_str, additional_cloud_helpers + "\n  " + target_str)
    print("Added additional cloud helper functions")

# 3. Update saveCACSubmission to sync to Firestore and activity_logs
old_save_cac = """  function saveCACSubmission(submission) {
    try {
      const existing = JSON.parse(localStorage.getItem(STORAGE_KEYS.CAC_SUBMISSIONS) || '[]');
      existing.unshift(submission);
      localStorage.setItem(STORAGE_KEYS.CAC_SUBMISSIONS, JSON.stringify(existing));
      return true;
    } catch (e) {
      console.error('Failed tosave CAC submission:', e);
      return false;
    }
  }"""

new_save_cac = """  function saveCACSubmission(submission) {
    try {
      const existing = JSON.parse(localStorage.getItem(STORAGE_KEYS.CAC_SUBMISSIONS) || '[]');
      existing.unshift(submission);
      localStorage.setItem(STORAGE_KEYS.CAC_SUBMISSIONS, JSON.stringify(existing));

      const db = getFirestore();
      if (db && submission) {
        const id = submission.refCode || ('CAC-' + Date.now().toString(36).toUpperCase());
        db.collection('cac_submissions').doc(id).set(submission).catch(e => console.warn('[CHT Cloud] CAC save error:', e));
        db.collection('activity_logs').add({
          type: 'CAC_REGISTRATION',
          page: 'CAC Registration Portal',
          device: window.innerWidth <= 768 ? 'Mobile' : 'Desktop',
          details: `CAC Request ${id}: ${submission.fullName} (${submission.email}) - ${submission.type || 'Filing'}`,
          timestamp: new Date().toISOString()
        }).catch(e => console.warn('[CHT Cloud] CAC log error:', e));
      }
      return true;
    } catch (e) {
      console.error('Failed to save CAC submission:', e);
      return false;
    }
  }"""

if old_save_cac in content:
    content = content.replace(old_save_cac, new_save_cac)
    print("Updated saveCACSubmission with Firestore cloud sync")

# 4. Update claimCertificate to also save to Firestore certificates
old_claim_cert_sync = """    saveCertificates(certs);

    // Update eligibility request status
    req.certificateIssued = true;
    req.certificateCode = certCode;
    saveEligibilityRequests(reqs);"""

new_claim_cert_sync = """    saveCertificates(certs);

    // Update eligibility request status
    req.certificateIssued = true;
    req.certificateCode = certCode;
    saveEligibilityRequests(reqs);

    const db = getFirestore();
    if (db) {
      db.collection('certificates').doc(certCode).set(newCert).catch(e => console.warn('[CHT Cloud] Cert save error:', e));
      db.collection('eligibility_requests').doc(requestId).update({
        certificateIssued: true,
        certificateCode: certCode
      }).catch(e => console.warn('[CHT Cloud] Req cert update error:', e));
      db.collection('activity_logs').add({
        type: 'CERTIFICATE_CLAIMED',
        page: 'Student Portal',
        device: window.innerWidth <= 768 ? 'Mobile' : 'Desktop',
        details: `Certificate ${certCode} claimed by ${req.fullName} (${req.email})`,
        timestamp: new Date().toISOString()
      }).catch(e => console.warn('[CHT Cloud] Cert log error:', e));
    }"""

if old_claim_cert_sync in content:
    content = content.replace(old_claim_cert_sync, new_claim_cert_sync)
    print("Updated claimCertificate with Firestore sync")

# 5. Update DOMContentLoaded at bottom of cht-core.js to auto-track visitor
old_dom_bottom = """document.addEventListener('DOMContentLoaded', () => {
  CHT.initNavToggle();
  CHT.applyLiveContentToDOM();
});"""

new_dom_bottom = """document.addEventListener('DOMContentLoaded', () => {
  CHT.initNavToggle();
  CHT.applyLiveContentToDOM();
  if (typeof window !== 'undefined' && !window.location.pathname.toLowerCase().includes('admin.html')) {
    if (CHT.trackVisitorActivity) {
      CHT.trackVisitorActivity(document.title);
    }
  }
});"""

if old_dom_bottom in content:
    content = content.replace(old_dom_bottom, new_dom_bottom)
    print("Updated DOMContentLoaded to auto-track visitor activity on all pages")

# 6. Expose the new methods in return object
old_return = """    // Eligibility
    getEligibilityRequests,
    submitEligibilityRequest,
    submitEligibilityRequestCloud,
    updateEligibilityStatusCloud,
    subscribeCloudRequests,
    trackVisitorActivity,
    subscribeVisitorStats,
    subscribeActivityLogs,
    claimCertificate,"""

new_return = """    // Eligibility & Cloud
    getEligibilityRequests,
    submitEligibilityRequest,
    submitEligibilityRequestCloud,
    updateEligibilityStatusCloud,
    createEligibilityRequestCloud,
    subscribeCloudRequests,
    subscribeCloudStudents,
    saveStudentCloud,
    subscribeCloudCAC,
    findCertificateByIdCloud,
    trackVisitorActivity,
    subscribeVisitorStats,
    subscribeActivityLogs,
    claimCertificate,"""

if old_return in content:
    content = content.replace(old_return, new_return)
    print("Exposed new cloud methods in return block")

with open('js/cht-core.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("js/cht-core.js successfully patched!")
