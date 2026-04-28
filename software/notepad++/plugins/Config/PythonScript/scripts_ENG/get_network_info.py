# -*- coding: utf-8 -*-
"""
Get Network Information
"""

import socket
import subprocess
import sys

def get_network_info():
    """Get network information"""
    info = []
    
    try:
        hostname = socket.gethostname()
        info.append("Hostname: {}\n".format(hostname))
        
        local_ips = socket.gethostbyname_ex(hostname)[2]
        local_ips = [ip for ip in local_ips if not ip.startswith('127.')]
        if local_ips:
            info.append("Local IPs: {}\n".format(', '.join(local_ips)))
    except:
        pass
    
    if sys.platform == 'win32':
        try:
            result = subprocess.run(['ipconfig'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
            lines = result.stdout.split('\n')
            for i, line in enumerate(lines):
                if 'IPv4' in line or ('IP Address' in line and ':' in line):
                    ip = line.split(':')[-1].strip()
                    if ip and ip != '0.0.0.0' and not ip.startswith('127.'):
                        info.append("IP: {}\n".format(ip))
                elif 'Default Gateway' in line and ':' in line:
                    gateway = line.split(':')[-1].strip()
                    if gateway:
                        info.append("Gateway: {}\n".format(gateway))
                elif 'DNS Servers' in line and ':' in line:
                    dns = line.split(':')[-1].strip()
                    if dns:
                        info.append("DNS: {}\n".format(dns))
        except:
            pass
    
    result_text = ''.join(info) if info else "No network information found.\n"
    result_text += "\n"
    
    editor.insertText(editor.getCurrentPos(), result_text)

get_network_info()
