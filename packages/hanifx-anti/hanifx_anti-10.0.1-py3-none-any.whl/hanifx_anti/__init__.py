# hanifx_anti/__init__.py

from .core.scanner import start_scan, scan_directory
from .core.firewall import monitor_ports, block_port
from .core.darkweb import detect_onion_links, scan_text_file_for_darkweb
from .core.phishing import scan_phishing_url, check_bulk_urls
from .core.ai_detect import ai_file_scan, extract_features
from .core.scriptguard import monitor_scripts, auto_block_script
from .core.mic_cam_watch import watch_microphone_camera, auto_kill_spyware
from .core.network_sniff import sniff_network, analyze_packet

from .utils.logger import log_event, export_logs
from .utils.notifier import notify, email_alert
from .utils.encryptor import encrypt_file, decrypt_file, encrypt_folder, decrypt_folder

__version__ = '10.0.1'
__author__ = 'Hanif'

__all__ = [
    "start_scan", "scan_directory", "monitor_ports", "block_port",
    "detect_onion_links", "scan_text_file_for_darkweb",
    "scan_phishing_url", "check_bulk_urls", "ai_file_scan",
    "extract_features", "monitor_scripts", "auto_block_script",
    "watch_microphone_camera", "auto_kill_spyware", "sniff_network",
    "analyze_packet", "log_event", "export_logs", "notify", "email_alert",
    "encrypt_file", "decrypt_file", "encrypt_folder", "decrypt_folder"
]
