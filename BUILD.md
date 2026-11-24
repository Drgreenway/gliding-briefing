# Soaring Meteogram as an Android app

This folder wraps the one-page meteogram in an Android app using Capacitor.
Capacitor puts the page inside a thin native shell. The setting in `capacitor.config.json`
(`CapacitorHttp` enabled) sends the page's web requests through Android's own network code,
so the NATS NOTAM file loads directly, with no server and no browser block.

The page lives in `src/soaring-meteogram.html`. Edit that file only. `www/` and `android/`
are generated and can be deleted at any time.

Nothing here has been built or run on a phone yet. The first build is the real test.

## Route A: build on your own computer

You need Node.js (current LTS, from nodejs.org) and Android Studio (developer.android.com/studio).
Open Android Studio once and let its setup wizard install the Android SDK.

1. Unzip this folder and open a terminal inside it.
2. Install Capacitor:
   ```
   npm install @capacitor/core @capacitor/android
   npm install -D @capacitor/cli
   ```
3. Create the Android project (first time only). This makes the `android/` folder:
   ```
   npx cap add android
   ```
4. Copy the page into the app:
   ```
   npm run sync
   ```
5. Open the project in Android Studio:
   ```
   npm run open
   ```
   Wait for Android Studio to finish its first sync (a progress bar at the bottom). The first run
   downloads Gradle and other parts, so allow several minutes and an internet connection.
6. In Android Studio choose **Build > Build Bundle(s) / APK(s) > Build APK(s)**.
   When it finishes, click **locate** in the pop-up. The file is
   `android/app/build/outputs/apk/debug/app-debug.apk`.
7. Put the APK on your phone (USB cable, Google Drive or email) and open it.
   Android asks you to allow installs from that app. Allow it for this install.
   Play Protect may call the app unrecognised because it is signed with a debug key. Choose to install anyway.

If your phone is plugged in with USB debugging on, `npx cap run android` builds and installs in one step.

## Route B: build for free on GitHub, no Android tools on your computer

1. Make a free GitHub account and a new repository. Private or public both work, since the app contains no secrets.
2. Upload everything in this folder. The hidden `.github` folder must go too. If drag and drop skips it,
   use **Add file > Create new file**, type `.github/workflows/build-apk.yml` as the name, and paste in that file.
3. Open the **Actions** tab, choose **Build APK**, then **Run workflow**. It takes about 5 to 10 minutes.
4. Open the finished run and download the **soaring-meteogram-apk** artifact. It is a zip holding `app-debug.apk`.
   Install it as in step 7 above.

## Updating the app later

Replace `src/soaring-meteogram.html` with the new version, then build again.

- Route A: `npm run sync`, then build the APK again. Installing over the old app keeps its saved settings and data.
- Route B: run the workflow again. GitHub's build machine makes a new debug signing key every run,
  so Android refuses to install over the old app. Uninstall the old one first, which clears its saved
  settings and saved forecast. Ask for a fixed signing key if you want to avoid that.

## If something does not work

- **"Could not fetch NOTAMs" inside the app:** the native web requests are not active. Check that
  `capacitor.config.json` still has `CapacitorHttp` enabled and that you ran `npm run sync` after any edit.
  Send me the exact message.
- **Grey map with no tiles:** set the Map dropdown to CARTO light. OpenStreetMap's tile server may refuse
  requests from an app.
- **Page content sits under the status bar or navigation bar:** tell me which phone and Android version.
- **Fetching the NOTAMs hangs or fails only in the app:** the NATS file is a few megabytes. Tell me how long it took.
- **`npx cap add android` complains about the Node version:** install the current Node LTS.
