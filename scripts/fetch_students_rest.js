const https = require('https');

const url = 'https://firestore.googleapis.com/v1/projects/coachhyelatech-d3207/databases/(default)/documents/students';

https.get(url, (res) => {
  let data = '';
  res.on('data', chunk => { data += chunk; });
  res.on('end', () => {
    try {
      const json = JSON.parse(data);
      if (json.documents) {
        console.log(`Found ${json.documents.length} student documents:`);
        json.documents.forEach(doc => {
          const fields = doc.fields || {};
          const unwrap = (f) => {
            if (!f) return undefined;
            if (f.stringValue !== undefined) return f.stringValue;
            if (f.booleanValue !== undefined) return f.booleanValue;
            if (f.integerValue !== undefined) return parseInt(f.integerValue);
            return f;
          };
          console.log({
            path: doc.name.split('/').pop(),
            fullName: unwrap(fields.fullName),
            email: unwrap(fields.email),
            vipAccess: unwrap(fields.vipAccess),
            googleAiProAccessed: unwrap(fields.googleAiProAccessed),
            museAiAccessed: unwrap(fields.museAiAccessed),
            flowAccessed: unwrap(fields.flowAccessed),
            canvaStatus: unwrap(fields.canvaStatus)
          });
        });
      } else {
        console.log('No documents found or response:', json);
      }
    } catch(e) {
      console.error('Error parsing JSON:', e, data);
    }
  });
}).on('error', err => {
  console.error('HTTPS error:', err);
});
