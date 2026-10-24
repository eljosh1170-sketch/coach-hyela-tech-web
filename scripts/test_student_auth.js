// Mock browser environment for cht-core.js
const storage = {};
global.localStorage = {
  getItem: (k) => storage[k] || null,
  setItem: (k, v) => { storage[k] = String(v); },
  removeItem: (k) => { delete storage[k]; },
  clear: () => { for (let k in storage) delete storage[k]; }
};
global.window = {
  location: { origin: 'http://localhost', pathname: '/certificates.html' }
};
global.document = {
  addEventListener: () => {}
};
global.crypto = require('crypto').webcrypto;

// Load cht-core.js
require('../js/cht-core.js');

const CHT = window.CHT;

async function testAuthFlow() {
  console.log('--- 1. Testing Student Registration ---');
  const regRes = await CHT.registerStudent('Test Student', 'test.student@example.com', 'mypassword123');
  console.log('Registration result:', regRes);
  if (!regRes.success) throw new Error('Registration failed: ' + regRes.message);

  const code = regRes.verificationCode;
  console.log('Verification code received:', code);

  console.log('--- 2. Testing Email Verification ---');
  const verifyRes = CHT.verifyEmail('test.student@example.com', code);
  console.log('Verification result:', verifyRes);
  if (!verifyRes.success) throw new Error('Verification failed: ' + verifyRes.message);

  console.log('--- 3. Testing Student Login ---');
  const loginRes = await CHT.loginStudent('test.student@example.com', 'mypassword123');
  console.log('Login result:', loginRes);
  if (!loginRes.success) throw new Error('Login failed: ' + loginRes.message);

  console.log('--- 4. Testing Student Eligibility Submission ---');
  const eligRes = CHT.submitEligibilityRequest(
    loginRes.user.id,
    loginRes.user.fullName,
    loginRes.user.email,
    'ai-video-ugc',
    'AI Video Creation & UGC-Style Advertising'
  );
  console.log('Eligibility submit result:', eligRes);
  if (!eligRes.success) throw new Error('Eligibility submission failed: ' + eligRes.message);

  console.log('ALL AUTH & STUDENT PORTAL TESTS PASSED PERFECTLY!');
}

testAuthFlow().catch(err => {
  console.error('TEST ERROR:', err);
  process.exit(1);
});
