import os, re, sys, json

LOG_NAME = "streaming_log.txt"
APP_DIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "SteamSessionTracker")
NAMES_FILE = os.path.join(APP_DIR, "names.json")
ARCHIVE = os.path.join(APP_DIR, "streaming_log_archive.txt")
TS = re.compile(r"^\[\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\]")

def steam_dir():
    default = r"C:\Program Files (x86)\Steam"
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as k:
            p = winreg.QueryValueEx(k, "SteamPath")[0]
            if os.path.isdir(p):
                return os.path.normpath(p)
    except Exception:
        pass
    return default

LOG_PATH = os.path.join(steam_dir(), "logs", LOG_NAME)

def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""

def merge(old, new):
    """Union of two logs: duplicate lines dropped, ordered by timestamp (stable)."""
    seen, items = set(), []
    for src in (old, new):
        ts = ""
        for line in src.splitlines():
            line = line.rstrip()
            if not line:
                continue
            m = TS.match(line)
            if m:
                ts = m.group(0)
            if line in seen:
                continue
            seen.add(line)
            items.append((ts, len(items), line))
    items.sort(key=lambda t: (t[0], t[1]))
    return "\n".join(t[2] for t in items) + "\n" if items else ""

_sig, _text = None, ""

def sync():
    """Merge Steam's current log into the permanent archive; return the full history."""
    global _sig, _text
    try:
        st = os.stat(LOG_PATH)
        sig = (st.st_mtime_ns, st.st_size)
    except OSError:
        sig = None
    if _text and sig == _sig:
        return _text
    _sig = sig
    archive = read(ARCHIVE)
    merged = merge(archive, read(LOG_PATH)) if sig else archive
    if merged != archive:
        os.makedirs(APP_DIR, exist_ok=True)
        tmp = ARCHIVE + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(merged)
        os.replace(tmp, ARCHIVE)
    _text = merged
    return merged

class Api:
    def get_log(self):
        return sync()

    def get_names(self):
        try:
            with open(NAMES_FILE, encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            return {}

    def set_names(self, names):
        try:
            os.makedirs(APP_DIR, exist_ok=True)
            with open(NAMES_FILE, "w", encoding="utf-8") as fh:
                json.dump(names, fh)
        except OSError:
            pass

def main():
    import webview
    if not sync():
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, f"Couldn't find:\n{LOG_PATH}", "Steam Session Tracker", 0x10)
        return
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(base, "template.html"), encoding="utf-8") as fh:
        html = fh.read().replace("/*__LIVE__*/false", "true", 1)
    os.makedirs(APP_DIR, exist_ok=True)
    page = os.path.join(APP_DIR, "report.html")
    with open(page, "w", encoding="utf-8") as fh:
        fh.write(html)
    webview.create_window("Steam Session Tracker", page, js_api=Api(),
                          width=1200, height=860, min_size=(700, 500), background_color="#0d0f17")
    webview.start()

if __name__ == "__main__":
    main()
