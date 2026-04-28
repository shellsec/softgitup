# -*- coding: utf-8 -*-
"""
AI Text Analysis
Use AI to analyze selected text (code review, summary, translation, explanation, etc.)
Supports: OpenAI API, local models (via configuration)
"""

import json
import os

def get_api_config():
    """Get API configuration"""
    config_file = os.path.join(os.path.dirname(__file__), 'ai_config.json')
    
    # Default configuration
    default_config = {
        "api_type": "openai",  # openai, claude, local
        "api_key": "",
        "api_base": "https://api.openai.com/v1",
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    # If config file exists, read configuration
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        except:
            pass
    
    return default_config

def save_api_config(config):
    """Save API configuration"""
    config_file = os.path.join(os.path.dirname(__file__), 'ai_config.json')
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        notepad.messageBox("Failed to save config: {}".format(str(e)), "Error", 0)
        return False

def configure_api():
    """Configure API"""
    config = get_api_config()
    
    # Select API type
    api_type_choice = notepad.prompt(
        "Select AI service:\n1.OpenAI 2.Custom 3.Skip",
        "AI Configuration",
        "1"
    )
    
    if api_type_choice is None or api_type_choice == "3":
        return config
    
    if api_type_choice == "1":
        config["api_type"] = "openai"
        config["api_base"] = "https://api.openai.com/v1"
        
        # Input API key
        api_key = notepad.prompt(
            "Enter OpenAI API key:\n(Leave empty to use existing config)",
            "API Configuration",
            config.get("api_key", "")
        )
        if api_key:
            config["api_key"] = api_key
        
        # Select model
        model_choice = notepad.prompt(
            "Select model:\n1.gpt-3.5 2.gpt-4 3.Custom",
            "Model Selection",
            "1"
        )
        if model_choice == "1":
            config["model"] = "gpt-3.5-turbo"
        elif model_choice == "2":
            config["model"] = "gpt-4"
        elif model_choice == "3":
            custom_model = notepad.prompt("Enter model name:", "Custom Model", config.get("model", ""))
            if custom_model:
                config["model"] = custom_model
    
    elif api_type_choice == "2":
        config["api_type"] = "custom"
        api_base = notepad.prompt(
            "Enter API endpoint URL:",
            "API Configuration",
            config.get("api_base", "https://api.openai.com/v1")
        )
        if api_base:
            config["api_base"] = api_base
        
        api_key = notepad.prompt(
            "Enter API key:",
            "API Configuration",
            config.get("api_key", "")
        )
        if api_key:
            config["api_key"] = api_key
        
        model = notepad.prompt(
            "Enter model name:",
            "Model Configuration",
            config.get("model", "gpt-3.5-turbo")
        )
        if model:
            config["model"] = model
    
    if save_api_config(config):
        notepad.messageBox("Configuration saved", "AI Configuration", 0)
    
    return config

def call_openai_api(config, prompt, user_text):
    """Call OpenAI compatible API (supports OpenAI, DeepSeek, etc.)"""
    try:
        import urllib.request
        import urllib.parse
        
        # Determine API endpoint format
        api_base = config["api_base"].rstrip('/')
        if '/chat/completions' in api_base:
            # If endpoint already contains chat/completions, use directly
            url = api_base
        else:
            # Otherwise append chat/completions
            url = "{}/chat/completions".format(api_base)
        
        data = {
            "model": config["model"],
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_text}
            ],
            "temperature": config.get("temperature", 0.7),
            "max_tokens": config.get("max_tokens", 2000)
        }
        
        json_data = json.dumps(data).encode('utf-8')
        
        req = urllib.request.Request(url, data=json_data, method='POST')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', 'Bearer {}'.format(config["api_key"]))
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result["choices"][0]["message"]["content"]
    
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode('utf-8')
        raise Exception("API request failed: {}".format(error_msg))
    except Exception as e:
        raise Exception("Request failed: {}".format(str(e)))

