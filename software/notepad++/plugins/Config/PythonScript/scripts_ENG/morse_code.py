# -*- coding: utf-8 -*-
"""
Morse Code Encoder/Decoder
Encode or decode selected text using Morse code
"""

MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.',
    '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
    '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-',
    '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.',
    '$': '...-..-', '@': '.--.-.', ' ': '/'
}

# Reverse mapping
MORSE_DECODE = {v: k for k, v in MORSE_CODE.items()}

def morse_encode_decode():
    """Morse code encode or decode"""
    selected_text = editor.getSelText()
    
    if not selected_text:
        notepad.messageBox(
            "Please select text to encode/decode",
            "Morse Code",
            0
        )
        return
    
    # Detect if it's Morse code format (contains . and -)
    text_upper = selected_text.upper().strip()
    is_encoded = False
    
    if text_upper:
        # Check if only contains Morse code characters
        morse_chars = set(['.', '-', '/', ' ', '\n', '\r', '\t'])
        text_clean = text_upper.replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
        if text_clean and all(c in morse_chars for c in text_clean):
            is_encoded = True
    
    editor.beginUndoAction()
    try:
        if is_encoded:
            # Decode
            try:
                decoded_parts = []
                # Split by space or slash
                words = text_upper.replace('\n', ' ').replace('\r', ' ').split('/')
                for word in words:
                    if not word.strip():
                        decoded_parts.append(' ')
                        continue
                    letters = word.strip().split()
                    for letter in letters:
                        if letter in MORSE_DECODE:
                            decoded_parts.append(MORSE_DECODE[letter])
                        else:
                            decoded_parts.append('?')  # Unknown character
                    decoded_parts.append(' ')
                
                decoded = ''.join(decoded_parts).strip()
                editor.replaceSel(decoded)
                notepad.messageBox("Morse code decoded", "Morse Code", 0)
            except Exception as e:
                notepad.messageBox("Decode failed: {}".format(str(e)), "Error", 0)
        else:
            # Encode
            try:
                encoded_parts = []
                text_upper = selected_text.upper()
                for char in text_upper:
                    if char in MORSE_CODE:
                        encoded_parts.append(MORSE_CODE[char])
                        encoded_parts.append(' ')  # Space between characters
                    elif char == '\n' or char == '\r':
                        encoded_parts.append('/ ')  # Newline represented by slash
                    else:
                        # Unknown character, skip
                        pass
                
                encoded = ''.join(encoded_parts).strip()
                editor.replaceSel(encoded)
                notepad.messageBox("Morse code encoded", "Morse Code", 0)
            except Exception as e:
                notepad.messageBox("Encode failed: {}".format(str(e)), "Error", 0)
    finally:
        editor.endUndoAction()

morse_encode_decode()

