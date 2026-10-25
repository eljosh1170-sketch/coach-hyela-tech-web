import json

# 1. Update js/cht-core.js with Firestore Real-time Sync and Analytics Tracking
with open('js/cht-core.js', 'r', encoding='utf-8') as f:
    core_js = f.read()

firestore_client_code = """
  // ==========================================
  // REAL-TIME CLOUD FIRESTORE SYNCHRONIZATION
  // ==========================================
  const CHT_FIREBASE_CONFIG = {
    projectId: 'coachhyelatech-d3207',
    appId: '1:946569619362:web:d03da6c819375625c034fb',
    storageBucket: 'coachhyelatech-d3207.firebasestorage.app',
    apiKey: 'AIzaSyB4j-litduC2dvVAdMcyJUTVa7sqDmqiPY',
    authDomain: 'coachhyelatech-d3207.firebaseapp.com',
    messagingSenderId: '946569619362',
    measurementId: 'G-5LNNMMX44T'
  };

  function getFirestore() {
    try {
      if (typeof firebase !== 'undefined' && firebase.firestore) {
        if (!firebase.apps.length) {
          firebase.initializeApp(CHT_FIREBASE_CONFIG);
        }
        return firebase.firestore();
      }
    } catch (e) {
      console.warn('[CHT Cloud] Firestore init error:', e);
    }
    return null;
  }

  // Real-time Cloud Eligibility Requests Listener
  function subscribeCloudRequests(callback) {
    const db = getFirestore();
    if (db) {
      return db.collection('eligibility_requests')
        .orderBy('submissionDate', 'desc')
        .onSnapshot(snapshot => {
          const cloudReqs = [];
          snapshot.forEach(doc => {
            const data = doc.data();
            data.id = doc.id;
            cloudReqs.push(data);
          });
          if (cloudReqs.length > 0) {
            saveEligibilityRequests(cloudReqs);
          }
          if (callback) callback(cloudReqs);
        }, err => {
          console.warn('[CHT Cloud] Requests snapshot error:', err);
          if (callback) callback(getEligibilityRequests());
        });
    } else {
      if (callback) callback(getEligibilityRequests());
      return null;
    }
  }

  // Real-time Cloud Activity Logger & Visitor Stats Tracker
  async function trackVisitorActivity(pageTitle) {
    const db = getFirestore();
    const isNewVisitor = !localStorage.getItem('cht_visited_before');
    localStorage.setItem('cht_visited_before', 'true');
    const device = window.innerWidth <= 768 ? 'Mobile' : 'Desktop';

    if (db) {
      try {
        // Increment metrics counter
        const metricsRef = db.collection('visitor_stats').doc('metrics');
        const increment = firebase.firestore.FieldValue.increment;
        await metricsRef.set({
          pageViews: increment(1),
          visitors: increment(isNewVisitor ? 1 : 0),
          lastActive: new Date().toISOString()
        }, { merge: true });

        // Record activity log item
        await db.collection('activity_logs').add({
          type: 'PAGE_VIEW',
          page: pageTitle || window.location.pathname,
          device: device,
          timestamp: new Date().toISOString()
        });
      } catch (e) {
        console.warn('[CHT Cloud] Stats tracking error:', e);
      }
    }
  }

  // Subscribe to Live Visitor Stats
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
  }

  // Subscribe to Live Activity Logs
  function subscribeActivityLogs(callback) {
    const db = getFirestore();
    if (db) {
      return db.collection('activity_logs')
        .orderBy('timestamp', 'desc')
        .limit(20)
        .onSnapshot(snapshot => {
          const logs = [];
          snapshot.forEach(doc => logs.push(doc.data()));
          callback(logs);
        }, err => console.warn('[CHT Cloud] Activity logs error:', err));
    }
    return null;
  }

  // Cloud Sync for Submitting Eligibility Request
  async function submitEligibilityRequestCloud(userId, fullName, email, courseId, courseTitle) {
    const res = submitEligibilityRequest(userId, fullName, email, courseId, courseTitle);
    if (!res.success) return res;

    const db = getFirestore();
    if (db && res.request) {
      try {
        await db.collection('eligibility_requests').doc(res.request.id).set(res.request);
        await db.collection('activity_logs').add({
          type: 'STUDENT_APPLICATION',
          page: 'Learner Portal',
          device: window.innerWidth <= 768 ? 'Mobile' : 'Desktop',
          details: `${fullName} (${email}) applied for ${courseTitle}`,
          timestamp: new Date().toISOString()
        });
        console.log('[CHT Cloud] Eligibility request synced to Firestore:', res.request.id);
      } catch (err) {
        console.warn('[CHT Cloud] Firestore submit error:', err);
      }
    }
    return res;
  }

  // Cloud Sync for Updating Eligibility Status
  async function updateEligibilityStatusCloud(requestId, newStatus, adminNotes = '') {
    const res = updateEligibilityStatus(requestId, newStatus, adminNotes);
    if (!res.success) return res;

    const db = getFirestore();
    if (db) {
      try {
        await db.collection('eligibility_requests').doc(requestId).update({
          status: newStatus,
          adminNotes: adminNotes || (newStatus === 'APPROVED' ? "Approved by Coach Hyela administration." : "Updated by administrator."),
          reviewedAt: new Date().toISOString()
        });
        await db.collection('activity_logs').add({
          type: 'ADMIN_DECISION',
          page: 'Operations Hub',
          device: window.innerWidth <= 768 ? 'Mobile' : 'Desktop',
          details: `Admin set Request ${requestId} to ${newStatus}`,
          timestamp: new Date().toISOString()
        });
        console.log('[CHT Cloud] Eligibility status updated in Firestore:', requestId, newStatus);
      } catch (err) {
        console.warn('[CHT Cloud] Firestore update error:', err);
      }
    }
    return res;
  }
"""

if 'REAL-TIME CLOUD FIRESTORE SYNCHRONIZATION' not in core_js:
    core_js = core_js.replace('  // Student Account Registration with Verification Code', firestore_client_code + '\n  // Student Account Registration with Verification Code')
    print("Inserted firestore_client_code into cht-core.js")

# Export cloud functions in CHT object
old_exp = "    submitEligibilityRequest,"
new_exp = """    submitEligibilityRequest,
    submitEligibilityRequestCloud,
    updateEligibilityStatusCloud,
    subscribeCloudRequests,
    trackVisitorActivity,
    subscribeVisitorStats,
    subscribeActivityLogs,"""

if old_exp in core_js and 'submitEligibilityRequestCloud,' not in core_js:
    core_js = core_js.replace(old_exp, new_exp)
    print("Exported cloud methods in cht-core.js")

with open('js/cht-core.js', 'w', encoding='utf-8') as f:
    f.write(core_js)

print("cht-core.js updated!")
