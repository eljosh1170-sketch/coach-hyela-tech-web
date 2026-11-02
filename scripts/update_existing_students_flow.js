const https = require('https');

const listUrl = 'https://firestore.googleapis.com/v1/projects/coachhyelatech-d3207/databases/(default)/documents/students';

function patchStudent(docPath, updateFields) {
  return new Promise((resolve, reject) => {
    const fields = {};
    const fieldPaths = [];
    for (const [k, v] of Object.entries(updateFields)) {
      fieldPaths.push(`updateMask.fieldPaths=${encodeURIComponent(k)}`);
      if (typeof v === 'boolean') {
        fields[k] = { booleanValue: v };
      } else if (typeof v === 'string') {
        fields[k] = { stringValue: v };
      }
    }

    const path = `https://firestore.googleapis.com/v1/${docPath}?${fieldPaths.join('&')}`;
    const url = new URL(path);
    const postData = JSON.stringify({ fields });

    const req = https.request({
      hostname: url.hostname,
      port: 443,
      path: url.pathname + url.search,
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    }, res => {
      let body = '';
      res.on('data', d => { body += d; });
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(JSON.parse(body));
        } else {
          reject(new Error(`Failed ${res.statusCode}: ${body}`));
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

https.get(listUrl, res => {
  let body = '';
  res.on('data', d => { body += d; });
  res.on('end', async () => {
    try {
      const data = JSON.parse(body);
      if (!data.documents) {
        console.log('No students found');
        return;
      }
      for (const doc of data.documents) {
        const studentId = doc.name.split('/').pop();
        const f = doc.fields || {};
        const isVip = f.vipAccess && f.vipAccess.booleanValue;
        const name = (f.fullName && f.fullName.stringValue) || studentId;
        
        if (isVip) {
          console.log(`Setting flowAccessed=true on VIP student: ${name} (${studentId})`);
          await patchStudent(doc.name.replace('projects/coachhyelatech-d3207/databases/(default)/documents/', 'projects/coachhyelatech-d3207/databases/(default)/documents/'), {
            flowAccessed: true,
            googleAiProAccessed: true
          });
          console.log(`✓ Updated ${name}`);
        }
      }
      console.log('All verified students updated with flowAccessed=true');
    } catch(e) {
      console.error('Error:', e);
    }
  });
});
