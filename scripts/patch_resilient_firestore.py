# scripts/patch_resilient_firestore.py
with open('js/cht-core.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update subscribeCloudRequests
old_sub_reqs = """  // Real-time Cloud Eligibility Requests Listener
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
  }"""

new_sub_reqs = """  // Real-time Cloud Eligibility Requests Listener
  function subscribeCloudRequests(callback) {
    const db = getFirestore();
    if (db) {
      return db.collection('eligibility_requests')
        .onSnapshot(snapshot => {
          const cloudReqs = [];
          snapshot.forEach(doc => {
            const data = doc.data();
            data.id = doc.id;
            cloudReqs.push(data);
          });
          cloudReqs.sort((a, b) => new Date(b.submissionDate || 0) - new Date(a.submissionDate || 0));
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
  }"""

if old_sub_reqs in code:
    code = code.replace(old_sub_reqs, new_sub_reqs)
    print("Updated subscribeCloudRequests to resilient in-memory sort")

# 2. Update subscribeCloudStudents
old_sub_studs = """  // Subscribe to Registered Students from Cloud Firestore
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
  }"""

new_sub_studs = """  // Subscribe to Registered Students from Cloud Firestore
  function subscribeCloudStudents(callback) {
    const db = getFirestore();
    if (db) {
      return db.collection('students')
        .onSnapshot(snapshot => {
          const cloudStudents = [];
          snapshot.forEach(doc => {
            const data = doc.data();
            data.id = doc.id;
            cloudStudents.push(data);
          });
          cloudStudents.sort((a, b) => new Date(b.registeredAt || 0) - new Date(a.registeredAt || 0));
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
  }"""

if old_sub_studs in code:
    code = code.replace(old_sub_studs, new_sub_studs)
    print("Updated subscribeCloudStudents to resilient in-memory sort")

# 3. Update subscribeCloudCAC
old_sub_cac = """  // Real-time Cloud CAC Inquiries Listener
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
  }"""

new_sub_cac = """  // Real-time Cloud CAC Inquiries Listener
  function subscribeCloudCAC(callback) {
    const db = getFirestore();
    if (db) {
      return db.collection('cac_submissions')
        .onSnapshot(snapshot => {
          const subs = [];
          snapshot.forEach(doc => {
            const data = doc.data();
            data.id = doc.id;
            subs.push(data);
          });
          subs.sort((a, b) => new Date(b.timestamp || 0) - new Date(a.timestamp || 0));
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
  }"""

if old_sub_cac in code:
    code = code.replace(old_sub_cac, new_sub_cac)
    print("Updated subscribeCloudCAC to resilient in-memory sort")

# 4. Update subscribeActivityLogs
old_sub_logs = """  // Subscribe to Live Activity Logs
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
  }"""

new_sub_logs = """  // Subscribe to Live Activity Logs
  function subscribeActivityLogs(callback) {
    const db = getFirestore();
    if (db) {
      return db.collection('activity_logs')
        .onSnapshot(snapshot => {
          const logs = [];
          snapshot.forEach(doc => logs.push(doc.data()));
          logs.sort((a, b) => new Date(b.timestamp || 0) - new Date(a.timestamp || 0));
          callback(logs.slice(0, 30));
        }, err => console.warn('[CHT Cloud] Activity logs error:', err));
    }
    return null;
  }"""

if old_sub_logs in code:
    code = code.replace(old_sub_logs, new_sub_logs)
    print("Updated subscribeActivityLogs to resilient in-memory sort")

with open('js/cht-core.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Firestore listeners patched successfully!")
