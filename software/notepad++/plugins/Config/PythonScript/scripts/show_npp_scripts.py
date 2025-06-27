# -*- coding: utf-8 -*-
import webbrowser

def show_npp_scripts():
    scripts = [
        "https://github.com/notepad-plus-plus/python-plus-plus",  # NPP Python脚本仓库
        "https://github.com/bruderstein/PythonScript/releases",  # PythonScript插件官方仓库
        "https://github.com/bruderstein/PythonScript",  # PythonScript插件官方仓库
        "https://community.notepad-plus-plus.org/topic/12327/python-script-collection",  # 社区脚本集合
        "https://github.com/vincentbernat/notepadpp-config/tree/master/scripts",  # 个人配置脚本集合
        "https://github.com/search?q=notepad%2B%2B+python+script",  # GitHub上的NPP Python脚本搜索
        "https://stackoverflow.com/questions/tagged/notepad%2B%2B+python",  # Stack Overflow相关问题
        "https://sourceforge.net/p/notepad-plus/discussion/python-scripting/",  # SourceForge讨论区
        "https://npp-user-manual.org/docs/plugin-communication/",  # NPP插件开发文档
        "https://github.com/topics/notepad-plus-plus-plugin",  # NPP插件主题
        "https://github.com/Krazal/nppopenai",  # OpenAI (aka. ChatGPT) plugin for Notepad++ 
        "https://github.com/notepad-plus-plus/notepad-plus-plus/wiki/Plugin-Development"  # NPP插件开发Wiki
    ]
    
    # 创建HTML文件以更好地展示链接
    html_content = u"""
    <html>
    <head>
        <title>Notepad++ Python Scripts References</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h2>Notepad++ Python Scripts 参考资源</h2>
        <ul>
    """
    
    for url in scripts:
        html_content += u'<li><a href="{0}">{0}</a></li>\n'.format(url)
    
    html_content += u"""
        </ul>
    </body>
    </html>
    """
    
    # 保存并打开HTML文件
    with open('npp_script_references.html', 'wb') as f:
        f.write(html_content.encode('utf-8'))
    
    webbrowser.open('npp_script_references.html')

show_npp_scripts()