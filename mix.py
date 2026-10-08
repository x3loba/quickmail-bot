# language: Python, file: mix.py
import aioimaplib

# Known IMAP servers per domain
DOMAIN_TO_IMAP = {
    "gmail.com":       ("imap.gmail.com", 993),
    "googlemail.com":  ("imap.gmail.com", 993),
    "outlook.com":     ("outlook.office365.com", 993),
       "hotmail.com":     ("outlook.office365.com "",a 993),
    "live.com":        ("outlook.office365.com", 993),
    "msn.com":         ("outlook.office365.com", 993),
    "yahoo.com":       ("imap.mail.yahoo.com", 993),
    "ymail.com":       ("imap.mail.yahoo.com", 993),
    "rocketmail.com":  ("imap.mail.yahoo.com", 993),
ol.com":         ("imap.aol.com", 993),
    "aim.com":         ("imap.aol.com", 993),
    "yandex.com":      ("imap.yandex.com", 993),
    "yandex.ru":       ("imap.yandex.ru", 993),
    "ya.ru":           ("imap.yandex.ru", 993),
    "gmx.com":         ("imap.gmx.com", 993),
    "gmx.net":         ("imap.gmx.net", 993),
    "gmx.de":          ("imap.gmx.net", 993),
    "web.de":          ("imap.web.de", 993),
    "mail.com":        ("imap.mail.com", 993),
    "zoho.com":        ("imap.zoho.com", 993),
    "zohomail.com":    ("imap.zoho.com", 993),
    "icloud.com":      ("imap.mail.me.com", 993),
    "me.com":          ("imap.mail.me.com", 993),
    "mac.com":         ("imap.mail.me.com", 993),
    "protonmail.com":  ("127.0.0.1", 1143),   # needs Proton Bridge
    "proton.me":       ("127.0.0.1", 1143),
    "tutanota.com":    ("imap.tutanota.com", 993),
    "tuta.io":         ("imap.tutanota.com", 993),
    "fastmail.com":    ("imap.fastmail.com", 993),
    "fastmail.fm":     ("imap.fastmail.com", 993),
    "hushmail.com":    ("imap.hushmail.com", 993),
    "runbox.com":      ("imap.runbox.com", 993),
    "mail.ru":         ("imap.mail.ru", 993),
    "inbox.ru":        ("imap.mail.ru", 993),
    "list.ru":         ("imap.mail.ru", 993),
    "bk.ru":           ("imap.mail.ru", 993),
    "rambler.ru":      ("imap.rambler.ru", 993),
    "ukr.net":         ("imap.ukr.net", 993),
    "i.ua":            ("imap.i.ua", 993),
    "seznam.cz":       ("imap.seznam.cz", 993),
    "wp.pl":           ("imap.wp.pl", 993),
    "o2.pl":           ("imap.o2.pl", 993),
    "interia.pl":      ("imap.interia.pl", 993),
    "onet.pl":         ("imap.poczta.onet.pl", 993),
    "libero.it":       ("imap.libero.it", 993),
    "virgilio.it":     ("imap.virgilio.it", 993),
    "tiscali.it":      ("imap.tiscali.it", 993),
    "alice.it":        ("imap.alice.it", 993),
    "tin.it":          ("imap.tin.it", 993),
    "orange.fr":       ("imap.orange.fr", 993),
    "wanadoo.fr":      ("imap.orange.fr", 993),
    "free.fr":         ("imap.free.fr", 993),
    "laposte.net":     ("imap.laposte.net", 993),
    "sfr.fr":          ("imap.sfr.fr", 993),
    "bbox.fr":         ("imap.bbox.fr", 993),
    "t-online.de":     ("secureimap.t-online.de", 993),
    "freenet.de":      ("imap.freenet.de", 993),
    "arcor.de":        ("imap.arcor.de", 993),
    "1und1.de":        ("imap.1und1.de", 993),
    "ionos.com":       ("imap.ionos.com", 993),
    "ionos.de":        ("imap.ionos.de", 993),
    "btinternet.com":  ("mail.btinternet.com", 993),
    "sky.com":         ("imap.tools.sky.com", 993),
    "virginmedia.com": ("imap.virginmedia.com", 993),
    "talktalk.net":    ("imap.talktalk.net", 993),
    "ntlworld.com":    ("imap.ntlworld.com", 993),
    "blueyonder.co.uk":("imap.blueyonder.co.uk", 993),
    "comcast.net":     ("imap.comcast.net", 993),
    "verizon.net":     ("incoming.verizon.net", 993),
    "att.net":         ("imap.mail.att.net", 993),
    "sbcglobal.net":   ("imap.mail.att.net", 993),
    "bellsouth.net":   ("imap.mail.att.net", 993),
    "cox.net":         ("imap.cox.net", 993),
    "charter.net":     ("imap.charter.net", 993),
    "earthlink.net":   ("imap.earthlink.net", 993),
    "juno.com":        ("imap.juno.com", 993),
    "netzero.net":     ("imap.netzero.net", 993),
    "shaw.ca":         ("imap.shaw.ca", 993),
    "telus.net":       ("imap.telus.net", 993),
    "rogers.com":      ("imap.rogers.com", 993),
    "bell.net":        ("imap.bell.net", 993),
    "bigpond.com":     ("imap.telstra.com", 993),
    "optusnet.com.au": ("imap.optusnet.com.au", 993),
    "qq.com":          ("imap.qq.com", 993),
    "163.com":         ("imap.163.com", 993),
    "126.com":         ("imap.126.com", 993),
    "sina.com":        ("imap.sina.com", 993),
    "naver.com":       ("imap.naver.com", 993),
    "daum.net":        ("imap.daum.net", 993),
    "hanmail.net":     ("imap.daum.net", 993),
    "rediffmail.com":  ("imap.rediffmail.com", 993),
    "sify.com":        ("imap.sify.com", 993),
}

# Port fallbacks to try if 993 fails
FALLBACK_PORTS = [993, 143]

def domain_of(email):
    return email.split("@", 1)[1].lower()

async def try_imap(host, port, user, pw, use_ssl=True):
    cli = None
    try:
        if use_ssl:
            cli = aioimaplib.IMAP4_SSL(host=host, port=port, timeout=15)
        else:
            cli = aioimaplib.IMAP4(host=host, port=port, timeout=15)
        await cli.wait_hello_from_server()
        r = await cli.login(user, pw)
        if r.result != "OK":
            return None
        await cli.select("INBOX")
        return {"proto": "IMAP", "host": host, "port": port, "ssl": use_ssl}
    except Exception:
        return None
    finally:
        if cli:
            try: await cli.logout()
            except Exception: pass

async def check(user, pw, proxies=None):
    dom = domain_of(user)

    # 1) Known provider — try its server
    if dom in DOMAIN_TO_IMAP:
        host, port = DOMAIN_TO_IMAP[dom]
        r = await try_imap(host, port, user, pw, use_ssl=(port != 143))
        if r:
            return {"email": user, "password": pw, **r}

    # 2) Guess common hostnames
    candidates = [
        (f"imap.{dom}", 993, True),
        (f"imap.{dom}", 143, False),
        (f"mail.{dom}", 993, True),
        (f"mail.{dom}", 143, False),
        (f"imap.mail.{dom}", 993, True),
        (f"pop.{dom}", 995, True),
    ]
    for host, port, ssl in candidates:
        r = await try_imap(host, port, user, pw, use_ssl=ssl)
        if r:
            return {"email": user, "password": pw, **r}

    return None