def ai_analyze():
    """AI text analysis"""
    selected_text = editor.getSelText()
    
    if not selected_text:
        notepad.messageBox(
            "Please select text to analyze",
            "AI Text Analysis",
            0
        )
        return
    
    # Get configuration
    config = get_api_config()
    
    # Check API key
    if not config.get("api_key"):
        choice = notepad.messageBox(
            "API key not configured. Configure now?",
            "AI Configuration",
            4  # Yes/No
        )
        if choice == 5:  # Yes (5=Yes, 6=No)
            config = configure_api()
            if not config.get("api_key"):
                notepad.messageBox("API key not configured, cannot use AI analysis", "Error", 0)
                return
        else:
            return
    
    # Select analysis task
    task_choice = notepad.prompt(
        "Select analysis task:\n"
        "1.Code Review 2.Code Explain 3.Text Summary\n"
        "4.Translate to Chinese 5.Translate to English 6.Find Issues\n"
        "7.Optimization 8.Custom Prompt",
        "AI Analysis Task",
        "1"
    )
    
    if task_choice is None:
        return
    
    # Process user input (extract number)
    import re
    if task_choice:
        match = re.search(r'\d+', task_choice)
        if match:
            task_choice = match.group()
        else:
            task_choice = task_choice.strip()
    
    # Set prompt based on task
    prompts = {
        "1": "You are a professional code reviewer. Please carefully review the following code, point out potential issues, improvement suggestions and best practices. Answer in English.",
        "2": "Please explain in detail the functionality, logic and implementation of the following code in English.",
        "3": "Please summarize the main content of the following text and extract key information in English.",
        "4": "Please translate the following text to Chinese, maintaining the original meaning and format.",
        "5": "Please translate the following text to English, maintaining the original meaning and format.",
        "6": "Please analyze the following code or text, find potential issues, errors or risks. Answer in English.",
        "7": "Please analyze the following code and provide optimization suggestions to improve performance, readability or maintainability. Answer in English.",
        "8": ""
    }
    
    if task_choice == "8":
        custom_prompt = notepad.prompt(
            "Enter custom prompt:",
            "Custom Prompt",
            ""
        )
        if not custom_prompt:
            return
        prompt = custom_prompt
    else:
        prompt = prompts.get(task_choice, prompts["1"])
    
    # Show processing
    notepad.messageBox("Analyzing, please wait...", "AI Analysis", 0)
    
    try:
        # Call API
        result = call_openai_api(config, prompt, selected_text)
        
        # Show result
        result_text = "=== AI Analysis Result ===\n\n{}\n\n=== Original Text ===\n\n{}".format(result, selected_text)
        
        # Ask if insert result
        choice = notepad.messageBox(
            "Analysis complete! Insert result to end of document?",
            "AI Analysis",
            4  # Yes/No
        )
        
        editor.beginUndoAction()
        try:
            if choice == 5:  # Yes (5=Yes, 6=No)
                # Insert to end of document
                doc_length = editor.getLength()
                if doc_length > 0:
                    last_char = editor.getTextRange(doc_length - 1, doc_length)
                    if last_char not in ['\n', '\r']:
                        editor.insertText(doc_length, "\n\n")
                        doc_length = editor.getLength()
                    else:
                        editor.insertText(doc_length, "\n")
                        doc_length = editor.getLength()
                editor.insertText(doc_length, result_text)
            else:
                # Only show result
                notepad.messageBox(result, "AI Analysis Result", 0)
        finally:
            editor.endUndoAction()
    
    except Exception as e:
        notepad.messageBox(
            "AI analysis failed:\n{}\n\nPlease check:\n1. Is API key correct\n2. Is network connection normal\n3. Is API service available".format(str(e)),
            "Error",
            0
        )

# Main function
if __name__ == "__main__":
    # Check if there's a config menu option
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "config":
        configure_api()
    else:
        ai_analyze()

