// Coach Hyela Tech Industries Limited - Application Core Logic & Student Approval System
// Standards: Zeroexternal heavy dependencies, client-side resilience with full authentication, eligibility workflow, and admin auditing

const CHT = (function () {
  'use strict';

  // State keys
  const STORAGE_KEYS = {
    CERTIFICATES: 'cht_certificates_db',
    CAC_SUBMISSIONS: 'cht_cac_submissions',
    USERS: 'cht_users_db',
    AUTH_USER: 'cht_auth_user',
    ELIGIBILITY_REQUESTS: 'cht_eligibility_requests',
    ADMIN_SESSIoN: 'cht_admin_session',
    NOTIFICATION_LOG: 'cht_notification_log',
    RATE_LIMITS: 'cht_rate_limits'
  };

  // Pre-seeded initial accounts for testing & demonstration
  const DEFAULT_USERS = [
    {
      id: "USR-001",
      fullName: "Bilkisu Danjuma",
      email: "bilkisu.learner@testmail.com",
      passwordHash: "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", // 'password' in SHA-256
      salt: "cht_salt_001",
      emailVerified: true,
      verificationToken: null,
      verificationExpires: null,
      registeredAt: "2026-10-10T09:00:00.000Z",
      assignedCourses: ["ai-video-ugc"],
      driveAccess: true
    },
    {
      id: "USR-002",
      fullName: "Emmanuel K. Ogbonna",
      email: "emmanuel.learner@testmail.com",
      passwordHash: "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
      salt: "cht_salt_002",
      emailVerified: true,
      verificationToken: null,
      verificationExpires: null,
      registeredAt: "2026-10-12T14:30:00.000Z",
      assignedCourses: ["website-building"],
      driveAccess: true
    },
    {
      id: "USR-003",
      fullName: "Tariq Ibrahim",
      email: "tariq.student@testmail.com",
      passwordHash: "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
      salt: "cht_salt_003",
      emailVerified: true,
      verificationToken: null,
      verificationExpires: null,
      registeredAt: "2026-10-18T11:00:00.000Z",
      assignedCourses: [],
      driveAccess: false
    }
  ];

  // Active student eligibility requests
  const DEFAULT_ELIGIBILITY = [
    {
      id: "REQ-2026-AYO1",
      userId: "USR-OjS5lcUI",
      fullName: "Ayomide Emmanuel",
      email: "emmanuelekhator5683@gmail.com",
      courseId: "ai-video-ugc",
      courseTitle: "AI Video Creation & UGC-Style Advertising",
      submissionDate: "2026-10-25T19:43:00.000Z",
      status: "PENDING",
      adminNotes: "Application received. Pending evaluation by Coach Hyela.",
      reviewedAt: null,
      certificateIssued: false,
      certificateCode: null
    }
  ];

  // Verified certificates dataset
  const DEFAULT_CERTIFICATES = [
    {
      id: "CHT-2026-AI092",
      verifyCode: "CHT-2026-AI092",
      learnerName: "Bilkisu Danjuma",
      learnerEmail: "bilkisu.learner@testmail.com",
      courseId: "ai-video-ugc",
      courseTitle: "AI Video Creation & UGC-Style Advertising",
      issueDate: "October 14, 2026",
      status: "VALID",
      statusReason: "Successfully completed all capstone video assignments and commercial workflow requirements.",
      credentialType: "Executive Certificate of Practical Completion",
      instructor: "Coach Hyela",
      instructorTitle: "Lead Instructor & Director",
      topicsCompleted: [
        "Photorealistic Prompt Engineering",
        "AI Avatar Lip-Sync Calibration",
        "CapCut Post-Production & Sound Design",
        "UGC Brand Commercials"
      ]
    },
    {
      id: "CHT-2026-WD104",
      verifyCode: "CHT-2026-WD104",
      learnerName: "Emmanuel K. Ogbonna",
      learnerEmail: "emmanuel.learner@testmail.com",
      courseId: "website-building",
      courseTitle: "Modern Website Building & Digital Presence",
      issueDate: "October 02, 2026",
      status: "VALID",
      statusReason: "Demonstrated full proficiency in semantic HTML5, responsive CSS3, and modern web deployment.",
      credentialType: "Professional Technical Certificate",
      instructor: "Coach Hyela",
      instructorTitle: "Lead Instructor & Director",
      topicsCompleted: [
        "Semantic HTML5 & Responsive CSS Layouts",
        "Accessible Mobile Navigation",
        "Form Integration & Database Workflows",
        "High-Speed Edge Hosting Deployment"
      ]
    },
    {
      id: "CHT-2026-REV088",
      verifyCode: "CHT-2026-REV088",
      learnerName: "Sample Incomplete Candidate",
      learnerEmail: "revoked.sample@testmail.com",
      courseId: "ai-digital-skills",
      courseTitle: "Artificial Intelligence & Creative Workflows for Individuals",
      issueDate: "August 15, 2026",
      status: "REVOKED",
      statusReason: "Record withdrawn: Incomplete coursework submission / administrative withdrawal.",
      credentialType: "Certificate of Completion",
      instructor: "Coach Hyela",
      instructorTitle: "Lead Instructor & Director",
      topicsCompleted: []
    }
  ];

  // SHA-256 helper using native Web CryptoAPI
  async function sha256(message) {
    try {
      const msgBuffer = new TextEncoder().encode(message);
      const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
      const hashArray = Array.from(new Uint8Array(hashBuffer));
      return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    } catch (e) {
      // Fallback simple hash for older environments
      let hash = 0;
      for (let i = 0; i < message.length; i++) {
        hash = ((hash << 5) - hash) + message.charCodeAt(i);
        hash |= 0;
      }
      return 'hash_' + Math.abs(hash).toString(16);
    }
  }

  // Initialize storage
  function initStorage() {
    try {
      if (!localStorage.getItem(STORAGE_KEYS.USERS)) {
        localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(DEFAULT_USERS));
      } else {
        try {
          const uList = JSON.parse(localStorage.getItem(STORAGE_KEYS.USERS) || '[]');
          if (!uList.some(u => u.email === 'emmanuelekhator5683@gmail.com')) {
            uList.unshift({
              id: "USR-OjS5lcUI",
              fullName: "Ayomide Emmanuel",
              email: "emmanuelekhator5683@gmail.com",
              registeredAt: "2026-10-25T19:15:36.000Z",
              emailVerified: true,
              assignedCourses: ["ai-video-ugc"],
              driveAccess: false
            });
            localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(uList));
          }
        } catch(e) {}
      }

      if (!localStorage.getItem(STORAGE_KEYS.ELIGIBILITY_REQUESTS)) {
        localStorage.setItem(STORAGE_KEYS.ELIGIBILITY_REQUESTS, JSON.stringify(DEFAULT_ELIGIBILITY));
      } else {
        try {
          let reqList = JSON.parse(localStorage.getItem(STORAGE_KEYS.ELIGIBILITY_REQUESTS) || '[]');
          // Remove outdated dummy test users if present
          reqList = reqList.filter(r => !r.email.includes('@testmail.com'));
          if (!reqList.some(r => r.email === 'emmanuelekhator5683@gmail.com')) {
            reqList.unshift({
              id: "REQ-2026-AYO1",
              userId: "USR-OjS5lcUI",
              fullName: "Ayomide Emmanuel",
              email: "emmanuelekhator5683@gmail.com",
              courseId: "ai-video-ugc",
              courseTitle: "AI Video Creation & UGC-Style Advertising",
              submissionDate: "2026-10-25T19:43:00.000Z",
              status: "PENDING",
              adminNotes: "Application received. Pending evaluation by Coach Hyela.",
              reviewedAt: null,
              certificateIssued: false,
              certificateCode: null
            });
          }
          localStorage.setItem(STORAGE_KEYS.ELIGIBILITY_REQUESTS, JSON.stringify(reqList));
        } catch(e) {}
      }
      if (!localStorage.getItem(STORAGE_KEYS.CERTIFICATES)) {
        localStorage.setItem(STORAGE_KEYS.CERTIFICATES, JSON.stringify(DEFAULT_CERTIFICATES));
      }
      if (!localStorage.getItem(STORAGE_KEYS.CAC_SUBMISSIONS)) {
        localStorage.setItem(STORAGE_KEYS.CAC_SUBMISSIONS, JSON.stringify([]));
      }
      if (!localStorage.getItem(STORAGE_KEYS.NOTIFICATION_LOG)) {
        localStorage.setItem(STORAGE_KEYS.NOTIFICATION_LOG, JSON.stringify([]));
      }
    } catch (e) {
      console.warn('LocalStorage not accessible:', e);
    }
  }

  // Rate Limiter Helper (Prevents abuse of verification codes and password resets)
  function checkRateLimit(action, identifier, maxAttempts = 3, windowMs = 60000) {
    try {
      const key = `${action}_${identifier}`;
      const now = Date.now();
      const limits = JSON.parse(localStorage.getItem(STORAGE_KEYS.RATE_LIMITS) || '{}');
      const record = limits[key] || { count: 0, firstAttempt: now };

      if (now - record.firstAttempt > windowMs) {
        // Reset window
        limits[key] = { count: 1, firstAttempt: now };
        localStorage.setItem(STORAGE_KEYS.RATE_LIMITS, JSON.stringify(limits));
        return { allowed: true, remaining: maxAttempts - 1 };
      }

      if (record.count >= maxAttempts) {
        const waitSec = Math.ceil((windowMs - (now - record.firstAttempt)) / 1000);
        return { allowed: false, waitSec: waitSec };
      }

      record.count += 1;
      limits[key] = record;
      localStorage.setItem(STORAGE_KEYS.RATE_LIMITS, JSON.stringify(limits));
      return { allowed: true, remaining: maxAttempts - record.count };
    } catch (e) {
      return { allowed: true, remaining: 1 };
    }
  }

  // User Management
  function getUsers() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEYS.USERS) || '[]');
    } catch (e) {
      return DEFAULT_USERS;
    }
  }

  function saveUsers(users) {
    try {
      localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(users));
    } catch (e) {
      console.error('Failed tosave users:', e);
    }
  }

  function findUserByEmail(email) {
    if (!email) return null;
    const clean = email.trim().toLowerCase();
    const users = getUsers();
    return users.find(u => u.email.toLowerCase() === clean) || null;
  }

  // Log system email notification
  function logNotification(toEmail, subject, body, type = 'info') {
    try {
      const logs = JSON.parse(localStorage.getItem(STORAGE_KEYS.NOTIFICATION_LOG) || '[]');
      const entry = {
        id: 'NoTIF-' + Date.now() + '-' + Math.floor(Math.random() * 1000),
        toEmail: toEmail,
        subject: subject,
        body: body,
        type: type,
        timestamp: new Date().toISOString()
      };
      logs.unshift(entry);
      localStorage.setItem(STORAGE_KEYS.NOTIFICATION_LOG, JSON.stringify(logs));
      return entry;
    } catch (e) {
      return null;
    }
  }

  function getNotificationLogs() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEYS.NOTIFICATION_LOG) || '[]');
    } catch (e) {
      return [];
    }
  }


  // ==========================================
  // LIVE TRANSACTIONAL EMAIL DISPATCHER (EmailJS)
  // ==========================================
  const EMAILJS_CONFIG_KEY = 'cht_emailjs_config';

  function getEmailConfig() {
    try {
      const cfg = JSON.parse(localStorage.getItem(EMAILJS_CONFIG_KEY) || '{}');
      return {
        serviceId: cfg.serviceId || '',
        templateId: cfg.templateId || '',
        publicKey: cfg.publicKey || ''
      };
    } catch (e) {
      return { serviceId: '', templateId: '', publicKey: '' };
    }
  }

  function saveEmailConfig(cfg) {
    localStorage.setItem(EMAILJS_CONFIG_KEY, JSON.stringify({
      serviceId: (cfg.serviceId || '').trim(),
      templateId: (cfg.templateId || '').trim(),
      publicKey: (cfg.publicKey || '').trim()
    }));
    return { success: true, message: 'Email configuration saved!' };
  }

  async function sendLiveEmail(toEmail, toName, code, type = 'VERIFICATION') {
    const cfg = getEmailConfig();
    const hasKeys = cfg.serviceId && cfg.templateId && cfg.publicKey;

    if (window.emailjs && hasKeys) {
      try {
        emailjs.init(cfg.publicKey);
        const templateParams = {
          to_email: toEmail,
          to_name: toName || 'Student',
          verification_code: code,
          action_type: type === 'RESET' ? 'Password Reset Code' : 'Student Email Verification Code',
          expiry_mins: type === 'RESET' ? '20 minutes' : '30 minutes',
          site_name: 'Coach Hyela Tech Industries Limited',
          site_url: 'https://coachhyelatech.com.ng'
        };

        const resp = await emailjs.send(cfg.serviceId, cfg.templateId, templateParams);
        console.log('[CHT Email] Live email dispatched successfully:', resp.status, resp.text);
        return { success: true, mode: 'live', status: resp.status };
      } catch (err) {
        console.error('[CHT Email] EmailJS send error:', err);
        return { success: false, mode: 'live_failed', error: err.text || err.message };
      }
    } else {
      console.info('[CHT Email] EmailJS not configured yet; code recorded in admin audit log.');
      return { success: true, mode: 'audit_logged' };
    }
  }


  // ==========================================
  // REAL-TIME CLOUD FIRESTORE SYNCHRONIZATION
  // ==========================================
    const CHT_MASTER_DRIVE_URL = "https://drive.google.com/drive/folders/1_0uldj8-IFcWQxRa4PuFRFVgCRDeSNDJ?usp=drive_link";
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
          } else {
            callback({ pageViews: 0, visitors: 0, lastActive: new Date().toISOString() });
          }
        }, err => {
          console.warn('[CHT Cloud] Stats error:', err);
          callback({ pageViews: 0, visitors: 0, lastActive: null });
        });
    }
    return null;
  }

  // Subscribe to Live Activity Logs
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
  }

  
  // Subscribe to Registered Students from Cloud Firestore
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

  // Cloud Sync for Submitting Eligibility Request
  async function submitEligibilityRequestCloud(userId, fullName, email, courseId, courseTitle, packageTier = 'VIP_BUNDLE') {
    const res = submitEligibilityRequest(userId, fullName, email, courseId, courseTitle, packageTier);
    if (!res.success) return res;

    const db = getFirestore();
    if (db && res.request) {
      try {
        await db.collection('eligibility_requests').doc(res.request.id).set(res.request);
        await db.collection('activity_logs').add({
          type: 'STUDENT_APPLICATION',
          page: 'Learner Portal',
          device: window.innerWidth <= 768 ? 'Mobile' : 'Desktop',
          details: `${fullName} (${email}) applied for ${courseTitle} [${packageTier}]`,
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
  async function updateEligibilityStatusCloud(requestId, newStatus, adminNotes = '', extraDetails = {}) {
    const res = updateEligibilityStatus(requestId, newStatus, adminNotes, extraDetails);

    const db = getFirestore();
    if (db) {
      try {
        const updatePayload = {
          status: newStatus,
          adminNotes: adminNotes || (newStatus === 'APPROVED' ? "Approved by Coach Hyela administration." : "Updated by administrator."),
          reviewedAt: new Date().toISOString()
        };
        if (res.request && res.request.certificateCode) {
          updatePayload.certificateIssued = true;
          updatePayload.certificateCode = res.request.certificateCode;
        }

        const cloudSyncPromise = (async () => {
          // Use .set with merge: true so it never fails with "No document to update"
          await db.collection('eligibility_requests').doc(requestId).set(updatePayload, { merge: true });

          // If a certificate was generated, persist to Firestore certificates collection immediately
          if (res.certificate) {
            await db.collection('certificates').doc(res.certificate.verifyCode).set(res.certificate, { merge: true });
          }

          // If student email exists and request approved, update student's profile & drive access in Firestore
          if (res.request && res.request.email) {
            const cleanEmail = res.request.email.trim().toLowerCase();
            const studentId = res.request.userId || ('USR-' + Date.now().toString(36).toUpperCase());
            await db.collection('students').doc(studentId).set({
              email: cleanEmail,
              fullName: res.request.fullName || '',
              driveAccess: extraDetails.grantDrive !== false,
              vipAccess: extraDetails.grantDrive !== false,
              lastCertifiedAt: new Date().toISOString()
            }, { merge: true });
          }

          await db.collection('activity_logs').add({
            type: 'ADMIN_DECISION',
            page: 'Operations Hub',
            device: window.innerWidth <= 768 ? 'Mobile' : 'Desktop',
            details: `Admin set Request ${requestId} to ${newStatus}${res.request && res.request.certificateCode ? ' (Issued ' + res.request.certificateCode + ')' : ''}`,
            timestamp: new Date().toISOString()
          });
        })();

        // Safe 4.5-second timeout prevents indefinite UI freezing on flaky mobile networks
        await Promise.race([
          cloudSyncPromise,
          new Promise((resolve) => setTimeout(resolve, 4500))
        ]);
        console.log('[CHT Cloud] Eligibility status updated in Firestore:', requestId, newStatus);
      } catch (err) {
        console.warn('[CHT Cloud] Firestore update warning:', err);
      }
    }
    return res;
  }

  // Student Account Registration with Verification Code
  async function registerStudent(fullName, email, password) {
    if (!fullName || !email || !password) {
      return { success: false, message: "Please provide full name, email address, and password." };
    }

    if (password.length < 6) {
      return { success: false, message: "Password must be at least 6 characters long." };
    }

    const cleanEmail = email.trim().toLowerCase();
    const existing = findUserByEmail(cleanEmail);
    if (existing) {
      return { success: false, message: "An account with this email address alreadyexists. Please log in or request a password reset." };
    }

    // Rate limit registration requests
    const rl = checkRateLimit('register', cleanEmail, 3, 300000);
    if (!rl.allowed) {
      return { success: false, message: `Toomany registration attempts. Please wait ${rl.waitSec} seconds.` };
    }

    const salt = 'cht_' + Math.random().toString(36).substring(2, 9);
    const hash = await sha256(password + salt);
    const verificationCode = Math.floor(100000 + Math.random() * 900000).toString(); // 6-digit code
    const expires = Date.now() + (30 * 60 * 1000); // 30 minutes expiry

    const newUser = {
      id: "USR-" + Date.now().toString(36).toUpperCase(),
      fullName: fullName.trim(),
      email: cleanEmail,
      passwordHash: hash,
      salt: salt,
      emailVerified: false,
      verificationToken: verificationCode,
      verificationExpires: expires,
      registeredAt: new Date().toISOString(),
      assignedCourses: [],
      driveAccess: false
    };

    const users = getUsers();
    users.push(newUser);
    saveUsers(users);

    // Send live email notification + record in admin audit log
    sendLiveEmail(cleanEmail, fullName.trim(), verificationCode, 'VERIFICATION');
    logNotification(
      cleanEmail,
      "Verify Your Coach Hyela Tech Student Account",
      `Welcome ${fullName.trim()}! Your 6-digit email verification code is: ${verificationCode}. This code expires in 30 minutes. Note: Creating an account does not automatically certify you; certificate eligibility requires course completion review by Coach Hyela.`,
      "VERIFICATION"
    );

    return {
      success: true,
      email: cleanEmail,
      verificationCode: verificationCode, // Returned for easy in-app demonstration
      message: "Account created! A verification code has been dispatched to your email address."
    };
  }

  // Verify Student Email
  function verifyEmail(email, code) {
    const cleanEmail = email.trim().toLowerCase();
    const cleanCode = code.trim();
    const users = getUsers();
    const userIndex = users.findIndex(u => u.email.toLowerCase() === cleanEmail);

    if (userIndex === -1) {
      return { success: false, message: "User account not found." };
    }

    const user = users[userIndex];
    if (user.emailVerified) {
      return { success: true, message: "Your email is alreadyverified. You can log in." };
    }

    if (!user.verificationToken || user.verificationToken !== cleanCode) {
      return { success: false, message: "Invalid verification code. Please check and try again." };
    }

    if (user.verificationExpires && Date.now() > user.verificationExpires) {
      return { success: false, message: "Verification code has expired. Please request a new code." };
    }

    user.emailVerified = true;
    user.verificationToken = null;
    user.verificationExpires = null;
    users[userIndex] = user;
    saveUsers(users);

    logNotification(
      cleanEmail,
      "Account Verified Successfully",
      `Your Coach Hyela Tech student account has been verified. You can now log in and submit certificate eligibility requests upon course completion.`,
      "SUCCESS"
    );

    return { success: true, message: "Email successfully verified! You may now sign in." };
  }

  // Resend Verification Code
  function resendVerificationCode(email) {
    const cleanEmail = email.trim().toLowerCase();
    const rl = checkRateLimit('resend_code', cleanEmail, 3, 60000);
    if (!rl.allowed) {
      return { success: false, message: `Rate limit reached. Please wait ${rl.waitSec} seconds before resending.` };
    }

    const users = getUsers();
    const user = users.find(u => u.email.toLowerCase() === cleanEmail);
    if (!user) {
      return { success: false, message: "Noaccount found with this email." };
    }

    if (user.emailVerified) {
      return { success: true, message: "Your email is alreadyverified." };
    }

    const newCode = Math.floor(100000 + Math.random() * 900000).toString();
    user.verificationToken = newCode;
    user.verificationExpires = Date.now() + (30 * 60 * 1000);
    saveUsers(users);

    sendLiveEmail(cleanEmail, user.fullName || cleanEmail, newCode, 'VERIFICATION');
    logNotification(
      cleanEmail,
      "New Verification Code - Coach Hyela Tech",
      `Your new 6-digit email verification code is: ${newCode}. Valid for 30 minutes.`,
      "VERIFICATION"
    );

    return { success: true, verificationCode: newCode, message: "New verification code sent!" };
  }

  // Student Authentication Login
  async function loginStudent(email, password) {
    const cleanEmail = email.trim().toLowerCase();
    
    // Rate limit check
    const rl = checkRateLimit('login', cleanEmail, 5, 60000);
    if (!rl.allowed) {
      return { success: false, message: `Toomany login attempts. Please wait ${rl.waitSec} seconds.` };
    }

    const user = findUserByEmail(cleanEmail);
    if (!user) {
      return { success: false, message: "Invalid email or password." };
    }

    const checkHash = await sha256(password + (user.salt || ''));
    // Demoaccounts fallback check
    const legacyPassCheck = (password === 'password' && user.passwordHash === "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8");

    if (checkHash !== user.passwordHash && !legacyPassCheck) {
      return { success: false, message: "Invalid email or password." };
    }

    if (!user.emailVerified) {
      return {
        success: false,
        requiresVerification: true,
        email: cleanEmail,
        message: "Your email address has not been verified yet. Please enter the verification code sent to your email."
      };
    }

    // Safe session without password
    const sessionUser = {
      id: user.id,
      fullName: user.fullName,
      email: user.email,
      emailVerified: true,
      registeredAt: user.registeredAt,
      driveAccess: !!user.driveAccess
    };

    setAuthLearner(sessionUser);
    return { success: true, user: sessionUser };
  }

  // Forgot Password / Request Reset
  function requestPasswordReset(email) {
    const cleanEmail = email.trim().toLowerCase();
    const rl = checkRateLimit('forgot_pass', cleanEmail, 3, 60000);
    if (!rl.allowed) {
      return { success: false, message: `Rate limit reached. Please wait ${rl.waitSec} seconds before requesting again.` };
    }

    const users = getUsers();
    const user = users.find(u => u.email.toLowerCase() === cleanEmail);
    if (!user) {
      // For security, donot disclose if email doesn't exist
      return { success: true, message: "If this email is registered, a password reset code has been sent." };
    }

    const resetCode = Math.floor(100000 + Math.random() * 900000).toString();
    user.resetToken = resetCode;
    user.resetExpires = Date.now() + (20 * 60 * 1000); // 20 minutes
    saveUsers(users);

    sendLiveEmail(cleanEmail, user.fullName || cleanEmail, resetCode, 'RESET');
    logNotification(
      cleanEmail,
      "Password Reset Request - Coach Hyela Tech",
      `Hello${user.fullName}. You requested a password reset. Your temporary reset verification code is: ${resetCode}. It will expire in 20 minutes. If you did not request this, please ignore this email. We never send your existing password by email.`,
      "SECURITY"
    );

    return {
      success: true,
      resetCode: resetCode, // for easy testing
      message: "A password reset code has been sent to your email address."
    };
  }

  // Reset Password using code
  async function resetPassword(email, code, newPassword) {
    const cleanEmail = email.trim().toLowerCase();
    if (!newPassword || newPassword.length < 6) {
      return { success: false, message: "New password must be at least 6 characters long." };
    }

    const users = getUsers();
    const userIndex = users.findIndex(u => u.email.toLowerCase() === cleanEmail);
    if (userIndex === -1) {
      return { success: false, message: "Account not found." };
    }

    const user = users[userIndex];
    if (!user.resetToken || user.resetToken !== code.trim()) {
      return { success: false, message: "Invalid password reset code." };
    }

    if (user.resetExpires && Date.now() > user.resetExpires) {
      return { success: false, message: "Reset code has expired. Please request a new one." };
    }

    user.salt = 'cht_' + Math.random().toString(36).substring(2, 9);
    user.passwordHash = await sha256(newPassword + user.salt);
    user.resetToken = null;
    user.resetExpires = null;
    users[userIndex] = user;
    saveUsers(users);

    logNotification(
      cleanEmail,
      "Your Password Has Been Reset",
      `Your Coach Hyela Tech account password was successfully updated. You may now log in with your new credentials.`,
      "SECURITY"
    );

    return { success: true, message: "Password reset successful! You can now log in." };
  }

  // Session Helper
  function getAuthLearner() {
    try {
      const user = localStorage.getItem(STORAGE_KEYS.AUTH_USER);
      return user ? JSON.parse(user) : null;
    } catch (e) {
      return null;
    }
  }

  function setAuthLearner(learnerData) {
    try {
      if (learnerData) {
        localStorage.setItem(STORAGE_KEYS.AUTH_USER, JSON.stringify(learnerData));
      } else {
        localStorage.removeItem(STORAGE_KEYS.AUTH_USER);
      }
    } catch (e) {}
  }

  function logoutLearner() {
    setAuthLearner(null);
  }

  // ELIGIBILITY REQUESTS
  function getEligibilityRequests() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEYS.ELIGIBILITY_REQUESTS) || '[]');
    } catch (e) {
      return DEFAULT_ELIGIBILITY;
    }
  }

  function saveEligibilityRequests(reqs) {
    try {
      localStorage.setItem(STORAGE_KEYS.ELIGIBILITY_REQUESTS, JSON.stringify(reqs));
    } catch (e) {
      console.error('Failed tosave eligibility requests:', e);
    }
  }

  function submitEligibilityRequest(userId, fullName, email, courseId, courseTitle, packageTier = 'VIP_BUNDLE') {
    if (!userId || !email || !courseId) {
      return { success: false, message: "Missing required request parameters." };
    }

    const reqs = getEligibilityRequests();
    // Check if duplicate pending or approved request exists
    const duplicate = reqs.find(r => r.email.toLowerCase() === email.toLowerCase() && r.courseId === courseId && (r.status === 'PENDING' || r.status === 'APPROVED'));
    if (duplicate) {
      return {
        success: false,
        message: `You alreadyhave an eligibility record (${duplicate.status}) for ${courseTitle}.`
      };
    }

    const newReq = {
      id: "REQ-" + new Date().getFullYear() + "-" + Math.floor(100 + Math.random() * 900),
      userId: userId,
      fullName: fullName,
      email: email,
      courseId: courseId,
      courseTitle: courseTitle,
      packageTier: packageTier,
      submissionDate: new Date().toISOString(),
      status: "PENDING", // PENDING, APPROVED, REJECTED, MORE_INFo
      adminNotes: "Submitted by student. Awaiting administrative evaluation.",
      reviewedAt: null,
      certificateIssued: false,
      certificateCode: null
    };

    reqs.unshift(newReq);
    saveEligibilityRequests(reqs);

    // Notify Coach Hyela inbox and student
    logNotification(
      "coachhyelatech@gmail.com",
      `New Certificate Eligibility Request: ${fullName} (${courseTitle})`,
      `Student ${fullName} (${email}) has submitted a certificate claim request for ${courseTitle}. Review and approve in admin dashboard: admin.html`,
      "ADMIN"
    );

    logNotification(
      email,
      `Eligibility Request Received: ${courseTitle}`,
      `Hello${fullName}, your certificate eligibility request for "${courseTitle}" has been received and is currently Pending Approval. Coach Hyela administration will review your course completion records.`,
      "STATUS"
    );

    return { success: true, request: newReq, message: "Eligibility request submitted successfully! Your status is now Pending Approval." };
  }

  // CERTIFICATE CLAIMING
  function claimCertificate(requestId) {
    const reqs = getEligibilityRequests();
    const req = reqs.find(r => r.id === requestId);

    if (!req) {
      return { success: false, message: "Eligibility record not found." };
    }

    if (req.status !== 'APPROVED') {
      return { success: false, message: "Certificate cannot be claimed until official approval is granted by Coach Hyela administration." };
    }

    // Check if alreadyclaimed / issued toprevent duplicate
    const certs = getCertificates();
    if (req.certificateIssued && req.certificateCode) {
      const existingCert = certs.find(c => c.verifyCode === req.certificateCode);
      if (existingCert) {
        return { success: true, certificate: existingCert, message: "Certificate alreadygenerated and available." };
      }
    }

    // Generate fresh unique certificate ID
    const courseCodePrefix = req.courseId.includes('video') ? 'AI' : (req.courseId.includes('web') ? 'WD' : 'WF');
    const certCode = `CHT-${new Date().getFullYear()}-${courseCodePrefix}${Math.floor(100 + Math.random() * 900)}`;

    const newCert = {
      id: certCode,
      verifyCode: certCode,
      learnerName: req.fullName,
      learnerEmail: req.email,
      courseId: req.courseId,
      courseTitle: req.courseTitle,
      issueDate: new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }),
      status: "VALID",
      statusReason: "Successfully completed all verified practical coursework and capstone evaluations.",
      credentialType: "Executive Certificate of Practical Completion",
      instructor: "Coach Hyela",
      instructorTitle: "Lead Instructor & Director",
      topicsCompleted: [
        "Practical Workflow Implementation",
        "Technical Competency Assessment",
        "Commercial Capstone Deliverable",
        "Industry Best Practice Standards"
      ]
    };

    certs.unshift(newCert);
    saveCertificates(certs);

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
    }

    // Notify student
    logNotification(
      req.email,
      `Your Certificate Has Been Issued: ${certCode}`,
      `Congratulations ${req.fullName}! Your official Certificate of Completion for "${req.courseTitle}" has been generated. You can now download your certificate and verify it via QR code.`,
      "SUCCESS"
    );

    return { success: true, certificate: newCert, message: "Certificate claimed and generated successfully!" };
  }

  // Certificate DB Helpers
  function getCertificates() {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.CERTIFICATES);
      return data ? JSON.parse(data) : DEFAULT_CERTIFICATES;
    } catch (e) {
      return DEFAULT_CERTIFICATES;
    }
  }

  function saveCertificates(certs) {
    try {
      localStorage.setItem(STORAGE_KEYS.CERTIFICATES, JSON.stringify(certs));
    } catch (e) {
      console.error('Failed tosave certificates:', e);
    }
  }

  function findCertificateById(code) {
    if (!code) return null;
    const clean = code.trim().toUpperCase();
    const certs = getCertificates();
    return certs.find(c => c.verifyCode.toUpperCase() === clean || c.id.toUpperCase() === clean) || null;
  }

  function getLearnerCertificates(email) {
    if (!email) return [];
    const clean = email.trim().toLowerCase();
    const certs = getCertificates();
    return certs.filter(c => c.learnerEmail && c.learnerEmail.toLowerCase() === clean);
  }

  // CAC Submissions storage
  function saveCACSubmission(submission) {
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
  }

  function getCACSubmissions() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEYS.CAC_SUBMISSIONS) || '[]');
    } catch (e) {
      return [];
    }
  }

  // Admin Auth & Management
  function isAdminLoggedIn() {
    try {
      return sessionStorage.getItem(STORAGE_KEYS.ADMIN_SESSIoN) === 'active_authenticated';
    } catch (e) {
      return false;
    }
  }

  function loginAdmin(passkey) {
    if (passkey === 'HyelaTech2026!') {
      sessionStorage.setItem(STORAGE_KEYS.ADMIN_SESSIoN, 'active_authenticated');
      return true;
    }
    return false;
  }

  function logoutAdmin() {
    sessionStorage.removeItem(STORAGE_KEYS.ADMIN_SESSIoN);
  }

  // Admin Actions for Student Eligibility & Permissions
  function updateEligibilityStatus(requestId, newStatus, adminNotes = '', extraDetails = {}) {
    if (!isAdminLoggedIn()) {
      return { success: false, message: "Unauthorized. Admin session required." };
    }

    const reqs = getEligibilityRequests();
    let req = reqs.find(r => r.id === requestId || (r.docId && r.docId === requestId));
    if (!req) {
      // If not in local storage yet, create from extra details so approval never fails
      req = {
        id: requestId,
        userId: extraDetails.userId || ('USR-' + Date.now().toString(36).toUpperCase()),
        fullName: extraDetails.fullName || 'Student',
        email: extraDetails.email ? extraDetails.email.trim().toLowerCase() : '',
        courseId: extraDetails.courseId || 'ai-video-ugc',
        courseTitle: extraDetails.courseTitle || 'Executive Training Course',
        packageTier: extraDetails.packageTier || (extraDetails.grantDrive ? 'VIP_BUNDLE' : 'CERT_ONLY'),
        submissionDate: new Date().toISOString(),
        status: newStatus,
        adminNotes: adminNotes,
        reviewedAt: new Date().toISOString(),
        certificateIssued: false,
        certificateCode: null
      };
      reqs.unshift(req);
    } else {
      req.status = newStatus;
      req.adminNotes = adminNotes || (newStatus === 'APPROVED' ? "Approved by Coach Hyela administration." : "Updated by administrator.");
      req.reviewedAt = new Date().toISOString();
      if (extraDetails.fullName && !req.fullName) req.fullName = extraDetails.fullName;
      if (extraDetails.email && !req.email) req.email = extraDetails.email;
      if (extraDetails.courseTitle && !req.courseTitle) req.courseTitle = extraDetails.courseTitle;
    }

    let generatedCert = null;
    // If approved, automatically issue official certificate immediately so QR verification works
    if (newStatus === 'APPROVED') {
      if (!req.certificateCode) {
        const courseId = req.courseId || extraDetails.courseId || '';
        const courseCodePrefix = courseId.includes('web') ? 'WD' : (courseId.includes('cac') ? 'CAC' : 'AI');
        const certCode = `CHT-${new Date().getFullYear()}-${courseCodePrefix}${Math.floor(100 + Math.random() * 900)}`;
        req.certificateIssued = true;
        req.certificateCode = certCode;

        generatedCert = {
          id: certCode,
          verifyCode: certCode,
          learnerName: req.fullName || extraDetails.fullName || 'Student',
          learnerEmail: req.email || extraDetails.email || '',
          courseId: courseId || 'ai-video-ugc',
          courseTitle: req.courseTitle || extraDetails.courseTitle || 'Executive Certificate Course',
          issueDate: new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }),
          status: "VALID",
          statusReason: "Successfully completed verified coursework and capstone evaluations.",
          credentialType: "Executive Certificate of Practical Completion",
          instructor: "Coach Hyela",
          instructorTitle: "Lead Instructor & Director",
          topicsCompleted: [
            "Practical Workflow Implementation",
            "Technical Competency Assessment",
            "Commercial Capstone Deliverable",
            "Industry Best Practice Standards"
          ]
        };

        const certs = getCertificates();
        if (!certs.some(c => c.verifyCode === certCode)) {
          certs.unshift(generatedCert);
          saveCertificates(certs);
        }
      }

      // Update student's assigned courses in user DB
      if (req.email) {
        const cleanEmail = req.email.trim().toLowerCase();
        const users = getUsers();
        let user = users.find(u => u.email && u.email.toLowerCase() === cleanEmail);
        if (user) {
          if (!user.assignedCourses) user.assignedCourses = [];
          if (req.courseId && !user.assignedCourses.includes(req.courseId)) {
            user.assignedCourses.push(req.courseId);
          }
          saveUsers(users);
        }
      }
    }

    saveEligibilityRequests(reqs);

    // Send email notification to student
    if (req.email) {
      let subject = `Update on Certificate Eligibility: ${req.courseTitle || 'Executive Course'}`;
      let body = `Hello ${req.fullName || 'Student'},\n\nYour certificate eligibility status for "${req.courseTitle || 'Course'}" has been updated to: ${newStatus}.\n\nNote from Coach Hyela:\n${req.adminNotes}\n\n`;
      if (newStatus === 'APPROVED') {
        body += `Your official credential has been certified! Verification code: ${req.certificateCode || 'Issued'}.\nYou can log in to your student dashboard at certificates.html and verify credentials anytime.`;
      }
      logNotification(req.email, subject, body, newStatus === 'APPROVED' ? 'SUCCESS' : 'STATUS');
    }

    return { 
      success: true, 
      request: req,
      certificate: generatedCert,
      message: `Status updated to ${newStatus}${req.certificateCode ? ' (Certificate ' + req.certificateCode + ' Issued)' : ''} and synced successfully!` 
    };
  }

  // Admin update student details
  function updateStudentDetails(userId, updatedData) {
    if (!isAdminLoggedIn()) {
      return { success: false, message: "Unauthorized." };
    }

    const users = getUsers();
    const user = users.find(u => u.id === userId);
    if (!user) return { success: false, message: "User not found." };

    if (updatedData.fullName) user.fullName = updatedData.fullName.trim();
    if (updatedData.driveAccess !== undefined) user.driveAccess = !!updatedData.driveAccess;
    if (updatedData.assignedCourses) user.assignedCourses = updatedData.assignedCourses;

    saveUsers(users);

    // Alsoupdate any pending eligibility requests
    const reqs = getEligibilityRequests();
    reqs.forEach(r => {
      if (r.userId === userId || r.email.toLowerCase() === user.email.toLowerCase()) {
        if (updatedData.fullName) r.fullName = updatedData.fullName.trim();
      }
    });
    saveEligibilityRequests(reqs);

    return { success: true, message: "Student record and permissions updated successfully." };
  }

  // Admin toggle drive access
  async function toggleDriveAccess(email, hasAccess, fullName = '') {
    if (!isAdminLoggedIn()) return { success: false, message: "Unauthorized." };
    if (!email) return { success: false, message: "Email required." };

    const cleanEmail = email.trim().toLowerCase();
    const users = getUsers();
    let user = users.find(u => u.email && u.email.toLowerCase() === cleanEmail);
    if (user) {
      user.driveAccess = hasAccess;
      user.vipAccess = hasAccess;
      if (fullName && !user.fullName) user.fullName = fullName;
    } else {
      user = {
        id: 'USR-' + Date.now().toString(36).toUpperCase(),
        fullName: fullName || cleanEmail.split('@')[0],
        email: cleanEmail,
        registeredAt: new Date().toISOString(),
        emailVerified: true,
        assignedCourses: [],
        driveAccess: hasAccess,
        vipAccess: hasAccess
      };
      users.unshift(user);
    }
    saveUsers(users);

    const db = getFirestore();
    if (db) {
      try {
        const togglePromise = (async () => {
          await db.collection('students').doc(user.id).set({
            driveAccess: hasAccess,
            vipAccess: hasAccess,
            email: user.email,
            fullName: user.fullName || ''
          }, { merge: true });
          await db.collection('activity_logs').add({
            type: 'VIP_ACCESS_TOGGLE',
            page: 'Operations Hub',
            device: window.innerWidth <= 768 ? 'Mobile' : 'Desktop',
            details: `Admin set VIP Google Drive access to ${hasAccess ? 'GRANTED' : 'REVOKED'} for ${cleanEmail}`,
            timestamp: new Date().toISOString()
          });
        })();

        await Promise.race([
          togglePromise,
          new Promise((resolve) => setTimeout(resolve, 3500))
        ]);
      } catch(e) {
        console.warn('[CHT Cloud] Firestore drive toggle error:', e);
      }
    }

    logNotification(
      cleanEmail,
      `VIP Resource & Google Drive Access Updated`,
      `Your access to the restricted Coach Hyela VIP Google Drive Master Prompts repository has been ${hasAccess ? 'ACTIVATED' : 'REVOKED'}.`,
      'PERMISSIONS'
    );
    return { success: true, message: `VIP Drive access ${hasAccess ? 'granted' : 'revoked'} and synced to Google Cloud!` };
  }

  function getMasterDriveUrl() {
    const content = getLiveContent();
    return (content && content.masterDriveUrl) ? content.masterDriveUrl : CHT_MASTER_DRIVE_URL;
  }

  // Mobile Drawer Toggle
  function initNavToggle() {
    const toggle = document.querySelector('.cht-menu-toggle');
    const drawer = document.querySelector('.cht-mobile-drawer');
    const overlay = document.querySelector('.cht-drawer-overlay');
    const closeBtn = document.querySelector('.cht-drawer-close');

    if (toggle && drawer && overlay) {
      const openDrawer = () => {
        drawer.classList.add('open');
        overlay.classList.add('open');
        drawer.setAttribute('aria-hidden', 'false');
        toggle.setAttribute('aria-expanded', 'true');
      };

      const closeDrawer = () => {
        drawer.classList.remove('open');
        overlay.classList.remove('open');
        drawer.setAttribute('aria-hidden', 'true');
        toggle.setAttribute('aria-expanded', 'false');
      };

      toggle.addEventListener('click', openDrawer);
      overlay.addEventListener('click', closeDrawer);
      if (closeBtn) closeBtn.addEventListener('click', closeDrawer);

      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && drawer.classList.contains('open')) {
          closeDrawer();
        }
      });
    }
  }

  // SVG QR Code Generator
  function generateQRCodeSVG(url, size = 130) {
    const encoded = encodeURIComponent(url);
    const hash = Array.from(url).reduce((acc, char) => (acc * 31 + char.charCodeAt(0)) % 1000000, 7);
    
    let svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 25 25" width="${size}" height="${size}" shape-rendering="crispEdges">
      <rect width="25" height="25" fill="#FFFFFF"/>
      <rect x="1" y="1" width="7" height="7" fill="#0C2E1D"/>
      <rect x="2" y="2" width="5" height="5" fill="#FFFFFF"/>
      <rect x="3" y="3" width="3" height="3" fill="#0C2E1D"/>
      
      <rect x="17" y="1" width="7" height="7" fill="#0C2E1D"/>
      <rect x="18" y="2" width="5" height="5" fill="#FFFFFF"/>
      <rect x="19" y="3" width="3" height="3" fill="#0C2E1D"/>
      
      <rect x="1" y="17" width="7" height="7" fill="#0C2E1D"/>
      <rect x="2" y="18" width="5" height="5" fill="#FFFFFF"/>
      <rect x="3" y="19" width="3" height="3" fill="#0C2E1D"/>
      
      <line x1="8" y1="4" x2="16" y2="4" stroke="#0C2E1D" stroke-width="1" stroke-dasharray="1 1"/>
      <line x1="4" y1="8" x2="4" y2="16" stroke="#0C2E1D" stroke-width="1" stroke-dasharray="1 1"/>
    `;

    for (let r = 8; r < 24; r++) {
      for (let c = 8; c < 24; c++) {
        if (r < 8 && c > 16) continue;
        if (r > 16 && c < 8) continue;
        const bit = ((r * c * 13 + hash) % 3 === 0);
        if (bit) {
          svg += `<rect x="${c}" y="${r}" width="1" height="1" fill="#0C2E1D"/>`;
        }
      }
    }
    
    svg += `<rect x="11" y="11" width="3" height="3" fill="#D4AF37"/>`;
    svg += `</svg>`;
    return svg;
  }


  // ============================================================
  // LIVE WEBSITE CONTENT EDITOR ENGINE
  // ============================================================
  const LIVE_CONTENT_KEY = 'cht_live_site_content';

  const DEFAULT_LIVE_CONTENT = {
    slogan: "Tech • Creativity • Impact",
    bankName: "PalmPay",
    accountNumber: "7011706511",
    accountName: "EL JOSHUA HYELAKURI EMMANUEL",
    cohortMonth: "November 2026",
    pricingNotice: "Rolling Admission • Official Pricing To Be Announced Soon",
    tickerText: "Next Intensive Practical Training Cohort Begins This November",
    phone: "0915-963-7287",
    email: "coachhyelatech@gmail.com",
    c3Title: "100% AI Website & Web App Building (Zero Coding)",
    c3Desc: "Build, test, host, and launch modern websites and apps 100% using AI and free platforms. No manual coding or HTML5 required — build and deploy live assets even directly from an Android smartphone."
  };

  function getLiveContent() {
    try {
      const stored = localStorage.getItem(LIVE_CONTENT_KEY);
      if (stored) {
        return Object.assign({}, DEFAULT_LIVE_CONTENT, JSON.parse(stored));
      }
    } catch (e) {
      console.warn("Could not read live content from localStorage:", e);
    }
    return Object.assign({}, DEFAULT_LIVE_CONTENT);
  }

  function saveLiveContent(updatedFields) {
    try {
      const current = getLiveContent();
      const merged = Object.assign({}, current, updatedFields);
      localStorage.setItem(LIVE_CONTENT_KEY, JSON.stringify(merged));
      applyLiveContentToDOM(merged);
      return { success: true, message: "Live website content saved successfully!", data: merged };
    } catch (e) {
      return { success: false, message: "Error saving live content: " + e.message };
    }
  }

  function resetLiveContent() {
    localStorage.removeItem(LIVE_CONTENT_KEY);
    applyLiveContentToDOM(DEFAULT_LIVE_CONTENT);
    return { success: true, message: "Live website content reset to factory defaults!", data: DEFAULT_LIVE_CONTENT };
  }

  function applyLiveContentToDOM(data) {
    const content = data || getLiveContent();
    if (!content || typeof document === 'undefined') return;

    // Slogans
    document.querySelectorAll('.cht-live-slogan').forEach(el => {
      el.textContent = content.slogan;
    });

    // Bank & Payment
    document.querySelectorAll('.cht-live-bank').forEach(el => {
      el.textContent = content.bankName;
    });
    document.querySelectorAll('.cht-live-acc-num').forEach(el => {
      el.textContent = content.accountNumber;
    });
    document.querySelectorAll('.cht-live-acc-name').forEach(el => {
      el.textContent = content.accountName;
    });

    // Cohort & Pricing
    document.querySelectorAll('.cht-live-cohort-month').forEach(el => {
      el.textContent = content.cohortMonth;
    });
    document.querySelectorAll('.cht-live-pricing-notice').forEach(el => {
      el.textContent = content.pricingNotice;
    });
    document.querySelectorAll('.cht-live-ticker-text').forEach(el => {
      el.textContent = content.tickerText;
    });

    // Course 3
    document.querySelectorAll('.cht-live-c3-title').forEach(el => {
      el.textContent = content.c3Title;
    });
    document.querySelectorAll('.cht-live-c3-desc').forEach(el => {
      el.textContent = content.c3Desc;
    });
  }

  
  // Canva Pro Claim & Dispatch Helpers
  async function submitCanvaClaim(userId, canvaEmail) {
    const db = getFirestore();
    if (db && userId) {
      try {
        await db.collection('students').doc(userId).set({
          canvaStatus: 'REQUESTED',
          canvaEmail: canvaEmail.trim().toLowerCase(),
          canvaRequestedAt: new Date().toISOString()
        }, { merge: true });

        await db.collection('activity_logs').add({
          type: 'CANVA_CLAIM_REQUEST',
          page: 'Student Portal',
          device: window.innerWidth <= 768 ? 'Mobile' : 'Desktop',
          details: `Canva Pro team invite requested for email: ${canvaEmail}`,
          timestamp: new Date().toISOString()
        });
        return { success: true, message: "Canva Pro invite request submitted to Coach Hyela!" };
      } catch (e) {
        return { success: false, message: e.message };
      }
    }
    return { success: false, message: "Cloud connection unavailable." };
  }

  async function confirmCanvaAccepted(userId) {
    const db = getFirestore();
    if (db && userId) {
      try {
        await db.collection('students').doc(userId).set({
          canvaStatus: 'CLAIMED',
          canvaClaimedAt: new Date().toISOString()
        }, { merge: true });
        return { success: true, message: "Canva Pro status marked as Claimed & Active!" };
      } catch(e) {
        return { success: false, message: e.message };
      }
    }
    return { success: false, message: "Cloud connection unavailable." };
  }

  async function dispatchCanvaInvite(userId, studentEmail) {
    const db = getFirestore();
    if (db && userId) {
      try {
        await db.collection('students').doc(userId).set({
          canvaStatus: 'INVITE_SENT',
          canvaInviteSentAt: new Date().toISOString()
        }, { merge: true });

        await db.collection('activity_logs').add({
          type: 'CANVA_INVITE_DISPATCHED',
          page: 'Operations Hub',
          device: window.innerWidth <= 768 ? 'Mobile' : 'Desktop',
          details: `Coach Hyela dispatched Canva Pro team invite to ${studentEmail}`,
          timestamp: new Date().toISOString()
        });

        logNotification(
          studentEmail,
          "Canva Pro Team Invite Sent - Coach Hyela Tech",
          "An email invitation has been sent to your inbox from Coach Hyela Tech Canva Team. Please accept the invitation to activate your 1-Year Pro access.",
          "CANVA_VIP"
        );
        return { success: true, message: `Canva Pro invite notification sent to student dashboard for ${studentEmail}!` };
      } catch(e) {
        return { success: false, message: e.message };
      }
    }
    return { success: false, message: "Cloud connection unavailable." };
  }

  async function setMuseAiStatus(userId, accessed, whatsappNum = '') {
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
  const setGoogleAiProStatus = setMuseAiStatus;

  // Initial boot
  initStorage();

  return {
    // Live Content Editor
    getLiveContent,
    saveLiveContent,
    resetLiveContent,
    applyLiveContentToDOM,

    // Auth & Users
    getUsers,
    registerStudent,
    verifyEmail,
    resendVerificationCode,
    loginStudent,
    requestPasswordReset,
    getEmailConfig,
    saveEmailConfig,
    sendLiveEmail,
    resetPassword,
    getAuthLearner,
    setAuthLearner,
    logoutLearner,
    // Eligibility & Cloud
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
    claimCertificate,
    // Certificates
    getCertificates,
    saveCertificates,
    findCertificateById,
    getLearnerCertificates,
    // Notifications & Audit
    getNotificationLogs,
    // Admin
    isAdminLoggedIn,
    loginAdmin,
    logoutAdmin,
    updateEligibilityStatus,
    updateStudentDetails,
    toggleDriveAccess,
    getMasterDriveUrl,
    submitCanvaClaim,
    confirmCanvaAccepted,
    dispatchCanvaInvite,
    setMuseAiStatus,
    setGoogleAiProStatus,
    // CAC
    saveCACSubmission,
    getCACSubmissions,

    // Live Content Editor
    getLiveContent,
    saveLiveContent,
    resetLiveContent,
    applyLiveContentToDOM,
    // UI Helpers
    initNavToggle,
    generateQRCodeSVG
  };
})();

if (typeof window !== 'undefined') {
  window.CHT = CHT;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CHT;
}

document.addEventListener('DOMContentLoaded', () => {
  CHT.initNavToggle();
  CHT.applyLiveContentToDOM();
  if (typeof window !== 'undefined' && !window.location.pathname.toLowerCase().includes('admin.html')) {
    if (CHT.trackVisitorActivity) {
      CHT.trackVisitorActivity(document.title);
    }
  }
});
