# -*- coding: utf-8 -*-
"""
AI Code Review
Quick AI code review for selected code
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

def code_review():
    """Code review"""
    selected_text = editor.getSelText()
    
    if not selected_text:
        notepad.messageBox(
            "Please select code to review",
            "AI Code Review",
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
    
    # Build request URL
    api_base = config.get("api_base", "https://api.openai.com/v1/chat/completions").rstrip('/')
    if '/chat/completions' in api_base:
        url = api_base
    else:
        url = "{}/chat/completions".format(api_base)
    
    prompt = """You are a professional code reviewer. Please review the following code and answer in English:
1. Code functionality and logic
2. Potential issues and bugs
3. Performance optimization suggestions
4. Code style and best practices
5. Security issues (if any)

Please answer in a clear structured format."""
    
    data = {
        "model": config.get("model", "gpt-3.5-turbo"),
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": selected_text}
        ],
        "temperature": config.get("temperature", 0.7),
        "max_tokens": config.get("max_tokens", 2000)
    }
    
    try:
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=json_data, method='POST')
        req.add_header('Content-Type', 'application/json')
        # Set authentication header based on API type
        if config.get("api_type") == "deepseek" or "deepseek" in api_base.lower():
            # DeepSeek may use different authentication
            req.add_header('Authorization', 'Bearer {}'.format(api_key))
        else:
            req.add_header('Authorization', 'Bearer {}'.format(api_key))
        
        notepad.messageBox("Reviewing code, please wait...", "AI Code Review", 0)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            review_result = result["choices"][0]["message"]["content"]
            
            # Show result and ask if insert
            choice = notepad.messageBox(
                "Review complete! Insert result to end of document?",
                "AI Code Review",
                4  # Yes/No
            )
            
            editor.beginUndoAction()
            try:
                if choice == 5:  # Yes (5=Yes, 6=No)
                    result_text = "\n\n=== AI Code Review Result ===\n\n{}\n\n=== Original Code ===\n\n{}".format(
                        review_result, selected_text
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
                    notepad.messageBox(review_result, "AI Code Review Result", 0)
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

code_review()

