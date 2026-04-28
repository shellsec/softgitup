# -*- coding: utf-8 -*-
"""
Get Public IP Address
"""

import urllib.request
import json

def get_public_ip():
    """Get public IP address"""
    services = [
        'https://api.ipify.org?format=json',
        'https://httpbin.org/ip',
        'https://icanhazip.com'
    ]
    
    for url in services:
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(req, timeout=5) as response:
                result = response.read().decode('utf-8').strip()
                
                # Parse JSON response
                if '{' in result:
                    data = json.loads(result)
                    ip = data.get('ip') or data.get('origin', '').split(',')[0].strip()
                else:
                    ip = result
                
                if ip:
                    result_text = "Public IP: {}\n".format(ip)
                    editor.insertText(editor.getCurrentPos(), result_text)
                    return
        except:
            continue

get_public_ip()
