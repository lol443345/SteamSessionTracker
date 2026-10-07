@echo off
python -m pip install pyinstaller pywebview
python -m PyInstaller --onefile --noconsole --collect-all webview --name SteamSessionTracker --add-data "template.html;." tracker.py
echo.
echo Done! Your exe is in the "dist" folder.
pause
