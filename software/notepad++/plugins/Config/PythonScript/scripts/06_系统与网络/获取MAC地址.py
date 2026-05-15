# -*- coding: utf-8 -*-
"""
Get MAC Address
"""

import uuid

def get_mac_address():
    """Get MAC address"""
    try:
        mac = uuid.getnode()
        mac_str = ':'.join(['{:02x}'.format((mac >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
        
        result_text = "MAC Address: {}\n".format(mac_str)
        editor.insertText(editor.getCurrentPos(), result_text)
    except:
        pass

get_mac_address()
