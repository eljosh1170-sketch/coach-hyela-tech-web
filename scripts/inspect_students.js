const admin = require('firebase-admin');
const serviceAccount = require('../serviceAccountKey.json');

if (!admin.apps.length) {
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
  });
}

const db = admin.firestore();

async function run() {
  console.log('--- FIRESTORE STUDENTS ---');
  const snapshot = await db.collection('students').get();
  console.log('Total students:', snapshot.size);
  snapshot.forEach(doc => {
    const d = doc.data();
    console.log(JSON.stringify({
      id: doc.id,
      fullName: d.fullName,
      email: d.email,
      vipAccess: d.vipAccess,
      googleAiProAccessed: d.googleAiProAccessed,
      museAiAccessed: d.museAiAccessed,
      flowAccessed: d.flowAccessed,
      flowStatus: d.flowStatus,
      raw: d
    }, null, 2));
  });

  console.log('\n--- FIRESTORE ELIGIBILITY REQUESTS ---');
  const reqSnap = await db.collection('eligibility_requests').get();
  console.log('Total eligibility requests:', reqSnap.size);
  reqSnap.forEach(doc => {
    const d = doc.data();
    console.log(JSON.stringify({
      id: doc.id,
      studentName: d.studentName || d.fullName,
      studentEmail: d.studentEmail || d.email,
      packageTier: d.packageTier,
      status: d.status,
      timestamp: d.timestamp
    }));
  });
}

run().then(() => process.exit(0)).catch(e => {
  console.error(e);
  process.exit(1);
});
