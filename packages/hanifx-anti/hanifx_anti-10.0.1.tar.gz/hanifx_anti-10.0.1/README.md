# Hanifx-Anti v10.0.0

**Hanifx-Anti** is a powerful Python-based security and malware detection framework designed for both Android (via Termux) and desktop platforms (Linux/Windows/macOS). It offers AI-powered malware detection, port/firewall monitoring, phishing/dark web link detection, script scanning, and real-time alerts — all in one tool.

---

## 🔐 Key Features

- ✅ Realtime File Scanner (detects malware and suspicious files)
- ✅ AI-based Malware Prediction (via heuristic scoring)
- ✅ Script Guard (detects obfuscated or harmful code)
- ✅ Phishing and Dark Web Link Detector
- ✅ Firewall & Port Activity Monitoring (with blocking support)
- ✅ Microphone & Camera Watchdog
- ✅ Network Packet Sniffer
- ✅ File & Folder Encryption/Decryption
- ✅ Alert system and full logging engine

---

## 📦 Installation

Install with pip:

```bash
pip install hanifx_anti

from hanifx_anti import start_scan

# Scan device or folder for threats
infected_files = start_scan("/sdcard")

if infected_files:
    print(f"{len(infected_files)} suspicious or malicious files detected!")
else:
    print("✅ Your system is clean.")

from hanifx_anti.core.ai_detect import ai_file_scan

result = ai_file_scan("example.py")
print("Threat detected" if result else "File is safe")

from hanifx_anti.core.firewall import monitor_ports

open_ports = monitor_ports()
if open_ports:
    print("⚠️ Suspicious open ports detected!")

from hanifx_anti.utils.encryptor import encrypt_file, decrypt_file

encrypt_file("sensitive.txt")
decrypt_file("sensitive.txt.enc")
