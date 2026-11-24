# Gliding Briefing

A free, single-page soaring forecast and NOTAM briefing tool for glider pilots, packaged as an Android app.
Built around Seighford Gliding Club (Staffordshire, UK), but the site location can be changed in the app.

## What it does

- **Soaring meteogram** in the style of SkySight, drawn from free [Open-Meteo](https://open-meteo.com/) data:
  thermal strength and tops, cloudbase, wind barbs, cloud layers, rain rate and probability, and a wave potential indicator.
- **NOTAM map** showing UK NOTAMs within 50 km of the airfield on OpenStreetMap tiles, with circles and polygons,
  hover or tap pop-ups, and filtering by date and time (including daily schedules such as `FRI SAT 1400-2300`).
  NOTAMs whose lower limit is below the forecast thermal ceiling are tagged.
- **Offline use:** the last forecast and NOTAM data are cached on the phone and shown with their age.

## Important caveats

- **This is not an official briefing source.** The forecast is a model-based guide and the wave and thermal
  figures are simple heuristics. Always check the official NOTAMs, the Met Office forecast and your own
  judgement before flying. Use at your own risk.
- NOTAM data comes from the NATS UK Pre-flight Information Bulletin (`pibs.nats.co.uk`). NATS describes these as
  contingency copies and sets no terms for automated use, so check with the NATS NOTAM Office before
  offering this to others.
- Map tiles are © OpenStreetMap contributors and need an internet connection.

## Repository layout

| Path | Purpose |
|---|---|
| `src/soaring-meteogram.html` | The whole app, one HTML file. Edit this only. |
| `capacitor.config.json` | Capacitor settings (native HTTP so the NATS file loads, safe-area handling). |
| `.github/workflows/build-apk.yml` | Builds a debug APK on GitHub for free. |
| `run.py`, `Soaring Meteogram.command` | One-step launcher for Mac/PC: starts the local server and opens the page. |
| `scripts/` | Helpers that copy the page into the app and build it locally. |
| `BUILD.md` | Step-by-step build and install instructions, and troubleshooting. |

## Getting the app

1. Open the **Actions** tab, choose the latest successful **Build APK** run, and download the `soaring-meteogram-apk` artifact.
2. Unzip it and install `app-debug.apk` on your Android phone (allow installs from your browser or file manager).
3. Each build is signed with a new debug key, so uninstall the previous version first.

See [BUILD.md](BUILD.md) for building on your own computer and for troubleshooting.

## Using it on a Mac or PC

Browsers block pages from reading the NATS NOTAM file directly, so the desktop version needs a tiny local server.
`run.py` starts one and opens the page in your browser, all in one step. It needs only Python 3, which
a Mac prompts you to install the first time if it is missing.

- **Mac:** double-click `Soaring Meteogram.command`. The first time, macOS may refuse; right-click it, choose **Open**, then **Open** again.
  If it says it cannot be executed, run `chmod +x "Soaring Meteogram.command"` once in Terminal.
- **Any system:** run `python3 run.py` in this folder (Windows: `py run.py`).

Leave the window open while you use the page and press Ctrl+C to stop. It serves the same `src/soaring-meteogram.html`
as the Android app and keeps the NOTAM file for 10 minutes between downloads.
The page saves its settings and cached forecast per address, so it uses port 8000 whenever that is free.

## Updating

Change `src/soaring-meteogram.html` and push to `main`. The workflow builds a fresh APK automatically.

## Credits

Weather data: [Open-Meteo](https://open-meteo.com/). Map tiles: © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors.
NOTAMs: NATS UK. Built with [Capacitor](https://capacitorjs.com/).
