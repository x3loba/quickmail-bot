# language: Python, file: reports.py
import os, zipfile, time

OUT = "reports"
os.makedirs(OUT, exist_ok=True)

def write_all_valid(valid):
    p = f"{OUT}/all_valid.txt"
    with open(p, "w") as f:
        for v in valid:
            f.write(f"{v['email']}:{v['password']}\n")
    return p

def write_countries(valid):
    by_cc = {}
    for v in valid:
        cc = (v.get("country") or "XX").upper()
        by_cc.setdefault(cc, []).append(f"{v['email']}:{v['password']}")
    zp = f"{OUT}/countries_{int(time.time())}.zip"
    with zipfile.ZipFile(zp, "w") as z:
        for cc, lines in by_cc.items():
            z.writestr(f"{cc}.txt", "\n".join(lines))
    return zp

def open_inbox_links(valid):
    p = f"{OUT}/open_inbox.txt"
    with open(p, "w") as f:
        for v in valid:
            host = v.get("host", "outlook.office365.com")
            if "gmail" in host:
                url = "https://mail.google.com"
            elif "yahoo" in host:
                url = "https://mail.yahoo.com"
            elif "aol" in host:
                url = "https://mail.aol.com"
            elif "yandex" in host:
                url = "https://mail.yandex.com"
            elif "icloud" in host or "me.com" in host:
                url = "https://www.icloud.com/mail"
            elif "gmx" in host:
                url = "https://www.gmx.com"
            elif "zoho" in host:
                url = "https://mail.zoho.com"
            elif "office365" in host or "outlook" in host:
                url = "https://outlook.office.com/mail/inbox"
            else:
                url = f"https://{host}"
            f.write(f"{url}  |  {v['email']}:{v['password']}\n")
    return p
