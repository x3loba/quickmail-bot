# language: Python, file: scanner.py
import json, email
from email.header import decode_header

def load_keywords(path="keywords.json"):
    return json.load(open(path))

def _dec(s):
    if not s:
        return ""
    return "".join(
        t.decode(e or "utf-8", errors="replace") if isinstance(t, bytes) else t
        for t, e in decode_header(s)
    )

def parse_msg(raw_bytes):
    m = email.message_from_bytes(raw_bytes)
    sender = _dec(m.get("From"))
    subject = _dec(m.get("Subject"))
    body = ""
    if m.is_multipart():
        for p in m.walk():
            if p.get_content_type() == "text/plain":
                body = (p.get_payload(decode=True) or b"").decode(
                    p.get_content_charset() or "utf-8", errors="replace")
                break
    else:
        body = (m.get_payload(decode=True) or b"").decode(
            m.get_content_charset() or "utf-8", errors="replace")
    return sender, subject, body

def match(sender, subject, body, kw):
    s, subj, b = sender.lower(), subject.lower(), body.lower()
    hits = []
    for x in kw.get("by_sender", []):
        if x.lower() in s:
            hits.append(("sender", x))
    for x in kw.get("by_phrase", []):
        if x.lower() in s or x.lower() in subj or x.lower() in b:
            hits.append(("phrase", x))
    for x in kw.get("by_sender_subject", []):
        a, _, c = x.partition("=")
        if a.lower() in s and c.lower() in subj:
            hits.append(("sender+subject", x))
    for x in kw.get("by_sender_body", []):
        a, _, c = x.partition("==")
        if a.lower() in s and c.lower() in b:
            hits.append(("sender+body", x))
    return hits
