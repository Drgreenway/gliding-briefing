// Builds a debug APK with Gradle. Run it through "npm run apk" so the page is copied and synced first.
const { spawnSync } = require('child_process');
const path = require('path');

const win = process.platform === 'win32';
const result = spawnSync(win ? 'gradlew.bat' : './gradlew', ['assembleDebug'], {
  cwd: path.join(__dirname, '..', 'android'),
  stdio: 'inherit',
  shell: win
});
if (result.status === 0) {
  console.log('\nDone. The APK is at android/app/build/outputs/apk/debug/app-debug.apk');
}
process.exit(result.status === null ? 1 : result.status);
