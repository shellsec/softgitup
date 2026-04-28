# -*- coding: utf-8 -*-
"""
Get Local IP Address
"""

import socket

def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        
        result_text = "Local IP: {}\n".format(ip)
        editor.insertText(editor.getCurrentPos(), result_text)
    except:
        pass

get_local_ip()
