# -*- coding: utf-8 -*-
"""
Get System Information
"""

import platform
import sys

def get_system_info():
    """Get system information"""
    info = []
    info.append("System: {}\n".format(platform.system()))
    info.append("Release: {}\n".format(platform.release()))
    info.append("Version: {}\n".format(platform.version()))
    info.append("Architecture: {}\n".format(platform.machine()))
    info.append("Processor: {}\n".format(platform.processor()))
    info.append("Hostname: {}\n".format(platform.node()))
    info.append("Python: {}\n".format(sys.version.split()[0]))
    info.append("\n")
    
    result_text = ''.join(info)
    editor.insertText(editor.getCurrentPos(), result_text)

get_system_info()
