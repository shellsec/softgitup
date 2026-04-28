# -*- coding: utf-8 -*-
"""
AI Text Summarize
Use AI to summarize selected text and extract key information
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

def summarize_text():
    """Summarize text"""
    selected_text = editor.getSelText()
    
    if not selected_text:
        notepad.messageBox(
            "Please select text to summarize",
            "AI Text Summarize",
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
    
    # Select summary type
    summary_type = notepad.prompt(
        "Select summary type:\n1.Brief 2.Detailed 3.Bullet Points 4.Custom",
        "Summary Type",
        "2"
    )
    
    if summary_type is None:
        return
    
    # Process user input (extract number)
    if summary_type:
        import re
        match = re.search(r'\d+', summary_type)
        if match:
            summary_type = match.group()
        else:
            summary_type = summary_type.strip()
    
    prompts = {
        "1": "Please briefly summarize the main content of the following text in 1-2 sentences:",
        "2": "Please summarize the main content of the following text in detail, extract key information, answer in paragraph form:",
        "3": "Please summarize the main content of the following text, list in bullet points:",
        "4": ""
    }
    
    if summary_type == "4":
        custom_prompt = notepad.prompt(
            "Enter custom summary requirements:",
            "Custom Summary",
            "Please summarize the following text:"
        )
        if not custom_prompt:
            return
        prompt = custom_prompt
    else:
        prompt = prompts.get(summary_type, prompts["2"])
    
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
        "temperature": 0.5,
        "max_tokens": 1000
    }
    
    try:
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=json_data, method='POST')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', 'Bearer {}'.format(api_key))
        
        notepad.messageBox("Summarizing, please wait...", "AI Text Summarize", 0)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            summary = result["choices"][0]["message"]["content"]
            
            # Ask if insert result
            choice = notepad.messageBox(
                "Summary complete! Insert result to end of document?",
                "AI Text Summarize",
                4  # Yes/No
            )
            
            editor.beginUndoAction()
            try:
                if choice == 5:  # Yes (5=Yes, 6=No)
                    result_text = "\n\n=== AI Text Summary ===\n\n{}\n\n=== Original Text ===\n\n{}".format(
                        summary, selected_text
                    )
                    # Insert to end of document
                    doc_length = editor.getLength()
                    if doc_length > 0:
                        last_char = editor.getTextRange(doc_length - 1, doc_length)
                        if last_char not in ['\n', '\r']:
                            editor.insertText(doc_length, "\n")
                            doc_length = editor.getLength()
                    editor.insertText(doc_length, result_text)
                else:
                    notepad.messageBox(summary, "AI Text Summarize", 0)
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

summarize_text()

