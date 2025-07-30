import re
import base64
import zlib

# ডেঞ্জারাস প্যাটার্ন লিস্ট
RISKY_PATTERNS = {
    r'os\.system".*rm -rf.*"': "CRITICAL: Deletes system files",
    r'os\.remove': "WARNING: Deletes local file",
    r'requests\.get"http': "WARNING: External HTTP request",
    r'eval': "DANGEROUS: Arbitrary code execution",
    r'exec': "DANGEROUS: Dynamic execution",
    r'subprocess\.': "CRITICAL: Subprocess execution",
    r'import socket': "WARNING: Opens network access",
}

# ডিকোড ফাংশন
def try_decode(content):
    try:
        decoded = base64.b64decode(content).decode("utf-8")
        return decoded, "base64"
    except:
        pass
    try:
        decoded = zlib.decompress(bytes(content, 'utf-8')).decode("utf-8")
        return decoded, "zlib"
    except:
        return None, None

# থ্রেট ডিটেকশন
def detect_threats(filepath):
    report = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_code = f.read()
    except Exception as e:
        return f"Error reading file: {e}"

    code_to_check = raw_code
    decoded_code, enc_type = try_decode(raw_code)
    if decoded_code:
        report.append(f"[+] Decoded content using {enc_type}")
        code_to_check += "\n" + decoded_code

    lines = code_to_check.splitlines()

    for i, line in enumerate(lines, 1):
        for pattern, risk in RISKY_PATTERNS.items():
            if re.search(pattern, line):
                report.append(f"[!] Risk Detected in Line {i}:")
                report.append(f"    Code: {line.strip()}")
                report.append(f"    Risk: {risk}")

    if not report:
        return "[✓] No threat detected."
    
    return "\n".join(report)
