<h1 align="center">
  <img src="icon.png" width="48" height="48" align="absmiddle" alt="icon">
  Steam Session Tracker
</h1>

A small Windows app that reads Steam's `streaming_log.txt` and shows your playtime in its own live-updating window: stats, charts (time per game, hours per day, hours of the day you play) and a sortable, filterable session list.

<img width="1143" height="756" alt="image" src="https://github.com/user-attachments/assets/1dcced7e-6940-452e-9e5b-33174fad6305" />

## Features
- Finds your Steam folder automatically (registry, falling back to `C:\Program Files (x86)\Steam`)
- Live updates every few seconds, with a "Playing now" card
- Permanent history: Steam wipes `streaming_log.txt` on big updates, so each launch (and each change while open) merges the log into `%LOCALAPPDATA%\SteamSessionTracker\streaming_log_archive.txt`. Nothing is ever deleted from the archive.
- Rename games (click a name in the Games table); names are saved in `names.json` next to the archive
- Everything stays on your machine

## Download
Grab `SteamSessionTracker.exe` from the **Releases** page. See `CHANGELOG.md` for what's new in each version.
Windows SmartScreen may warn about the unsigned exe. Choose "More info → Run anyway".

## Build it yourself
Requires Python 3.9+ on Windows (and the Edge WebView2 runtime, already on most Windows 10/11 installs).

    build.bat

The exe ends up in `dist\`.

## Files
- `tracker.py`: finds/merges the logs and opens the window (pywebview)
- `template.html`: the dashboard (Chart.js loaded from cdnjs)
- `icon.ico`: the exe/window icon
- `icon.png`: the same icon, used in this README
- `build.bat`: local PyInstaller build
- `CHANGELOG.md`: version history

## Notes
- Game names are only known for a few Steam app IDs; others show as "App 1234" until renamed.
- If Steam closes mid-game, that session is cut off at the last log line before the next Steam launch, so its length is approximate.
- Will not be maintaining this piece of garbage

## AI Disclosure

Parts of this project, including code, documentation, and/or text, were generated with the help of AI tools (such as Claude). All AI-generated content has been reviewed and edited by me, but it may still contain errors or mistakes.
