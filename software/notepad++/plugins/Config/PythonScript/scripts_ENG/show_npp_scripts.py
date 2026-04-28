# -*- coding: utf-8 -*-
import webbrowser

def show_npp_scripts():
    scripts = [
        "https://github.com/notepad-plus-plus/python-plus-plus",  # NPP Python script repository
        "https://github.com/bruderstein/PythonScript/releases",  # PythonScript plugin official repository
        "https://github.com/bruderstein/PythonScript",  # PythonScript plugin official repository
        "https://community.notepad-plus-plus.org/topic/12327/python-script-collection",  # Community script collection
        "https://github.com/vincentbernat/notepadpp-config/tree/master/scripts",  # Personal config script collection
        "https://github.com/search?q=notepad%2B%2B+python+script",  # GitHub NPP Python script search
        "https://stackoverflow.com/questions/tagged/notepad%2B%2B+python",  # Stack Overflow related questions
        "https://sourceforge.net/p/notepad-plus/discussion/python-scripting/",  # SourceForge discussion forum
        "https://npp-user-manual.org/docs/plugin-communication/",  # NPP plugin development documentation
        "https://github.com/topics/notepad-plus-plus-plugin",  # NPP plugin topics
        "https://github.com/Krazal/nppopenai",  # OpenAI (aka. ChatGPT) plugin for Notepad++ 
        "https://github.com/notepad-plus-plus/notepad-plus-plus/wiki/Plugin-Development"  # NPP plugin development Wiki
    ]
    
    # Create HTML file to better display links
    html_content = u"""
    <html>
    <head>
        <title>Notepad++ Python Scripts References</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h2>Notepad++ Python Scripts Reference Resources</h2>
        <ul>
    """
    
    for url in scripts:
        html_content += u'<li><a href="{0}">{0}</a></li>\n'.format(url)
    
    html_content += u"""
        </ul>
    </body>
    </html>
    """
    
    # Save and open HTML file
    with open('npp_script_references.html', 'wb') as f:
        f.write(html_content.encode('utf-8'))
    
    webbrowser.open('npp_script_references.html')

show_npp_scripts()
