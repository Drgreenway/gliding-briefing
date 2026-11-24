// Copies the page into www/index.html, which is the folder Capacitor packages into the app.
// The page itself lives in src/soaring-meteogram.html. Edit that file, never www/.
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const from = path.join(root, 'src', 'soaring-meteogram.html');
const to = path.join(root, 'www', 'index.html');

if (!fs.existsSync(from)) {
  console.error('Missing ' + from);
  process.exit(1);
}
fs.mkdirSync(path.dirname(to), { recursive: true });
fs.copyFileSync(from, to);
console.log('Copied page to www/index.html (' + fs.statSync(to).size + ' bytes)');
