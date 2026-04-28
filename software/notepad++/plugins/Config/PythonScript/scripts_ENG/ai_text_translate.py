# -*- coding: utf-8 -*-
"""
AI Text Translate
Use AI to translate selected text (supports Chinese-English translation)
"""

import json
import os
import urllib.request
import urllib.parse

def get_api_key():
    """Get API key"""
    config_file = os.path.join(os.path.dirname(__file__), 'ai_config.json')
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get("api_key", "")
        except:
            pass
    
    # If not configured, prompt user to input
    api_key = notepad.prompt(
        "First time use requires OpenAI API key configuration\n\n"
        "Please enter your OpenAI API key:\n"
        "(Available at https://platform.openai.com/api-keys)",
        "API Configuration",
        ""
    )
    
    if api_key:
        # Save configuration
        config = {
            "api_key": api_key,
            "api_base": "https://api.openai.com/v1",
            "model": "gpt-3.5-turbo"
        }
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    return api_key

def translate_text():
    """Translate text"""
    selected_text = editor.getSelText()
    
    if not selected_text:
        notepad.messageBox(
            "Please select text to translate",
            "AI Text Translate",
            0
        )
        return
    
    # Get full configuration
    config_file = os.path.join(os.path.dirname(__file__), 'ai_config.json')
    config = {
        "api_key": "",
        "api_base": "https://api.openai.com/v1/chat/completions",
        "model": "gpt-3.5-turbo"
    }
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                config.update(user_config)
        except:
            pass
    
    api_key = config.get("api_key", "")
    if not api_key:
        api_key = get_api_key()
        if not api_key:
            notepad.messageBox("API key not configured", "Error", 0)
            return
    
    # Detect language and select translation direction
    # Simple detection: if contains Chinese characters, translate to English; otherwise translate to Chinese
    has_chinese = any('\u4e00' <= char <= '\u9fff' for char in selected_text)
    
    if has_chinese:
        target_lang = "English"
        prompt = "Please translate the following Chinese text to English, maintaining the original meaning and format:"
    else:
        target_lang = "Chinese"
        prompt = "Please translate the following English text to Chinese, maintaining the original meaning and format:"
    
    # Let user choose
    choice = notepad.prompt(
        "Detected text may be {}, please select:\n1.Translate to Chinese 2.Translate to English 3.Auto detect".format(
            "Chinese" if has_chinese else "English"
        ),
        "Translation Direction",
        "3"
    )
    
    # Process user input (extract number)
    if choice:
        import re
        match = re.search(r'\d+', choice)
        if match:
            choice = match.group()
        else:
            choice = choice.strip()
    
    if choice == "1":
        target_lang = "Chinese"
        prompt = "Please translate the following text to Chinese, maintaining the original meaning and format:"
    elif choice == "2":
        target_lang = "English"
        prompt = "Please translate the following text to English, maintaining the original meaning and format:"
    
    # Build request URL
    api_base = config.get("api_base", "https://api.openai.com/v1/chat/completions").rstrip('/')
    if '/chat/completions' in api_base:
        url = api_base
    else:
        url = "{}/chat/completions".format(api_base)
    
    data = {
        "model": config.get("model", "gpt-3.5-turbo"),
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": selected_text}
        ],
        "temperature": 0.3,  # Translation uses lower temperature for more accurate results
        "max_tokens": 2000
    }
    
    try:
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=json_data, method='POST')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', 'Bearer {}'.format(api_key))
        
        notepad.messageBox("Translating, please wait...", "AI Text Translate", 0)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            translated = result["choices"][0]["message"]["content"]
            
            # Ask if replace original text
            choice = notepad.messageBox(
                "Translation complete!\n\nTranslation result:\n{}\n\nReplace selected original text?".format(translated[:100] + "..." if len(translated) > 100 else translated),
                "AI Text Translate",
                4  # Yes/No
            )
            
            editor.beginUndoAction()
            try:
                if choice == 5:  # Yes (5=Yes, 6=No)
                    editor.replaceSel(translated)
                else:
                    # Insert after selected text
                    editor.insertText(editor.getSelectionEnd(), "\n\n[Translation Result]\n" + translated)
            finally:
                editor.endUndoAction()
    
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode('utf-8')
        notepad.messageBox(
            "API request failed:\n{}\n\nPlease check if API key is correct".format(error_msg),
            "Error",
            0
        )
    except Exception as e:
        notepad.messageBox(
            "Request failed:\n{}\n\nPlease check network connection".format(str(e)),
            "Error",
            0
        )

translate_text()

