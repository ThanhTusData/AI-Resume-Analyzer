import re

EMAIL_RE = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
PHONE_RE = re.compile(r'(\+?\d{1,4}[\s\-]?)?(\(?\d{2,4}\)?[\s\-]?)?[\d\s\-]{6,14}')

def extract_emails(text):
    return list({m.group(0) for m in EMAIL_RE.finditer(text)}) if text else []

def extract_phones(text):
    phones = [m.group(0) for m in PHONE_RE.finditer(text or "")]
    # cleanup
    phones = [re.sub(r'\s+', '', p) for p in phones]
    return list(dict.fromkeys(phones))

def first_nonempty_line(text):
    if not text:
        return ""
    for line in text.splitlines():
        s = line.strip()
        if s:
            return s
    return ""
