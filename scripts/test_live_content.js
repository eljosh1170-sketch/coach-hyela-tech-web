const storage = {};
global.localStorage = {
  getItem: (k) => storage[k] || null,
  setItem: (k, v) => { storage[k] = String(v); },
  removeItem: (k) => { delete storage[k]; },
  clear: () => { for (let k in storage) delete storage[k]; }
};
global.window = {
  location: { origin: 'http://localhost', pathname: '/admin.html' }
};
global.document = {
  querySelectorAll: () => [],
  addEventListener: () => {}
};
global.crypto = require('crypto').webcrypto;

require('../js/cht-core.js');
const CHT = window.CHT;

console.log('--- Testing Live Content Editor Engine ---');
const initial = CHT.getLiveContent();
console.log('Initial live bank:', initial.bankName);
console.log('Initial slogan:', initial.slogan);

if (initial.bankName !== 'PalmPay') throw new Error('Expected PalmPay as default bank!');

// Test saving update
const updateRes = CHT.saveLiveContent({
  slogan: "Tech • Creativity • Real Impact",
  bankName: "PalmPay"
});
console.log('Save result:', updateRes);
if (!updateRes.success) throw new Error('Save failed');

const updated = CHT.getLiveContent();
console.log('Updated slogan:', updated.slogan);
if (updated.slogan !== "Tech • Creativity • Real Impact") throw new Error('Slogan was not updated!');

// Test reset
const resetRes = CHT.resetLiveContent();
console.log('Reset result:', resetRes);
if (CHT.getLiveContent().slogan !== "Tech • Creativity • Impact") throw new Error('Reset failed!');

console.log('LIVE CONTENT EDITOR TESTS PASSED PERFECTLY!');
